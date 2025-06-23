import requests

def call_solar_ai(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "solar",  # 또는 정확한 모델 이름 (예: solar:latest)
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]