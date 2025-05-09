import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    inputs = {
        'COSAQ00102InBlock1': {
            "RecCnt": 1,            # 레코드갯수
            "QryTpCode": "1",       # 조회구분코드 (1@계좌별)
            "BkseqTpCode": "2",     # 역순구분코드 (1@역순, 2@정순)
            "OrdMktCode": "82",     # 주문시장코드 (81@유욕거래소, 82@나스닥)
            "BnsTpCode": "0",       # 매매구분코드 (0@전체, 1@매도, 2@매수)
            "IsuNo": "",            # 종목번호
            "SrtOrdNo": 0,          # 시작주문번호 (역순인경우 9999999999, 정순인경우 0)
            "OrdDt": "",            # 주문일자
            "ExecYn": "2",          # 체결여부 (0@전체, 1@체결, 2@미체결)
            "CrcyCode": "USD",      # 통화코드 (000:전체, USD:달러)
            "ThdayBnsAppYn": "0",   # 당일매매적용여부 (0@전체, 1@당일적용)
            "LoanBalHldYn": "0",    # 대출잔고보유여부 (0@전체, 1@대출잔고보유)
        },
    }
    response = await api.request('COSAQ00102', inputs)
    if not response: return print(f"요청 실패: {api.last_message}")
    
    # print(response)
    unfills = [dict({
        "주문번호": x["OrdNo"],
        "종목코드": x["ShtnIsuNo"],
        "주문유형": x["OrdPtnCode"],
        "주문수량": x["OrdQty"],
        "주문가격": x["OvrsOrdPrc"],
        "미체결잔량": x["UnercQty"],
        "원주문번호": x["OrgOrdNo"],
        "주문시간": x["OrdTime"],
    }) for x in response.body["COSAQ00102OutBlock3"]]
    print(unfills)
    

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
[]
'''
