import pcap
import dpkt

pc = pcap.pcap()
pc.setfilter('tcp port 1433')

for ptime, pdata in pc:
    p = dpkt.ethernet.Ethernet(pdata)
    if p.data.__class__.__name__ == 'IP':
        ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
        if p.data.data.__class__.__name__ == 'TCP':
            if p.data.data.dport == 1433:
                sStr1 = p.ip.tcp.data+''
                if sStr1:
                    print sStr1.replace('\0','')