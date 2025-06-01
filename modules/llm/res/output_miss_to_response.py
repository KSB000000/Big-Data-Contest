def output_miss_to_response(model):
    prompt = f"""
            "찾지 못했어요. 다른 질문을 해주시겠어요?" 를 출력해야 하는데
            제주도 방언으로 출력해줘.
        """
    response = model.generate_content(prompt)

    return response.text