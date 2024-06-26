from urllib import parse
from fastapi import APIRouter, Request
from src.schemas import schema_gpt
from src.services import service_gpt

router = APIRouter(
    prefix="/api/v1",
    tags=["API"]
)


@router.post("/ask")
async def post_ask(request: Request):
    body = await request.json()
    user_id: str = body["user_id"]
    question: str = body["question"]
    result = await service_gpt.gpt_answer(question=question, model=schema_gpt.GptModel.BASIC)
    result = parse.quote(result)
    return result
