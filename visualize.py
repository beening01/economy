from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import pandas as pd
import seaborn as sns
from utils.preprocess import OUT_DIR
from utils.economic_data import OUT1, OUT2

# 국고 금리 상승 => 회사 금리 상승
# 투자위축 => 코스피지수 하락 => 원달러환율 상숭

# 코스피지수 시각화
def kospi(OUT_DIR, OUT1):
    df = pd.read_excel(OUT1, sheet_name='코스피지수', dtype='string')
    df['TIME'] = pd.to_datetime(df['TIME'], format="%Y%m%d")
    df['DATA_VALUE'] = df['DATA_VALUE'].astype(float)

    # 시각화
    sns.set_theme(context="poster", style="whitegrid", font="Malgun Gothic")
    sns.set_style({'grid.linestyle': ":", "grid.color": "#CCCCCC"})

    fig, ax = plt.subplots(figsize=(20, 8), dpi=100)    # 크기 및 해상도
    sns.lineplot(data=df, x="TIME", y="DATA_VALUE", ax=ax)    # 선 그래프
    sns.despine(top=True, right=True)    # 축 제거 여부
    ax.set(title="코스피지수", xlabel="날짜", ylabel="지수")
    fig.set_layout_engine("tight")    # 이미지 여백 제거
    plt.show()
    fig.savefig(OUT_DIR / "kospi.png")

# kospi(OUT_DIR, OUT1)


#주요 경제지표 시각화
def economic_indicator(OUT_DIR, OUT1):
    sns.set_theme(context="poster", style="whitegrid", font="Malgun Gothic")
    sns.set_style({'grid.linestyle': ":", "grid.color": "#CCCCCC"})

    fig, axes = plt.subplots(figsize=(16, 9), dpi=100, nrows=2, ncols=2)    # 4칸을 만들거임
    sheet_names = [['국고채', '코스피지수'], ['회사채', '원달러환율']]  
    for idx_row, row in enumerate(sheet_names):
        for idx_col, name in enumerate(row):
            df = pd.read_excel(OUT1, sheet_name=name, dtype='string')
            df['TIME'] = pd.to_datetime(df['TIME'], format="%Y%m%d")
            df['DATA_VALUE'] = df['DATA_VALUE'].astype(float)
            df_tail = df.tail(100)    # 마지막 100개만 사용
            ax: Axes = axes[idx_row][idx_col]

            sns.lineplot(data=df_tail, x="TIME", y="DATA_VALUE", ax=ax)
            sns.despine(top=True, right=True, bottom=True, left=True)
            ax.set(title=name, ylabel=None, facecolor="#EEEEEE")
            ax.xaxis.set_visible(False)    # 가로축 전체 숨김
    
    fig.set_layout_engine("tight")
    plt.show()
    fig.savefig(OUT_DIR / "economic_indicator.png")

# economic_indicator(OUT_DIR, OUT1)

def bond_line(OUT_DIR, OUT2):
    gk = pd.read_excel(OUT2, sheet_name='국고채(3년)')[['TIME', 'DATA_VALUE', 'ITEM_NAME1']].copy()   # 국고채 시트
    hs = pd.read_excel(OUT2, sheet_name='회사채(3년, AA-)')[['TIME', 'DATA_VALUE', 'ITEM_NAME1']].copy()   # 회사채 시트

    gk['TIME'] = pd.to_datetime(gk['TIME'], format="%Y%m")
    gk['DATA_VALUE'] = gk['DATA_VALUE'].astype(float)

    hs['TIME'] = pd.to_datetime(hs['TIME'], format="%Y%m")
    hs['DATA_VALUE'] = hs['DATA_VALUE'].astype(float)


    # 하나의 리스트에 concat
    df = pd.concat([gk, hs], ignore_index=True)
    df = df.rename(columns={'수익률': '금리'})  # seaborn용 공통 컬럼명

    # 시각화
    sns.set_theme(style='whitegrid', font='Malgun Gothic')
    fig, ax = plt.subplots(figsize=(16, 9), dpi=100)

    sns.lineplot(data=df, x='TIME', y='DATA_VALUE', hue='ITEM_NAME1', ax=ax)

    ax.set(xlabel='', ylabel='시장금리')
    ax.legend_.set_title(None)

    plt.tight_layout()
    plt.show()
    fig.savefig(OUT_DIR / "bond.png")

# bond_line(OUT_DIR, OUT2)