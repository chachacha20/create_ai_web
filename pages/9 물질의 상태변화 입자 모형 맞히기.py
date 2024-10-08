import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import openai

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # OpenAI API 키 설정
    openai.api_key = api_key

    # Streamlit 페이지 제목 설정
    st.title("입자 모형 상태 맞히기")

    # 이미지 업로드 받기
    uploaded_image = st.file_uploader("입자 모형 이미지를 업로드하세요")

    if uploaded_image is not None:
        # 업로드된 이미지 열기
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # 이미지에서 텍스트 추출을 위한 프롬프트 생성
        prompt = "Analyze the uploaded image and determine which state of matter it represents: solid, liquid, or gas. Describe the characteristics of the particle arrangement."

        # OpenAI API를 사용하여 텍스트 생성
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )

        # 분석 결과 가져오기
        analysis_text = response.choices[0].text.strip()
        st.text_area("분석 결과", analysis_text, height=200)

        # 교과서 그림 보여주기
        state_images = {
            "solid": "solid_example.jpg",
            "liquid": "liquid_example.jpg",
            "gas": "gas_example.jpg"
        }

        if "solid" in analysis_text.lower():
            state_image = state_images["solid"]
        elif "liquid" in analysis_text.lower():
            state_image = state_images["liquid"]
        elif "gas" in analysis_text.lower():
            state_image = state_images["gas"]
        else:
            state_image = None

        if state_image:
            st.image(state_image, caption="교과서에서 발췌한 해당 상태의 입자 모형", use_column_width=True)

else:
    st.warning("API 키를 사이드바에 입력하세요.")