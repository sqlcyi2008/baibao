#!/usr/bin/python
#encoding:utf-8
import urllib
import os
def Schedule(a,b,c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100 :
        per = 100
    print '%.2f%%' % per
url = 'https://ss0.bdstatic.com/5aV1bjqh_Q23odCf/static/superman/img/logo/logo_white_fe6da1ec.png'
#local = url.split('/')[-1]
local = os.path.join('d:\\','logo_white_fe6da1ec.png')
print local
urllib.urlretrieve(url,local,Schedule)
######output######
#0.00%
#0.07%
#0.13%
#0.20%
#....
#99.94%
#100.00%