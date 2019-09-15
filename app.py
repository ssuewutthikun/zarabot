import os
import sys
from argparse import ArgumentParser


from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
#from linebot.models import (
#    MessageEvent, TextMessage, TextSendMessage, #import image audio เพิ่มได้ comma ต่อเลย
#)
from linebot.models import * #เอาทุก Message เลย

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = 'eecc21eba22ac65ee5a4250c15d60e58'
channel_access_token ='cEOJvRa3nKHWbGOMfrKsmskR9z4TWk2AWn3zK06a14wzeR1UJbw3ihyGlgOiCgjItX1CIbeBW++vmE6ZEvSwYEZJdyHxjnTXJmblv0ttRwZl9yranqTBdMv25mmjInbtA66jKd5GsS2adhGDrNLvlwdB04t89/1O/w1cDnyilFU='


line_bot_api = LineBotApi(channel_access_token) #ตัวส่ง API
handler = WebhookHandler(channel_secret)


@app.route("/webhook", methods=['POST']) #ใช้ได้เฉพาะ POST ใน sdk
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage) #มันมาจากเรียก handler.handle(body, signature) #ถ้า event เข้ามาเป็น MessageEvent เป็นประเภท Text #ถ้าเป็น image ก็เปลี่ยน message=ImageMessage
def message_text(event):
    #fuction reply_token #line ส่งมาหา server เรา ได้
    print("reply_token: "+ event.reply_token) #debug
    print("userId: "+event.source.user_id) #debug 
    print("message id: "+event.message.id) #debug 
    print("message: "+event.message.text) #debug

    Reply_token = event.reply_token # reply token

    text_fromuser = event.message.text # get ข้อความที่ user ส่งมา
    
    if "ราคา" in text_fromuser:
        from Resource.bxAPI import GetBxPrice
        #from random import randint
        #num = randint(1,5)
        data = GetBxPrice(Number_to_get=3)
        from Resource.FlexMessage import setCarousel, setbubble

        flex = setCarousel(data)
        from Resource.reply import SetMenuMessage_Object,send_flex
        flex = SetMenuMessage_Object(flex)
        send_flex(Reply_token,file_data=flex,bot_access_key=channel_access_token)
        #text_tosend = TextSendMessage(text=str(price))
        #text_tosend02 = TextSendMessage(text="Hello")
        #line_bot_api.reply_message(Reply_token,messages=text_tosend)
    else:
        text_list =[
            "ฉันไม่เข้าใจที่คุณพูด ลองใหม่",
            "ขออภัย ไม่ทราบ",
            "ขอโทษ ระบบไม่มีข้อมูล"
        ]

        from random import choice # random ข้อควมมตอบ user

        text_data = choice(text_list)

        text_random=TextSendMessage(text=text_data)
        line_bot_api.reply_message(Reply_token,text_random)

@handler.add(FollowEvent)
def RegisRichmenu(event):
    userid= event.source.user_id
    username = line_bot_api.get_profile(user_id=userid).display_name

    button_1= QuickReply(action=MessageAction(label="ราคา",text="ราคา"))
    button_2= QuickReply(action=MessageAction(label="ข่าว",text="ข่าว"))
    qbtn=QuickReply(items=[button_1,button_2])

    text=TextSendMessage(text="สวัสดีคุณ {} ยินดีต้อนรับสู่ bot".format(username))
    text_2=TextSendMessage(text="กรุณาเลือก เมนูที่ต้องการ",quick_reply=qbtn)

    line_bot_api.link_rich_menu_to_user(userid,"richmenu-edf466945f66da98e98f20056cfe1034")

    #line_bot_api.reply_message(event.reply_token,messages=[text,text_2])

if __name__ =="__main__":
    app.run(port=200) #app นี้คือชื่อไฟล์