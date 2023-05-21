from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage


from .scraper import IFoodie


# 取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN) 
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
 
 
@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            print(events) #印出事件 爬蟲part
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件

                food = IFoodie(event.message.text)  #使用者傳入的訊息文字
                
                line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    #TextSendMessage(text=event.message.text),  # 回應文字訊息 (一次只能有一個textsendmessage)
                    TextSendMessage(text=food.scrape())  # # 回應前五間最高人氣且營業中的餐廳訊息文字
                )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()