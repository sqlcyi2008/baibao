import scapy.all

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

scapy.all.sniff(prn=arp_monitor_callback, filter="arp", store=0)