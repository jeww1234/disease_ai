import requests
import streamlit as st

def call_solar_ai(prompt):
    response = requests.post(
        "https://david-translated-immigrants-progressive.trycloudflare.com/api/generate",
        json={
            "model": "solar",
            "prompt": prompt,
            "stream": False
        }
    )

    print("status_code:", response.status_code)
    print("response.text:", response.text)

    try:
        return response.json()["response"]
    except Exception as e:
        st.write("🚨 JSON 파싱 실패:", e)
        return "❌ AI 응답 파싱 실패: 응답이 없거나 JSON 형식이 아닙니다."