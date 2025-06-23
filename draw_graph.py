import matplotlib.pyplot as  plt
import pandas as pd
import streamlit as st
from make_folder import IN_DIR


def plot_level_total(level_df, level_name: str):
    plt.rcParams["font.family"] = "Malgun Gothic"
    totals = level_df.sum(axis=1)
    fig, ax = plt.subplots(figsize=(10, 8))
    totals.plot(kind="bar", title=f"{level_name} 질병 총합(지역별)", color="skyblue", ax=ax)
    ax.set_ylabel("발병 횟수")
    ax.set_ylim(bottom=0)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    ax.set_xlabel("지역")
    ax.tick_params(axis='x', rotation=25)
    plt.tight_layout()
    st.pyplot(fig)

def plot_each_disease(level_df, level_name: str):
    plt.rcParams["font.family"] = "Malgun Gothic"
    st.subheader(f"{level_name} 질병별 지역 발병 그래프")
    disease = st.selectbox(f"{level_name} 질병을 선택하세요", level_df.columns.tolist())
    data = pd.to_numeric(level_df[disease], errors="coerce")
    fig, ax = plt.subplots(figsize=(10, 8))
    data.plot(kind="bar", title=f"{level_name}-{disease} 발병 횟수", color="lightcoral", ax=ax)
    ax.set_ylabel("발병 횟수")
    ax.set_ylim(bottom=0)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))
    ax.set_xlabel("지역")
    ax.tick_params(axis='x', rotation=25)
    plt.tight_layout()
    st.pyplot(fig)        

if __name__ == "__main__":
    plot_each_disease()
    plot_level_total
