import streamlit as st
from openai import OpenAI
from PIL import Image
import io

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=api_key)

    # Streamlit 페이지 제목 설정
    st.title("팔다리")

    # 이미지 업로드 받기
    uploaded_image = st.file_uploader("이미지를 업로드하세요")

    if uploaded_image is not None:
        # 업로드된 이미지 열기
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # 이미지에서 텍스트 추출 (OCR 기능을 사용할 수 있다고 가정)
        response_text = client.images.extract_text(
            image=image
        )
        extracted_text = response_text['text']
        st.text_area("추출된 텍스트", extracted_text, height=200)

        # 추출된 텍스트를 기반으로 새 이미지 생성
        if st.button("텍스트로부터 이미지 생성"):
            response = client.images.generate(
                model="dall-e-3",
                prompt=extracted_text,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            # 생성된 이미지 URL 가져오기
            generated_image_url = response.data[0].url

            # 이미지 출력
            st.image(generated_image_url, caption=f"Generated Image from Text")

    # 사용자 입력 받기
    prompt = st.text_input("이미지 생성 프롬프트를 입력하세요", "a favorite object with arms and legs")

    # 버튼을 클릭했을 때 이미지 생성
    if st.button("이미지 생성"):
        # 프롬프트에 팔다리를 추가하여 사용자 입력 수정
        modified_prompt = f"{prompt} with arms and legs"

        # OpenAI API를 사용하여 이미지 생성
        response = client.images.generate(
            model="dall-e-3",
            prompt=modified_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # 생성된 이미지 URL 가져오기
        image_url = response.data[0].url

        # 이미지 출력
        st.image(image_url, caption=f"Generated Image: {modified_prompt}")
else:
    st.warning("API 키를 사이드바에 입력하세요.")