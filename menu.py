# -*- coding: utf-8 -*-
# filename: menu.py
import urllib, json
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from basic import Token

class Menu(object):
    def __init__(self):
        self.xmlfile="menu.xml"

    def readConfig(self):
        cfgXmlData = self.parseXml()
        if len(cfgXmlData) == 0:
            return None
        else:
            return json.dumps(cfgXmlData, ensure_ascii=False, encoding="utf-8")

    def parseXml(self):
        menuDict = {}
        menuTree = ET.parse(self.xmlfile)
        menuRoot = menuTree.getroot()
        menuTag = menuRoot.tag
        if menuTag == "menu": 
            menuTag="button"
            menuDict = {menuTag: []}
        else:
            return menuDict
        for button in menuRoot:
            btnName = button.attrib['name'].encode('utf-8')
            if isinstance(button.find('subbutton'), Element):
                btnDict = {'name': btnName, "sub_button": []}
                for subutton in button:
                    subtnName = subutton.attrib['name'].encode('utf-8')
                    subtnType = subutton.find('type').text
                    subtnArgName = self.keyOrUrl(subtnType)
                    subtnArg = subutton.find(subtnArgName).text
                    subtnDict = {'name': subtnName, \
                                 'type': subtnType, \
                                 subtnArgName: subtnArg}
                    btnDict["sub_button"].append(subtnDict)
            else:
                btnType = button.find('type').text
                btnArgName = self.keyOrUrl(btnType)
                btnArg = button.find(btnArgName).text
                btnDict = {'name': btnName, \
                           'type': btnType, \
                           btnArgName: btnArg}
            menuDict[menuTag].append(btnDict)
        return menuDict
            

    def keyOrUrl(self, btnType):
        if btnType == "view":
            return "url"
        elif btnType == "click"             or \
             btnType == "scancode_waitmsg"  or \
             btnType == "scancode_push"     or \
             btnType == "location_select"   or \
             btnType == "pic_weixin"        or \
             btnType == "pic_sysphoto"      or \
             btnType == "pic_photo_or_album":
            return "key"

    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        return urlResp.read()

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()
        
    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()

if __name__ == '__main__':
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
    myMenu = Menu()
    accessToken = Token().get_access_token()
    print myMenu.create(myMenu.readConfig(), accessToken)
