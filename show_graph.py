import streamlit as st
import matplotlib.pyplot as  plt
from make_folder import IN_DIR
from save_csv import read_excel
from draw_graph import plot_each_disease, plot_level_total


def show_graph():
    st.set_page_config(layout="wide")
    st.title("📊 질병 등급별 지역 발병 현황")

    year_range = range(2015, 2024)    
    tabs_by_year = st.tabs([f"{year}년" for year in year_range])

    for i, year in enumerate(year_range):
        with tabs_by_year[i]:
            excel_path = IN_DIR / f"{year}년.xlsx"
            if not excel_path.exists():
                st.warning(f"{year}년 파일이 없습니다.")
                continue

            level1, level2, level3 = read_excel(excel_path)            

            st.markdown(f"📅 {year}년 데이터")
            st.subheader("☑️ 1급 질병")
            plot_each_disease(level1, f"{year}년 1급")

            st.subheader("☑️ 2급 질병")
            plot_each_disease(level2, f"{year}년 2급")

            st.subheader("☑️ 3급 질병")
            plot_each_disease(level3, f"{year}년 3급")


if __name__ == "__main__":
    show_graph()