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

    # GSH : 해외주식 호가
    await api.add_realtime('GSH', tr_key)
    
    print('10초동안 실시간 작동중...');
    await asyncio.sleep(10) # 10초동안 대기
    
    await api.remove_realtime('GSH', tr_key)
    print('실시간중지');

def on_realtime(api:ebest.OpenApi, trcode, key, realtimedata):
    if trcode == 'GSH':
        print(f'해외주식 호가: {trcode}, {key}, {realtimedata}')

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
해외주식 호가: GSH, 82TSLA            , {'offerho4': '285.7500', 'symbol': 'TSLA', 'offerho3': '285.7300', 'offerho6': '285.8200', 'offerho5': '285.8100', 'offerno2': '0', 'offerho8': '285.8700', 'offerno1': '0', 'offerho7': '285.8500', 'offerno4': '0', 'offerno3': '0', 'offerho9': '285.9000', 'offerno6': '0', 'offerno5': '0', 'offerno8': '0', 'offerno7': '0', 'offerno9': '0', 'offerno10': '0', 'bidno10': '0', 'offerho2': '285.7100', 'offerho1': '285.7000', 'offerho10': '285.9100', 'loctime': '232149', 'totofferrem': '3354', 'totbidrem': '1178', 'offerrem2': '90', 'bidho5': '285.5600', 'offerrem3': '22', 'bidho4': '285.5900', 'bidno1': '0', 'offerrem4': '4', 'bidho7': '285.5400', 'offerrem5': '156', 'bidho6': '285.5500', 'bidno3': '0', 'bidho9': '285.5000', 'bidno2': '0', 'bidho8': '285.5100', 'bidno5': '0', 'offerrem1': '80', 'bidno4': '0', 'bidno7': '0', 'bidno6': '0', 'bidno9': '0', 'totoffercnt': '0', 'bidno8': '0', 'offerrem6': '2937', 'totbidcnt': '0', 'offerrem7': '20', 'offerrem8': '20', 'offerrem9': '5', 'bidrem3': '28', 'bidrem4': '296', 'bidrem1': '61', 'bidrem2': '52', 'bidrem9': '645', 'bidho1': '285.6300', 'bidrem7': '20', 'bidrem8': '20', 'bidho3': '285.6000', 'bidrem5': '6', 'bidho2': '285.6200', 'bidrem6': '47', 'bidrem10': '3', 'bidho10': '285.4500', 'kortime': '122149', 'offerrem10': '20'}
해외주식 호가: GSH, 82TSLA            , {'offerho4': '285.7500', 'symbol': 'TSLA', 'offerho3': '285.7300', 'offerho6': '285.8200', 'offerho5': '285.8100', 'offerno2': '0', 'offerho8': '285.8700', 'offerno1': '0', 'offerho7': '285.8500', 'offerno4': '0', 'offerno3': '0', 'offerho9': '285.9000', 'offerno6': '0', 'offerno5': '0', 'offerno8': '0', 'offerno7': '0', 'offerno9': '0', 'offerno10': '0', 'bidno10': '0', 'offerho2': '285.7100', 'offerho1': '285.7000', 'offerho10': '285.9100', 'loctime': '232149', 'totofferrem': '3354', 'totbidrem': '1178', 'offerrem2': '90', 'bidho5': '285.5800', 'offerrem3': '22', 'bidho4': '285.5900', 'bidno1': '0', 'offerrem4': '4', 'bidho7': '285.5400', 'offerrem5': '156', 'bidho6': '285.5600', 'bidno3': '0', 'bidho9': '285.5000', 'bidno2': '0', 'bidho8': '285.5100', 'bidno5': '0', 'offerrem1': '80', 'bidno4': '0', 'bidno7': '0', 'bidno6': '0', 'bidno9': '0', 'totoffercnt': '0', 'bidno8': '0', 'offerrem6': '2937', 'totbidcnt': '0', 'offerrem7': '20', 'offerrem8': '20', 'offerrem9': '5', 'bidrem3': '28', 'bidrem4': '296', 'bidrem1': '61', 'bidrem2': '52', 'bidrem9': '645', 'bidho1': '285.6300', 'bidrem7': '20', 'bidrem8': '20', 'bidho3': '285.6000', 'bidrem5': '47', 'bidho2': '285.6200', 'bidrem6': '6', 'bidrem10': '3', 'bidho10': '285.4500', 'kortime': '122149', 'offerrem10': '20'}
해외주식 호가: GSH, 82TSLA            , {'offerho4': '285.7500', 'symbol': 'TSLA', 'offerho3': '285.7300', 'offerho6': '285.8500', 'offerho5': '285.8200', 'offerno2': '0', 'offerho8': '285.9000', 'offerno1': '0', 'offerho7': '285.8700', 'offerno4': '0', 'offerno3': '0', 'offerho9': '285.9100', 'offerno6': '0', 'offerno5': '0', 'offerno8': '0', 'offerno7': '0', 'offerno9': '0', 'offerno10': '0', 'bidno10': '0', 'offerho2': '285.7100', 'offerho1': '285.7000', 'offerho10': '285.9200', 'loctime': '232149', 'totofferrem': '3574', 'totbidrem': '1178', 'offerrem2': '90', 'bidho5': '285.5900', 'offerrem3': '22', 'bidho4': '285.6000', 'bidno1': '0', 'offerrem4': '4', 'bidho7': '285.5400', 'offerrem5': '3093', 'bidho6': '285.5600', 'bidno3': '0', 'bidho9': '285.5000', 'bidno2': '0', 'bidho8': '285.5100', 'bidno5': '0', 'offerrem1': '80', 'bidno4': '0', 'bidno7': '0', 'bidno6': '0', 'bidno9': '0', 'totoffercnt': '0', 'bidno8': '0', 'offerrem6': '20', 'totbidcnt': '0', 'offerrem7': '20', 'offerrem8': '5', 'offerrem9': '20', 'bidrem3': '47', 'bidrem4': '28', 'bidrem1': '61', 'bidrem2': '192', 'bidrem9': '645', 'bidho1': '285.6300', 'bidrem7': '20', 'bidrem8': '20', 'bidho3': '285.6100', 'bidrem5': '156', 'bidho2': '285.6200', 'bidrem6': '6', 'bidrem10': '3', 'bidho10': '285.4500', 'kortime': '122149', 'offerrem10': '220'}
해외주식 호가: GSH, 82AAPL            , {'offerho4': '198.0200', 'symbol': 'AAPL', 'offerho3': '198.0000', 'offerho6': '198.0400', 'offerho5': '198.0300', 'offerno2': '0', 'offerho8': '198.0700', 'offerno1': '0', 'offerho7': '198.0600', 'offerno4': '0', 'offerno3': '0', 'offerho9': '198.1000', 'offerno6': '0', 'offerno5': '0', 'offerno8': '0', 'offerno7': '0', 'offerno9': '0', 'offerno10': '0', 'bidno10': '0', 'offerho2': '197.9900', 'offerho1': '197.9800', 'offerho10': '198.1300', 'loctime': '232149', 'totofferrem': '1164', 'totbidrem': '1332', 'offerrem2': '102', 'bidho5': '197.8500', 'offerrem3': '260', 'bidho4': '197.8600', 'bidno1': '0', 'offerrem4': '126', 'bidho7': '197.8200', 'offerrem5': '60', 'bidho6': '197.8400', 'bidno3': '0', 'bidho9': '197.7700', 'bidno2': '0', 'bidho8': '197.8100', 'bidno5': '0', 'offerrem1': '20', 'bidno4': '0', 'bidno7': '0', 'bidno6': '0', 'bidno9': '0', 'totoffercnt': '0', 'bidno8': '0', 'offerrem6': '20', 'totbidcnt': '0', 'offerrem7': '242', 'offerrem8': '242', 'offerrem9': '16', 'bidrem3': '10', 'bidrem4': '84', 'bidrem1': '10', 'bidrem2': '73', 'bidrem9': '60', 'bidho1': '197.9100', 'bidrem7': '50', 'bidrem8': '136', 'bidho3': '197.8700', 'bidrem5': '506', 'bidho2': '197.9000', 'bidrem6': '62', 'bidrem10': '341', 'bidho10': '197.7600', 'kortime': '122149', 'offerrem10': '76'}
해외주식 호가: GSH, 82AAPL            , {'offerho4': '198.0100', 'symbol': 'AAPL', 'offerho3': '198.0000', 'offerho6': '198.0300', 'offerho5': '198.0200', 'offerno2': '0', 'offerho8': '198.0600', 'offerno1': '0', 'offerho7': '198.0400', 'offerno4': '0', 'offerno3': '0', 'offerho9': '198.0700', 'offerno6': '0', 'offerno5': '0', 'offerno8': '0', 'offerno7': '0', 'offerno9': '0', 'offerno10': '0', 'bidno10': '0', 'offerho2': '197.9900', 'offerho1': '197.9800', 'offerho10': '198.1000', 'loctime': '232150', 'totofferrem': '1098', 'totbidrem': '1332', 'offerrem2': '102', 'bidho5': '197.8500', 'offerrem3': '260', 'bidho4': '197.8600', 'bidno1': '0', 'offerrem4': '10', 'bidho7': '197.8200', 'offerrem5': '126', 'bidho6': '197.8400', 'bidno3': '0', 'bidho9': '197.7700', 'bidno2': '0', 'bidho8': '197.8100', 'bidno5': '0', 'offerrem1': '20', 'bidno4': '0', 'bidno7': '0', 'bidno6': '0', 'bidno9': '0', 'totoffercnt': '0', 'bidno8': '0', 'offerrem6': '60', 'totbidcnt': '0', 'offerrem7': '20', 'offerrem8': '242', 'offerrem9': '242', 'bidrem3': '10', 'bidrem4': '84', 'bidrem1': '10', 'bidrem2': '73', 'bidrem9': '60', 'bidho1': '197.9100', 'bidrem7': '50', 'bidrem8': '136', 'bidho3': '197.8700', 'bidrem5': '506', 'bidho2': '197.9000', 'bidrem6': '62', 'bidrem10': '341', 'bidho10': '197.7600', 'kortime': '122150', 'offerrem10': '16'}
해외주식 호가: GSH, 82TSLA            , {'offerho4': '285.7500', 'symbol': 'TSLA', 'offerho3': '285.7300', 'offerho6': '285.8500', 'offerho5': '285.8200', 'offerno2': '0', 'offerho8': '285.9000', 'offerno1': '0', 'offerho7': '285.8700', 'offerno4': '0', 'offerno3': '0', 'offerho9': '285.9100', 'offerno6': '0', 'offerno5': '0', 'offerno8': '0', 'offerno7': '0', 'offerno9': '0', 'offerno10': '0', 'bidno10': '0', 'offerho2': '285.7100', 'offerho1': '285.7000', 'offerho10': '285.9200', 'loctime': '232150', 'totofferrem': '3574', 'totbidrem': '1178', 'offerrem2': '90', 'bidho5': '285.5800', 'offerrem3': '22', 'bidho4': '285.5900', 'bidno1': '0', 'offerrem4': '4', 'bidho7': '285.5400', 'offerrem5': '3093', 'bidho6': '285.5600', 'bidno3': '0', 'bidho9': '285.5000', 'bidno2': '0', 'bidho8': '285.5100', 'bidno5': '0', 'offerrem1': '80', 'bidno4': '0', 'bidno7': '0', 'bidno6': '0', 'bidno9': '0', 'totoffercnt': '0', 'bidno8': '0', 'offerrem6': '20', 'totbidcnt': '0', 'offerrem7': '20', 'offerrem8': '5', 'offerrem9': '20', 'bidrem3': '28', 'bidrem4': '156', 'bidrem1': '61', 'bidrem2': '192', 'bidrem9': '645', 'bidho1': '285.6300', 'bidrem7': '20', 'bidrem8': '20', 'bidho3': '285.6000', 'bidrem5': '47', 'bidho2': '285.6200', 'bidrem6': '6', 'bidrem10': '3', 'bidho10': '285.4500', 'kortime': '122150', 'offerrem10': '220'}
실시간중지
'''