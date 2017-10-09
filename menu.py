# -*- coding: utf-8 -*-
# filename: menu.py

import urllib, json
from basic import Token

import xml.etree.ElementTree as ET

class Menu(object):
    def __init__(self):
        self.mainCfgXml="menu.xml"

    def readConfig(self, cfgXmlFile=""):
        if cfgXmlFile == "":
            #Convert XML to python struct
            cfgXmlData = self.parseXml(self.mainCfgXml)
        else:
            cfgXmlData = self.parseXml(cfgXmlFile)
        #Convert pystruct to JSON
        return (json.dumps(cfgXmlData, ensure_ascii=False, encoding="utf-8") if len(cfgXmlData) else None)

    def parseXml(self, configXml):
        btnElmtName = "button"
        mrElmtName = "matchrule"
        subtnElmtName = "sub_button"
        menuDict = {}
        menuTree = ET.parse(configXml)
        menuRoot = menuTree.getroot()
        
        hasBtnElmt = True if isinstance(menuRoot.find(btnElmtName), ET.Element) else False
        hasMrElmt = True if isinstance(menuRoot.find(mrElmtName), ET.Element) else False
        if hasBtnElmt and hasMrElmt:
            menuDict = {btnElmtName: [], mrElmtName:{}}
        elif hasBtnElmt and not hasMrElmt:
            menuDict = {btnElmtName: []}
        else:
            return menuDict
        
        for element in menuRoot:
            if element.tag == btnElmtName:
                btnElement = element
                btnName = btnElement.attrib['name'].encode('utf-8')
                if isinstance(btnElement.find(subtnElmtName), ET.Element):
                    btnDict = {'name': btnName, subtnElmtName: []}
                    for subutton in btnElement:
                        subtnName = subutton.attrib['name'].encode('utf-8')
                        subtnType = subutton.find('type').text
                        subtnArgName = self.keyOrUrl(subtnType)
                        subtnArg = subutton.find(subtnArgName).text
                        subtnDict = {'name': subtnName, 'type': subtnType, \
                                     subtnArgName: subtnArg}
                        btnDict[subtnElmtName].append(subtnDict)
                else:
                    btnType = btnElement.find('type').text
                    btnArgName = self.keyOrUrl(btnType)
                    btnArg = btnElement.find(btnArgName).text
                    btnDict = {'name': btnName, 'type': btnType, \
                               btnArgName: btnArg}
                menuDict[btnElmtName].append(btnDict)
            elif element.tag == mrElmtName:
                mrElement = element
                subElemnts = ["tag_id", "sex", "country", "province", "city", "language", "client_platform_type"]
                subElemntNum = len(subElemnts)
                num = subElemntNum
                if not menuDict.has_key(mrElmtName):
                    print "no %s object in menuDict"%mrElmtName
                    return {}
                for subElemnt in subElemnts:
                    subElemntString = mrElement.find(subElemnt).text
                    if subElemntString:
                        menuDict[mrElmtName].update({subElemnt: subElemntString})
                        num -= 1
                if num == subElemntNum:
                    return {}
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
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s"%accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        return urlResp.read()

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s"%accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s"%accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()
    
    #创建个性化菜单
    def createCustomMenu(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/addconditional?access_token=%s"%accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        return urlResp.read()
    
    #删除个性化菜单
    def deleteCustomMenu(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delconditional?access_token=%s"%accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()
    
    #测试个性化菜单
    def testCustomMenu(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delconditional?access_token=%s"%accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()
        
    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/trymatch?access_token=%s"%accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()

if __name__ == '__main__':
    myMenu = Menu()
    while True:
        print ""
        print "[1] Create the menu"
        print "[2] Query the menu"
        print "[3] Delete the menu"
        print "[4] Get selfmenu info"
        print "[5] Create the custom menu"
        print "[*] Press any key to exit"
        opt = raw_input()
        accessToken = Token().get_access_token()
        if opt == '1':
            #Create
            print myMenu.create(myMenu.readConfig(), accessToken)
        elif opt == '2':
            #Query
            print myMenu.query(accessToken)
        elif opt == '3':
            #Delete
            continue
        elif opt == '4':
            #Get
            #menuInfo = json.loads(myMenu.get_current_selfmenu_info(accessToken))
            #print menuInfo
            print myMenu.get_current_selfmenu_info(accessToken)
        elif opt == '5':
            print myMenu.createCustomMenu(myMenu.readConfig("custommenu_android.xml"), accessToken)
        else:
            break
