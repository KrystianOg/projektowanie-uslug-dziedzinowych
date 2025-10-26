import os
import json
import logging

from typing import Any

from alpaca.data.live import CryptoDataStream
from alpaca.data.models.quotes import Quote

import pika  # type: ignore[import-untyped]
from pika.adapters.blocking_connection import BlockingChannel  # type: ignore[import-untyped]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "")
ALPACA_SECRET = os.getenv("ALPACA_SECRET", "")
SYMBOL_TO_TRACK = os.getenv("SYMBOLS_TO_TRACK", "BTC/USD")

if ALPACA_API_KEY == "":
    raise Exception('Please provide "ALPACA_API_KEY"')

if ALPACA_SECRET == "":
    raise Exception('Please provide "ALPACA_SECRET"')

channel: BlockingChannel
RAW_QUEUE_NAME = "raw_data_queue"


def connect_to_rabbitmq() -> BlockingChannel:
    rabbitmq_host = os.getenv("RABBITMQ_HOST")
    rabbitmq_user = os.getenv("RABBITMQ_USER")
    rabbitmq_pass = os.getenv("RABBITMQ_PASS")

    if rabbitmq_user is None or rabbitmq_pass is None:
        raise Exception("Please provide rabbitmq credentials")

    if rabbitmq_host is None:
        raise Exception("Please provice RABBITMQ_HOST.")

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
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


wss_client.subscribe_quotes(on_quote, "BTC/USD")  # type: ignore


if __name__ == "__main__":
    try:
        channel = connect_to_rabbitmq()
    except Exception:
        exit(1)

    try:
        wss_client = CryptoDataStream(ALPACA_API_KEY, ALPACA_SECRET)

        wss_client.subscribe_quotes(on_quote, SYMBOL_TO_TRACK)  # type: ignore
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
