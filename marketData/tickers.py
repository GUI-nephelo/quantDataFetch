import okx.PublicData as PublicData

import pandas as pd
import sqlite3
from time import sleep

flag = "0"  # 实盘:0 , 模拟盘：1

publicDataAPI = PublicData.PublicAPI(flag=flag)

dic = dict()

for coin in ["SPOT","SWAP"]:
    # 获取交易产品基础信息
    result = publicDataAPI.get_instruments(instType=coin)
    if result["code"]!="0":
        print(result)
        exit(1)
    data = pd.DataFrame(result["data"])
    data = data["instId"].to_list()
    dic[coin] = data

def spider(coins = ["SPOT","SWAP"]):
    def decorator(func):
        def warpper():
            for coin in coins:
                func(coin,dic[coin])
        return warpper
    return decorator