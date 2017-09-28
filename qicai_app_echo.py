# -*- encoding:utf-8 -*-

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import socket
import dpkt
import time
from multiprocessing import Process, Queue

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message(u"你好，主人！")

    def on_message(self, message):
        self.write_message(u"Your message was: " + message)
        while True:
            value = q.get(True)
            print("##"+value)
            self.write_message('Get %s from queue.' % value)
            time.sleep(0.1)

    def on_close(self):
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/echo', WebSocketHandler)
        ]

        settings = {'template_path': '.','static_path':'1111static','static_url_prefix':'/1111static/'}
        tornado.web.Application.__init__(self, handlers, **settings)

# 抓包进程执行代码:
def capture_packet(q):
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    sniffer.bind(("127.0.0.1", 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # receive all packages
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ipp = dpkt.ip.IP(raw_buffer)
            #ip = '%d.%d.%d.%d' % tuple(map(ord, list(ipp.src.decode())))
            #print(ip + ":" + str(ipp.data.dport))
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 8080:
                #print (ipp.data.data)
                tcp=''
                try:
                    tcp = ipp.data.data.decode()
                except Exception as e:
                    print(e)

                if tcp.startswith('GET') or tcp.startswith('POST'):
                    print(tcp.splitlines()[0])
                    q.put(tcp.splitlines()[0])
    except KeyboardInterrupt:
        pass
    # disabled promiscuous mode
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

if __name__ == '__main__':
    # 全局变量存储抓包消息
    global q
    q = Queue()
    pw = Process(target=capture_packet, args=(q,))
    pw.start()

    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8081)
    tornado.ioloop.IOLoop.instance().start()
