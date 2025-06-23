import requests

def call_solar_ai(prompt):
    response = requests.post(
        "https://david-translated-immigrants-progressive.trycloudflare.com",
        json={
            "model": "solar",
            "prompt": prompt,
            "stream": False
        }
    )
    try:
        return response.json()["response"]
    except ValueError:
        print("⚠️ JSON 응답 아님! 받은 내용:", response.text)
        return response.text  # 필요하면 fallback으로 단순 텍스트 반환