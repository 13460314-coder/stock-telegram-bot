import requests
from bs4 import BeautifulSoup
import re
import os

# 股票代號：台積電
stock_id = "2330.TW"

# Yahoo 股市網址
url = f"https://tw.stock.yahoo.com/quote/{stock_id}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 抓取網頁
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")
text = soup.get_text(" ", strip=True)

# 抓取目前股價
match = re.search(r"成交\s*([\d,]+(?:\.\d+)?)", text)

if match:
    price = match.group(1)
    print("台積電目前股價：", price)
else:
    raise Exception("無法找到股價")

# 從 GitHub Secrets 取得 Telegram 資料
bot_token = os.environ["BOT_TOKEN"]
chat_id = os.environ["CHAT_ID"]

# Telegram 訊息
message = f"""📈 股票即時通知
股票代號：{stock_id}
目前股價：{price} 元"""

telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

data = {
    "chat_id": chat_id,
    "text": message
}

response = requests.post(telegram_url, data=data)

print(response.json())
