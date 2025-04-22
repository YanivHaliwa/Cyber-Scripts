# GoBuster Enhance

A Python wrapper that enhances the Gobuster tool with configuration management and improved user experience, making web directory discovery and DNS enumeration faster and more efficient.

## Features

- Easy-to-use CLI interface for Gobuster
- Save and reuse scan configurations with a JSON-based settings system
- Support for both directory (dir) and DNS enumeration modes
- Configurable options for threads, status codes, extensions, and more
- Configuration file editing with your preferred editor (auto-detects $EDITOR environment variable)
- Smart handling of extensions and exclude-length parameters (supports file loading)
- Strong URL validation to prevent errors
- Proper error handling and user feedback
- Secure configuration storage (doesn't store target URLs)

## Prerequisites

- Python 3.x
- Gobuster must be installed and available in your PATH
- Standard wordlists (such as dirbuster's lists, typically found in `/usr/share/wordlists/`)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/YanivHaliwa/Cyber-Stuff.git
cd Cyber-Stuff/gobuster_enhance
```

2. Make the script executable:

```bash
chmod +x gob
```

3. Set up the initial configuration:

```bash
./gob --setup
```

This creates a default configuration file from the template.

## Usage

### Basic Usage

```bash
./gob -u [TARGET_URL] -w [WORDLIST_PATH]
```

Example:

```bash
./gob -u http://example.com -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
```

When running this command, the tool will prompt you for additional parameters such as mode, threads, status codes, extensions, etc. Your inputs will be saved for future use.

### Using Saved Settings

To use previously saved settings (stored in config.json):

```bash
./gob -j -u [TARGET_URL]
```

This allows you to reuse all your previous configuration parameters with a new target URL.

### Managing Configuration

To edit the configuration file:

```bash
./gob -e
```

This will open the configuration file in your preferred editor (automatically detected from your environment or defaults to common editors).

To reset the configuration to default values:

```bash
./gob --setup
```

## Configuration Options

The tool supports the following configuration options:

- **mode**: Scan mode - either 'dir' for directory scans or 'dns' for DNS enumeration. Default is 'dir'.
- **wordlist**: Path to the wordlist file to use for scanning. Points to dirbuster lists by default.
- **threads**: Number of concurrent threads for scanning. Default is 60 threads.
- **status_code_show**: HTTP status codes to display in results (e.g., "200,301,302,403"). Default shows common response codes (200,301,302,403,401,500).
- **status_code_avoid**: HTTP status codes to hide from results. Used as an alternative to status_code_show.
- **extensions**: File extensions to scan for (comma-separated list like "php,html,js" or path to a file containing extensions). Default includes common web extensions.
- **exclude_length**: Response lengths to exclude from results (comma-separated list or path to a file).
- **cname**: Boolean value (true/false) determining whether to include CNAME records in DNS mode (only applicable for DNS scans).

## Advanced Features

- **Smart Parameter Handling**:

  - For the `extensions` parameter, you can provide a file path instead of typing a long comma-separated list
  - Similarly, for `exclude_length`, you can reference a file containing response lengths to exclude
  - The tool automatically detects if you're providing a file path or direct values
- **Intelligent Editor Detection**:

  - Automatically detects your preferred editor from the `$EDITOR` environment variable
  - Falls back to common editors (nano, vim, emacs, etc.) if $EDITOR is not set
  - Ensures you can always edit your configuration comfortably
- **Secure Configuration Storage**:

  - Target URLs aren't stored in the configuration file for security reasons
  - Only saves parameters that don't contain sensitive information
- **Robust Error Handling**:

  - Validates input parameters to prevent common mistakes
  - Provides clear error messages when something goes wrong
  - Gracefully handles keyboard interrupts and command failures
- **Default Values**:

  - Sensible defaults are used when parameters aren't specified
  - Default extensions include common web file types
  - Default status codes show the most relevant responses

## Security Considerations

- This tool is intended for authorized security testing only
- Always ensure you have permission before scanning any target
- Review the generated commands before execution
- The tool does not store target URLs in the configuration file for security reasons

## License

This project is available under the MIT License.

## Author

Created by [Yaniv Haliwa](https://github.com/YanivHaliwa) for security testing and educational purposes.
