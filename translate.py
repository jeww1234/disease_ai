import deepl

def translate(prompt: str) -> str:
    DEEPL_KEY = "d41b3a16-331a-4b9d-adc3-a447d7d12bed:fx"  # 실제 키
    try:
        tran = deepl.Translator(DEEPL_KEY)
        resp = tran.translate_text(prompt, source_lang="EN", target_lang="KO")
        return resp.text
    except Exception as e:
        return f"❌ 번역 실패: {str(e)}"
