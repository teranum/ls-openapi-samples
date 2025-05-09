import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    inputs = {
        'COSOQ00201InBlock1': {
            "RecCnt": 1,            # 레코드갯수
            "BaseDt": "",           # 기준일자
            "CrcyCode": "USD",      # 통화코드 (ALL:전체, USD:달러)
            "AstkBalTpCode": "00",  # 해외증권잔고구분코드 (00:전체, 10:일반, 20:소수점))
        },
    }
    response = await api.request('COSOQ00201', inputs)
    if not response: return print(f"요청 실패: {api.last_message}")
    
    # print(response)
    print(f"원화예수금: {response.body["COSOQ00201OutBlock2"]["WonDpsBalAmt"]}")
    balances = [dict({
        "통화코드": x["CrcyCode"],
        "종목코드": x["ShtnIsuNo"],
        "잔고수량": x["AstkBalQty"],
        "매도가능수량": x["AstkSellAbleQty"],
        "평균단가": x["FcstckUprc"],
        "현재가": x["OvrsScrtsCurpri"],
        "수익율": x["PnlRat"],
    }) for x in response.body["COSOQ00201OutBlock4"]]
    print(balances)
    

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey):
        return print(f'연결실패: {api.last_message}')
    await sample(api)
    await api.close()

if __name__ == '__main__':
    asyncio.run(main())


# Output:
'''
원화예수금: 0
[]
'''
