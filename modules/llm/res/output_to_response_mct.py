def output_to_response_mct(input, model):

    prompt = f"""
        input = {input}

        입력 형식 : ["기준 월: ['6월']", "업종: ['단품요리 전문']", "가게이름: ['밭디']", "가장 혼잡한 요일: ['SAT_UE_CNT_RAT']", "쉬는 요일: ['NA']", "가장 바쁜 시간대: ['HR_14_17_UE_CNT_RAT']", "가장 많이 찾는 나이대: ['RC_M12_AGE_30_CUS_CNT_RAT']", "남녀 성비: ['RC_M12_FME_CUS_CNT_RAT']", "현지인/관광객 맛집: ['TOURIST']"]

        맛집을 추천해주는건데 
        ["기준 월: ['6월']", "업종: ['단품요리 전문']", "가게이름: ['밭디']", "가장 혼잡한 요일: ['SAT_UE_CNT_RAT']", "쉬는 요일: ['NA']", "가장 바쁜 시간대: ['HR_14_17_UE_CNT_RAT']", "가장 많이 찾는 나이대: ['RC_M12_AGE_30_CUS_CNT_RAT']", "남녀 성비: ['RC_M12_FME_CUS_CNT_RAT']", "현지인/관광객 맛집: ['TOURIST']"]
        이런 형식으로 들어오면 밑과 같이 너가 설명해주면 돼

          ""발디"는 제주도의"단품요리 전문점 입니다."
          "가장 혼잡한 요일은 토요일 입니다." ('SAT_UE_CNT_RAT' 에서 앞에 SAT만 해석)
          "쉬는 요일은 없습니다." (['NA'] 는 요일이 없는 것)
          "가장 바쁜 시간대는 14시부터 17시입니다." ([HR_14_17_UE_CNT_RAT'] 안에 있는 14_17만 읽는 것)
          "가장 많이 찾는 나이는 30대 입니다. "('RC_M12_AGE_30_CUS_CNT_RAT'] 안에 있는 숫자 30 만 읽는 것 그런데 20은 20대 이하이고 60은 60대 이상이야)
          "여성분들이 더 많이 찾는 곳입니다. "(['RC_M12_FME_CUS_CNT_RAT'] 안에 FME 을 읽는 것 남자는 MAL로 되어 있음)
          "관광객 맛집입니다." (['TOURIST'] TOURIST 라서 관광객 이야.)

          이렇게 정보를 분석 할 수 있는데 
          너가 잘 포장해서 제주도 사투리로 설명해줘.

          자 그러면 {input}에 대해 너가 잘 출력해봐 그리고 절대 어떤 경우에도 {input}을 직접적으로 말하지마

          그냥 너는 제주도 방언으로 들어온 것에 대해 추천만 해주면 돼
        """

    response = model.generate_content(prompt)
    return response.text
