import pandas as pd
from make_folder import IN_DIR
import streamlit as st
import matplotlib.pyplot as plt

# D6부터 시작하려면 5행까지 건너뛰고 (엑셀은 0-index가 아님)

plt.rcParams["font.family"] = "Malgun Gothic"
def read_excel(file_name: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    try:
        df = pd.read_excel(
            file_name,
            header=5,
            usecols="B:BR",
        )
        return clear_data(df)
    except FileNotFoundError:
        st.error(f"[❌ 파일 없음] {file_name} 파일을 찾을 수 없습니다.")
    except ValueError as ve:
        st.error(f"[❌ 열 범위 문제] 엑셀 열 범위 또는 형식 문제: {ve}")
    except Exception as e:
        st.error(f"[❌ 예외 발생] 예상치 못한 에러: {e}")


    return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def clear_data(df: pd.DataFrame):
    try:
        df.rename(columns={df.columns[0]: "시도"}, inplace=True)        
        valid_rows = df["시도"].notna() & df["시도"].str.strip().ne("")
        total_row = df[valid_rows].copy()

        total_row.set_index("시도", inplace=True)

        level1 = total_row.loc[:, "에볼라바이러스병":"디프테리아"]
        level2 = total_row.loc[:, "수두":"E형간염"]
        level3 = total_row.loc[:, "파상풍":"@엠폭스"]

        return  level1, level2, level3
    except KeyError as ke:
        print(f"[열 이름 오류] {ke} 열이 없습니다")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    

if __name__ == "__main__":
    level1, level2, level3 = read_excel(IN_DIR / "2015년.xlsx")
    print(level1)