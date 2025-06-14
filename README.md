# Cyber-Scripts: Professional Cybersecurity Toolkit

A curated collection of professional-grade cybersecurity tools for security professionals, penetration testers, and ethical hackers. This repository contains high-quality standalone tools for encoding/decoding, hash analysis, payload generation, and network reconnaissance.

## Installation

Clone the repository:

```bash
git clone https://github.com/YanivHaliwa/Cyber-Scripts.git
cd Cyber-Scripts
```

**Requirements:**
- Python 3.6+
- Python packages: `termcolor`, `nltk`, `wordninja`, `requests`, `magic`
- System tools: `nmap`, `msfvenom`

Install Python dependencies:
```bash
pip install termcolor nltk wordninja requests python-magic
```

## Professional Tools

### Text Encoding/Decoding Suite

#### `decode` - Advanced Multi-Format Decoder

A sophisticated decoder with intelligent format detection and English language validation. Supports 30+ encoding formats with automatic detection capabilities.

**Features:**
- Intelligent encoding detection with accuracy scoring
- English language validation using NLTK
- Support for Base encodings, ciphers, compression, and more
- Batch processing capabilities

**Usage:**
```bash
./decode [OPTIONS] [file_path]
```

**Key Options:**
- `-a, --all` - Activate all decoding methods (except XOR)
- `-c, --chiper` - Classic Cipher Decoders (ROT47, Caesar, Atbash)
- `-i, --internet` - URL and Internet Format Decoders
- `-s, --system` - Numeral System Decoders (ASCII, Octal, Binary, Hex)
- `-b, --base` - Base Decoders (Base16/32/58/64/85)
- `-e, --english` - Limit results to English strings only
- `-x, --xor` - XOR cipher decoder

**Examples:**
```bash
./decode -a suspicious_string.txt          # Try all methods
./decode -e encoded_data.txt               # English strings only
./decode -b "SGVsbG8gV29ybGQ="            # Base64 specific
```

#### `encode` - Comprehensive Encoding Toolkit

Multi-format encoder supporting 30+ encoding types including hashing, ciphers, and data serialization formats.

**Features:**
- Complete encoding suite (Base, Hash, Cipher, Compression)
- Hash generation (MD4, MD5, SHA family, CRC32)
- Classic cipher implementations
- Data serialization formats

**Usage:**
```bash
./encode [OPTIONS] [file_path]
```

**Options:**
- `-a, --all` - Include all encoding types
- `-c, --basic` - Basic encodings (ASCII, Octal, Binary, Hex)
- `-b, --base` - Base encodings (Base16/32/58/64/85)
- `-s, --hash` - Hash encodings (MD5, SHA family)
- `-d, --advanced` - Advanced encodings (URL, ROT47, Caesar, etc.)

**Examples:**
```bash
./encode -a plaintext.txt                  # All encoding methods
./encode -s "password123"                  # Hash values only
./encode -b sensitive_data.txt             # Base encodings only
```

### Hash Analysis Tools

#### `haid` - Professional Hash Identifier

Advanced hash analysis tool with comprehensive hash type detection using an extensive reference database.

**Features:**
- Identifies 500+ hash types and variants
- Uses comprehensive hash_mode.txt reference
- Provides Hashcat mode numbers for cracking
- Batch hash analysis support
- Detailed hash characteristics

**Usage:**
```bash
./haid [HASH_STRING]
```

**Examples:**
```bash
./haid "5d41402abc4b2a76b9719d911017c592"
./haid -f hash_file.txt                    # Batch analysis
```

#### `hash_mode.txt` - Hash Reference Database

Comprehensive reference file containing detailed information about hash types, their characteristics, and corresponding Hashcat modes. Used by the `haid` tool for accurate hash identification.

### Payload Generation

#### `mvenom` - Advanced Metasploit Payload Generator

Sophisticated msfvenom wrapper with intelligent payload selection, encoder options, and cross-platform support.

**Features:**
- Interactive payload selection with 18+ payload types
- Intelligent encoder selection based on target architecture
- Template file support for evasion
- Cross-platform compatibility (Windows, Linux, Android, Web)
- UPX packing support for size reduction
- Architecture-aware encoder recommendations

**Usage:**
```bash
./mvenom
```

The tool provides an interactive interface for:
- Target IP/interface resolution
- Port configuration
- Payload type selection (reverse shells, meterpreter, etc.)
- Encoder selection (polymorphic, alphanumeric, evasion-focused)
- Output format selection
- Template integration

**Example Session:**
```bash
./mvenom
IP attacker? [default: tun0]: 192.168.1.100
PORT attacker [default: 9000]? 4444
Select payload: windows/x64/meterpreter/reverse_tcp
Select encoder: x64/xor_dynamic
Output file: payload.exe
```

### Network Reconnaissance

#### `nmapy` - Automated Nmap Scanning Suite

Professional network scanning automation tool that performs intelligent multi-stage reconnaissance with detailed reporting.

**Features:**
- Two-stage scanning (discovery + detailed analysis)
- Automatic service enumeration
- XML and text report generation
- Domain to IP resolution
- Customizable port ranges
- Detailed service fingerprinting

**Usage:**
```bash
./nmapy [OPTIONS] <IP_ADDRESS or DOMAIN>
```

**Options:**
- `-p-` - Scan all 65535 ports
- `-p PORT` - Scan specific ports (comma-separated)
- `-h, --help` - Show detailed help

**Examples:**
```bash
./nmapy 192.168.1.1                       # Common ports scan
./nmapy -p- target.com                     # Full port scan
./nmapy -p 80,443,8080 192.168.1.0/24     # Specific ports
```

**Output:**
- Detailed scan reports with timestamps
- Service version detection
- XML output for further processing
- Summary of discovered services

## Use Cases

### For Penetration Testers
- **Reconnaissance**: Use `nmapy` for comprehensive network discovery and service enumeration
- **Payload Generation**: Create sophisticated payloads with `mvenom` for various target platforms
- **Data Analysis**: Decode captured data and identify hash types during engagements

### For CTF Players
- **Encoding Challenges**: Use `decode` with English validation to solve complex encoding puzzles
- **Hash Cracking**: Identify unknown hash types with `haid` before attempting to crack
- **Quick Encoding**: Generate various encoded formats for testing and validation

### For Security Researchers
- **Malware Analysis**: Decode obfuscated strings and identify hash algorithms
- **Network Analysis**: Automate scanning and service discovery with detailed reporting
- **Payload Research**: Study and generate various payload types for research purposes

## Installation Notes

All tools are standalone Python scripts with minimal dependencies. The toolkit is designed to work on any Linux distribution commonly used for security testing (Kali, Parrot, Ubuntu, etc.).

**Quick Setup:**
```bash
git clone https://github.com/YanivHaliwa/Cyber-Scripts.git
cd Cyber-Scripts
pip install termcolor nltk wordninja requests python-magic
```

## Legal Disclaimer

These tools are intended for authorized security testing and educational purposes only. Users are responsible for ensuring they have proper authorization before using these tools against any systems. Unauthorized use of these tools may violate local, state, national, or international laws.

## Author

Created by [Yaniv Haliwa](https://github.com/YanivHaliwa) for security testing and educational purposes.
