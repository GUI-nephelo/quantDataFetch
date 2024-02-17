import okx.PublicData as PublicData

import pandas as pd
import sqlite3
from time import sleep

def elasticInsert(sqlTable,cur,keys, data_iter):
    for row in data_iter:
        row = [str(i) for i in row]
        row[0] = f'"{row[0]}"'
        values = ','.join(row)
        
        try:
            cur.execute(f"insert into {sqlTable.name} ({','.join(keys)}) VALUES({values})")
        except sqlite3.Error as e:
            print(e)


flag = "0"  # 实盘:0 , 模拟盘：1

publicDataAPI = PublicData.PublicAPI(flag=flag)

# 获取持仓总量
result = publicDataAPI.get_open_interest(instType="SWAP")
if result["code"]!="0":
    print(result)
    exit(1)
data = result["data"]
data = pd.DataFrame(data)
conn = sqlite3.connect("openInterest.db")
schema = "create table if not exists main(instId TEXT,ts INTERGER,oi INTERGER,oiCcy REAL,UNIQUE(instId,ts));"
conn.execute(schema)

cols = ["instId","oi","oiCcy","ts"]
data[cols].to_sql("main",conn,if_exists="append",index=False,method=elasticInsert)


conn.close()