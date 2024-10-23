import asyncio
import json

from loguru import logger

from common.tasks import process_text
from services.storage.models import add_task


async def on_message(ch, method, properties, body):
    """
    Callback function to process incoming messages from RabbitMQ.

    Args:
        ch: Channel object.
        method: Method frame.
        properties: Message properties.
        body: Message body containing the task data.
    """
    try:
        message = json.loads(body)
        task_id = message.get("task_id")
        text = message.get("text")
        text_type = message.get("type")

        if not all([task_id, text, text_type]):
            raise ValueError("Missing required fields in message.")

        # Process the text
        processed_data = process_text(text)

        # Validate processed data
        if not processed_data:
            raise ValueError("Processing failed, no data returned.")

        logger.info("Processed data:")
        word_count = processed_data.get("word_count")
        processed_text = processed_data.get("processed_text")
        language = processed_data.get("language")

        if not all([word_count, processed_text, language]):
            raise ValueError("Processed data is missing required fields.")

        # Store the result in the database
        await add_task(
            task_id, text, processed_text, text_type, word_count, language, "completed"
        )
        logger.info(f"Task {task_id} processed and stored successfully.")

    except json.JSONDecodeError:
        logger.info("Failed to decode JSON message.")
    except ValueError as ve:
        logger.info(f"Value error: {ve}")
    except Exception as e:
        logger.info(f"An error occurred: {e}")


def consume(channel):
    """
    Start consuming messages from RabbitMQ.

    Args:
        channel: RabbitMQ channel object.
    """

    # Update to handle asynchronous function calls
    def callback(ch, method, properties, body):
        asyncio.run(on_message(ch, method, properties, body))

    channel.basic_consume(
        queue="text_processing", on_message_callback=callback, auto_ack=True
    )
    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
