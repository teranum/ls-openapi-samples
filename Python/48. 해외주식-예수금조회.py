import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    inputs = {
        'COSOQ02701InBlock1': {
            'RecCnt': 1,        # 레코드갯수
            'CrcyCode': 'ALL',  # 통화코드
        },
    }
    response = await api.request('COSOQ02701', inputs)
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
COSOQ02701OutBlock1
Field Count = 4
+----------+-------------+
|   key    |    value    |
+----------+-------------+
|  RecCnt  |      1      |
|  AcntNo  | XXXXXXXXXXX |
|   Pwd    |   ********  |
| CrcyCode |     ALL     |
+----------+-------------+
COSOQ02701OutBlock2
Row Count = 4
+----------+-------------------+-------------------+-------------------+-------------------+--------------------+--------------------+--------------------+--------------------+-----------------+-----------------+-----------------+-----------------+---------------------+---------------------+---------------------+---------------------+
| CrcyCode | FcurrBuyAdjstAmt1 | FcurrBuyAdjstAmt2 | FcurrBuyAdjstAmt3 | FcurrBuyAdjstAmt4 | FcurrSellAdjstAmt1 | FcurrSellAdjstAmt2 | FcurrSellAdjstAmt3 | FcurrSellAdjstAmt4 | PrsmptFcurrDps1 | PrsmptFcurrDps2 | PrsmptFcurrDps3 | PrsmptFcurrDps4 | PrsmptMxchgAbleAmt1 | PrsmptMxchgAbleAmt2 | PrsmptMxchgAbleAmt3 | PrsmptMxchgAbleAmt4 |
+----------+-------------------+-------------------+-------------------+-------------------+--------------------+--------------------+--------------------+--------------------+-----------------+-----------------+-----------------+-----------------+---------------------+---------------------+---------------------+---------------------+
|   JPY    |       0.0000      |       0.0000      |       0.0000      |       0.0000      |       0.0000       |       0.0000       |       0.0000       |       0.0000       |      0.0000     |      0.0000     |      0.0000     |      0.0000     |        0.0000       |        0.0000       |        0.0000       |        0.0000       |
|   HKD    |       0.0000      |       0.0000      |       0.0000      |       0.0000      |       0.0000       |       0.0000       |       0.0000       |       0.0000       |      0.0000     |      0.0000     |      0.0000     |      0.0000     |        0.0000       |        0.0000       |        0.0000       |        0.0000       |
|   CNY    |       0.0000      |       0.0000      |       0.0000      |       0.0000      |       0.0000       |       0.0000       |       0.0000       |       0.0000       |      0.0000     |      0.0000     |      0.0000     |      0.0000     |        0.0000       |        0.0000       |        0.0000       |        0.0000       |
|   USD    |       0.0000      |       0.0000      |       0.0000      |       0.0000      |       0.0000       |       0.0000       |       0.0000       |       0.0000       |      0.0000     |      0.0000     |      0.0000     |      0.0000     |        0.0000       |        0.0000       |        0.0000       |        0.0000       |
+----------+-------------------+-------------------+-------------------+-------------------+--------------------+--------------------+--------------------+--------------------+-----------------+-----------------+-----------------+-----------------+---------------------+---------------------+---------------------+---------------------+
COSOQ02701OutBlock3
Row Count = 2
+---------+----------+------------+----------+-----------------+------------------+-------------+--------------+------------------+-------------------+------------+
| CntryNm | CrcyCode | T4FcurrDps | FcurrDps | FcurrOrdAbleAmt | PrexchOrdAbleAmt | FcurrOrdAmt | FcurrPldgAmt | ExecRuseFcurrAmt | FcurrMxchgAbleAmt | BaseXchrat |
+---------+----------+------------+----------+-----------------+------------------+-------------+--------------+------------------+-------------------+------------+
|   미국  |   USD    |   0.0000   |  0.0000  |      0.0000     |      0.0000      |    0.0000   |    0.0000    |      0.0000      |       0.0000      | 1396.0000  |
|   홍콩  |   HKD    |   0.0000   |  0.0000  |      0.0000     |      0.0000      |    0.0000   |    0.0000    |      0.0000      |       0.0000      |  179.5700  |
+---------+----------+------------+----------+-----------------+------------------+-------------+--------------+------------------+-------------------+------------+
COSOQ02701OutBlock4
Field Count = 5
+------------------+-------+
|       key        | value |
+------------------+-------+
|      RecCnt      |   1   |
|   WonDpsBalAmt   |   0   |
|  MnyoutAbleAmt   |   0   |
| WonPrexchAbleAmt |   0   |
|     OvrsMgn      |   0   |
+------------------+-------+
COSOQ02701OutBlock5
Field Count = 2
+---------+-------+
|   key   | value |
+---------+-------+
|  RecCnt |   1   |
| NrfCode |   01  |
+---------+-------+
rsp_cd
00136
rsp_msg
조회완료
'''
