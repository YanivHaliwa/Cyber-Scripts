# Brute WiFi with Common Passwords

A lightweight Python-based GUI application to scan WiFi networks for common default passwords. This tool attempts to connect to wireless networks using a simple list of commonly used passwords.

**IMPORTANT LEGAL DISCLAIMER:**

This tool is intended for legitimate security testing of networks you own or have explicit permission to test. Unauthorized use against networks without permission is illegal in most jurisdictions and could result in criminal charges.

Use responsibly and ethically.

## Description

WiFi Brute Force is a simple yet effective tool for security professionals to:

- Scan for available wireless networks
- Test networks against a list of common passwords
- Detect weak WiFi security configurations
- Document successful access for security reports

Unlike more complex tools such as Aircrack-ng or Hashcat, this application uses a straightforward approach by attempting direct logins to wireless networks. It doesn't perform advanced attacks like packet capture, handshake analysis, or GPU-accelerated cracking.

## Features

- Clean GTK-based user interface
- Automatically detects available WiFi networks
- Lists networks with signal strength and security type
- Tests connections using a customizable password list
- Colored status feedback with timestamped logs
- Automatic reconnection to original network after testing
- Proper cleanup of temporary connection profiles
- Abort functionality to stop operations in progress

## Installation

1. Clone the repository:

```bash
git clone https://github.com/YanivHaliwa/Cyber-Stuff.git
cd Cyber-Stuff/brute_wifi
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Run the application with sudo privileges:

```bash
python3 bwifi.py
```

2. Click "Scan Networks" to detect available WiFi networks
3. Select a target network from the dropdown list
4. Click "Start Attack" to begin testing with default password list or browse for a custom list
5. Use the "Abort" button to stop an attack in progress

## Password Lists

The tool comes with a default list of common passwords (`default.txt`). You can create your own custom password lists as plain text files with one password per line.

## Requirements

- Python 3.6+
- GTK 3.0
- NetworkManager CLI (nmcli)
- Sudo privileges

## Ethics & Responsible Use

- Only use this tool on networks you own
- Always obtain explicit written permission before testing others' networks
- Document all testing activities for audit purposes
- Report vulnerabilities responsibly to network owners

## License

This project is released under the GNU General Public License v3.0 - see the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to submit pull requests with improvements or additional features.

## Disclaimer

The authors of this tool are not responsible for any misuse or damage caused by this program. Users are solely responsible for ensuring they comply with all applicable laws and regulations.
