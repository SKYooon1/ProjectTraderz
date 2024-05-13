import pykis
import requests
import json
import yaml
import time
import websockets
import asyncio
import os
import mplfinance as mpf
import pandas as pd
from pykis import *

from pandas import DataFrame

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

with open(r'config.yaml', encoding='UTF-8') as f:
    _cfg = yaml.load(f, Loader=yaml.FullLoader)
APP_KEY = _cfg['APP_KEY']
APP_SECRET = _cfg['APP_SECRET']
ACCESS_TOKEN = ""
CANO = _cfg['CANO']
ACNT_PRDT_CD = _cfg['ACNT_PRDT_CD']
ACTUAL_DOMAIN = _cfg['ACTUAL_DOMAIN']
WEB_SOCKET_DOMAIN = _cfg['WEB_SOCKET_DOMAIN']

kis = Api(APP_KEY, APP_SECRET)


def get_access_token():
    url = '/oauth2/tokenP'
    request_url = f"{ACTUAL_DOMAIN}/{url}"
    headers = {}
    body = {
        "grant_type": "client_credentials",
        "appkey": "PSbo0XjQiPUzcPC9LmxHAzZdLhZa8CZRChhg",
        "appsecret": "bF4yV1QtvBJBifPzw4B8mOsYwCPnX/vUZv38nBP8yA3mdc3QmwmWghwrSx3M+jdqiTqLhroebxgc69zwZwFdf2BgnhYuHA0usueZyvQQrbq/8lzPDQ3+Zi5xGXR1yqu3eFlz5lhxL4OTtqFeKvJKU8TrEJYAKo4pKZUE9vIEbJ53sWnfHGo=",
    }

    res = requests.post(request_url, data=json.dumps(body), headers=headers)
    rescode = res.status_code
    if rescode == 200:
        ACCESS_TOKEN = res.json()["access_token"]
    else:
        print("Error Code : " + str(rescode) + " | " + res.text)

    return ACCESS_TOKEN


def get_approval():
    url = '/oauth2/Approval'
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": APP_KEY,
            "secretkey": APP_SECRET}
    request_url = f"{ACTUAL_DOMAIN}/{url}"
    res = requests.post(request_url, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key



def get_balance():
    url = "/uapi/domestic-stock/v1/trading/inquire-psbl-order"
    request_url = f"{ACTUAL_DOMAIN}/{url}"
    headers = {"Content-Type": "application/json",
               "authorization": f"Bearer {ACCESS_TOKEN}",
               "appKey": APP_KEY,
               "appSecret": APP_SECRET,
               "tr_id": "TTTC8908R",  # 실전투자값: TTTC8908R
               "custtype": "P",  # P: 개인
               }
    params = {
        "CANO": CANO,  # 계좌번호
        "ACNT_PRDT_CD": ACNT_PRDT_CD,  # 계좌번호 뒷자리
        "PDNO": "005930",  # 종목 코드 005930은 삼성
        "ORD_UNPR": "65500",  # 1주당 가격
        "ORD_DVSN": "01",  # 01: 시장가
        "CMA_EVLU_AMT_ICLD_YN": "Y",  # CMA 평가금액포함여부: Y
        "OVRS_ICLD_YN": "Y"  # 해외포함여부: Y
    }
    res = requests.get(request_url, headers=headers, params=params)
    cash = res.json()['output']['ord_psbl_cash']
    print(f"주문 가능 현금 잔고: {cash}원")
    return int(cash)


# 국내주식기간별시세
def get_kor_stock_period_data(stock_code="005930", start_date="20210901", end_date="20220101", period="D"):
    url = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
    request_url = f"{ACTUAL_DOMAIN}/{url}"
    headers = {"Content-Type": "application/json",
               "authorization": f"Bearer {ACCESS_TOKEN}",
               "appKey": APP_KEY,
               "appSecret": APP_SECRET,
               "tr_id": "FHKST03010100",
               "custtype": "P",  # P: 개인
               }

    params = {
        "FID_COND_MRKT_DIV_CODE": "J",  # J : 주식
        "FID_INPUT_ISCD": stock_code,  # 종목번호 (6자리)
        "FID_INPUT_DATE_1": start_date,  # 조회 시작일자 (ex. 20220501)
        "FID_INPUT_DATE_2": end_date,  # 조회 종료일자 (ex. 20220530)
        "FID_PERIOD_DIV_CODE": period,  # D:일봉, W:주봉, M:월봉, Y:년봉
        "FID_ORG_ADJ_PRC": "1",  # 0:수정주가 1:원주가
    }

    res = requests.get(request_url, headers=headers, params=params)
    print(res.json())
    return res.json()


# 국내주식실시간 체결가
async def get_kor_realtime_stock_price(stock_code='005930'):
    # 웹 소켓에 접속.( 주석은 koreainvest test server for websocket)
    g_personalsecKey = '651e382e-72ce-4cde-9ff7-6e51006e6a11'
    custtype = 'P'  # customer type, 개인:'P' 법인 'B'
    tr_type = '1'
    tr_id = 'H0STCNT0'

    async with websockets.connect(WEB_SOCKET_DOMAIN, ping_interval=None) as websocket:
        senddata = '{"header":{"appkey":"' + APP_KEY \
                   + '","appsecret":"' + APP_SECRET + '","personalseckey":"' + g_personalsecKey \
                   + '","custtype":"' + custtype + '","tr_type":"' + tr_type \
                   + '","content-type":"utf-8"},"body":{"input":{"tr_id":"' + tr_id \
                   + '","tr_key":"' + stock_code + '"}}}'
        await websocket.send(senddata)
        time.sleep(1)

        # 데이터가 오기만 기다린다.
        while True:
            data = await websocket.recv()
            # print("Recev Command is :", data)
            if data[0] == '0':
                recv_str = data.split('|')
                stock_data = recv_str[3]
                stock_data_split = stock_data.split('^')
                stock_now_price = stock_data_split[2]  # 2 = 현재가 인덱스
                print(stock_now_price)

# 주식현재가 시세
def get_current_price(stock_no):
    PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
    URL = f"{ACTUAL_DOMAIN}/{PATH}"

    # 헤더 설정
    headers = {"Content-Type":"application/json",
            "authorization": f"Bearer {ACCESS_TOKEN}",
            "appKey":APP_KEY,
            "appSecret":APP_SECRET,
            "tr_id":"FHKST01010100"}

    params = {"fid_cond_mrkt_div_code":"J",
            "fid_input_iscd": stock_no}

    # 호출
    res = requests.get(URL, headers=headers, params=params)

    if res.status_code == 200 and res.json()["rt_cd"] == "0" :
        return(res.json())
    else:
        print("Error Code : " + str(res.status_code) + " | " + res.text)
        return None


def json_to_df_kor_stock_data(json_data):
    stock_data = json_data['output2']

    df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])
    for i in stock_data:
        stock_day_data = [
            [i['stck_bsop_date'], i['stck_oprc'], i['stck_hgpr'], i['stck_lwpr'], i['stck_clpr'], i['acml_vol']]]
        stock_day_data_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        stock_day_data_index = [i['stck_bsop_date']]
        stock_day_df = DataFrame(data=stock_day_data, index=stock_day_data_index, columns=stock_day_data_columns)
        df = pd.concat([df, stock_day_df])

    df = df.sort_index(ascending=True)
    return df


