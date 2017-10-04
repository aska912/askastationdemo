# -*- coding: utf-8 -*-
# filename: basic.py
import urllib
import time
import json


def ReadLines(filename):
    lines = ()
    try:
        fd = open(filename, 'r')
        lines = fd.readlines()
        fd.close()
    except:
        print "No such as file: %s"%filename
        lines = ()
    return lines

def WriteLines(filename, strlist):
    try:
        fd = open(filename, 'w')
        fd.writelines(strlist)
        fd.close()
        return True
    except:
        print "No such as file: %s"%filename
        return False


class Token:
    def __init__(self):
        self.tokenFile="/opt/weixin/access_token"
        self.time_index = 0
        self.token_index = 1

        self.__accessToken = ''
        self.__leftTime = 0

    def __real_get_access_token(self):
        #appId = "wx7fca4fa8e9090fe6"
        #appSecret = "3114bc1517e7fb03f8c86ff3436923d4"
        appId = "wxa46aef2dfdf8ecb9"
        appSecret = "901db4a5388aaf315848a21abe0babe8"


        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        
        self.__accessToken = urlResp['access_token']
        self.__leftTime = int(time.time()) + int(urlResp['expires_in']) - 50  
        self.__write_access_token_to_file(self.__accessToken, self.__leftTime)
        print self.__leftTime
        print self.__accessToken

    def __write_access_token_to_file(self, token, leftime):
        strlist = ["%d\n"%leftime, "%s"%token]
        return WriteLines(self.tokenFile, strlist)


    def __read__access_token_from_file(self):
        tokenlines = ()
        tokenlines = ReadLines(self.tokenFile)
        if not len(tokenlines) == 2:
            tokenlines = ()
        return tokenlines
        

    def get_access_token(self):
        tokenlines = self.__read__access_token_from_file()
        tokenlinenum = len(tokenlines)
        if tokenlinenum == 2:
            leftime = int(tokenlines[self.time_index])
            curtime = int(time.time())
            print "leftime: ", leftime
            print "curtime: ", curtime
            if leftime > curtime:
                print "Get token from tokenfile"
                return tokenlines[self.token_index]
        if tokenlinenum == 0 or leftime <= curtime:
           print "Update token from api.weixin.qq.com"
           self.__real_get_access_token()
           return self.__accessToken


    def run(self):
        while(True):
            self.get_access_token()
            time.sleep(5)












