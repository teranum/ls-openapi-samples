﻿import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요
from prettytable import *

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "t8410InBlock": {
            "shcode": "005930", # 삼성전자
            "gubun": "2", # 주기구분(2:일3:주4:월5:년)
            "qrycnt": 100, # 요청건수(최대-압축:2000비압축:500)
            "sdate": "", # 시작일자
            "edate": "99999999", # 종료일자
            "cts_date": "", # 연속일자
            "comp_yn": "N", # 압축여부(Y:압축N:비압축)
            "sujung": "Y", # 수정주가여부(Y:적용N:비적용)
        }
    }
    response = await api.request("t8410", request)
    
    if not response: return print(f"요청실패: {api.last_message}")
    
    data1 = response.body["t8410OutBlock1"]
    data2 = []
    
    # 연속조회
    if response.tr_cont == "Y":
        await asyncio.sleep(1) # 1초 대기
        request["t8410InBlock"]["cts_date"] = response.body["t8410OutBlock"]["cts_date"]
        response = await api.request("t8410", request, tr_cont=response.tr_cont, tr_cont_key=response.tr_cont_key)
        
        if not response: return print(f"연속 요청실패: {api.last_message}")
    
        data2.extend(response.body["t8410OutBlock1"])
    
    data = data2 + data1 # 연속조회 데이터와 첫번째 조회 데이터를 합침
    table = PrettyTable()
    table.field_names = data[0]
    table.add_rows([x.values() for x in data])
    print(table)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())
