import pcap
import dpkt
import redis

hp = ''
pc = pcap.pcap('lo')
pc.setfilter('tcp port 8080')

for ptime, pdata in pc:
    p = dpkt.ethernet.Ethernet(pdata)
    if p.data.__class__.__name__ == 'IP':
        ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
        if p.data.data.__class__.__name__ == 'TCP' and p.data.data.dport == 8080:
            hp = p.ip.tcp.data
            # print hp
            if hp.strip() and (hp.startswith('GET') or hp.startswith('POST')):
                print hp
                #r = redis.Redis(host='localhost', port=6379, db=0)
                #r.lpush("baibaoxiang", "pcap_http=" + hp)