def calc_SMA(data, period=20):
    return data.rolling(window=period).mean()


def calc_ICMK(data, period=26):
    period_high = data['High'].rolling(window=period).max()
    period_low = data['Low'].rolling(window=period).min()
    return (period_high + period_low) / 2


ACCESS_TOKEN = get_access_token()
#ACCESS_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJ0b2tlbiIsImF1ZCI6Ijg5MDE4OWIwLWU3YTUtNDU0NS04OGQ0LWE5ZGQzZDhjYzRmOSIsInByZHRfY2QiOiIiLCJpc3MiOiJ1bm9ndyIsImV4cCI6MTcxNTY1NTQ0MCwiaWF0IjoxNzE1NTY5MDQwLCJqdGkiOiJQU2JvMFhqUWlQVXpjUEM5TG14SEF6WmRMaFphOENaUkNoaGcifQ.oASa_W4gL8TS860x-s6pq5aL6o9ikwNFfiErqRcNHOmF6tb2otQQNtizPg-qroUAytyX_vMlAFvsFLHJYHAPKA"
print(ACCESS_TOKEN)

# get_balance()

stockJson = get_kor_stock_period_data()
stockDF = json_to_df_kor_stock_data(stockJson)
stockDF['SMA5'] = calc_SMA(stockDF['Close'], 5)
stockDF['SMA20'] = calc_SMA(stockDF['Close'], 20)
stockDF['SMA60'] = calc_SMA(stockDF['Close'], 60)

stockDF['ICMK'] = calc_ICMK(stockDF, 26)

print(stockDF)

df = stockDF
df = df.sort_values(by='Date')
df.index = pd.to_datetime(df.Date)
df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
df = df.astype(float)
print(df)

# mpf.plot(df, title='Celltrion candle chart', type='candle')
# mpf.plot(df, title='Celltrion ohlc chart', type='ohlc')
kwargs = dict(title='Celltrion customized chart', type='candle',
              mav=(5, 10, 20), volume=True, ylabel='ohlc candles')
mc = mpf.make_marketcolors(up='r', down='b', inherit=True)
s = mpf.make_mpf_style(marketcolors=mc)
mpf.plot(df, **kwargs, style=s)

#get_current_price('005930')
