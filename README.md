# WTower Dashboard

WTower Dashboard is a network-wide ad-blocking solution built on top of the Pi-hole software, utilizing a Raspberry Pi as the host device. It includes a Flask-based web dashboard for easy management and monitoring of network traffic and ad blocking. It aims to make Pi-hole a plug-and-play solution enabling users regardless of their technical background to take advantage of this solution.

## Features

- **Network-wide Ad Blocking**: Blocks advertisements across all devices on your network.
- **DNS CNAME Aliasing**: Handles DNS requests efficiently by leveraging DNS CNAME records.
- **24-Hour Activity Graph**: Visualizes DNS query activity over the last 24 hours, enhancing user interaction with dynamic data representation.
- **Dynamic IP Configuration**: Automatically configures a static IP address for the Raspberry Pi using DNS-level solutions.
- **User-Friendly Interface**: Provides an easy-to-navigate web interface for managing network settings and viewing statistics.
- **Multi-Device Configuration Guides**: Detailed instructions on how to configure DNS settings on various devices including iPhones, Macs, Windows PCs, and Android devices.

## Getting Started

### Prerequisites

- Raspberry Pi (Model 3B+ or newer recommended)
- SD Card with Raspberry Pi OS installed
- Internet connection
- Basic knowledge of networking

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/asalam-1/WTower-Dashboard.git
   cd WTower-Dashboard
   
2. **Setup Python Environment on Raspberry-Pi**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

4. **Run the Flask Application**
   ```bash
   python app.py

## Configuration 
- Configuring Your Network: Follow the DNS configuration guides included in the dashboard to set up each device to use your Pi-hole as its DNS server.
- Setting up Cron Jobs: Ensure that the dynamic IP setter and activity data fetch scripts run at startup by configuring cron jobs as described in the project documentation.

## Usage
  - After setting up the WTower Dashboard, you can access it via your web browser to monitor and manage ad blocking across your network. Use the provided configuration guides to direct DNS traffic from your devices through the Pi-hole on your Raspberry Pi.
 
## License
Distributed under the MIT License. See LICENSE for more information.

## Acknowledgments 
- Pi-hole for providing the fundamental ad-blocking technology.
- Flask for the web framework used to create the dashboard.
- Chart.js for the graphical representation of activity data.

