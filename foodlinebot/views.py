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

# from .scraper import IFoodie
from .scraper import iDrink


# 取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN) 
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)

'''
# 建立經緯度列表_test
coordinates = [
    (24.943134055011537, 121.3724875281764), #comebuy
    (24.942855244813064, 121.37269469336194), #milkshop
    (24.94226154270322, 121.37267765958076), #wootea
    (24.94378253440997, 121.37416293381938), #coco
    (24.937186, 121.367094), #truedan
    (24.942898036215105, 121.37372763003792) #machu
]
'''


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

                    # user的經緯度
                    user_latitude = event.message.latitude #緯度 24.多
                    user_longitude = event.message.longitude  #精度 121.多

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f"你傳送了位置資訊--> {user_latitude}, {user_longitude}")
                    )

                    drinkShop = iDrink() #可得到爬蟲經緯度的結果。資料型態是coordinates。程式在scraper.py
                    # print("drinkShop ", drinkShop.scrape(), "\n user_latitude: ", user_latitude, " user_longitude: ", user_longitude) #檢查drinkShop是否有得到web的經緯度                   
                    for ll, nn in drinkShop.scrape():
                        lat_try = ll
                        lon_try = nn
                        print("d: ", haversine(user_latitude, user_longitude, lat_try, lon_try))
                    
                   

        return HttpResponse()
        
    else:
        return HttpResponseBadRequest()
    
# 計算兩點間的距離
def haversine(lat1, long1, lat2, long2):
    R = 6371  # 地球半徑(公里)
    def rad(x):
        return x * math.pi / 180

    dLat = rad(lat2 - lat1)
    dLong = rad(long2 - long1)

    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
        math.cos(rad(lat1)) * math.cos(rad(lat2)) * \
        math.sin(dLong / 2) * math.sin(dLong / 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    d = R * c

    return d




'''
# 取得距離前五名短的店家
def get_rank_list(latitude, longitude, skip):
    json = _cacheService.get_json()
    dataList = json['features']
    rankList = sorted([
        {
            'rank': haversine(
                float(it['geometry']['coordinates'][1]),
                float(it['geometry']['coordinates'][0]),
                float(latitude),
                float(longitude)
            ),
            'data': it
        }
        for it in dataList
    ], key=lambda x: x['rank'])[skip:skip+5]
    
    rankList = [it['data'] for it in rankList]
    return rankList
'''



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