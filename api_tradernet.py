from datetime import datetime
import json
import os

from typing import Dict

import PublicApiClient as NtApi


pub_ = os.getenv("PUBLIC_KEY")
sec_ = os.getenv("SECRET_KEY")


def write_to_json(content, filename)->None:
    filename = filename if filename else "response"
    with open(f'output/{filename}.json', 'w', encoding='utf8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


def mk_request(cmd_:str, params_:Dict={}, isV1=False, filename=None,
               url:str = None)->None:
    res = NtApi.PublicApiClient(pub_, sec_, NtApi.PublicApiClient().V2)
    if isV1:
        res = NtApi.PublicApiClient(pub_, sec_, NtApi.PublicApiClient().V1)
    if url:
        res.setApiUrl(url)
    write_to_json(res.sendRequest(cmd_, params_).json(), filename=filename)


def search_ticker(search_str: str)->None:
    cmd_ = "tickerFinder"
    params_ = {
        "text": search_str
    }
    mk_request(cmd_, params_, True) 
     

def get_user_data()->None:
    cmd_ = "getOPQ"
    mk_request(cmd_)
    

def get_trade_hist(ticker, from_, to_, timeframe=1440):
    cmd_   = 'getHloc'
    params_ = {
        'id'           : ticker,
        'count'        : -1,
        'timeframe'    : timeframe,
        # "date_from"    : '16.08.2020 00:00',
        # "date_to"      : '17.08.2020 00:00',
        'date_from'    : datetime.strftime(from_, "%d.%m.%Y %H:%M"),
        'date_to'      : datetime.strftime(to_, "%d.%m.%Y %H:%M"),
        'intervalMode' : 'ClosedRay'
    }
    
    mk_request(cmd_, params_, filename=f'trades_{ticker}', isV1=True) 
     

def get_session_info()->None:
    cmd_ = "getSidInfo"
    params_ = {}
    
    mk_request(cmd_, params_, filename="sid_info") 


def get_trades()->None:
    """
    Получении истории сделок по пользователю
    """
    cmd_ ='getTradesHistory'
    params_ = {
        "nt_ticker": "SBER",
    }

    mk_request(cmd_, params_)


def get_sec_info(ticker: str)->None:
    cmd_ ='getSecurityInfo'
    params_ = {
        'ticker': f'{ticker}',
        'sup': True
    }
    mk_request(cmd_, params_)


def get_sec_data(ticker)->None:
    cmd_ ='getStockData'
    params_ = {
        'ticker': f'{ticker}',
        'lang': 'ru'
    }
    mk_request(cmd_, params_)
    

def auth()->None:
    cmd_ = "getSecuritySms"
    mk_request(cmd_)

    sms_code = input("Введи код из смс: ")
    sms_code = sms_code.strip()
    
    cmd_ = "openSecuritySession"

    params_ = {
        "safetyTypeId": 3,
        "validationKey": f"{sms_code}"
    }
    
    mk_request(cmd_, params_)
    
    
if __name__=="__main__":
    # auth()
    # get_trades()
    search_ticker("MUM132_0007")
    # get_sec_data("AAPL")
    # get_session_info()
    # get_user_data() 
    get_trade_hist("MUM132_0007.KZ", 
                   from_=datetime(2022, 8, 23), 
                   to_=datetime(2022, 12, 31))