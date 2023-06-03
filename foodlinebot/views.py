import json, requests
import math
import urllib.parse
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

# from .scraper import IFoodie
from .scraper import iDrink, iMenu


# 取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN) 
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


drinkShop_options = [] # 存距離短的店名的list
drink_category =[] #特定飲料店的菜單 (第一列是店名)

Shop_name = ["CoCo都可", "珍煮丹", "迷客夏", "可不可熟成紅茶", "麻古茶坊", "五桐號WooTEA", "COMEBUY", "清心福全"]

# 特定飲料店的菜單，t為使用者的輸入
def get_drink_category(t):
    aa = iMenu(t) #爬蟲
    category =[]

    for type, item, price, kcal in aa.scrape():
        TYPE = type
        ITEM = item
        PRICE = price
        KCAL = kcal
        category.append((t,TYPE, ITEM, PRICE, KCAL))
    for i in range(0, len(category)):
        drink_category.append({
            'shop': category[i][0],
            'type': category[i][1],
            'item': category[i][2],
            'price': category[i][3],
            'kcal': category[i][4]
        })
    return drink_category
    

# 傳送特定飲料店的大種類 (不重複)
def send_category_of_menu(category):
    columns=[]
    unique_types = get_unique_types(category)
    shop = drink_category[0]['shop']

    for option in unique_types:
        
        column = CarouselColumn(
            title = option['type'],
            text = shop + "   Try it!!",
            actions = [ #action最多只能添加三個
                MessageAction(
                label = '點我看 '+option['type'], #顯示在按鈕上的文字
                text = shop + ", " + option['type'] #顯示在聊天室的文字
                )
            ]
        )
        columns.append(column)
        # 创建 CarouselTemplate，并指定 columns 参数为上述列表
        carousel_template = CarouselTemplate(columns=columns)
                        
        # 使用上述 CarouselTemplate 创建 TemplateSendMessage
        template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template=carousel_template
        )
    return template_message

#列印不重複的飲料類別
def get_unique_types(category):
    unique_types = []
    printed_types = set()

    for item in category:
        drink_type = item['type']
        if drink_type not in printed_types:
            unique_types.append({
                'type': drink_type
                })
            printed_types.add(drink_type)

    return unique_types

'''
#判斷回傳的文字是否在[]中 
def check_text_in_list(text, drink_category):
    if text in drink_category:
        return True
    else:
        return False
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
        # print("event的細節: ", events)

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

                # 如果傳入的是文字訊息
                if event.message.type == 'text':
                    text = event.message.text
                    
                    #print("5555555 :", drinkShop_options)

                    if text == "我想喝飲料❗❗❗":
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text="歡迎使用iDrinkSpot!!! \n請傳送位置資訊~~~")
                        )

                    elif text in Shop_name:
                        drink_category.clear()
                        category = get_drink_category(text) # 傳送飲料店名稱，得到大項目

                        #顯示種類的選單
                        line_bot_api.reply_message(
                            event.reply_token,
                            send_category_of_menu(category)# 輸入大項目，顯示不重複的飲料type
                        )
                    else:
                        line_bot_api.reply_message(  # 輸入其他文字時，回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage("馬上使用 iDrinkSpot 吧!!! \n請傳送位置資訊~~~")
                    )
                    

                # 如果傳入的是位置訊息
                elif event.message.type == 'location':

                    # user的經緯度
                    user_latitude = event.message.latitude #緯度 24.多
                    user_longitude = event.message.longitude  #精度 121.多
                    

                    drinkShop = iDrink() #可得到爬蟲經緯度的結果。資料型態是coordinates。程式在scraper.py
                    # print("drinkShop ", drinkShop.scrape(), "\n user_latitude: ", user_latitude, " user_longitude: ", user_longitude) #檢查drinkShop是否有得到web的經緯度                   
                    
                    distance = [] #存所有距離的list
                    drinkShop_options.clear() # 重新存data

                    for shopname, branchshop, addr, ll, nn in drinkShop.scrape():
                        ShopName = shopname
                        BRANCH_SHOP = branchshop
                        address = addr
                        lat_try = ll
                        lon_try = nn

                        # 計算所有距離，存入distance[]
                        distance.append((haversine(user_latitude, user_longitude, lat_try, lon_try), BRANCH_SHOP, ShopName, address))
                        #print("d: ", haversine(user_latitude, user_longitude, lat_try, lon_try), "shop name: ", shopname) #檢查haversine是否有得到距離
                       
                    distance.sort() #距離由小到大排序
                    count=0 #用來看有沒有距離小於1公里的店家
                                        
                    #查看前8筆距離短的資料，如果距離小於1公里，就回傳。如果有回傳一筆就跳出回圈。
                    for i in range (0, 5):
                        if distance[i][0] < 1:
                            #print("店名: ", distance[i][2], " / 分店: ", distance[i][1], " / 距離: ", distance[i][0], " / 地址: ", distance[i][3])
                            
                            google_maps_link = generate_google_maps_link(distance[i][3])
                            #print("google_maps_link: ",google_maps_link)
                            
                            drinkShop_options.append({
                                'ShopName': distance[i][2],
                                'BRANCH_SHOP': distance[i][1],
                                'url': google_maps_link
                                }
                            )
                            count+=1

                        else:
                            print("Sorry~ 方圓一公里內沒有飲料店喔")
                            line_bot_api.reply_message(
                                event.reply_token,
                                TextSendMessage(text= "Sorry~ 方圓一公里內沒有飲料店喔")
                            )
                            break
                            
                    print("drinkShop_options: ", drinkShop_options)
                    if count > 0:
                        #右滑式選單，顯示飲料店選單
                        near_shop = send_near_shop()
                        line_bot_api.reply_message(
                            event.reply_token,
                            near_shop
                        )
                        count=0

                    
                            
                        
                        
        return HttpResponse()
        
    else:
        return HttpResponseBadRequest()





# 傳送user附近的飲料店
def send_near_shop():
    columns=[]
    for option in drinkShop_options:
        column = CarouselColumn(
            title = option['ShopName'],
            text = option['BRANCH_SHOP'],
            actions = [ #action最多只能添加三個
                MessageAction(
                label = '點我看菜單', #顯示在按鈕上的文字
                text = option['ShopName'] #顯示在聊天室的文字
                ),
                URIAction(
                    label = 'Google Map',
                    uri = option['url']
                )
            ]
        )
        columns.append(column)
        # 创建 CarouselTemplate，并指定 columns 参数为上述列表
        carousel_template = CarouselTemplate(columns=columns)
                        
        # 使用上述 CarouselTemplate 创建 TemplateSendMessage
        template_message = TemplateSendMessage(
            alt_text='CarouselTemplate',
            template=carousel_template
        )
    return template_message

        






# 輸入地址產生Google Maps連結
def generate_google_maps_link(address):
    base_url = 'https://www.google.com/maps/search/?api=1'
    encoded_address = urllib.parse.quote(address)
    return f'{base_url}&query={encoded_address}'


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


''' 滑軌選單模板
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
'''


''' 四個選擇 模板
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

'''