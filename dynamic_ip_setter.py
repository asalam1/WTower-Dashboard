import os
import subprocess
import netifaces as ni
import nmap

def get_subnet():
    gws = ni.gateways()
    default_gateway = gws['default'][ni.AF_INET][0]
    interface = gws['default'][ni.AF_INET][1]
    addrs = ni.ifaddresses(interface)
    ip_info = addrs[ni.AF_INET][0]
    ip = ip_info['addr']
    netmask = ip_info['netmask']
    ip_parts = ip.split('.')
    netmask_parts = netmask.split('.')
    subnet_base = '.'.join(str(int(ip_parts[i]) & int(netmask_parts[i])) for i in range(3))
    return subnet_base, interface


def scan_for_free_ip(subnet_base):
    nm = nmap.PortScanner()
    nm.scan(hosts=f'{subnet_base}.0/24', arguments='-sn')  # Ensure correct subnet formatting
    used_ips = nm.all_hosts()
    for ip_end in range(2, 255):  # Starts from .2 to avoid the typical gateway .1
        ip = f"{subnet_base}.{ip_end}"  # Ensure correct IP formatting
        if ip not in used_ips:
            return ip
    return None

def set_static_ip(ip_address, interface):
    config_path = '/etc/dhcpcd.conf'
    new_config = f"""
interface {interface}
static ip_address={ip_address}/24
static routers={ip_address.rsplit('.', 1)[0]}.1
static domain_name_servers=1.1.1.1 8.8.8.8
"""

    # Read the current contents of the file
    with open(config_path, 'r') as file:
        lines = file.readlines()

    # Filter out any lines related to the specified interface
    with open(config_path, 'w') as file:
        interface_found = False
        for line in lines:
            if line.strip().startswith('interface ' + interface):
                interface_found = True
                continue  # Skip this line
            if interface_found:
                if line.strip().startswith('static'):
                    continue  # Skip subsequent static config lines
                interface_found = False
            file.write(line)

        # Append the new configuration for the interface
        file.write(new_config)

    # Restart the network service to apply changes
    subprocess.run(['sudo', 'service', 'dhcpcd', 'restart'], check=True)



if __name__ == "__main__":
    subnet_base, interface = get_subnet()
    free_ip = scan_for_free_ip(subnet_base)
    if free_ip:
        print(f"Configuring IP: {free_ip} on interface {interface}")
        set_static_ip(free_ip, interface)
    else:
        print("No free IP found in the subnet.")