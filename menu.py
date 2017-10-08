# -*- coding: utf-8 -*-
# filename: menu.py

import urllib, json
from basic import Token

import xml.etree.ElementTree as ET

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
        if menuRoot.tag == "menu": 
            menuTag="button"
            menuDict = {menuTag: []}
        else:
            return menuDict
        for button in menuRoot:
            btnName = button.attrib['name'].encode('utf-8')
            if isinstance(button.find('subbutton'), ET.Element):
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
    myMenu = Menu()
    accessToken = Token().get_access_token()
    print myMenu.create(myMenu.readConfig(), accessToken)
