import streamlit as st
import google.generativeai as genai

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("Google Gemini API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # API 키 설정
    genai.configure(api_key=api_key)

    # Streamlit 페이지 제목 설정
    st.title("원영적 사고? 나도!")

    # 생성 설정
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # 모델 초기화
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # 사용자 입력 받기
    user_input = st.text_area("당신의 슬픈 기분을 입력해 보세요", 
                              "예: 오랜 기다림 끝에 빵을 살 수 있게 되었는데 내 앞에서 품절되었다. 띠로리")

    if st.button("원영적 사고 생성"):
        # 인공지능 모델을 사용하여 상장 생성
        response = model.generate_content([
            "따뜻한 빵을 살 수 있게 되었네? 완전 럭키비키잖앙.",
            f"input: {user_input}",
        ])

        # 결과 출력
        st.subheader("생성된 원영적 사고")
        st.write(response.text)
else:
    st.warning("API 키를 사이드바에 입력하세요.")
