# Device_Finder: Network Device Discovery Tool

This repository contains a Python-based network device discovery tool that uses ARP scanning to identify devices on your local network.

**for more scripts related cyber and securiy check here: [Cyber Security Scripts section](https://github.com/YanivHaliwa/Linux-Stuff/blob/master/readme.md#cyber-security-scripts).**

## Scripts

- **device_f**: A bash script that runs the main Python script with sudo privileges.
- **device_finder**: The main Python script that performs network scanning and device discovery.

## Features

- Automatically detects and scans all active network interfaces.
- Uses ARP scanning to discover devices on the local network.
- Retrieves MAC addresses, IP addresses, and hostnames of discovered devices.
- Multithreaded scanning for improved performance.
- Saves results to a JSON file for easy parsing and further analysis.

the script:
1. Determine your local IP and network range.
2. Identify active network interfaces.
3. Perform ARP scans on each interface.
4. Display results in real-time.
5. Save complete results to `scan_results.json`.

## Usage
Important: This tool is designed to run on the local machine (localhost) and scan the local network. It cannot be used to scan remote networks.

Run the `device_f`  

## Requirements

- Python 3
- scapy
- psutil

Ensure you have the necessary permissions to perform network scans on your system.



