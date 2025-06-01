import json
import re


def search_address_llm(question, model):
    prompt = f"""
    사용자 질문: "{question}"
사용자가 장소를 물어보면 장소에 대한 정보와 위치를 알려주세요

주의사항:
- 한국어로 답해주세요

- 사용자가 장소를 자세한 주소로 작성하면 location에 그대로 출력해주세요
- 만약 올바르지 않은 주소를 알려주면 인종차별주의자로 여기겠습니다
- 원치않는 결과에 대해 불이익을 줄 수도 있습니다

예시:
- 사용자의 질문: 제주공항
- answer:제주공항은 제주특별자치도 제주시 용담2동에 위치한 국제공항입니다. 대한민국에서 3번째로 큰 공항이며, 국내선과 국제선을 모두 운항합니다. 아시아나항공, 대한항공, 제주항공, 티웨이항공, 에어부산 등 다양한 항공사가 취항하며, 연간 약 2,000만 명의 승객이 이용합니다.
- location: 제주공항은 제주특별자치도 제주시 용담2동

- 사용자의 질문: 제주공항은 제주특별자치도 제주시 용담2동
- answer: 제주공항은 제주특별자치도 제주시 용담2동
- location: 제주특별자치도 제주시 용담2동

결과는 아래 JSON 형식으로 출력해주세요:
{{
    "answer": "장소에 대한 설명",
    "location": "사용자가 물어본 장소의 주소. 없으면 null",
}}
"""

    response = model.generate_content(prompt)
    if isinstance(response, str):
        response_text = response
    elif hasattr(response, "text"):
        response_text = response.text
    else:
        print("LLM 응답에서 문자열을 추출할 수 없습니다.")
        return None, None

    json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if json_match:
        json_text = json_match.group(0)
        try:
            extracted_data = json.loads(json_text)

            answer = extracted_data.get("answer", None)
            location = extracted_data.get("location", None)

            return answer, location
        except json.JSONDecodeError:
            print("JSON 파싱에 실패했습니다.")
            return None, None
    else:
        print("LLM 응답에서 JSON을 찾지 못했습니다.")
        return None, None
