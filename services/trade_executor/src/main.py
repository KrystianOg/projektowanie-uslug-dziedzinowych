
import aio_pika
import json
import asyncio
from risk_validator import RiskValidator
from trade_executor import TradeExecutor

from models import Signal


import logging
logger = logging.getLogger(__name__)

risk_validator = RiskValidator()
trade_executor = TradeExecutor()


async def consume_signals():
    connection = await aio_pika.connect_robust('amqp://guest:guest@rabbitmq/')
    channel = await connection.channel()
    queue = await channel.declare_queue('signal.trade_executor', durable=True)

    async with queue.iterator() as q:
        async for message in q:
            async with message.process():
                logger.info(message.body)
                signal_dict = json.loads(message.body)
                signal = Signal.from_dict(signal_dict)

                if signal is None:
                    continue

                if not risk_validator.is_safe(signal):
                    continue

                trade_executor.order(signal)

if __name__ == "__main__":
    asyncio.run(consume_signals())
