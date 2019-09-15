richdata={
  "size": {
    "width": 2500,
    "height": 1686
  },
  "selected": True,
  "name": "Rich Menu 1",
  "chatBarText": "เมนูหลัก",
  "areas": [
    {
      "bounds": {
        "x": 32,
        "y": 28,
        "width": 768,
        "height": 788
      },
      "action": {
        "type": "message",
        "text": "ราคา"
      }
    },
    {
      "bounds": {
        "x": 929,
        "y": 37,
        "width": 666,
        "height": 763
      },
      "action": {
        "type": "message",
        "text": "ข่าว"
      }
    },
    {
      "bounds": {
        "x": 1749,
        "y": 37,
        "width": 702,
        "height": 767
      },
      "action": {
        "type": "postback",
        "text": "",
        "data": "ถามเรื่องทั่วไป"
      }
    }
  ]
}

from app import channel_access_token

import json

import requests


#RegisRich เพื่อเอา Rich menu id ที่ line สร้างให้ #richmenu-edf466945f66da98e98f20056cfe1034
def RegisRich(Rich_json,channel_access_token):

    url = 'https://api.line.me/v2/bot/richmenu'

    Rich_json = json.dumps(Rich_json)

    Authorization = 'Bearer {}'.format(channel_access_token)


    headers = {'Content-Type': 'application/json; charset=UTF-8',
    'Authorization': Authorization}

    response = requests.post(url,headers = headers , data = Rich_json)

    print(str(response.json()['richMenuId']))

    return str(response.json()['richMenuId'])

def CreateRichMenu(ImageFilePath,Rich_json,channel_access_token):

    richId = RegisRich(Rich_json = Rich_json,channel_access_token = channel_access_token)

    url = ' https://api.line.me/v2/bot/richmenu/{}/content'.format(richId)

    Authorization = 'Bearer {}'.format(channel_access_token)

    headers = {'Content-Type': 'image/jpeg',
    'Authorization': Authorization}

    img = open(ImageFilePath,'rb').read()

    response = requests.post(url,headers = headers , data = img)

    print(response.json())

CreateRichMenu(ImageFilePath='Resource/Slide1.jpg',Rich_json=richdata,channel_access_token=channel_access_token)



