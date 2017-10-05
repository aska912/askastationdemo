# -*- coding: utf-8 -*-
# filename: menu.py
import urllib
from basic import Token

class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()
        
    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print urlResp.read()

if __name__ == '__main__':
    myMenu = Menu()
    postJson = """
    {
        "button":
        [
            {
                "type": "click",
                "name": "开发指引",
                "key":  "dev_guide"
            },
            {
                "name": "公众平台",
                "sub_button":
                [
                    {
                        "type": "view",
                        "name": "更新公告",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "接口权限说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                    },
                    {
                        "type": "view",
                        "name": "返回码说明",
                        "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                    },
                    {
                        "type": "scancode_waitmsg",
                        "name": "扫码",
                        "key": "scan_sub_menu"
                    }
                ]
            },
            {
                "name": "发送",
                "sub_button":
                [
                    {
                        "type": "scancode_push",
                        "name": "扫一扫",
                        "key":  "send_menu_1_1",
                        "sub_button":[]
                    },
                    {
                        "type": "location_select",
                        "name": "位置",
                        "key":  "send_menu_1_2",
                        "sub_button":[]
                    },
                    {
                        "type": "pic_weixin",
                        "name": "照片",
                        "key":  "send_menu_1_3",
                        "sub_button":[]
                    },
                    {
                        "type": "pic_sysphoto",
                        "name": "拍摄",
                        "key":  "send_menu_1_4",
                        "sub_button":[]
                    },
                    {
                        "type": "pic_photo_or_album",
                        "name": "照片or拍摄",
                        "key":  "send_menu_1_5",
                        "sub_button":[]
                    }
                ]
            },
          ]
    }
    """
    accessToken = Token().get_access_token()
    #myMenu.delete(accessToken)
    myMenu.create(postJson, accessToken)
