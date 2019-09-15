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
channel_secret = os.getenv('eecc21eba22ac65ee5a4250c15d60e58', None)
channel_access_token = os.getenv('cEOJvRa3nKHWbGOMfrKsmskR9z4TWk2AWn3zK06a14wzeR1UJbw3ihyGlgOiCgjItX1CIbeBW++vmE6ZEvSwYEZJdyHxjnTXJmblv0ttRwZl9yranqTBdMv25mmjInbtA66jKd5GsS2adhGDrNLvlwdB04t89/1O/w1cDnyilFU=',None)


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
    print(event.reply_token) #debug
    print(event.message.text) #debug

    Reply_token = event.reply_token # reply token

    test_fromuser = event.message.text # get ข้อความที่ user ส่งมา
    text_to_send1=TextSendMessage(text="Hello",quick_reply=None) 
    text_to_send2=TextSendMessage(text="World",quick_reply=None) 
    #ส่งไป 2 ข้อความได้มากสุด 5 ข้อความ
    
    image_mesage_1 = ImageSendMessage(
        original_content_url="http://www.pinoy7.com/psptutorials/9/neonglow/images/img5.jpg",
        preview_image_url="http://www.pinoy7.com/psptutorials/9/neonglow/images/img5.jpg"
    )
    line_bot_api.reply_message(
        #event.reply_token, # ได้ reply token
        #TextSendMessage("Hello") #ส่ง text
        Reply_token,
        messages=[text_to_send1,text_to_send2,image_mesage_1]
    )



if __name__ =="__main__":
    app.run(port=200)