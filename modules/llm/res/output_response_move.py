def output_response_move(output, where):
    # output은 딕셔너리 형태
    prompt_parts = [f"사용자의 위치: {where}"]  # 사용자 위치 추가

    for key, value in output.items():
        # 각 업종과 가게 이름을 포맷팅
        prompt_parts.append(f"업종: {key}, 가게 이름: {value}")

    # 모든 정보를 하나의 문자열로 결합
    prompt = "\n".join(prompt_parts)

    # 출력하거나 필요한 대로 사용
    return prompt
