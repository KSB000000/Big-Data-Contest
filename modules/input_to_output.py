import json
import os

import pandas as pd

import modules.function as fn
from modules.llm.req.input_to_list_mct import input_to_list_mct
from modules.llm.req.input_to_list_move import input_to_list_move
from modules.llm.res.output_response_move import output_response_move
from modules.location_to_index import location_to_index
from modules.util.find_closest_type import find_closest_type


def input_to_output(input, type, model):
    base_dir = os.path.dirname(__file__)
    data_dir = os.path.join(base_dir, "../data")
    csv_file_dir = os.path.join(data_dir, "FINAL.csv")
    df = pd.read_csv(csv_file_dir, dtype=str)

    try:
        if type == "MCT":
            llm_list = input_to_list_mct(input, model)
        elif type == "MOVE":
            llm_list = input_to_list_move(input, model)
        cleaned_json = llm_list.replace("```json\n", "").replace("\n```", "")
        cleaned_json = cleaned_json.replace("{{", "{").replace("}}", "}")
        cleaned_json = cleaned_json.replace("'", '"')
        data = json.loads(cleaned_json)
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        return "-1"
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")
        return "-1"

    list_data = data["List"]
    output = None  # 초기화

    if type == "MCT":
        keys = [
            "방문하는 월",
            "원하는 맛집 업종",
            "위치",
            "이용건수",
            "이용금액",
            "건당 평균 이용금액",
            "방문요일",
            "방문시간",
            "현지인 맛집 선호여부",
            "성별",
            "나이",
        ]
        extracted_info = dict(zip(keys, list_data))
        output = fn.RECOMMEND(
            extracted_info["방문하는 월"],
            extracted_info["원하는 맛집 업종"],
            extracted_info["위치"],
            extracted_info["이용건수"],
            extracted_info["이용금액"],
            extracted_info["건당 평균 이용금액"],
            extracted_info["방문요일"],
            extracted_info["방문시간"],
            extracted_info["현지인 맛집 선호여부"],
            extracted_info["성별"],
            extracted_info["나이"],
            df,
        )

    elif type == "MOVE":
        keys = [
            "사용자의 위치",
            "추천 장소의 종류",
            "방문하는 월",
            "방문요일",
            "방문시간",
        ]
        extracted_info = dict(zip(keys, list_data))
        user_location = extracted_info.get("사용자의 위치")
        extracted_info["사용자의 위치"] = int(float(df.loc[location_to_index(user_location, df, model)[3], "Distance_Index"]))

        output = fn.Move_Recommend(
            extracted_info["사용자의 위치"],
            find_closest_type(extracted_info["추천 장소의 종류"]),
            extracted_info["방문하는 월"],
            extracted_info["방문요일"],
            extracted_info["방문시간"],
            df,
        )
        if output == "-1":
            return output
        else:
            output = output_response_move(output, user_location)
    return output
