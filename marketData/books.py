import okx.MarketData as MarketData


import pandas as pd
import sqlite3
from time import sleep

from tickers import spider

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


conn = sqlite3.connect("books.db")

schema1 = "create table if not exists SPOT(ts INTERGER,instId TEXT,AP REAL,AC REAL,AQ INTERGER,BP REAL,BC REAL,BQ INTERGER,UNIQUE(ts,instId));"
schema2 = "create table if not exists SWAP(ts INTERGER,instId TEXT,AP REAL,AC REAL,AQ INTERGER,BP REAL,BC REAL,BQ INTERGER,UNIQUE(ts,instId));"

conn.execute(schema1)
conn.execute(schema2)

flag = "0"  # 实盘:0 , 模拟盘：1

marketDataAPI =  MarketData.MarketAPI(flag=flag,debug=False)

@spider()
def books(coin,l):
    rl = []

    for instId in l:
        result = marketDataAPI.get_orderbook(instId=instId)
        if result["code"]!="0":
            print(result)
            exit(1000)
        data = result["data"][0]
        stdData = {"ts":data["ts"],"instId":instId,"AP":None,"AC":None,"AQ":None,"BP":None,"BC":None,"BQ":None}
        
        stdData["AP"],stdData["AC"],stdData["AQ"] = data["asks"][0][0],data["asks"][0][1],data["asks"][0][3]
        stdData["BP"],stdData["BC"],stdData["BQ"] = data["bids"][0][0],data["bids"][0][1],data["bids"][0][3],
        
        rl.append(stdData)
        sleep(0.1)
    data = pd.DataFrame(rl)
    # print(data)
    data.to_sql(coin,conn,if_exists="append",index=False,method=elasticInsert)
books()