#Web上のおてほんを参照しました。上が自作、下がお手本


## from bs4 import BeautifulSoup
# # import urllib.request as req
# # import urllib.parse  as parse
# # from os import makedirs
# # import os.path, time, re
#
#
# from bs4 import BeautifulSoup
# import urllib
# import urllib.request
# from urllib.parse import urlparse
# from urllib.parse import urljoin
# from urllib.request import urlretrieve
# from os import makedirs
# import os.path, time, re
#
#
# # 処理済み判断変数
# proc_files = {}
#
#
# # HTML内にあるリンクを抽出する関数。
# def enum_links(html, base):
#     soup = BeautifulSoup(html, "html.parser")
#     links = soup.select("link[rel='stylesheet']")  # CSS
#     links += soup.select("a[href]")  # link
#     result = []
#     # href属性を取り出し、リンクを絶対パスに変換
#     for a in links:
#         href = a.attrs['href']
#         url = urljoin(base, href)
#         result.append(url)
#     return result
#
#
# # ファイルをダウンロードし保存する関数
# def download_file(url):
#     o = urlparse(url)
#     savepath = "./" + o.netloc + o.path
#     if re.search(r"/$", savepath):  # ディレクトリならindex.path
#         savepath += "index.html"
#     savedir = os.path.dirname(savepath)
#     # すでにダウンロード済み？
#     if os.path.exists(savedir): return savepath
#     # ダウンロード先のディレクトリを作成
#     if not os.path.exists(savedir):
#         print("mkdir=",savedir)
#         os.makedirs(savedir)
#     # ファイルをダウンロード
#     try:
#         print("download = ", url)
#         urlretrieve(url, savepath)
#         time.sleep(1)  # 礼儀として1秒スリープ
#         return savepath
#     except:
#         print("ダウンロード失敗：", url)
#         return None
#
#
# # THMLを解析して ダウンロードする関数。
# def analize_html(url, root_url):
#     savepath = download_file(url)
#     if savepath is None: return
#     if savepath in proc_files: return  # 解析済みなら処理しない
#     proc_files[savepath] = True
#     print("analize_html=", url)
#     # リンクを抽出
#     html = open(savepath, "r", encoding="utf-8").read()
#     links = enum_links(html, url)
#     for link_url in links:
#         if link_url.find(root_url) != 0:  # リンクがルート以外のパスを指していたら無視
#             if not re.search(r".css$", link_url): continue
#         if re.search(r".(html|htm)$", link_url):  # 再帰的にHTMLファイルを解析
#             analize_html(link_url, root_url)
#             continue
#         # それ以外のファイル
#         download_file(link_url)
#
#
# if __name__ == "__main__":  # url丸ごとダウンロード
#     url = "https://docs.python.jp/3.6/library/"
#     analize_html(url, url)
#######################################################################################################

import os.path
import re
import time
from os import makedirs
from urllib.parse import urljoin
from urllib.parse import urlparse
from urllib.request import urlretrieve

from bs4 import BeautifulSoup

sugi_files = {}


def enum_links(html, base):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.select("link[rel='stylesheet']")
    links += soup.select("a[href]")
    result = []

    for a in links:
        href = a.attrs['href']
        url = urljoin(base, href)
        result.append(url)
    return result


def download_file(url):
    o = urlparse(url)
    savepath = "./" + o.netloc + o.path
    if re.search(r"/$", savepath):
        savepath += "index.html"
    savedir = os.path.dirname(savepath)

    if os.path.exists(savepath): return savepath

    if not os.path.exists(savedir):
        print("mkdir=", savedir)
        makedirs(savedir)

    try:
        print("download=", url)
        urlretrieve(url, savepath)
        time.sleep(1)
        return savepath
    except:
        print("ダウンロード失敗:", url)
        return None


def analize_html(url, root_url):
    savepath = download_file(url)
    if savepath is None: return
    if savepath in sugi_files: return
    sugi_files[savepath] = True
    print("analize_html=", url)

    html = open(savepath, "r", encoding="utf-8").read()
    links = enum_links(html, url)
    for link_url in links:
        if link_url.find(root_url) != 0:
            if not re.search(r".css$", link_url): continue

        if re.search(r".(html|htm)$", link_url):
            analize_html(link_url, root_url)
            continue

        download_file(link_url)


if __name__ == "__main__":
    url = "https://docs.python.jp/3.6/library/"
    analize_html(url, url)