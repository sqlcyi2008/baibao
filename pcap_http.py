import pcap
import dpkt
import redis

aaa = ''
url = ''
pc = pcap.pcap()
pc.setfilter('tcp port 80')

for ptime, pdata in pc:
    p = dpkt.ethernet.Ethernet(pdata)
    if p.data.__class__.__name__ == 'IP':
        ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
        if p.data.data.__class__.__name__ == 'TCP':
            if p.data.data.dport == 80:
                sStr1 = p.data.data.data
                #print '==>'+sStr1

                sStr2 = 'Host: '
                sStr3 = 'Connection'
                sStr4 = 'GET /'
                sStr41 = 'POST /'
                sStr5 = ' HTTP/1.1'
                sStr6 = 'Referer:'
                sStr7 = 'Content-Length:'

                nPos = sStr1.find(sStr3)
                nPosa = sStr1.find(sStr5)

                for n in range(sStr1.find(sStr2) + 6, nPos - 1):
                    aaa = sStr1[sStr1.find(sStr2) + 6:n]
                for n in range(sStr1.find(sStr4) + 4, nPosa + 1):
                    url = sStr1[sStr1.find(sStr4) + 4:n]
                for n in range(sStr1.find(sStr41) + 5, nPosa + 1):
                    url = sStr1[sStr1.find(sStr41) + 5:n]

                #aaa = sStr1[sStr1.find(sStr6) + 5:sStr1.find(sStr7)]
                #ccc = aaa + bbb
                #print '###'+ccc
                print url

                r = redis.Redis(host='localhost', port=6379, db=0)
                r.lpush("baibaoxiang", url)
