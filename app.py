import os

import google.generativeai as genai
import streamlit as st
import torch
from dotenv import dotenv_values

from modules.input_to_output import input_to_output
from modules.llm.res.output_miss_to_response import output_miss_to_response
from modules.llm.res.output_to_response_mct import output_to_response_mct
from modules.llm.res.output_to_response_move import output_to_response_move

base_dir = os.path.dirname(__file__)
config_dir = os.path.join(base_dir, "./.streamlit/secrets.toml")

config = dotenv_values(config_dir)

GOOGLE_API_KEY = config.get("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="🍊참신한 제주 맛집!")

# Replicate Credentials
with st.sidebar:
    st.title("🍊효율적인! 제주 동선")

    st.write("")

    st.subheader("가장 좋은 갈팡 찾아줄게마씸.")

    st.write("")

    # 사용설명서 내용 추가
    st.sidebar.markdown(
        """
    ** 사용설명서 **
    1. MCT 데이터 관련해서 질문을 하고 싶으면 '맛집 추천'을 선택, 동선 관련해서 질문을 하려면 '동선 추천'을 선택해주세요.
    2. '동선 추천'은 시작하는 장소, 들리고 싶은 장소들, 방문하는 월,요일,시간대를 입력해주면 더 자세하게 찾아 줄 수 있습니다.
    """
    )

    st.write("")

    st.markdown(
        """
        <style>
        .stRadio > label {
            display: none;
        }
        .stRadio > div {
            margin-top: -20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    move_choice = st.radio("", ("맛집 추천", "동선 추천"))

st.title("삼춘! 밥 먹언? 추천 좀 받고 가게!")
st.subheader("무사 밥을 안 먹언! 영 갑서양.")

st.write("")

st.write("#맛집 #동선 #관광지 #쇼핑 #숙박 #제주 🤤")

st.write("")

image_path = "https://i.ibb.co/M2vQKFs/202101003982-500.jpg"
image_html = f"""
<div style="display: flex; justify-content: center;">
    <img src="{image_path}" alt="centered image" width="50%">
</div>
"""
st.markdown(image_html, unsafe_allow_html=True)

st.write("")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "어드런 식당 찾으시쿠과?"}
    ]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = [
        {"role": "assistant", "content": "어드런 식당 찾으시쿠과?"}
    ]


st.sidebar.button("Clear Chat History", on_click=clear_chat_history)


# RAG

# 디바이스 설정
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Device is {device}.")


# User-provided prompt
if prompt := st.chat_input():  # (disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)


if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            placeholder = st.empty()
            if move_choice == "맛집 추천":
                move_choice = "MCT"
            elif move_choice == "동선 추천":
                move_choice = "MOVE"

            source_output = input_to_output(prompt, move_choice, model)

            if source_output == "-1":
                response_text = output_miss_to_response(model)
            else:
                if move_choice == "MCT":
                    response_text = output_to_response_mct(source_output, model)
                elif move_choice == "MOVE":
                    response_text = output_to_response_move(source_output, model)
            placeholder.markdown(response_text)  # 최종 응답을 출력

    # 세션 상태에 메시지 추가
    message = {"role": "assistant", "content": response_text}
    st.session_state.messages.append(message)
