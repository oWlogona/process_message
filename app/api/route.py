import json
import uuid

from api.schemas.text_payload import TextPayload
from fastapi import FastAPI, HTTPException
from services.rabbit.connection import connect_to_rabbitmq
from services.storage.models import get_task

process_api = FastAPI()


TEXT_LENGTH_LIMITS = {"chat_item": 300, "summary": 3000, "article": 300000}


@process_api.post("/process-text")
async def process_text(payload: TextPayload):
    """
    Process text and publish to RabbitMQ.

    Args:
        payload (TextPayload): The text and its type to process.

    Raises:
        HTTPException: If the text length exceeds the allowed limit for its type.

    Returns:
        dict: A response containing the generated task ID.
    """
    connection, channel = connect_to_rabbitmq()
    task_id = str(uuid.uuid4())

    max_length = TEXT_LENGTH_LIMITS.get(payload.type)
    if max_length is None:
        raise HTTPException(status_code=400, detail="Invalid text type provided.")

    if len(payload.text) > max_length:
        raise HTTPException(
            status_code=400, detail=f"Text too long for '{payload.type}'."
        )

    message = json.dumps(
        {"task_id": task_id, "text": payload.text, "type": payload.type}
    )
    channel.basic_publish(exchange="", routing_key="text_processing", body=message)

    return {"task_id": task_id}


@process_api.get("/results/{task_id}")
async def get_results(task_id: str):
    """
    Retrieve the results of a processed task by task ID.

    Args:
        task_id (str): The ID of the task to retrieve.

    Raises:
        HTTPException: If the task ID is not found.

    Returns:
        dict: The results of the processed task.
    """
    result = await get_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found.")

    return {
        "task_id": result.task_id,
        "original_text": result.original_text,
        "processed_text": result.processed_text,
        "type": result.type,
        "word_count": result.word_count,
        "language": result.language,
        "status": result.status,
    }
