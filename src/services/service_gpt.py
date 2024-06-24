import openai

from src.const import const
from src.schemas import schema_gpt

client = openai.OpenAI(api_key=const.AI_API_KEY)


async def gpt_answer(question: str, model: schema_gpt.GptModel):
    context = [{"role": "user", "content": question}]
    response = client.chat.completions.create(
        model=model.value,
        messages=context,
        temperature=0,
        top_p=0
    ).model_dump()

    return response['choices'][0]['message']['content']