import requests
import time


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
    return response.json()["response"]


import requests
r = requests.get("http://localhost:11434")
print(r.text)  # 콘솔 실행
