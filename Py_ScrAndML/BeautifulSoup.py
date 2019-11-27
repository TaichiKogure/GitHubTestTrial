"""
Beautiful Soupのテスト↓
"""

# from bs4 import BeautifulSoup
#
# #解析したいHTML
# html = """
# <html><body>
#    <h1>スクレイピングとは?</h1>
#    <p>webページを解析すること。</p>
#    <p>任意の箇所を抽出すること。</p>
#    </body></html>
#    """
#
# #HTMLを解析する
# soup = BeautifulSoup(html,'html.parser')
#
# #任意の部分を抽出する。
# h1 = soup.html.body.h1
# p1 = soup.html.body.p
# p2 = p1.next_sibling.next_sibling
#
# #要素のテキストを表示する
# print("h1 = "+ h1.string)
# print("p = "+ p1.string)
# print("p = "+ p2.string)

"""
Yahooからドルー円の現在価格を引用する方法↓
"""
# from bs4 import BeautifulSoup
# import urllib.request as req
#
# #HTMLを取得
# url = "https://finance.yahoo.co.jp/"
# res = req.urlopen(url)
#
# soup = BeautifulSoup(res, "html.parser")
#
# pricelist = soup.select('div[class="dtl"]')
# for dtl in pricelist:
#     print("usd/jpy=",dtl.string)
#
# aaa = soup.select("div.boardFinDark")
# for boardFinDark in aaa:
#     print("株式ランキングから=",boardFinDark.text)

"""
Selenium webdriverで駆動させる方法↓
"""
#
# from selenium import webdriver
# url = "http://www.aozora.gr.jp/cards/000081/files/46268_23911.html"
#
# browser = webdriver.PhantomJS(executable_path=r'C:\Users\Kogure Taichi\phantomjs-2.1.1-windows\bin\phantomjs.exe')
# browser.implicitly_wait(3)
# browser.get(url)
#
# browser.save_screenshot("website.png")
# browser.quit()

# Pythonのマニュアルを再帰的にダウンロード
# モジュールの取り込み

"""
リンク先を全ダウンロードするやりかた。
"""

import os.path
import re
import time
import urllib.parse  as parse
import urllib.request as req
from os import makedirs

from bs4 import BeautifulSoup

# 処理済み判断変数
proc_files = {}


# HTML内にあるリンクを抽出する関数。
def enum_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("link[rel='stylesheet']")  # CSS
    links += soup.select("a[href]")  # link
    result = []
    # href属性を取り出し、リンクを絶対パスに変換
    for a in links:
        href = a.attrs['href']
        url = req.urljoin(base, href)
        result.append(url)
    return result


# ファイルをダウンロードし保存する関数
def download_file(url):
    o = parse.urlparse(url)
    savepath = "./" + o.netloc + o.path
    if re.search(r"/$", savepath):  # ディレクトリならindex.path
        savepath += "index.html"
    savedir = os.path.dirname(savepath)
    # すでにダウンロード済み？
    if os.path.exists(savepath): return savepath
    # ダウンロード先のディレクトリを作成
    if not os.path.exists(savedir):
        makedirs(savedir)
    # ファイルをダウンロード
    try:
        print("download = ", url)
        req.urlretrieve(url, savepath)
        time.sleep(1)  # 礼儀として1秒スリープ
        return savepath
    except:
        print("ダウンロード失敗：", url)
        return None


# THMLを解析して ダウンロードする関数。
def analize_html(url, root_url):
    savepath = download_file(url)
    if savepath is None: return
    if savepath in proc_files: return  # 解析済みなら処理しない
    proc_files[savepath] = True
    print("analize_html=", url)
    # リンクを抽出
    html = open(savepath, "r", encoding="utf-8").read()
    links = enum_links(html, url)
    for link_url in links:
        if link_url.find(root_url) != 0:  # リンクがルート以外のパスを指していたら無視
            if not re.search(r".css$", link_url): continue

        if re.search(r".(html|htm)$", link_url):  # 再帰的にHTMLファイルを解析
            analize_html(link_url, root_url)
            continue
        # それ以外のファイル
        download_file(link_url)


if __name__ == "__main__":  # url丸ごとダウンロード
    url = "https://docs.python.jp/3.6/library/"
    analize_html(url, url)

