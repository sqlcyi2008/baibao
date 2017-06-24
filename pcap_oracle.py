import pcap
import dpkt
import redis

sql = ''
pc = pcap.pcap()
pc.setfilter('tcp port 1521')


def OnlyCharNum(s, oth=''):
    s2 = s.lower();
    fomart = "abcdefghijklmnopqrstuvwxyz0123456789 ()*\"',.:/_=\\"
    for c in s2:
        if not c in fomart:
            s = s.replace(c, '');
    return s;


for ptime, pdata in pc:
    p = dpkt.ethernet.Ethernet(pdata)

    if p.data.__class__.__name__ == 'IP':
        ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
        if p.data.data.__class__.__name__ == 'TCP' and p.data.data.dport == 1521:
            sql = p.ip.tcp.data
            i_select = sql.find('select')
            i_insert = sql.find('insert')
            i_update = sql.find('update')
            i_delete = sql.find('delete')

            sql = OnlyCharNum(sql)
            print sql
            r = redis.Redis(host='localhost', port=6379, db=0)
            r.lpush("baibaoxiang", "pcap_sql_oracle=" + sql)
