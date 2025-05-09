import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

########################################################################################
# 1. 계좌 실시간 등록 ("AS0", "AS1", "AS2", "AS3", "AS4")
# 2. 잔고 / 미체결 조회 (COSOQ00201, COSAQ00102)
# 3. 주문요청 : (매수, 매도, 정정, 취소), (시장가, 지정가) (COSAT00301, COSAT00311)
########################################################################################

async def sample(api):
    print("해외주식계좌 실시간 등록")
    for real_cd in ["AS0", "AS1", "AS2", "AS3", "AS4"]: # AS0: 해외주식주문접수, AS1: 해외주식주문체결, AS2: 해외주식주문정정, AS3: 해외주식주문취소, AS4: 해외주식주문거부
        await api.add_realtime(real_cd, "")

    while True:
        # 잔고 표시
        print("잔고조회중...")
        inputs = {
            'COSOQ00201InBlock1': {
                "RecCnt": 1,            # 레코드갯수
                "BaseDt": "",           # 기준일자
                "CrcyCode": "USD",      # 통화코드 (ALL:전체, USD:달러)
                "AstkBalTpCode": "00",  # 해외증권잔고구분코드 (00:전체, 10:일반, 20:소수점))
            },
        }
        response = await api.request("COSOQ00201", inputs)
        if not response:
            print(f"잔고 요청실패: {api.last_message}")
            break
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

        # 미체결 표시
        print("미체결조회중...")
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
        if not response:
            print(f"미체결 요청실패: {api.last_message}")
            break
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

        # 주문요청 입력
        주문요청 = await ainput("주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):")
        if len(주문요청) == 0:
            break
        if 주문요청 in ("1", "2"):
            # 주문 정보 입력
            try:
                종목코드 = await ainput("미국주식 종목코드를 입력하세요 (ex 82TSLA: 테슬라, 82AAPL: 애플):")
                주문유형 = "02" if 주문요청 == "1" else "01"
                호가구분 = await ainput("호가구분을 입력하세요 (00:지정가, 03:시장가):")
                주문가격 = float(0 if 호가구분 == "03" else await ainput("주문가격을 입력하세요:"))
                주문수량 = int(await ainput("주문수량을 입력하세요:"))
            except :
                print("입력오류")
                break

            주문시장코드, 종목번호 = 종목코드[:2], 종목코드[2:]
        
            # 신규주문 요청
            inputs = {
                'COSAT00301InBlock1': {
                    "RecCnt": 1,                # 레코드갯수
                    "OrdPtnCode": 주문유형,     # 주문유형코드 (01:매도 02:매수 08:취소)
                    "OrgOrdNo": 0,              # 원주문번호
                    "OrdMktCode": 주문시장코드, # 주문시장코드 (81:뉴욕거래소, 82:나스닥)
                    "IsuNo": 종목번호,          # 종목번호 (ex.TSLA:테슬라, AAPL:애플)
                    "OrdQty": 주문수량,         # 주문수량
                    "OvrsOrdPrc": 주문가격,     # 해외주문가
                    "OrdprcPtnCode": 호가구분,  # 호가유형코드 (00:보통, 03:시장가)
                    "BrkTpCode": "",            # 중개인구분코드
                },
            }
            response = await api.request('COSAT00301', inputs)
            # print(response)
            if not response:
                print(f"주문요청 실패: {api.last_message}")
            else:
                print(f"주문요청 결과: [{response.body['rsp_cd']}] {response.body['rsp_msg']}")
    
        elif 주문요청 in ("3", "4"):
            # 정정/취소 정보 입력
            try:
                주문번호 = int(await ainput("주문번호를 입력하세요:"))
                정정가격 = int(await ainput("정정가격을 입력하세요:") if 주문요청 == "3" else 0)
            except :
                print("입력오류")
                break
        
            # 주문번호 일치하는 미체결내역 조회
            matched_unfill = next((x for x in unfills if x["주문번호"] == 주문번호), None)
            if not matched_unfill:
                print(f"주문번호 {주문번호}에 대한 미체결내역이 없습니다.")
            else:
                if 주문요청 == "3":
                    # 정정요청
                    inputs = {
                        'COSAT00311InBlock1': {
                            "RecCnt": 1,                # 레코드갯수
                            "OrdPtnCode": "07",         # 주문유형코드 (07:입력)
                            "OrgOrdNo": 주문번호,       # 원주문번호
                            "OrdMktCode": "",           # 주문시장코드 (81:뉴욕거래소, 82:나스닥)
                            "IsuNo": "",                # 종목번호
                            "OrdQty": 0,                # 주문수량 (0 입력)
                            "OvrsOrdPrc": 정정가격,     # 해외주문가 (정정가격: 원주문과 다른 가격)
                            "OrdprcPtnCode": "",        # 호가유형코드
                            "BrkTpCode": "",            # 중개인구분코드
                        },
                    }
                    response = await api.request("COSAT00311", inputs)
                    if not response:
                        print(f"정정 요청실패: {api.last_message}")
                    else:
                        print(f"정정 요청 결과: [{response.body['rsp_cd']}] {response.body['rsp_msg']}")
                else:
                    # 취소요청
                    inputs = {
                        'COSAT00301InBlock1': {
                            "RecCnt": 1,                # 레코드갯수
                            "OrdPtnCode": "08",         # 주문유형코드 (01:매도 02:매수 08:취소)
                            "OrgOrdNo": 주문번호,       # 원주문번호
                            "OrdMktCode": "",           # 주문시장코드 (81:뉴욕거래소, 82:나스닥)
                            "IsuNo": "",                # 종목번호 (ex.TSLA:테슬라, AAPL:애플)
                            "OrdQty": 0,                # 주문수량
                            "OvrsOrdPrc": 0,            # 해외주문가
                            "OrdprcPtnCode": "00",      # 호가유형코드 (00:보통, 03:시장가)
                            "BrkTpCode": "",            # 중개인구분코드
                        },
                    }
                    response = await api.request("COSAT00301", inputs)
                    if not response:
                        print(f"취소 요청실패: {api.last_message}")
                    else:
                        print(f"취소 요청 결과: [{response.body['rsp_cd']}] {response.body['rsp_msg']}")

        else:
            print("잘못된 입력입니다.")
            break
        
        await asyncio.sleep(1) # 1초 대기 후 반복
        pass

    print("해외주식계좌 실시간 해지")
    for real_cd in ["AS0", "AS1", "AS2", "AS3", "AS4"]:
        await api.remove_realtime(real_cd, "")
    print("주문종료")
    

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    print(f'실시간 이벤트: {trcode}, {key}, {realtimedata}')

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey):
        return print(f'연결실패: {api.last_message}')

    # 실시간 이벤트 핸들러 등록
    api.on_realtime.connect(on_realtime)

    await sample(api)

    # 실시간 이벤트 핸들러 해제
    api.on_realtime.disconnect(on_realtime)
    await api.close()

if __name__ == '__main__':
    asyncio.run(main())


# Output:
'''
해외주식계좌 실시간 등록
잔고조회중...
원화예수금: 0
[]
미체결조회중...
[]
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):1
미국주식 종목코드를 입력하세요 (ex 82TSLA: 테슬라, 82AAPL: 애플):82TSLA
호가구분을 입력하세요 (00:지정가, 03:시장가):00
주문가격을 입력하세요:280
주문수량을 입력하세요:1
주문요청 결과: [02611] 장시작 전 또는 장마감 되었습니다.
잔고조회중...
원화예수금: 0
[]
미체결조회중...
[]
주문을 입력하세요 (1:매수, 2:매도, 3:정정, 4:취소):
해외주식계좌 실시간 해지
주문종료
'''
