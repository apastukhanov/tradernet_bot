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


def mk_request(cmd_:str, params_:Dict={}, isV1=False, filename=None)->None:
    res = NtApi.PublicApiClient(pub_, sec_, NtApi.PublicApiClient().V2)
    if isV1:
        res = NtApi.PublicApiClient(pub_, sec_, NtApi.PublicApiClient().V1)
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
    

def get_session_info()->None:
    cmd_ = "getSidInfo"
    params_ = {}
    
    mk_request(cmd_, params_, filename="sid_info") 


def get_trades():
    """
    Получении истории сделок по пользователю
    """
    cmd_ ='getTradesHistory'
    params_ = {
        "nt_ticker": "SBER",
    }

    mk_request(cmd_, params_)


def get_sec_info(ticker: str):
    cmd_ ='getSecurityInfo'
    params_ = {
        'ticker': f'{ticker}',
        'sup': True
    }
    mk_request(cmd_, params_)


def get_sec_data(ticker):
    cmd_ ='getStockData'
    params_ = {
        'ticker': f'{ticker}',
        'lang': 'ru'
    }
    mk_request(cmd_, params_)
    

def auth():
    cmd_ = "openSecuritySession"
    params_ = {
        "safetyTypeId": 3,
        "validationKey": "745166"
    }
    
    mk_request(cmd_, params_)
    
    
if __name__=="__main__":
    # auth()
    # get_trades()
    # search_ticker("AAPL")
    get_sec_data("AAPL")
    get_session_info()
    # get_user_data()