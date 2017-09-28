import socket
import struct
import binascii
import dpkt
from dpkt.ip import IP

can_frame_fmt = "=IB3x8s"
can_frame_size = struct.calcsize(can_frame_fmt)


def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)


def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
    return (can_id, can_dlc, data[:can_dlc])


# the public network interface
HOST = socket.gethostbyname(socket.gethostname())

HOST = "127.0.0.1"
# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

# Include IP headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# receive all packages
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# receive a package
while True:
    # print(s.recvfrom(2048))
    # pkt = s.recvfrom(2048)
    data,addr = s.recvfrom(65565)
    print(data)
    response_id = struct.unpack('!H', data[4:6])
    print(response_id)

    # print('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))
    #p = dpkt.ethernet.Ethernet(cf)
    #print(p)
    # print(cf)
    # ip = dpkt.ip.IP(cf)
    #ip = dpkt.ip.IP(cf)
    # print(pkt)
    #print(ip)

# disabled promiscuous mode
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
