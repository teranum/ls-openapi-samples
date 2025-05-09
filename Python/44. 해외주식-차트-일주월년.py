import asyncio
import ebest
from common import *
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요

async def sample(api):
    keysymbol = "82TSLA" # 82TSLA: 테슬라, 82AAPL: 애플
    inputs = {
        'g3204InBlock': {
            "delaygb": "R",             # 지연구분 "R":실시간
            "keysymbol": keysymbol,     # KEY종목코드
            "exchcd": keysymbol[:2],    # 거래소코드(81: 뉴욕/아멕스, 82: 나스닥)
            "symbol": keysymbol[2:],    # 종목코드
            "gubun": "2",               # 2:일, 3:주, 4:월, 5:년
            "qrycnt": 100,              # 요청건수(최대-압축:2000비압축:500)
            "comp_yn": "N",             # 압축여부(Y:압축N:비압축)
            "sdate": "",                # 시작일자
            "edate": "",                # 종료일자
            "cts_date": "",             # 연속일자 (연속조회시 필요)
            "cts_info": "",             # 연속정보 (연속조회시 필요)
            "sujung": "Y",              # 수정주가여부(Y:적용N:비적용)
        },
    }
    response = await api.request('g3204', inputs)
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
tr_cont='Y', tr_cont_key='0'
g3204OutBlock
Field Count = 21
+-----------+----------+
|    key    |  value   |
+-----------+----------+
|  delaygb  |    R     |
| keysymbol |  82TSLA  |
|   exchcd  |    82    |
|   symbol  |   TSLA   |
|  cts_date | 20241212 |
|  cts_info |  999999  |
| rec_count |   100    |
|  preopen  | 279.6300 |
|  prehigh  | 289.8000 |
|   prelow  | 279.4100 |
|  preclose | 284.8200 |
| prevolume | 97539448 |
|    open   | 285.5000 |
|    high   | 286.8200 |
|    low    | 284.1000 |
|   close   | 286.6600 |
|  uplimit  |  0.0000  |
|  dnlimit  |  0.0000  |
|   s_time  |  200000  |
|   e_time  |  180000  |
|   dshmin  |          |
+-----------+----------+
g3204OutBlock1
Row Count = 100
+----------+----------+----------+----------+----------+-----------+-------------+---------+-----------+----------+-----------+------+
|   date   |   open   |   high   |   low    |  close   |   volume  |    amount   | jongchk | prtt_rate | pricechk | ratevalue | sign |
+----------+----------+----------+----------+----------+-----------+-------------+---------+-----------+----------+-----------+------+
| 20241213 | 420.0000 | 436.3000 | 415.7100 | 436.2300 |  89000158 | 38136331583 |    0    |    0.00   |    0     |     0     |  2   |
| 20241216 | 441.0900 | 463.1900 | 436.1500 | 463.0200 | 114083811 | 51736778265 |    0    |    0.00   |    0     |     0     |  2   |
| 20241217 | 475.9000 | 483.9900 | 457.5101 | 479.8600 | 131222978 | 62193946613 |    0    |    0.00   |    0     |     0     |  2   |
| 20241218 | 466.4950 | 488.5399 | 427.0100 | 440.1300 | 149340788 | 68874607975 |    0    |    0.00   |    0     |     0     |  5   |
| 20241219 | 451.8800 | 456.3600 | 420.0200 | 436.1700 | 118566146 | 53295269266 |    0    |    0.00   |    0     |     0     |  5   |
| 20241220 | 425.5050 | 447.0800 | 417.6400 | 421.0600 | 132216176 | 56933896802 |    0    |    0.00   |    0     |     0     |  5   |
| 20241223 | 431.0000 | 434.5100 | 415.4112 | 430.6000 |  72698055 | 31179012089 |    0    |    0.00   |    0     |     0     |  2   |
| 20241224 | 435.9000 | 462.7800 | 435.1400 | 462.2800 |  59551750 | 26891698383 |    0    |    0.00   |    0     |     0     |  2   |
| 20241226 | 465.1600 | 465.3299 | 451.0200 | 454.1300 |  76651210 | 35030495710 |    0    |    0.00   |    0     |     0     |  5   |
| 20241227 | 449.5200 | 450.0000 | 426.5000 | 431.6600 |  82666821 | 35956708323 |    0    |    0.00   |    0     |     0     |  5   |
| 20241230 | 419.4000 | 427.0000 | 415.7500 | 417.4100 |  64941012 | 27324404110 |    0    |    0.00   |    0     |     0     |  5   |
| 20241231 | 423.7900 | 427.9300 | 402.5400 | 403.8400 |  76825121 | 31725973778 |    0    |    0.00   |    0     |     0     |  5   |
| 20250102 | 390.1000 | 392.7299 | 373.0400 | 379.2800 | 109710749 | 41965428409 |    0    |    0.00   |    0     |     0     |  5   |
| 20250103 | 381.4800 | 411.8799 | 379.4500 | 410.4400 |  95423329 | 37896934237 |    0    |    0.00   |    0     |     0     |  2   |
| 20250106 | 423.2000 | 426.4300 | 401.7000 | 411.0500 |  85516534 | 35266944219 |    0    |    0.00   |    0     |     0     |  2   |
...
| 20250417 | 243.4700 | 244.3400 | 237.6833 | 241.3700 |  83404775 | 20101311698 |    0    |    0.00   |    0     |     0     |  5   |
| 20250421 | 230.2600 | 232.2100 | 222.7900 | 227.5000 |  97768007 | 22105856716 |    0    |    0.00   |    0     |     0     |  5   |
| 20250422 | 230.9600 | 242.7900 | 229.8501 | 237.9700 | 120858452 | 28669416641 |    0    |    0.00   |    0     |     0     |  2   |
| 20250423 | 254.8600 | 259.4499 | 244.4300 | 250.7400 | 150381903 | 38245448524 |    0    |    0.00   |    0     |     0     |  2   |
| 20250424 | 250.5000 | 259.5400 | 249.2000 | 259.5100 |  94464195 | 24123135539 |    0    |    0.00   |    0     |     0     |  2   |
| 20250425 | 261.6900 | 286.8500 | 259.6300 | 284.9500 | 167560688 | 46683748618 |    0    |    0.00   |    0     |     0     |  2   |
| 20250428 | 288.9800 | 294.8600 | 272.4200 | 285.8800 | 151731771 | 42948011138 |    0    |    0.00   |    0     |     0     |  2   |
| 20250429 | 285.5000 | 293.3200 | 279.4695 | 292.0300 | 108906553 | 31079741528 |    0    |    0.00   |    0     |     0     |  2   |
| 20250430 | 279.9000 | 284.4500 | 270.7800 | 282.1600 | 128961057 | 35988072639 |    0    |    0.00   |    0     |     0     |  5   |
| 20250501 | 280.0100 | 290.8688 | 279.8100 | 280.5200 |  99658974 | 28346669926 |    0    |    0.00   |    0     |     0     |  5   |
| 20250502 | 284.9000 | 294.7800 | 279.8100 | 287.2100 | 114454683 | 32962705745 |    0    |    0.00   |    0     |     0     |  2   |
| 20250505 | 284.5700 | 284.8490 | 274.4000 | 280.2600 |  94618882 | 26433183690 |    0    |    0.00   |    0     |     0     |  5   |
| 20250506 | 273.1050 | 277.7300 | 271.3500 | 275.3500 |  76715792 | 21057567879 |    0    |    0.00   |    0     |     0     |  5   |
| 20250507 | 276.8800 | 277.9200 | 271.0000 | 276.2200 |  71882408 | 19753805950 |    0    |    0.00   |    0     |     0     |  2   |
| 20250508 | 279.6300 | 289.8000 | 279.4100 | 284.8200 |  97539448 | 27846070698 |    0    |    0.00   |    0     |     0     |  2   |
| 20250509 | 285.5000 | 286.8200 | 284.1000 | 286.6600 |   175352  |   50109882  |    0    |    0.00   |    0     |     0     |  2   |
+----------+----------+----------+----------+----------+-----------+-------------+---------+-----------+----------+-----------+------+
rsp_cd
00000
rsp_msg
조회완료
'''
