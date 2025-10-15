import os
import json
import logging

from alpaca.data.live import CryptoDataStream
from alpaca.data.models.quotes import Quote

import pika  # type: ignore[import-untyped]
from pika.adapters.blocking_connection import BlockingChannel  # type: ignore[import-untyped]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
RAW_QUEUE_NAME = "raw_data_queue"
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET = os.getenv("ALPACA_SECRET", "")
SYMBOL_TO_TRACK = os.getenv("SYMBOLS_TO_TRACK", "BTC/USD")

if ALPACA_API_KEY == "":
    raise Exception('Please provide "ALPACA_API_KEY"')

if ALPACA_SECRET == "":
    raise Exception('Please provice "ALPACA_SECRET"')

channel: BlockingChannel


def connect_to_rabbitmq() -> BlockingChannel:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST)
        )
        channel = connection.channel()

        channel.queue_declare(queue=RAW_QUEUE_NAME, durable=True)
        logging.info(
            f"Successfully connected to RabbitMQ and declared queue '{RAW_QUEUE_NAME}"
        )
        return channel
    except Exception as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")
        raise


wss_client = CryptoDataStream(ALPACA_API_KEY, ALPACA_SECRET)


async def on_quote(quote: Quote) -> None:
    try:
        if not channel or channel.is_closed:
            logging.warning("RabbitMQ channel is closed. Dropping message.")
            return

        quote_data = {
            "source": "alpaca",
            "symbol": quote.symbol,
            "bid_price": quote.bid_price,
            "ask_price": quote.ask_price,
            "timestamp": quote.timestamp.isoformat(),
            "source_type": "quote",
        }

        message_body = json.dumps(quote_data).encode("utf-8")

        channel.basic_publish(
            exchange="",
            routing_key=RAW_QUEUE_NAME,
            body=message_body,
            properties=pika.BasicProperties(delivery_mode=2),
        )

        logging.info(
            f"Published trade for {quote.symbol}: Bid={quote.bid_price} Ask={quote.ask_price}"
        )
    except Exception as e:
        logging.error(f"Error processing trade data: {e}")


wss_client.subscribe_quotes(on_quote, "BTC/USD")  # type: ignore[arg-type]


if __name__ == "__main__":
    try:
        channel = connect_to_rabbitmq()
    except Exception:
        exit(1)

    try:
        wss_client = CryptoDataStream(ALPACA_API_KEY, ALPACA_SECRET)

        wss_client.subscribe_quotes(on_quote, SYMBOL_TO_TRACK)  # type: ignore[arg-type]
        logging.info(f"Subscribed to quotes for {SYMBOL_TO_TRACK}. Starting stream...")

        # Start the stream (this is a blocking call that runs forever)
        wss_client.run()

    except Exception as e:
        logging.error(f"Alpaca streaming error: {e}")
    finally:
        # Close the Pika connection gracefully on exit
        if channel and not channel.is_closed:
            channel.connection.close()
            logging.info("RabbitMQ connection closed.")
