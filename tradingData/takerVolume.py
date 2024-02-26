import okx.TradingData as TradingData_api

import pandas as pd
import sqlite3
from time import sleep

def elasticInsert(sqlTable,cur,keys, data_iter):
    for row in data_iter:
        row = list(row)
        row[-1] = f'"{row[-1]}"'
        values = ','.join(row)
        try:
            cur.execute(f"insert into {sqlTable.name} ({','.join(keys)}) VALUES({values})")
        except sqlite3.Error as e:
            pass# print(e)

takerVolume = sqlite3.connect("takerVolume.db")

flag = "0"  # 实盘: 0, 模拟盘: 1
tradingDataAPI = TradingData_api.TradingDataAPI(flag=flag)

# 获取交易大数据支持币种
result = tradingDataAPI.get_support_coin()
data_class = result["data"]

for coin in data_class:
    
    print("抓取"+coin+"主动买入/卖出情况 ")
    if coin != "option":
        i=0
        while i<len(data_class[coin]):
            print(data_class[coin][i])
            # 获取主动买入/卖出情况
            result = tradingDataAPI.get_taker_volume(
                ccy=data_class[coin][i],
                instType=(coin+"s" if coin[0]=="c" else coin).upper(),
                period="1H"
            )

            if result["code"]=="50011":
                print("超出请求速度")
                continue
            
            d = pd.DataFrame(result["data"],columns=["ts","sellVol","buyVol"])
            d["ccy"]=data_class[coin][i]
            d.to_sql(coin.upper(),takerVolume,if_exists='append', index=False,method=elasticInsert)
            # print(d)
            if "data" in result: 
                print(len(result["data"]))
            else:
                # print(result)
                raise result
            # break
            i+=1
            sleep(0.5) 
    # break

takerVolume.close()