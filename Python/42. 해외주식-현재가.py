import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    keysymbol = "82TSLA" # 82TSLA: 테슬라, 82AAPL: 애플
    inputs = {
        'g3101InBlock': {
            'delaygb': 'R', # 지연구분
            'keysymbol': keysymbol, # KEY종목코드
            'exchcd': keysymbol[:2], # 거래소코드
            'symbol': keysymbol[2:], # 종목코드
        },
    }
    response = await api.request('g3101', inputs)
    if not response: return print(f"요청 실패: {api.last_message}")
    
    print(response)
    

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
tr_cont='N', tr_cont_key='0'
g3101OutBlock
Field Count = 26
+------------+----------------+
|    key     |     value      |
+------------+----------------+
|  delaygb   |       R        |
| keysymbol  |     82TSLA     |
|   exchcd   |       82       |
|  exchange  |      0537      |
|  suspend   |       N        |
|  sellonly  |       0        |
|   symbol   |      TSLA      |
|  korname   |     테슬라     |
|  induname  | 자동차 및 부품 |
| floatpoint |       4        |
|  currency  |      USD       |
|   price    |    286.5500    |
|    sign    |       2        |
|    diff    |     1.7300     |
|    rate    |      0.61      |
|   volume   |     126074     |
|   amount   |    36021759    |
|  high52p   |    488.5399    |
|   low52p   |    167.4100    |
|  uplimit   |     0.0000     |
|  dnlimit   |     0.0000     |
|    open    |    285.5000    |
|    high    |    286.8200    |
|    low     |    284.1000    |
|    perv    |     151.90     |
|    epsv    |      1.82      |
+------------+----------------+
rsp_cd
00000
rsp_msg
조회완료
'''
