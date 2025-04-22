# SQLMap Automation Script (sqlm)

A powerful bash script that enhances and automates SQLMap operations for SQL injection testing with advanced output processing and data organization.

## Disclaimer

This tool is intended for legal security testing purposes only. Using this tool against any website or application without explicit permission is illegal. Always ensure you have proper authorization before conducting security tests.

## Description

This script streamlines SQLMap usage for security professionals by:

- Automating common SQLMap commands with an easy-to-use interface
- Organizing extracted data in a structured, readable format
- Providing an interactive menu for various SQL injection testing options
- Extracting and organizing database schemas and content systematically
- Capturing and securely storing password hashes and credentials
- Generating comprehensive reports of discovered vulnerabilities

## Features

### Core Functionality
- Interactive testing menu with guided options
- Support for both URL targets and request file inputs
- DBMS type specification for targeted testing
- Structured output organization in user-defined directories

### Automated Detection & Extraction
- Complete database enumeration and discovery
- Table schema automatic extraction and organization
- Intelligent data extraction from vulnerable tables
- Password hash capture and secure storage
- System information gathering (OS, hostname, web server details)
- Privilege escalation opportunity detection

### Data Management
- Rebuilds structure logs with consistent formatting
- Deduplicates extracted data for clean results
- Creates separate files for each database and table
- Merges cached results to prevent data loss
- Maintains session context across multiple runs

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YanivHaliwa/Cyber-Stuff.git
   ```

2. Navigate to the SQLMap enhance directory:
   ```bash
   cd Cyber-Stuff/sqlmap_enhance
   ```

3. Make the script executable:
   ```bash
   chmod +x sqlm
   ```

4. Ensure you have SQLMap installed:
   ```bash
   # Install sqlmap if not already installed
   sudo apt-get install sqlmap
   ```

## Usage

```bash
./sqlm -r <request-file> | -u <url-or-ip> [-d <dbms>]
```

### Options:
- `-r` - Specify a request file (captured HTTP request)
- `-u` - Specify a target URL or IP address
- `-d` - Specify the DBMS type (optional)

## Example Workflows

### Testing a vulnerable web form:
```bash
./sqlm -u "http://vulnerable-site.com/page.php?id=1"
```

### Using a captured request with Burp Suite:
```bash
./sqlm -r request.txt
```

### Targeting a specific database type:
```bash
./sqlm -u "http://vulnerable-site.com/page.php?id=1" -d mysql
```

## Requirements

- SQLMap installed and available in PATH
- Bash shell environment
- Standard Unix utilities

## Security Considerations

- Only use on systems you have explicit permission to test
- Handle extracted data securely and confidentially
- Follow responsible disclosure practices
- Delete sensitive extracted data when testing is complete

## License

This script is provided for educational and professional security testing purposes only.

## Author

Created by [Yaniv Haliwa](https://github.com/YanivHaliwa) for security testing and educational purposes.
