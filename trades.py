from datetime import datetime
import json
from typing import Dict

from pathlib import Path

import pandas as pd
import numpy as np


def read_json_file(ticker: str):
    filepath = Path(f"output/trades_{ticker}.json")
    with open(filepath, 'r', encoding='utf8') as f:
        df_json = json.load(f)
    return df_json


def mk_df_from_json(ticker: str, df_json: Dict=None):

    if not df_json:
        df_json = read_json_file(ticker)

    df = pd.DataFrame()

    for ticker in df_json['hloc'].keys():
        hloc = np.array(df_json['hloc'][ticker])
        l, _ = hloc.shape
        vl = df_json['vl'][ticker]
        tradedates = df_json['xSeries'][ticker]
        high_price = hloc[:,0]
        low_price = hloc[:,1]
        open_price = hloc[:,2]
        close_price = hloc[:,3]

        dataset = {
            'tradedate': tradedates,
            'ticker': [ticker] * l,
            'short_name': [df_json['info'][ticker]['short_name']] * l, 
            'currency': [df_json['info'][ticker]['currency']] * l, 
            'high_price': high_price,
            'low_price': low_price,
            'open_price': open_price,
            'close_price': close_price,
            'volume': vl
        }

        tmp = pd.DataFrame(dataset).sort_values('tradedate')
        tmp['tradedate'] = pd.to_datetime(tmp['tradedate'], unit='s') 
        df = pd.concat([df, tmp])
    
    return df 
    
    
print(mk_df_from_json('MUM132_0007.KZ'))