# iDrinkSpot

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


