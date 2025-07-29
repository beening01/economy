from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import statsmodels.api as sm


from utils.preprocess import OUT_DIR
from utils.preprocess import total_data_load
from utils.economic_data import OUT1

df = total_data_load(OUT1)
df = df.pivot(index="TIME", columns="ITEM_NAME1", values="DATA_VALUE").dropna()
df.rename(columns={
    '한국은행 기준금리': '기준금리',
    'KOSPI지수': 'KOSPI',
    '원/미국달러(매매기준율)': '환율'
}, inplace=True)

def corr_heatmap(OUT_DIR, df):
    # ------------------------------------
    # ✅ 3. 상관관계 히트맵 (Plotly)
    # ------------------------------------
    corr = df.corr().round(2)  # << 소수점 2자리로 반올림

    # 히트맵 생성
    fig = ff.create_annotated_heatmap(
        z=corr.values,
        x=corr.columns.tolist(),
        y=corr.index.tolist(),
        annotation_text=corr.values.round(2).astype(str),  # 보기 좋은 숫자만 표시
        colorscale="RdBu",  # 컬러맵 바꿈 (양/음 대비 뚜렷)
        showscale=True
    )

    # 레이아웃 개선
    fig.update_layout(
    title="📊 금융지표 간 상관관계 히트맵",
    width=1200,
    height=800,
    font=dict(size=13),
    margin=dict(t=80, l=250),  # 왼쪽 여백 더 늘림
    yaxis=dict(automargin=True)  # 자동 여백 적용
    )
    fig.update_yaxes(tickangle=0)  # 0도: 수평

    fig.show()
    # 이미지 저장 (plotly는 .write_image 사용)
    fig.write_image(str(OUT_DIR / "corr_heatmap.png"))

# corr_heatmap(OUT_DIR, df)

def bubble(OUT_DIR, df):
    # ------------------------------------
    # ✅ 4. 버블 차트 (Plotly)
    # 예: 기준금리 (x), KOSPI (y), 환율 (버블 크기)
    # ------------------------------------
    df = df.reset_index()

    # 2. 필요한 컬럼만 추출하고 결측 제거
    df_plot = df[['TIME', '기준금리', 'KOSPI', '환율']].dropna()

    # 3. 기준금리를 구간으로 나눔 (시각적 구분)
    bins = [0, 2.0, 2.5, 3.0, 3.5, 10]
    labels = ['~2.0%', '2.0~2.5%', '2.5~3.0%', '3.0~3.5%', '3.5%~']
    df_plot['기준금리_구간'] = pd.cut(df_plot['기준금리'], bins=bins, labels=labels)

    # 4. 버블차트 생성
    fig = px.scatter(
        df_plot,
        x='환율',
        y='KOSPI',
        size='기준금리',
        color='기준금리_구간',
        hover_data=['TIME', '기준금리', '환율', 'KOSPI'],
        title='환율 vs KOSPI (버블: 기준금리, 색: 기준금리 구간)',
        size_max=25,
        template='plotly_white'
    )

    # 5. 시각화 옵션
    fig.update_layout(
        height=700,
        width=900,
        font=dict(size=13),
        legend_title='기준금리 구간',
    )

    fig.show()
    fig.write_image(str(OUT_DIR / "bubble.png"))


bubble(OUT_DIR, df)