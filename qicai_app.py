# -*- encoding:utf-8 -*-

import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import socket
import dpkt
import time
from multiprocessing import Process, Queue
import json
import psutil

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class TheQRCodeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('theqrcode.png')

#返回网络包信息
class PacketHandler(tornado.web.RequestHandler):
    def get(self):
        ll=[]
        while not q.empty():
            ll.append(q.get(True))
        self.write(json.dumps(ll))

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
            (r'/theqrcode.png', TheQRCodeHandler),
            (r'/pkt', PacketHandler)
        ]

        settings = {'template_path': '.','static_path':'static','static_url_prefix':'/static/'}
        tornado.web.Application.__init__(self, handlers, **settings)


# 操作系统监控
def os_watch(q):
    while True:
        for proc in psutil.process_iter():
            try:
                pinfo = proc.as_dict(attrs=['pid', 'name', 'cmdline'])
            except psutil.NoSuchProcess:
                pass
            else:
                if pinfo.get("cmdline"):
                    jj = json.dumps(pinfo)
                    print(jj)
                    q.put(jj)
        #暂停
        time.sleep(10)

# 抓包进程执行代码:
def capture_packet(q):
    sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    #10.9.11.72
    sniffer.bind(("10.9.11.72", 0))
    sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # receive all packages
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    try:
        while True:
            raw_buffer = sniffer.recvfrom(65535)[0]
            ipp = dpkt.ip.IP(raw_buffer)
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 80:
                tcp=''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                print(tcp)
                if tcp.startswith('GET') or tcp.startswith('POST'):
                    print(tcp.splitlines()[0])
                    q.put(tcp.splitlines()[0])
            #mysql
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 3306:
                #print (ipp.data.data)   ignore
                tcp=''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                if tcp.index('select') > -1 or tcp.index('insert') > -1 or tcp.index('update') > -1 or tcp.index('delete') > -1:
                    q.put(tcp.splitlines()[0])
            #oracle
            if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 1521:
                #print (ipp.data.data)   ignore
                tcp=''
                try:
                    tcp = ipp.data.data.decode(encoding="utf-8", errors="ignore")
                except Exception as e:
                    print(e)
                if tcp.index('select') > -1 or tcp.index('insert') > -1 or tcp.index('update') > -1 or tcp.index('delete') > -1:
                    q.put(tcp.splitlines()[0])
    except KeyboardInterrupt:
        pass
    # disabled promiscuous mode
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

#获取本机默认IP地址
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

if __name__ == '__main__':

    print("IP:"+get_ip())
    # 全局变量存储抓包消息
    global q
    q = Queue()
    pw = Process(target=capture_packet, args=(q,))
    pw.start()

    ow = Process(target=os_watch, args=(q,))
    ow.start()

    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
