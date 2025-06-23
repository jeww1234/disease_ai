import pandas as pd
from population import calculate_incidence_rate

def parse_count(value):
    try:
        return int(str(value).replace(',', '').strip())
    except:
        return 0 


def generate_prompt(disease: str, regions: list, data: pd.DataFrame, year_range: list, level: int) -> str:

    

    rows = ["Region | Year | Disease | Cases | Rate_per_100k"]
    for region in regions:
        for year in year_range:
            count_series = data[
                (data["지역"] == region) &
                (data["질병명"].str.contains(disease.strip(), na=False, regex=False)) &
                (data["연도"] == year) &
                (data["등급"] == level)
            ]["건수"]

            count = parse_count(count_series.sum())
            print("🔎 데이터에 포함된 질병명 목록:")
            print(data["질병명"].unique())

            print("🔍 전달된 disease 파라미터:")
            print(disease)

            count_series = pd.to_numeric(count_series, errors="coerce").fillna(0)
            raw_sum = count_series.sum()
            print(f"✅ count_series: {count_series.tolist()} → sum: {raw_sum}")
            count = int(raw_sum)


            try:
                rate = calculate_incidence_rate(region, year, count)
                rate_str = f"{rate:.3f}"
            except ValueError:
                rate_str = "N/A"
            
            row = f"{region} | {year} | {disease} | {count} | {rate_str}"
            rows.append(row)
            print(f"APPENDED -> {row}")
        

    table_text = "\n".join(rows)

    full_prompt = (
    "⚠️ Please answer in English only.\n\n"
    "You are an infectious disease statistics expert. Below is the outbreak data by region.\n"
    "Below is a structured table showing the number of reported cases of a specific disease.\n"
    "Use only the data provided in the table. Do not make assumptions about what is likely or unlikely.\n\n"
    f"{table_text}\n\n"
    "INSTRUCTIONS:\n"
    "- If all values in the table are zero, clearly state that there have been no reported cases from 2020 to 2024. You may still comment on the importance of maintaining surveillance despite the absence of cases.\n"
    "- If any value is greater than zero (even just 1 case), treat it as a confirmed occurrence and conduct a full analysis, including regional trends, predictions for 2025, and public health recommendations.\n"
    "- Do not summarize or omit any entry with a non-zero case count. Even a single case or low incidence rate (e.g., 0.011 per 100k) is epidemiologically significant.\n"
    "- For example: Seoul in 2020 reported 4 cases of VRSA, resulting in a rate of 0.042 per 100k population. This must be interpreted as a confirmed occurrence.\n"
    "- Never summarize the data as ‘no cases’ if any value is greater than zero. Always cite the actual numbers.\n"
)  

    return full_prompt