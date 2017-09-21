# coding:utf-8
import socket
import dpkt

# 监听的主机IPhost = "192.168.1.100"

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
        ip = '%d.%d.%d.%d' % tuple(map(ord, list(ipp.src.decode())))
        print(ip+":"+str(ipp.data.dport))
        if ipp.data.__class__.__name__ == 'TCP' and ipp.data.dport == 8080:
            tcp = ipp.data.data.decode()
            if tcp.startswith('GET') or tcp.startswith('POST'):
                print(tcp.splitlines()[0])

except KeyboardInterrupt:
    pass

# disabled promiscuous mode
sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)