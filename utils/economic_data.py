# 기준금리: 시중 은행의 대출 및 예금 금리를 결정하는 기준이 되는 금리
# 국고채 금리: 정부가 자금을 조달하기 위해 발행하는 채권의 금리
# 회사채 금리: 기업이 자금을 조달하기 위해 발행하는 채권의 금리
# 코스피지수: 코스피 시장에 상장된 주식의 전체적인 가격 변동을 반영
# 원달러환율: 원화와 달러간 교환 비율(환율이 낮으면 원화의 가치가 높음)

from pathlib import Path
import pandas as pd
from datakart import Ecos
from .preprocess import OUT_DIR, api_info


OUT1 = OUT_DIR / 'total_data.xlsx'

ECOS_KEY = api_info['KEY']
def economic_data(ECOS_KEY):
    with pd.ExcelWriter(OUT1) as writer:
        ecos = Ecos(ECOS_KEY)
        for data in list(api_info.items())[1:6]:
            resp = ecos.stat_search(
                stat_code=data[1]['code'],
                freq=data[1]['freq'],
                item_code1=data[1]['item_code1'],
                limit=data[1]['limit']
            )
            df = pd.DataFrame(resp)
            df.to_excel(writer, sheet_name=data[1]['name'], index=False)



OUT2 = OUT_DIR / 'bond_data.xlsx'
def bond_data(ECOS_KEY):
    with pd.ExcelWriter(OUT2) as writer:
        ecos = Ecos(ECOS_KEY)
        for data in list(api_info.items())[6:8]:
            resp = ecos.stat_search(
                stat_code=data[1]['code'],
                freq=data[1]['freq'],
                item_code1=data[1]['item_code1'],
                start=data[1]['start'],
                end=data[1]['end']
            )
            df = pd.DataFrame(resp)
            df.to_excel(writer, sheet_name=data[1]['name'], index=False)

if __name__ == "__main__":
    from preprocess import OUT_DIR, api_info
    economic_data(ECOS_KEY)
    bond_data(ECOS_KEY)