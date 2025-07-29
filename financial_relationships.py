from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

from utils.preprocess import OUT_DIR
from utils.preprocess import total_data_load
from utils.economic_data import OUT1, OUT2


def corr_heatmap(OUT_DIR, OUT1):
    # ------------------------------------
    # ✅ 3. 상관관계 히트맵 (Plotly)
    # ------------------------------------
    df = total_data_load(OUT1)
    df_wide = df.pivot(index="TIME", columns="ITEM_NAME1", values="DATA_VALUE")


    corr = df_wide.corr().round(2)  # << 소수점 2자리로 반올림

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

corr_heatmap(OUT_DIR, OUT1)