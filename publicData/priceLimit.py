import okx.PublicData as PublicData

import pandas as pd
import sqlite3
from time import sleep

from instruments import spider

flag = "0"  # 实盘:0 , 模拟盘：1

publicDataAPI = PublicData.PublicAPI(flag=flag)


@spider()
def priceLimit(coin,l):
    rl = []

    for instId in l:
        result = publicDataAPI.get_price_limit(instId=instId)
        if result["code"]!="0":
            print(result)
            exit(1)
        data = result["data"]
        rl.append(data)
    
    data = pd.DataFrame(rl)
    print(data)

priceLimit()