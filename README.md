# Cyber-Stuff: Cybersecurity Toolkit Collection

A comprehensive collection of cybersecurity tools and utilities for security professionals, penetration testers, and ethical hackers. This repository contains various tools focused on different aspects of cybersecurity testing and analysis.

## Available Tools

### [Easy Scanner](./easy_scanner/)

A GUI-based network security scanner with support for multiple scanning tools including nmap, nikto, gobuster, dirsearch, enum4linux, wpscan, and sqlmap. Features intelligent service detection with targeted scanning and automatic output organization.

### [GoBuster Enhance](./gobuster_enhance/)

A Python wrapper that enhances the Gobuster tool with configuration management and improved user experience, making web directory discovery and DNS enumeration faster and more efficient.

### [SQLMap Enhance](./sqlmap_enhance/)

A powerful bash script that enhances and automates SQLMap operations for SQL injection testing with advanced output processing and data organization.

### [Exploit Search](./exploit_search/)

A command-line tool that searches for exploits and vulnerability information across multiple security databases including ExploitDB (via searchsploit), Metasploit Framework modules, AttackerKB, and National Vulnerability Database (NVD).

### [Brute WiFi](./brute_wifi/)

A lightweight Python-based GUI application to scan WiFi networks for common default passwords, intended for legitimate security testing of networks.

### [Devices Finder](./devices_finder/)

A network device discovery tool that uses ARP scanning to identify devices on your local network, capturing MAC addresses, IP addresses, and hostnames.

### [Keylogger Reader](./keylogger_reader/)

A Python-based keylogger for monitoring keystrokes and capturing the active window title on Linux systems, designed for educational purposes only.

### [Pass Finder](./pass_finder/)

An advanced file content search tool designed for searching sensitive information within files, particularly useful for cybersecurity professionals and system administrators.

### [Vuln-Analyzer](./vuln-analyzer/)

A comprehensive vulnerability analysis toolkit for processing and analyzing Nmap scan outputs, searching for CVEs, and generating detailed vulnerability reports.

#### [CLI Version](./vuln-analyzer/vuln_analyzer-CLI/)

Command-line tool that analyzes Nmap XML outputs, extracts vulnerabilities, and generates detailed reports with CVE information using standard or Vulners API lookups.

#### [GUI Version](./vuln-analyzer/vuln_analyzer-GUI/)

Web interface with cybersecurity-themed UI that uses AI to analyze scan data, categorize vulnerabilities, and provide exploitation guidance from various security tool outputs.

### [Scripts](./scripts/)

A collection of various cybersecurity-related scripts including:

- **decode/encode**: Tools for various encoding formats
- **dir_finder**: Asynchronous directory discovery tool
- **getlink**: Web scraper for extracting links
- **gtfbin**: Checks binaries against GTFOBins
- **haid**: Hash analysis and identification tool
- **hash** tools: Various scripts for hash cracking and analysis
- **john** tools: John the Ripper wrappers for different file types
- **mvenom**: Metasploit payload generator
- **nmapy**: Automated Nmap scanning tool
- **portf**: Port scanning and service detection
- **soc** tools: Socat wrappers for networking
- **vt** tools: VirusTotal API integration
- **webscan_sub**: Subdomain and folder scanner

## Legal Disclaimer

These tools are intended for legal security testing purposes only. Using any of these tools against systems without explicit permission is illegal. Always ensure you have proper authorization before conducting security tests.

## Author

Created by [Yaniv Haliwa](https://github.com/YanivHaliwa) for security testing and educational purposes.