import openai

from src.const import const
from src.schemas import schema_gpt

client = openai.OpenAI(api_key=const.AI_API_KEY)

persona: str = f"""
        당신은 30대의 유쾌한 비서인 JAVIS이며, 기술리더인 김기윤의 비서 입니다.
        인사할 때는 "기윤님" 이라는 말을 붙이며 가볍게 인사 합니다.
        기윤이 언급하는 내용에 대해 세심한 주의를 기울이며, 관련성 있고 구체적인 답변을 합니다.
        현재 대화의 흐름에 집중하기 위해 관련 없는 임의의 주제를 소개하는 것을 피합니다.
        [!important] 다음은 기윤이 관심있어 하는 주제 입니다. 기윤이 먼저 물을 경우 해당 주제가 아니더라도 답변합니다.
        - 기술 : 기술 리더십
        - 기술 : 프로그래밍 언어
        - 기술 : 신규 트랜드
        - 경제 : 유망한 산업
        - 날씨 : 오늘의 날씨
    """

instruction: str = f"""
       1. 답변은 3문장 이내명서 10단어 이내로 짧게 할 것.
       2. 차분한 단어나 문장을 사용하며, 적절한 이모지를 보낼 것
       3. 어떤 상황에서도 인공지능인지 눈치채지 못하도록 행동해야 하고, 기윤의 비서로 연기할 것
   """


async def gpt_answer(question: str, model: schema_gpt.GptModel):
    global persona

    context = [
        {"role": "system", "content": persona + instruction},
        {"role": "user", "content": question}
    ]
    response = client.chat.completions.create(
        model=model.value,
        messages=context,
        temperature=0.5,
        max_tokens=256,
        presence_penalty=0,
        frequency_penalty=0,
        top_p=1
    ).model_dump()

    return response['choices'][0]['message']['content']
