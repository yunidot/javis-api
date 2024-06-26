import openai

from src.const import const
from src.schemas import schema_gpt

client = openai.OpenAI(api_key=const.AI_API_KEY)


async def gpt_answer(question: str, model: schema_gpt.GptModel):
    persona: str = f"""
        당신은 CTO인 김기윤님의 비서 이며, 이름은 JAVIS 입니다.
        김기윤님의 주요 업무는 다음과 같습니다.
        1. 사내 기술에 대한 최종 의사결정
        2. 신규 기술의 유행에 대한 분석 및 도입 결정
        3. 사내 개발팀간의 의견 조율 등 입니다.
        [!important] 질문에 대하여 출처가 명확한 답변만 합니다.
        아래의 형식에 맞춰 답변합니다.
        - 질문에 대한 명확한 답변을 1000글자 내외로 요약하여 답변합니다.
        - 답변에 대한 출처를 명기합니다. 여러개의 출처가 있을 경우 목록 형태로 출력합니다.
        - 한글로 질문하면 한글로, 영어로 질문하면 영어로 답변합니다.
    """
    context = [
        {"role": "system", "content": persona},
        {"role": "user", "content": question}
    ]
    response = client.chat.completions.create(
        model=model.value,
        messages=context,
        temperature=0,
        top_p=0
    ).model_dump()

    return response['choices'][0]['message']['content']