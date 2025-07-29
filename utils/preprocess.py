from pathlib import Path
import requests
import yaml
import pandas as pd

WORK_DIR = Path(__file__).parent.parent
OUT_DIR = WORK_DIR / 'outputs'
OUT_DIR.mkdir(exist_ok=True)


API_INFO = WORK_DIR / "api.yaml"
with open(API_INFO, "r", encoding='utf-8') as f:
    api_info = yaml.load(f, Loader=yaml.Loader)

total_data = OUT_DIR / "total_data.xlsx"
def total_data_load(total_data):
    sheet_names = [['기준금리', '국고채', '회사채'], ['코스피지수', '원달러환율']]
    i=0  
    for idx_row, row in enumerate(sheet_names):
        for idx_col, name in enumerate(row):
            df = pd.read_excel(total_data, sheet_name=name, dtype='string')
            df['TIME'] = pd.to_datetime(df['TIME'], format="%Y%m%d")
            df['DATA_VALUE'] = df['DATA_VALUE'].astype(float)
            if i==0:
                result = df
                i += 1
            else:
                result = pd.concat([result, df], ignore_index=True)

    return result



if __name__ == "__main__":
    resp = requests.get(api_info['API'])
    print(resp.json())