#!/usr/bin/python

import redis
from sys import stdout
from time import sleep

r=redis.Redis(host='localhost',port=6379,db=0)
while(1):
    str = r.rpop('baibaoxiang')
    if str:
        print str
        stdout.flush()
    sleep(0.05)
