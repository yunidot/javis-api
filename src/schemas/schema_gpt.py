from enum import Enum
from pydantic import BaseModel


class GptModel(Enum):
    BASIC: str = "gpt-3.5-turbo-1106"
    ADVANCED: str = "gpt-4-1106-preview"

