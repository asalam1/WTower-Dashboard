def fetch_ip_from_dhcpcd():
    """Fetch the static IP address configured in dhcpcd.conf."""
    config_path = '/etc/dhcpcd.conf'
    try:
        with open(config_path, 'r') as file:
            for line in file:
                # Check for active static IP configurations and ignore commented lines
                if line.strip().startswith('static ip_address') and not line.strip().startswith('#'):
                    # Extract IP address, remove subnet notation and any potential comments
                    ip_address = line.split('=')[1].strip().split('/')[0]
                    return ip_address
    except FileNotFoundError:
        return "dhcpcd.conf file not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    return "Static IP address not found."

if __name__ == "__main__":
    ip_address = fetch_ip_from_dhcpcd()
    print(f"Static IP Address from dhcpcd.conf: {ip_address}")
