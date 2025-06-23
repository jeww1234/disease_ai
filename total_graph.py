import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import colormaps
import numpy as np
import re
import matplotlib.font_manager as fm



from pathlib import Path
from generate_prompt import generate_prompt
from itertools import product
from matplotlib.ticker import FormatStrFormatter
from make_folder import IN_DIR
from save_csv import read_excel
from call_AI import call_solar_ai
from translate import translate

font_path = Path(__file__).parent / "fonts_gothic" / "malgun.ttf"
font_prop = fm.FontProperties(fname=font_path).get_name()
plt.rcParams["font.family"] = font_prop

REGIONS = ["서울", "부산", "대구", "인천", "광주", "대전", "울산", 
            "경기", "강원", "충북", "충남", "전북", "전남", "경북", "경남",
            "제주", "세종"]

def extract_abbreviation(name: str) -> str:
    if not name or not isinstance(name, str):
        print(f"⚠️ extract_abbreviation에 잘못된 값 들어옴: {name}")
        return ""
    print(f"extract_abbreviation 받은 값: {name}")
    match = re.search(r"\(([^)]+)\)", name)
    return match.group(1) if match else ""


def show_total_graph(year_range):
    all_data_by_level = {1: [], 2: [], 3: []}
    for year in year_range:
        excel_path = IN_DIR / f"{year}년.xlsx"
        level1, level2, level3 = read_excel(excel_path)        

        for level_df, level in zip([level1, level2, level3], [1, 2, 3]):
            temp = level_df.copy()
            temp.index.name = "지역"
            temp = temp.reset_index()
            temp = temp.melt(id_vars="지역", var_name="질병명", value_name="건수")
            
            temp["연도"] = year
            temp["등급"] = level
            all_data_by_level[level].append(temp)
    # 각 등급별 탭
    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
        div.block-container {
            padding-top: 60px !important;
        }
    </style>
""", unsafe_allow_html=True)
    tabs = st.tabs(["1급 질병", "2급 질병", "3급 질병"])
    for level, tab in zip([1, 2, 3], tabs):
        st.write("📄 원본 level_df 샘플:", level_df.head())
        with tab:
            

            data = pd.concat(all_data_by_level[level])   
            data.columns = data.columns.str.strip().str.replace("\u200b", "", regex=True) 
            st.write("🔍 데이터프레임 컬럼:", data.columns.tolist())
            full_data = data.copy()
            # 질병명 컬럼을 문자열로 한 번만 변환            
            data["질병명"] = data["질병명"].astype(str)   
            st.write("🔍 질병명:", data["질병명"].unique())
            st.dataframe(data.head())  # 또는 data.tail()
            # NaN이나 float 섞인 문제 방지
            disease_options = sorted(data["질병명"].unique())   
            st.write("🔍 질병명 리스트:", disease_options)
            # 지역 선택
            regions = st.multiselect("지역 선택", options=REGIONS, default='서울', key=f"region_{level}")    
            # 질병 선택
            disease = st.selectbox("질병 선택", disease_options, key=f"disease_{level}")                            
            st.write("🔍 현재 선택된 질병:", disease) 
            color_map = colormaps['tab20']  # 20개까지 구분 가능한 색상
            colors = [color_map(i / len(regions)) for i in range(len(regions))]
            years = sorted(data["연도"].unique())            
            bar_width = 0.8 / len(regions)
            fig, ax = plt.subplots(figsize=(6,2.7), dpi=100)
            for i, region in enumerate(regions):                
                filtered = data[(data["지역"] == region) & (data["질병명"] == disease)]
                summary = filtered.groupby("연도")["건수"].sum().reset_index()
                summary["연도"] = summary["연도"].astype(int)
                summary["건수"] = pd.to_numeric(summary["건수"], errors='coerce').fillna(0)

                region_x = [year + i * bar_width for year in summary["연도"]]
                ax.bar(region_x, summary["건수"], width=bar_width, label=region, color=colors[i])
                ax.tick_params(axis='x', labelrotation=15)            
            ax.legend(
                    title="지역",
                    fontsize=6,
                    bbox_to_anchor=(1.05, 1),  # 오른쪽 바깥
                    loc='upper left'
                )            
            ax.xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
            ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f'))
            tick_positions = [year + bar_width * (len(regions)/ 2 -0.5)for year in years]
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(years, fontsize=4)
            ax.set_xlabel("년도", fontsize = 5)
            ax.set_ylabel("건수", fontsize = 5)   
            abbr = extract_abbreviation(disease)             
            ax.set_title(f"{abbr} 연도별 지역 비교", fontsize=5)
            fig.tight_layout(pad=0)  # 여백 줄이기
            col1, col2 = st.columns([2,1])
            with col1:                
                st.pyplot(fig, clear_figure=True, use_container_width=True)

            with col2:
                with st.expander("📈 AI 분석 결과 보기"):
                    if st.button("AI 분석 실행", key=f"analyze_btn_{level}"):
                        prompt = generate_prompt(disease, regions, full_data, year_range, level)
                        with st.spinner("AI 분석 중..."):
                            ai_response = call_solar_ai(prompt)
                            result = translate(ai_response)
                            st.write(result)

    


if __name__ == "__main__":    
    year_range = [int(y) for y in range(2020, 2025)]
    show_total_graph(year_range)
    