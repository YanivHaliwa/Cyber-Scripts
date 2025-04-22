# EasyScanner - Security Scanning Tool

A GUI-based network security scanner with support for multiple scanning tools including nmap, nikto, gobuster, dirsearch, enum4linux, wpscan, and sqlmap.

## Features

- Easy-to-use PyQt6 interface for common security scanning tools
- Dark mode interface for extended usage
- Configurable scan parameters and output locations
- Detailed scan results displayed in a user-friendly interface
- Support for multiple scanning tools:
  - Nmap: Port scanning and OS detection with 100+ specialized scripts
  - Nikto: Web server vulnerability scanning
  - Gobuster: Directory/file enumeration
  - Dirsearch: Web path discovery
  - Enum4linux: Windows/Samba enumeration
  - WPScan: WordPress vulnerability scanning
  - SQLMap: SQL injection testing
- Intelligent service detection with targeted scanning
- Automatic output organization in project folders
- Comprehensive logging and report generation

## Advanced Scanning Capabilities

### Nmap Script Automation

EasyScanner uses intelligent service detection to automatically apply specialized Nmap scripts based on detected services:

#### Network Services
- **SMB/Windows**: Enumerate shares, domains, users, and OS details
- **NFS/RPC**: List shares, mount points, and accessible files
- **FTP**: Check anonymous access and list accessible files
- **SSH**: Enumerate authentication methods and key algorithms
- **DNS**: Test zone transfers, cache snooping, and service discovery
- **SNMP**: Gather interface data, OS info, and user accounts

#### Web Services
- **HTTP/HTTPS**: Detect WAFs, test CSRF/CORS, scan for SQL injection points
- **WordPress**: Full vulnerability scanning via WPScan integration
- **Web Directories**: Multiple tools (Gobuster, Dirsearch) for thorough enumeration

#### Databases
- **MySQL/MSSQL/PostgreSQL**: Check for empty passwords, enumerate users and tables
- **MongoDB/Redis/Cassandra**: Configuration and info gathering
- **Elasticsearch/CouchDB**: Database enumeration

#### Application Services
- **Docker/Kubernetes**: Registry enumeration, API security testing
- **Jenkins/RabbitMQ/Zookeeper**: Service configuration analysis
- **APIs**: GraphQL, REST endpoint discovery and testing

#### Security Testing
- **SSL/TLS**: Cipher testing, certificate validation, vulnerability checks (Heartbleed, POODLE)
- **IoT Devices**: UPNP, MQTT protocol testing
- **VNC/RDP**: Authentication bypass testing, info gathering

## Setup

### Prerequisites

- Python 3.x
- PyQt6
- The following security tools installed:
  - nmap
  - nikto
  - gobuster
  - dirsearch
  - enum4linux
  - wpscan
  - sqlmap

### Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `config.template.json` to `config.json` and adjust settings as needed:
   ```bash
   cp config.template.json config.json
   ```

### Configuration

The `config.json` file allows you to customize:
- Output directory for scan results
- Tool-specific settings and timeout values
- Default options for each scanning tool
- Custom wordlists and scan parameters

## Usage

Run the application with:

```bash
./run
```

Or manually:
```bash
pyuic6 appui.ui -o appui.py
python3 main.py
```

## Output and Reports

Scan results are saved in the configured output directory, which defaults to a subfolder under `reports/`. Each scan creates organized output files:

- Full Nmap scan details with OS detection
- Service-specific scan results
- Discovered files and directories
- Identified vulnerabilities
- Comprehensive logs with timestamps

The following files are generated:
- `app_log.txt`: Overall application logs
- `full_nmap_output.txt`: Complete nmap scan results
- Tool-specific output files (SQLMap, Gobuster, etc.)

## Customization

The UI is built with PyQt6 and can be modified by editing `appui.ui` with Qt Designer and regenerating the UI code:

```bash
pyuic6 appui.ui -o appui.py
```

## Troubleshooting

- **Sudo Password Prompts**: Some tools like nmap require sudo privileges for certain scan types. The application will prompt for your password when needed.
- **Missing Tools**: If you receive errors about missing commands, ensure all the security tools are installed on your system.
- **Scan Timeouts**: Adjust the timeout settings in `config.json` if scans are timing out.

## Security Notice

This tool is intended for authorized security testing only. Always ensure you have permission to scan the target systems. Unauthorized scanning of networks may be illegal in many jurisdictions.

## Legal Disclaimer

This tool is provided for educational and professional security testing purposes only. The developers are not responsible for any misuse or damage caused by this program. Always ensure you have proper authorization before scanning any systems.

## Author

Created by [Yaniv Haliwa](https://github.com/YanivHaliwa) for security testing and educational purposes.