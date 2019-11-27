
import urllib.parse as parse
import urllib.request as req

#コマンドラインの引数を得る。
# ?\if len(sys.argv) <= 1:
print("USAGE: Input keyword")
keyword = input()
    # sys.exit()
# keyword = sys.argv[1]　#コマンドラインが使えないのでインプットすることにした。



#パラメーターをURLエンコードする
API = "http://api.aoikujira.com/hyakunin/get.php"
query = {
    "fmt":"ini",
    "key": keyword
}
params = parse.urlencode(query)
url = API + "?" + params
print("url=",url)

#ダウンロード
with req.urlopen(url) as r :
    b = r.read()
    data = b.decode('utf-8')
    print(data)
