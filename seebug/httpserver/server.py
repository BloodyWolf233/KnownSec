# -*- coding: utf-8 -*-
import socket
import seebugSpider
import time
import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from StringIO import StringIO

import os
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')



class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

class ServerResquest(BaseHTTPRequestHandler):
    def do_GET(self):
        enc = "UTF-8"  # 设置返回的编码格式
        path = str(self.path)  # 获取请求的url
        if path == '/favicon.ico':
            return
        print(path)
        keyword = path.split('keyword=')[1]
        print(keyword)

        try:
            a, count = seebugSpider.seebugapi(keyword)
            information = json.loads(a, encoding='utf-8')
            print(information)
            print(count)
            self.send_response(200)
            if count == 10:
                #self.send_response(233)
                information = {"code": "busy"}
        except:
            #self.send_error(233,message="please request again")
            self.send_response(666)
            information = {"code": "error"}

        self.send_header("Server", "My server")
        self.end_headers()
        self.wfile.write(json.dumps(information, ensure_ascii=False))



def socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 9999))
    server_socket.listen(5)
    while True:
        client_socket, client_address = server_socket.accept()
        # 请求处理 | 得到客户端的请求信息，请求的路径，请求的方法 ... 我们在通过这些信息做出不同的响应
        request = client_socket.recv(1024)
        #print(request)
        #  响应处理
        requestdetial = HTTPRequest(request)
        #print(requestdetial.command, requestdetial.path)
        if requestdetial.command == 'GET':
            try:
                keyword = requestdetial.path.split('keyword=')[1]
                print(keyword)

                try:
                    response_body = json.loads(seebugSpider.seebugapi(keyword), encoding='utf-8')
                    time.sleep(20)
                    print(response_body)
                except:
                    response_body = "error"
                    pass
                response_start_line = "HTTP/1.1 200 OK\r\n"
                response_headers = "Content-Type: text/html\r\n"
                response = response_start_line + response_headers + "\r\n" + "<html>" + json.dumps(response_body, ensure_ascii=False) + "</html>"
                print("1111111")
                print(response)

                client_socket.sendall(bytes(response, "utf-8"))
            except:
                pass
        client_socket.close()

if __name__ == '__main__':
    #print(sys.getdefaultencoding())
    reload(sys)
    sys.setdefaultencoding('utf8')
    #print(sys.getdefaultencoding())
    host =('', 8888)
    server = HTTPServer(host,ServerResquest)
    print("Starting http server, listen at: %s:%s" % host)
    server.serve_forever()







