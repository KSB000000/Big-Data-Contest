import os

import requests
from dotenv import dotenv_values


def geocode_address(address):
    base_dir = os.path.dirname(__file__)
    config_dir = os.path.join(base_dir, "../../.streamlit/secrets.toml")
    config = dotenv_values(config_dir)
    KAKAO_API_KEY = config.get("KAKAO_API_KEY")

    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": address}
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["meta"]["total_count"] > 0:
            first_result = data["documents"][0]["address"]
            latitude = first_result["y"]
            longitude = first_result["x"]
            return latitude, longitude
        else:
            print("해당 주소에 대한 결과가 없습니다.")
            return None
    else:
        print(f"API 요청 실패: {response.status_code}")
        return None
