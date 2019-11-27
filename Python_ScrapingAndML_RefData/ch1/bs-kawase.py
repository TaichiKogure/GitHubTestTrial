import urllib.request as req

from bs4 import BeautifulSoup

# 為替情報XMLを取得
url = "http://api.aoikujira.com/kawase/xml/usd"
res = req.urlopen(url)

# HTMLを解析
soup = BeautifulSoup(res, "html.parser")

# 任意のデータを抽出 --- (※1)
jpy = soup.select_one("jpy").string
print("usd/jpy=", jpy)

