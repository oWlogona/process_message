import os

import pika
from loguru import logger

RABBITMQ_URL = os.environ.get("RABBITMQ_URL")

if RABBITMQ_URL is None:
    raise ValueError("RABBITMQ_URL is not set in the environment variables.")


def connect_to_rabbitmq(url: str = RABBITMQ_URL):
    """Establish a connection to RabbitMQ."""
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(url))
        channel = connection.channel()
        channel.queue_declare(queue="text_processing")
        logger.info("Connected to RabbitMQ")
        return connection, channel
    except pika.exceptions.AMQPConnectionError as e:
        raise RuntimeError(f"Connection error: {e}")
