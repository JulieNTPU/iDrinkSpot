import json, requests
import math
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (MessageEvent, TextSendMessage, TemplateSendMessage,
     ButtonsTemplate, MessageTemplateAction, CarouselTemplate, CarouselColumn, MessageAction,
    PostbackAction, URIAction, LocationMessage, TextComponent, BoxComponent, BubbleContainer, FlexSendMessage,
)
from numpy import var


#from flask import abort

from .scraper import IFoodie


# 取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN) 
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

'''
# 處理user傳送的location
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):

    position = "新北市三峽區國慶路150號" # 位置
    mapResponse = map.newGeocoder().geocode(position)
    print("666新北市三峽區國慶路150號: ", mapResponse)


    latitude = event.message.latitude  # 取得緯度
    longitude = event.message.longitude  # 取得經度
    address = event.message.address  # 取得地址

    # 建立 Flex Message 的內容
    bubble = BubbleContainer(
        body = BoxComponent(
            layout='vertical',
            contents =[
                TextComponent(text=f"緯度: {latitude}"),
                TextComponent(text=f"經度: {longitude}")
            ]
        )
    )
    # 建立 Flex Message
    flex_message = FlexSendMessage(alt_text="經緯度資訊", contents=bubble)

    # 回覆 Flex Message 給使用者
    line_bot_api.reply_message(
        event.reply_token, 
        flex_message
    )
    '''


# 處理地址資訊，地址轉經緯度



@csrf_exempt
def callback(request):
 
    if request.method == 'POST':

        # 獲取 request 的內容，這邊假設為 JSON 格式
        body = request.body.decode('utf-8')
        # 解析 JSON
        events = json.loads(body)['events']

        # 逐個處理事件
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        # events = parser.parse(body, signature)  # 傳入的事件

        print("event的細節: ", events)

        
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            # print("111 ", events) #印出事件 爬蟲part
        except InvalidSignatureError:
            # abort(400)
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                print("進入訊息事件")

                '''
                #linebot 只回傳文字
                food = IFoodie(event.message.text)  #使用者傳入的訊息文字
                line_bot_api.reply_message(  # 回復訊息
                    event.reply_token,
                    #TextSendMessage(text=event.message.text),  # 回應文字訊息 (一次只能有一個textsendmessage)
                    TextSendMessage(text=food.scrape()) # 回應前五間最高人氣且營業中的餐廳訊息文字
                )
                '''
                '''
                #linebot 回傳按鈕，最多四個
                if event.message.text == "哈囉":
                     line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='Menu',
                                text='請選擇地區',
                                actions=[
                                    MessageTemplateAction(
                                        label='台北市',
                                        text='台北市'
                                    ),
                                    MessageTemplateAction(
                                        label='台中市',
                                        text='台中市'
                                    ),
                                    MessageTemplateAction(
                                        label='高雄市',
                                        text='高雄市'
                                    ),
                                    MessageTemplateAction(
                                        label='花蓮縣',
                                        text='花蓮縣'
                                    )
                                ]
                            )
                        )
                    )
                else:
                    food = IFoodie(event.message.text)
 
                    line_bot_api.reply_message(  # 回應前五間最高人氣且營業中的餐廳訊息文字
                        event.reply_token,
                        TextSendMessage(text=food.scrape())
                    )
                '''
                # 如果傳入的是文字訊息
                if event.message.type == 'text':
                    text = event.message.text
                    if text == "我想喝飲料❗❗❗":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="請傳送位置資訊")
                        )
                    
                    elif text == "哈囉":
                        line_bot_api.reply_message(  #linebot 回傳 CarouselTemplate 最多十個
                            event.reply_token,
                            TemplateSendMessage(    
                                alt_text='CarouselTemplate',
                                template=CarouselTemplate(
                                    columns=[
                                        CarouselColumn(
                                            title='茶湯會',
                                            text='solgan',
                                            actions=[
                                                    PostbackAction(
                                                    label='postback',
                                                    data='data1'
                                                ),
                                                MessageAction(
                                                label='茶湯會',
                                                text='茶湯會'
                                                ),
                                                URIAction(
                                                label='點我進入茶湯會官網',
                                                uri='https://tw.tp-tea.com/'
                                                )
                                            ]
                                        ),
                                        CarouselColumn(
                                            title='50嵐',
                                            text='solgan',
                                            actions=[
                                                PostbackAction(
                                                label='postback',
                                                data='data1'
                                                ),
                                                MessageAction(
                                                    label='50嵐',
                                                    text='50嵐'
                                                ),
                                                URIAction(
                                                    label='點我進入50嵐官網',
                                                    uri='http://50lan.com/web/news.asp'
                                                )
                                            ]
                                        )
                                    ]
                                )
                            )
                        )
                    else:
                        line_bot_api.reply_message(  # 輸入其他文字時，回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage("請說哈囉~")
                    )
                                    
                    
                
                # 如果傳入的是位置訊息
                elif event.message.type == 'location':
                    latitude = event.message.latitude
                    longitude = event.message.longitude
                    print("傳入location囉 333: ", latitude," & ", longitude)

                    lat_try = 24.945198700385056
                    lon_try = 121.3724270516457

                    Lat1 = latitude * math.pi / 180.0
                    Long1 = longitude * math.pi / 180.0
                    
                    dLat = (lat_try - latitude) * math.pi / 180.0
                    dLong = (lon_try - longitude) * math.pi / 180.0

                    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(Lat1) * math.cos(lat_try) * math.sin(dLong / 2) * math.sin(dLong / 2)
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

                    R = 6371
                    d = R * c
                    print("d: ", d)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f"你傳送了位置資訊--> {latitude}, {longitude}")
                    )

                    '''
                    position = "新北市三峽區國慶路150號" # 位置
                    mapResponse = maps.newGeocoder().geocode(position)

                    print("666新北市三峽區國慶路150號: ", mapResponse)
                    '''
        return HttpResponse()
        
    else:
        return HttpResponseBadRequest()