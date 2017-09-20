# coding:utf-8
import socket
import struct
from ctypes import *
import dpkt

# 监听的主机IPhost = "192.168.1.100"

# IP头定义
class IP(Structure):
    _fields_ = [
        ("ihl",             c_ubyte, 4),
        ("version",         c_ubyte, 4),
        ("tos",             c_ubyte),
        ("len",             c_ushort),
        ("id",              c_ushort),
        ("offset",          c_ushort),
        ("ttl",             c_ubyte),
        ("protocol_num",    c_ubyte),
        ("sum",             c_ushort),
        ("src",             c_uint),
        ("dst",             c_uint),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}

        # readable ip address
        self.src_address = socket.inet_ntoa(struct.pack("<I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<I", self.dst))

        # type of protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

socket_protocol = socket.IPPROTO_IP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind(("127.0.0.1", 0))
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
# receive all packages
sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        raw_buffer = sniffer.recvfrom(65535)[0]

        ipp = dpkt.ip.IP(raw_buffer)
        #ip.unpack(raw_buffer)
        #ip = '%d.%d.%d.%d' % tuple(map(ord, list(ipp.data.src)))
        #print("##"+ipp.data.__class__.__name__)
        if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 8080:
            tcp = ipp.data.data.decode()
            if tcp.startswith('GET') or tcp.startswith('POST'):
                print(tcp)

        #ip_header = IP(raw_buffer[:20])

        #print ("Protocol: %s %s -> %s " % (ip_header.protocol, ip_header.src_address, ip_header.dst_address))

except KeyboardInterrupt:
    pass

# disabled promiscuous mode
sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)