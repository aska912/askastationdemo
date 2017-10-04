# -*- coding: utf-8 -*-
# filename: handle.py

import web
import hashlib
import reply
import receive

urls = (
    '/wx', 'Handle',
)

app = web.application(urls, globals())

#import sys
#print sys.getdefaultencoding()

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "hello"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print "\nHandle Post webdata is \n", webData  
            recMsg = receive.parse_xml(webData)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    if recMsg.Content == 'help':
                        content = u'您有什么需要帮助的吗？'
                    elif recMsg.Content == 'test':
                        content = u'请选择测试项'
                    elif recMsg.Content == '菜单':
                        content = u"""\r[1]天气预报
                                      \r[2]消消乐
                                      \r[3]王者荣耀
                                  """
                    else:
                        content = u"对不起,请原来小弟我才疏学浅，不明白您说的话！"
                elif recMsg.MsgType == 'image':
	            replyMsg = reply.ImageMsg(toUser, fromUser, recMsg.MediaId)
                    return replyMsg.send()
                elif recMsg.MsgType == 'voice':
                    content = u'您的声音真动听！'
		else:
		    content = u'未知的信息类型'
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                return replyMsg.send()
            
            print "Not Process"
            return "success"
        except Exception, Argment:
            return Argment

application = app.wsgifunc()
