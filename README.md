# iDrinkSpot

https://www.learncodewithmike.com/2020/06/python-line-bot.html
1. 安裝Python在本地端
2. 開terminal測試是否安裝成功 >> py --version
3. 使用pip需更改環境變數  https://dragongo.co/%E8%A7%A3%E6%B1%BA%EF%BC%9A%E7%84%A1%E6%B3%95%E8%BE%A8%E8%AD%98-pip-%E8%A9%9E%E5%BD%99%E6%98%AF%E5%90%A6%E7%82%BA-cmdlet%E3%80%81%E5%87%BD%E6%95%B8%E3%80%81%E6%8C%87%E4%BB%A4%E6%AA%94%E6%88%96/

4. pip install 需要的套件，見requirments.txt  >> pip install -r requirements.txt
5. pip list 確認套件都安裝好了 
   (更新pip >>python.exe -m pip install --upgrade pip)

6. 在terminal輸入下列
django-admin startproject mylinebot .  #建立Django專案
python manage.py startapp foodlinebot  #建立Django應用程式
python manage.py migrate  #執行資料遷移(Migration)

7. 開啟mylinebot專案主程式下的settings.py檔案，增加LINE Developers的兩個憑證設定，來與LINE進行連結
LINE_CHANNEL_ACCESS_TOKEN = 'Messaging API的Channel access token'
LINE_CHANNEL_SECRET = 'Basic settings的Channel Secret'

8. 並且，在INSTALL_APPS的地方，加上剛剛所建立的Django應用程式(APP)，
    'foodlinebot.apps.FoodlinebotConfig',

9. https://www.learncodewithmike.com/2020/06/python-line-bot.html
    跟著 "四、開發LINE Bot應用程式" 的步驟

10. 安裝Ngrok 
11. 在ngrok.exe 輸入官網提供的command line >> ngrok config add-authtoken 2Q5lhBX3aUR4QqfpkW3zUMmNKSz_2orpE2WGrBBTrc95xVNNa
12. 接著，就可以透過Ngrok，將本機的埠號對外公開，以本文為例，Django在本機運行的埠號為8000，所以輸入以下的指令：ngrok http 8000

13. line developer Webhook URL >>https://7d3a-114-36-66-27.ngrok-free.app/foodlinebot/callback

- 到這邊目前完成一個echo line bot (py manage.py runserver 8000 & ngrok 要執行，linebot才能用)
- 但是網頁目前還是Page not found (404)

# [Python+LINE Bot教學]建構具網頁爬蟲功能的LINE Bot機器人
https://www.learncodewithmike.com/2020/07/python-web-scraping-line-bot.html

1. 跟著步驟做
2. 利用BeautifulSoup套件來解析網頁中的HTML原始碼
3. scraper.py 要先拆解URL，在分別讀取HTML的class類別。
4. 拿到class就可以回傳class的index給linebot



# 重新啟動 (ngrok會變)
1. 開啟ngrok.exe 
2. >> ngrok config add-authtoken 2Q5lhBX3aUR4QqfpkW3zUMmNKSz_2orpE2WGrBBTrc95xVNNa
3. >> ngrok http 8000

4. line developer Webhook URL >>https://7d3a-114-36-66-27.ngrok-free.app/foodlinebot/callback

5. 開啟VSCode，修正settings.py的ALLOWED_HOSTS = ['7d3a-114-36-66-27.ngrok-free.app']
6. >> python manage.py runserver 8000
7. 驗證line developer Webhook URL


# 建置linebot對話框
✓ 使用 ButtonsTemplate 建置 linebot 對話框，最多四個選項按鈕，每個按鈕最多有三個動作
https://www.learncodewithmike.com/2020/07/line-bot-buttons-template-message.html

✓ 使用 CarouselTemplate 建置 linebot 對話框，最多十個選項按鈕，每個按鈕最多有三個動作
https://steam.oxxostudio.tw/category/python/example/line-template-message.html#a3

# get user location
1. 使用 def handle_location_message(event) 
2. 需要加入 handler = WebhookHandler(settings.LINE_CHANNEL_SECRET) 這行。 
3. 加入 from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage
4. 加入 from linebot import WebhookHandler
5. 使用 event.message.type 來判斷傳入的訊息為 文字 or 位置

# 爬蟲
1. 使用 drinkShop.scrape() 爬飲料店分店的經緯度資料
2. 用 haversine() function 計算使用者與飲料店分店的距離

# 地址導入google map
1. 使用generate_google_maps_link()，在views.py裡面。

# 未完成
1. 自動爬不同的URL (目前寫死)
2. 根據shop_name做飲料選單





