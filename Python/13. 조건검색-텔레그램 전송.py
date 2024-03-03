﻿import asyncio
import ebest
from prettytable import *
from app_keys import appkey, appsecretkey, user_id, telegram_token, telegram_chatid
# app_keys.py 파일에 appkey, appsecretkey, user_id, telegram_token, telegram_chatid 변수를 정의하고 사용하세요

from telegram import Bot # pip install python-telegram-bot
bot = Bot(telegram_token)

async def main():
    api=ebest.OpenApi()
    api.on_message = on_message
    api.on_realtime = on_realtime
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    if api.is_simulation: return print("실시간검색은 실서버에서만 가능합니다")
     
    # 조건검색식 리스트 조회
    request = {
        "t1866InBlock": {
            "user_id": user_id, # 사용자ID 8자리
            "gb": "0", # 0 : 그룹+조건리스트 조회, 1 : 그룹리스트조회, 2 : 그룹명에 속한 조건리스트조회
            "group_name": "",
            "cont": "0",
            "cont_key": "",
        }
    }
    response = await api.request("t1866", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    cond_df = response.body["t1866OutBlock1"]
    table = PrettyTable()
    table.field_names = cond_df[0]
    table.add_rows([x.values() for x in cond_df])
    print(table)
    
    # 요청할 조건검색식 선택
    cond_len = len(cond_df)
    sel_index = int(input(f'조건검색식index (0~{cond_len-1})를 입력하세요:'))
    if sel_index >= cond_len: return print("잘못된 index")
    
    # 조건검색식 조회
    query_index = cond_df[sel_index]['query_index']
    request = {
        "t1859InBlock": {
            "query_index": query_index,
        }
    }
    response = await api.request("t1859", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    item_list = response.body.get('t1859OutBlock1', None)
    if item_list:
        table = PrettyTable()
        table.field_names = item_list[0]
        table.add_rows([x.values() for x in item_list])
        print(table)
    else:
        print(f"조건검색식[{query_index}] 결과 없음")
    
    # 실시간검색 등록
    request = {
        "t1860InBlock": {
            "sSysUserFlag": "U", # 'U' 고정
            "sFlag": "E", # 'E:'등록, 'D':중지
            "sAlertNum": "", # Flag 값 'D':중지 일떄만 입력 - 등록 요청 시 수신받은 t1860OutBlock.sAlertNum 값
            "query_index": query_index,
        }
    }
    response = await api.request("t1860", request)
    if not response: return print(f"요청실패: {api.last_message}")
    
    real_req_data = response.body["t1860OutBlock"]
    table = PrettyTable(['key','value'])
    table.add_rows([list(x) for x in real_req_data.items()])
    print(table)
    
    sAlertNum:str = real_req_data["sAlertNum"]
    if sAlertNum == "":
        print("실시간검색 등록실패")
    else:
        print("실시간검색 등록성공, 5분동안 작동...")
        await api.add_realtime("AFR", sAlertNum)
        await bot.send_message(telegram_chatid, f"조건검색 실시간 시작 ({cond_df[sel_index]['query_name']})")

        await asyncio.sleep(5*60) # 5분 동안 유효, 후에 중지
        
        # 실시간검색 중지
        await api.remove_realtime("AFR", sAlertNum)
        await bot.send_message(telegram_chatid, f"조건검색 실시간 중지 ({cond_df[sel_index]['query_name']})")
        await asyncio.sleep(1)
    
    ... # 다른 작업 수행
    await api.close()

def on_message(api:ebest.OpenApi, msg:str): print(f"on_message: {msg}")

async def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == "AFR":
        # 결과중 진입만 텔레그램으로 알림
        if realtimedata["gsJobFlag"] == "N":
            gsCode = realtimedata["gsCode"] # 종목코드
            gshname = realtimedata["gshname"] # 종목명
            gsPrice = realtimedata["gsPrice"] # 현재가
            gsChgRate = realtimedata["gsChgRate"] # 등락률
            gsVolume = realtimedata["gsVolume"] # 거래량
            
            msg = f"[{gsCode}] {gshname}\n {gsPrice}원 {gsChgRate}% {gsVolume}주"
            gg = await bot.send_message(telegram_chatid, msg)
            print(gg.text)

asyncio.run(main())
