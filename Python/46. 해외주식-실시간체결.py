import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

########################################################################################
# 실시간 키값은 오른쪽에 공백을 넣고 18자리로 맞춰야 함.
########################################################################################

async def sample(api:ebest.OpenApi):
    tr_key = "82TSLA".ljust(18) # 테슬라
    tr_key += "82AAPL".ljust(18) # 애플 시세도 함께 수신할 경우

    # GSC : 해외주식 체결
    await api.add_realtime('GSC', tr_key)
    
    print('10초동안 실시간 작동중...');
    await asyncio.sleep(10) # 10초동안 대기
    
    await api.remove_realtime('GSC', tr_key)
    print('실시간중지');

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == 'GSC':
        print(f'해외주식 체결: {trcode}, {key}, {realtimedata}')

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
10초동안 실시간 작동중...
해외주식 체결: GSC, 82AAPL            , {'symbol': 'AAPL', 'lSeq': '0', 'high52p': '260.1000', 'low52p': '169.2101', 'amount': '5663092', 'kordate': '20250509', 'trdtm': '231504', 'sign': '2', 'ovsdate': '20250508', 'diff': '0.5000', 'totq': '28630', 'high': '198.1800', 'rate': '0.25', 'low': '197.1200', 'price': '197.9900', 'cgubun': '+', 'trdq': '1', 'open': '197.6800', 'kortm': '121504'}
해외주식 체결: GSC, 82TSLA            , {'symbol': 'TSLA', 'lSeq': '0', 'high52p': '488.5399', 'low52p': '167.4100', 'amount': '43736989', 'kordate': '20250509', 'trdtm': '231504', 'sign': '2', 'ovsdate': '20250508', 'diff': '1.2500', 'totq': '153066', 'high': '286.8200', 'rate': '0.44', 'low': '284.1000', 'price': '286.0700', 'cgubun': '-', 'trdq': '128', 'open': '285.5000', 'kortm': '121504'}
해외주식 체결: GSC, 82TSLA            , {'symbol': 'TSLA', 'lSeq': '1', 'high52p': '488.5399', 'low52p': '167.4100', 'amount': '43749004', 'kordate': '20250509', 'trdtm': '231504', 'sign': '2', 'ovsdate': '20250508', 'diff': '1.2500', 'totq': '153108', 'high': '286.8200', 'rate': '0.44', 'low': '284.1000', 'price': '286.0700', 'cgubun': '-', 'trdq': '42', 'open': '285.5000', 'kortm': '121504'}
실시간중지
'''