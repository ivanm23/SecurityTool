import nmap3
import config.constants as cons


def discover_hosts():
    nmap = nmap3.NmapHostDiscovery()
    results = nmap.nmap_no_portscan(cons.DEFAULT_GATEWAY + '/24')
    hosts = list()

    for host in results['hosts']:
        temp_dict = dict()
        os_dict=return_os(host['addr'])
        temp_dict['ip'] = host['addr']
        temp_dict['type']=os_dict['type']
        temp_dict['os'] = os_dict['name']
        temp_dict['probability'] = os_dict['accuracy']
        hosts.append(temp_dict)

    return (hosts)


def return_os(ip_address):
    nmap = nmap3.Nmap()
    result = nmap.nmap_os_detection(ip_address)
    if result.__len__() != 0:
        return {'name': result[0]['name'], 'accuracy': result[0]['accuracy'], 'type': result[0]['osclass']['type']}
    #return {'name': 'Android 4.1 - 6.0 (Linux 3.4 - 3.14)', 'accuracy': 100, 'type': 'phone'}  # istraziti preko DHCP-a detekciju mobilnog OS
    return {'name': 'ne znam', 'accuracy': 100, 'type': 'ne znam'}

if __name__ == '__main__':
    print(discover_hosts())
