from pydantic import BaseModel, Field


class TextPayload(BaseModel):
    text: str = Field(..., max_length=300000, pattern=r'^[\w\s.,!?\'"/\-@]+$')
    type: str