# -*- coding: utf-8 -*-
# filename: material.py
import urllib2, urllib
import json
import poster.encode
from poster.streaminghttp import register_openers
from basic import Token


class Material(object):
    def __init__(self):
        register_openers()

    #上传
    def upload(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")
        fileName = "hello"
        param = {'media': openFile, 'filename': fileName}
        #param = {'media': openFile}
        postData, postHeaders = poster.encode.multipart_encode(param)
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" % (accessToken, mediaType)
        request = urllib2.Request(postUrl, postData, postHeaders)
        urlResp = urllib2.urlopen(request)
        return urlResp.read()

    #下载
    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        headers = urlResp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            return jsonDict
        else:
            buffer = urlResp.read()  # 素材的二进制
            mediaFile = file("test_media.jpg", "wb")
            mediaFile.write(buffer)
            return "get successful"

    #删除
    def delete(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        return urlResp.read()

    #查询保存在公众号上素材的数量
    def query_cnt(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s"%accessToken
        urlResp = urllib.urlopen(url=postUrl)
        return urlResp.read()

    #获取素材列表
    def batch_get(self, accessToken, mediaType, offset=0, count=20):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/material"
               "/batchget_material?access_token=%s" % accessToken)
        postData = ("{ \"type\": \"%s\", \"offset\": %d, \"count\": %d }"
                    % (mediaType, offset, count))
        urlResp = urllib2.urlopen(postUrl, postData)
        print urlResp.read()


if __name__ == '__main__':
    myMedia = Material()
    while True:
        print "(u) Upload material into weixin"
        print "(d) Delete material from weixin"
        print "(g) Download material from weixin"
        print "(q) Query the count of materials"
        print "(b) Get the material list from weixin"
        print "(*) Press any key to exit"
        opt = raw_input()
        accessToken = Token().get_access_token()
        if opt == 'u':
            print myMedia.upload(accessToken, "capture.jpg", "image")
        elif opt == 'd':
            print myMedia.delete(accessToken, "Fiqs__Oot3SV3YnZ2OSYqOnhXtVb4WT53jyjbJ7Ry2I")
        elif opt == 'g':
            print myMedia.get(accessToken, "Fiqs__Oot3SV3YnZ2OSYqNES4lsR8mXVLGbbl4ILoxM")
        elif opt == 'q':
            print myMedia.query_cnt(accessToken)
        elif opt == 'b':
            print myMedia.batch_get(accessToken, 'image')
        else:
            break
        print
        


