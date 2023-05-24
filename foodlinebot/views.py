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

#from flask import abort

from .scraper import IFoodie


# 取得settings.py中的LINE Bot憑證來進行Messaging API的驗證
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN) 
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
# 處理接收到的訊息事件
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
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
    line_bot_api.reply_message(event.reply_token, flex_message)



@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE'] # 傳入的事件
        body = request.body.decode('utf-8') # 獲取 request 的內容，這邊假設為 JSON 格式

        signatureLo = request.headers['X-Line-Signature'] # 傳入的位置事件
        bodyLo = request.body.decode('utf-8')

 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
            # print("111 ", events) #印出事件 爬蟲part

            location_events = handler.handle(bodyLo, signatureLo)  # 傳入的位置事件
            print("222: ", location_events) #印出位置事件 爬蟲part

        except InvalidSignatureError:
            # abort(400)
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件

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
                
                #linebot 回傳 CarouselTemplate 最多十個
                if event.message.text == "哈囉":
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='CarouselTemplate', 
                            template=CarouselTemplate(
                                columns=[
                                    CarouselColumn(
                                        #thumbnail_image_url='https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/270016692_916592362328666_8079011016379207964_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=noyydldOoz4AX8a_ciM&_nc_ht=scontent-tpe1-1.xx&oh=00_AfA91FCOMU6QSrUfaT8VuJD23OETOykHfgpmvVjkFDWeRA&oe=6472AF3B',
                                        title='選單 1',
                                        text='說明文字 1',
                                        actions=[
                                            PostbackAction(
                                            label='postback',
                                            data='data1'
                                            ),
                                            MessageAction(
                                                label='哈囉',
                                                text='哈囉'
                                            ),
                                            URIAction(
                                                label='youtube url',
                                                uri='https://www.youtube.com/'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        #thumbnail_image_url='hhttps://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                                        title='選單 2',
                                        text='說明文字 2',
                                        actions=[
                                            PostbackAction(
                                            label='postback',
                                            data='data1'
                                            ),
                                            MessageAction(
                                                label='台北市',
                                                text='台北市'
                                            ),
                                            URIAction(
                                                label='茶湯會',
                                                uri='https://tw.tp-tea.com/'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        #thumbnail_image_url='hhttps://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                                        title='選單 3',
                                        text='說明文字 3',
                                        actions=[
                                            PostbackAction(
                                            label='postback',
                                            data='data1'
                                            ),
                                            MessageAction(
                                                label='台北市',
                                                text='台北市'
                                            ),
                                            URIAction(
                                                label='茶湯會',
                                                uri='https://tw.tp-tea.com/'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        #thumbnail_image_url='hhttps://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                                        title='選單 4',
                                        text='說明文字 4',
                                        actions=[
                                            PostbackAction(
                                            label='postback',
                                            data='data1'
                                            ),
                                            MessageAction(
                                                label='台北市',
                                                text='台北市'
                                            ),
                                            URIAction(
                                                label='茶湯會',
                                                uri='https://tw.tp-tea.com/'
                                            )
                                        ]
                                    ),
                                    CarouselColumn(
                                        #thumbnail_image_url='hhttps://steam.oxxostudio.tw/download/python/line-template-message-demo2.jpg',
                                        title='選單 5',
                                        text='說明文字 5',
                                        actions=[
                                            PostbackAction(
                                            label='postback',
                                            data='data1'
                                            ),
                                            MessageAction(
                                                label='台北市',
                                                text='台北市'
                                            ),
                                            URIAction(
                                                label='茶湯會',
                                                uri='https://tw.tp-tea.com/'
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

        return HttpResponse()
        
    else:
        return HttpResponseBadRequest()