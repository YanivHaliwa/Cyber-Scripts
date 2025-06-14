
# Cyber-Stuff: Cybersecurity Scripts Collection

A focused collection of cybersecurity scripts and utilities for security professionals, penetration testers, and ethical hackers. This repository contains standalone tools for encoding/decoding, hash analysis, password cracking, network scanning, and more.

## Scripts Overview

**decode**: Multi-format decoding tool (base64, URL, HTML, etc.)

**dir_finder**: Asynchronous directory discovery for web servers.

**encode**: Multi-format encoding and hash utility.

**getlink**: Extracts all links from a given webpage.

**gtfbin**: Checks binaries against GTFOBins for privilege escalation vectors.

**haid**: Hash analysis and identification using hash_mode.txt reference.

**hashc**: Bash wrapper for Hashcat (crack hashes with wordlists).

**hashline**: Python script for processing and joining hash files.

**johng**: Crack GPG-encrypted files using John the Ripper.

**johnp**: Crack hashes with John the Ripper (custom format/wordlist).

**johns**: Crack SSH private keys with John the Ripper.

**johnw**: Crack Linux shadow file passwords with John the Ripper.

**johnz**: Crack ZIP file passwords with John the Ripper.

**mvenom**: Metasploit msfvenom payload generator (Python).

**nmapy**: Automated Nmap scanning and report tool.

**portf**: Port scanner and service detector.

**soclisten**: Socat-based listener setup (Python wrapper).

**socremote**: Socat-based remote connection (Python wrapper).

**vtf**: VirusTotal file scanner (Bash, uses vtcli).

**vtu**: VirusTotal URL scanner (Bash, uses vtcli).

**webscan_sub**: Scans for subdomains and folders in HTML (BeautifulSoup).

**hash_mode.txt**: Reference file for hash types and modes (used by haid).

Scripts are located in the root and `scripts/` subfolder. All are standalone and can be used independently.

## Installation & Usage

clone the full repository:

```bash
git clone https://github.com/YanivHaliwa/Cyber-Scripts.git
cd Cyber-Scripts
```

Most scripts require Python 3 and some require additional packages (see script headers for requirements). Bash scripts require standard Linux tools and John the Ripper/Hashcat for password cracking.

## Legal Disclaimer

These tools are intended for legal security testing purposes only. Using any of these tools against systems without explicit permission is illegal. Always ensure you have proper authorization before conducting security tests.

## Author

Created by [Yaniv Haliwa](https://github.com/YanivHaliwa) for security testing and educational purposes.