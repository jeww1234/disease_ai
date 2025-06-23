import requests
import streamlit as st
import time

OLLAMA_HOST = "http://192.168.20.72:11434"

def call_solar_ai(prompt):
    time.sleep(1)
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={"model": "solar", "prompt": prompt, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("response", "응답이 없습니다.")
    except Exception as e:
        return f"AI 호출 실패: {e}"

def check_ollama_status():
    try:
        r = requests.get(OLLAMA_HOST, timeout=5)
        return r.text
    except Exception as e:
        return f"Ollama 연결 실패: {e}"

st.title("Ollama AI 테스트")

if st.button("Ollama 상태 확인"):
    with st.spinner("Ollama 서버 상태 확인 중..."):
        status = check_ollama_status()
    st.write(status)

prompt = st.text_area("프롬프트 입력", "안녕하세요?")

if st.button("AI 호출 실행"):
    with st.spinner("AI 호출 중..."):
        result = call_solar_ai(prompt)
    st.write(result)
