import okx.PublicData as PublicData

flag = "0"  # 实盘:0 , 模拟盘：1

publicDataAPI = PublicData.PublicAPI(flag=flag)

# 获取永续合约历史资金费率
result = publicDataAPI.funding_rate_history(
    instId="BTC-USD-SWAP",
)
print(result)
