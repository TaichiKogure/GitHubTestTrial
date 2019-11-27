import json
import os.path
import random
import urllib.request as req

# JSONデータをダウンロード --- (※1)
url = "http://api.aoikujira.com/hyakunin/get.php?fmt=json"
savename = "hyakunin.json"
if not os.path.exists(url):
    req.urlretrieve(url, savename)

# JSONファイルを解析 --- (※2)
data = json.load(open(savename, "r", encoding="utf-8"))
# あるいは...
# s = open(savename, "r", encoding="utf-8").read()
# data = json.loads(s)

# ランダムに一首表示 --- (※3)
r = random.choice(data)
print(r['kami'], r['simo'])


