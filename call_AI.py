import requests
import time
import streamlit as st


def call_solar_ai(prompt):
    time.sleep(1)  # 요청 전 1초 대기
    OLLAMA_HOST = "http://192.168.20.72:11434"
    response = requests.post(
                f"{OLLAMA_HOST}/api/generate",  # ✅ 원래 로컬 주소로 복원
        json={
            "model": "solar",
            "prompt": prompt,
            "stream": False
        }
    )
    r = requests.get(OLLAMA_HOST)
    return response.json()["response"]





