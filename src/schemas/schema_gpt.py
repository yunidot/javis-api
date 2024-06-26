from enum import Enum
from pydantic import BaseModel, Field


class GptModel(Enum):
    BASIC: str = "gpt-3.5-turbo-1106"
    ADVANCED: str = "gpt-4-1106-preview"


class GptRequest(BaseModel):
    user_id: str | None = Field(title="user_id", description="사용자 아이디", default=None)
    question: str | None = Field(title="question", description="질문", default=None)

    class Config:
        from_attributes=True