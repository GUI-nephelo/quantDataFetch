import okx.PublicData as PublicData

import pandas as pd
import sqlite3
from time import sleep

from instruments import spider

def elasticInsert(sqlTable,cur,keys, data_iter):
    for row in data_iter:
        row = [str(i) for i in row]
        row[1] = f'"{row[1]}"'
        values = ','.join(row)
        
        # print()
        try:
            cur.execute(f"insert into {sqlTable.name} ({','.join(keys)}) VALUES({values})")
        except sqlite3.Error as e:
            print(e)


flag = "0"  # 实盘:0 , 模拟盘：1

publicDataAPI = PublicData.PublicAPI(flag=flag,debug=False)

conn = sqlite3.connect("priceLimit.db")
schema1 = "create table if not exists SPOT(ts INTERGER,instId TEXT,buyLmt REAL,sellLmt REAL,UNIQUE(ts,instId));"
schema2 = "create table if not exists SWAP(ts INTERGER,instId TEXT,buyLmt REAL,sellLmt REAL,UNIQUE(ts,instId));"
conn.execute(schema1)
conn.execute(schema2)


cols = ["ts","instId","buyLmt","sellLmt"]

@spider(coins = ["SPOT","SWAP"])
def priceLimit(coin,l):
    rl = []

    for instId in l:
        result = publicDataAPI.get_price_limit(instId=instId)
        if result["code"]!="0":
            print(result)
            exit(1)
        data = result["data"][0]
        rl.append(data)
    
    data = pd.DataFrame(rl)
    data = data[data["enabled"]][cols]
    # print(data)
    data.to_sql(coin,conn,if_exists="append",index=False,method=elasticInsert)

priceLimit()