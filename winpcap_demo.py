from winpcapy import WinPcapUtils
import dpkt

# Example Callback function to parse IP packets
def packet_callback(win_pcap, param, header, pkt_data):
    # Assuming IP (for real parsing use modules like dpkt)
    ip_frame = pkt_data[14:]
    # Parse ips
    src_ip = ".".join([str(ord(b)) for b in ip_frame[0xc:0x10]])
    dst_ip = ".".join([str(ord(b)) for b in ip_frame[0x10:0x14]])
    #print("%s -> %s" % (src_ip, dst_ip))
    p = dpkt.ethernet.Ethernet(pkt_data)
    if p.data.__class__.__name__ == 'IP':
        ip = '%d.%d.%d.%d' % tuple(map(ord, list(p.data.dst)))
        #print "IP:"+ip
        if p.data.data.__class__.__name__ == 'TCP' and p.data.data.dport == 80:
            hp = p.ip.tcp.data
            # print hp
            if hp.strip() and (hp.startswith('GET') or hp.startswith('POST')):
                print hp

WinPcapUtils.capture_on("*Ethernet*", packet_callback)