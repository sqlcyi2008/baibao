#!/usr/bin/env python
# coding=utf-8
# This program is optimized for Python 2.7.

import socket
import fcntl
import struct
import os
import time


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


if __name__ == "__main__":
    ip = get_ip_address("enp0s3")
    # ip = get_ip_address("virbr0")
    print ip
    # http://192.168.31.56:9000/ws/?ip=192.168.31.56
    os.system("qrencode -s 8 -o ~/urlcode.png 'http://" + ip + ":9000/ws/?ip="+ip+"'")
    time.sleep(1)
    os.system("composite -gravity center ~/urlcode.png ~/background.png ~/dushiniang.png")
    time.sleep(1)
    # composite -gravity center dushiniang.png background.png des.png
    os.system("gsettings set org.gnome.desktop.background picture-uri 'file:///root/dushiniang.png'")
