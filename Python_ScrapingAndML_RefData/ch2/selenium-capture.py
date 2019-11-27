from selenium import webdriver

url = "http://www.aozora.gr.jp/cards/000081/files/46268_23911.html"

# PhantomJSのドライバを得る --- (※1)
browser = webdriver.PhantomJS()
# 暗黙的な待機を最大3秒行う --- (※2)
browser.implicitly_wait(3)
# URLを読み込む --- (※3)
browser.get(url)
# 画面をキャプチャしてファイルに保存 --- (※4)
browser.save_screenshot("website.png")
# ブラウザを終了 --- (※5)
browser.quit()

