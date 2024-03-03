﻿import asyncio
import ebest
from app_keys import appkey, appsecretkey # app_keys.py 파일에 appkey, appsecretkey 변수를 정의하고 사용하세요
from prettytable import *

async def main():
    api=ebest.OpenApi()
    if not await api.login(appkey, appsecretkey): return print(f"연결실패: {api.last_message}")
    
    request = {
        "t8424InBlock": {
            "gubun1": "0",
        }
    }
    response = await api.request("t8424", request)
    
    if not response: return print(f"요청실패: {api.last_message}")
    
    data = response.body["t8424OutBlock"]
    table = PrettyTable()
    table.field_names = data[0]
    table.add_rows([x.values() for x in data])
    print(table)
    
    ... # 다른 작업 수행
    await api.close()

asyncio.run(main())


# Output:
"""
+----------------------+--------+
|        hname         | upcode |
+----------------------+--------+
|     종       합      |  001   |
|     대   형  주      |  002   |
|     중   형  주      |  003   |
|     소   형  주      |  004   |

(중략 ...)
"""
