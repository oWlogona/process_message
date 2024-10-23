from services.storage.database import Base, database
from sqlalchemy import Column, Integer, String, Text


class TextProcessingTask(Base):
    __tablename__ = "text_processing_tasks"

    task_id = Column(String, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    processed_text = Column(Text, nullable=False)
    type = Column(String, nullable=False)
    word_count = Column(Integer, nullable=False)
    language = Column(String, nullable=False)
    status = Column(String, nullable=False)


async def add_task(
    task_id: str,
    original_text: str,
    processed_text: str,
    task_type: str,
    word_count: int,
    language: str,
    status: str,
):
    try:
        query = TextProcessingTask.__table__.insert().values(
            task_id=task_id,
            original_text=original_text,
            processed_text=processed_text,
            type=task_type,
            word_count=word_count,
            language=language,
            status=status,
        )
        await database.execute(query)
    except Exception as e:
        print(f"Error adding task: {e}")


async def get_task(task_id: str):
    query = TextProcessingTask.__table__.select().where(
        TextProcessingTask.task_id == task_id
    )
    return await database.fetch_one(query)
