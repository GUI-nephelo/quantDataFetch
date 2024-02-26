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

conn = sqlite3.connect("openInterestVolume.db")
coin = "contract"

schema = f"CREATE TABLE IF NOT EXISTS main(ccy VARCHAR(16),ts INTERER,oi REAL,vol REAL,UNIQUE(ccy,ts));"
conn.execute(schema)

flag = "0"  # 实盘: 0, 模拟盘: 1
tradingDataAPI = TradingData_api.TradingDataAPI(flag=flag)

# 获取交易大数据支持币种
result = tradingDataAPI.get_support_coin()
data_class = result["data"]


print("获取交割永续的持仓量和交易量")

i=0
while i<len(data_class[coin]):
    print(data_class[coin][i])
    # 获取主动买入/卖出情况
    result = tradingDataAPI.get_contracts_interest_volume(
        ccy=data_class[coin][i],
        period="1H"
    )

    if result["code"]=="50011":
        print("超出请求速度")
        continue
    
    d = pd.DataFrame(result["data"],columns=["ts","oi","vol"])
    d["ccy"]=data_class[coin][i]
    d.to_sql("main",conn,schema=schema,if_exists='append', index=False,method=elasticInsert)
    # print(d)
    if "data" in result: 
        print(len(result["data"]))
    else:
        # print(result)
        raise result
    # break
    i+=1
    sleep(0.5) 


conn.close()