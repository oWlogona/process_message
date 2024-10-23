from loguru import logger

from logic.consumer import consume
from services.rabbit.connection import connect_to_rabbitmq

if __name__ == "__main__":
    connection, channel = connect_to_rabbitmq()
    try:
        consume(channel)
    except KeyboardInterrupt:
        logger.info("Stopping the consumer...")
    finally:
        connection.close()
