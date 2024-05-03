from flask import Flask, render_template, jsonify, request
import requests
import socket
import os
import random  # This is used for generating sample data for the graph

app = Flask(__name__)

def get_pihole_auth_token():
    """Read the Pi-hole authentication token from the local setupVars file."""
    setup_vars_path = '/etc/pihole/setupVars.conf'
    try:
        with open(setup_vars_path, 'r') as file:
            for line in file:
                if line.startswith('WEBPASSWORD='):
                    return line.strip().split('=')[1]
    except FileNotFoundError:
        return 'default_token_if_not_set'
    return 'default_token_if_not_set'

AUTH_TOKEN = get_pihole_auth_token()

def fetch_ip_from_dhcpcd():
    """Fetch the static IP address configured in dhcpcd.conf."""
    config_path = '/etc/dhcpcd.conf'
    try:
        with open(config_path, 'r') as file:
            for line in file:
                if line.strip().startswith('static ip_address') and not line.strip().startswith('#'):
                    ip_address = line.split('=')[1].strip().split('/')[0]
                    return ip_address
    except FileNotFoundError:
        return "dhcpcd.conf file not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"
    return "Static IP address not found."

def get_pihole_data(query):
    """Fetch data from Pi-hole Admin API using dynamic URL and AUTH_TOKEN."""
    ip_address = fetch_ip_from_dhcpcd()  # Use the new method to get the IP address
    url = f"http://{ip_address}/admin/api.php"
    full_url = f"{url}{query}&auth={AUTH_TOKEN}"
    try:
        response = requests.get(full_url)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/')
def dashboard():
    """Render the dashboard with Pi-hole statistics and IP address."""
    summary_data = get_pihole_data('?summary')
    
    if 'error' not in summary_data:
        stats = {
            'total_queries': summary_data.get('dns_queries_today', 'Unavailable'),
            'queries_blocked': summary_data.get('ads_blocked_today', 'Unavailable'),
            'domains_blocked': summary_data.get('domains_being_blocked', 'Unavailable')
        }
    else:
        stats = {
            'total_queries': 'Unavailable',
            'queries_blocked': 'Unavailable',
            'domains_blocked': 'Unavailable',
            'error': summary_data['error']
        }

    pi_hole_ip = fetch_ip_from_dhcpcd()  # Get the Pi-hole IP directly from dhcpcd.conf
    
    return render_template('dashboard.html', stats=stats, ip_address=pi_hole_ip)

@app.route('/api/activity-data', methods=['GET'])
def activity_data():
    """Endpoint to provide data for the 24-hour activity chart."""
    # Sample data generation
    hours = [f"{i}AM" if i != 12 else "12PM" for i in range(1, 13)] + [f"{i}PM" if i != 12 else "12AM" for i in range(1, 13)]
    queries = [random.randint(50, 200) for _ in range(24)]  # Random data for demonstration

    return jsonify({"hours": hours, "queries": queries})

@app.route('/api/blacklist', methods=['POST'])
def blacklist():
    """Add a domain to the Pi-hole blacklist."""
    url = request.form.get('url')
    response = get_pihole_data(f"?list=black&add={url}")
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
