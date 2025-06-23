import requests

def call_solar_ai(prompt):
    response = requests.post(
        "https://your-cloudflare-url/api/generate",
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
        print("🚨 JSON 파싱 실패:", e)
        return ""