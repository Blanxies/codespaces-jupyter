pip install streamlit requests
import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Azure Custom Vision API 정보 입력
ENDPOINT = "https://a0371102-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/6640f1bc-5032-4859-8fa4-282247afb802/classify/iterations/Iteration3/image"
PREDICTION_KEY = "25JDXCYhC6oyL6utB3ycTqQkCWOXoKVe18fIvR9qdasSVmiezQI8JQQJ99AKACYeBjFXJ3w3AAAIACOGpCC2"
HEADERS = {
    "Content-Type": "application/octet-stream",
    "Prediction-Key": PREDICTION_KEY
}

# Streamlit UI 설정
st.title("Azure Custom Vision Classification with Streamlit")
st.write("Azure Custom Vision 모델을 사용한 이미지 분류 예시")

uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("이미지 분류를 진행 중입니다...")

    # 이미지를 바이너리로 변환하여 API 요청
    image_data = BytesIO()
    image.save(image_data, format="JPEG")
    image_data = image_data.getvalue()

    response = requests.post(ENDPOINT, headers=HEADERS, data=image_data)

    # 예측 결과 처리 및 출력
    if response.status_code == 200:
        predictions = response.json()["predictions"]
        st.write("예측 결과:")
        for prediction in predictions:
            st.write(f"{prediction['tagName']}: {prediction['probability'] * 100:.2f}%")
    else:
        st.write("API 요청 오류:", response.status_code, response.text)