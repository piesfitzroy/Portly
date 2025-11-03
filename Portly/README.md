# PortScanPy

A lightweight, modern port scanner built in Python - designed for cybersecurity professionals, penetration testers, and network administrators.

## Overview

PortScanPy is a fast, concurrent TCP port scanner with a clean command-line interface. It's built with clean, type-hinted Python code and designed to be easy to read, extend, and showcase in a professional portfolio.

## Features

- **Fast Concurrent Scanning** - Uses ThreadPoolExecutor for parallel port scanning
- **Flexible Port Specification** - Single ports, ranges, or comma-separated lists
- **Service Detection** - Automatically identifies common services on open ports
- **Multiple Output Formats** - Human-readable text or JSON for scripting
- **Clean Architecture** - Modular design with clear separation of concerns
- **Type-Safe** - Full type hints throughout the codebase
- **Well Tested** - Comprehensive unit test coverage
- **Zero Dependencies** - CLI tool uses only Python standard library

## Installation

### Prerequisites

- Python 3.10 or higher

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/PortScanPy.git
cd PortScanPy
```

2. (Optional) Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. (Optional) Install dependencies for the web UI:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Scanning

Scan default ports (1-1024):
```bash
python main.py 192.168.1.10
```

### Specify Custom Ports

Single port:
```bash
python main.py scanme.nmap.org -p 80
```

Multiple ports:
```bash
python main.py scanme.nmap.org -p 22,80,443
```

Port range:
```bash
python main.py scanme.nmap.org -p 20-1024
```

### Advanced Options

Adjust timeout and concurrency:
```bash
python main.py example.com -p 1-65535 -w 500 -t 1.0
```

JSON output for scripting:
```bash
python main.py 192.168.1.10 -p 1-1024 --json
```

Verbose mode:
```bash
python main.py example.com -p 80-443 -v
```

### Command-Line Options

```
positional arguments:
  target                Target hostname or IP address to scan

options:
  -h, --help            Show help message and exit
  -p, --ports PORTS     Port specification: single (80), list (22,80,443),
                        or range (1-1024). Default: "1-1024"
  -t, --timeout TIMEOUT Socket timeout in seconds (default: 0.5)
  -w, --workers WORKERS Maximum number of concurrent workers (default: 100)
  -j, --json            Output results in JSON format
  -v, --verbose         Enable verbose output
```

## Example Output

### Human-Readable Format

```
PortScanPy - scanning host: 192.168.1.10
Ports: 1-1024 | Timeout: 0.5s | Workers: 100

[+] 22/tcp   open     ssh
[+] 80/tcp   open     http
[+] 443/tcp  open     https

Scan complete in 2.41 seconds.
Open ports: 3
```

### JSON Format

```json
{
  "target": "192.168.1.10",
  "ports_scanned": "1-1024",
  "timeout": 0.5,
  "results": [
    {"port": 22, "status": "open", "service": "ssh"},
    {"port": 80, "status": "open", "service": "http"},
    {"port": 443, "status": "open", "service": "https"}
  ],
  "summary": {
    "open_ports": 3,
    "scan_time_seconds": 2.41
  }
}
```

## Running Tests

Run the test suite:
```bash
python -m pytest tests/
```

Or using unittest:
```bash
python -m unittest discover tests
```

## Project Structure

```
PortScanPy/
├── portscanpy/
│   ├── __init__.py       # Package initialization
│   ├── scanner.py        # Core port scanning logic
│   ├── cli.py            # CLI argument parsing and formatting
│   └── services.py       # Common port-to-service mappings
├── tests/
│   ├── __init__.py
│   └── test_scanner.py   # Unit tests
├── web/                  # Optional web UI (coming soon)
├── main.py               # CLI entry point
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
```

## Legal and Ethical Use

**Important**: Only scan systems you own or have explicit written permission to test.

- Unauthorized port scanning may be illegal in your jurisdiction
- This tool is intended for:
  - Security testing on your own systems
  - Authorized penetration testing engagements
  - Educational and research purposes
  - Network administration tasks

Always obtain proper authorization before scanning any network or system.

## Future Enhancements

Potential features to add:

- **Rich Terminal Output** - Colorized output using the `rich` library
- **UDP Scanning** - Support for UDP port scanning
- **Service Banner Grabbing** - Capture service banners for fingerprinting
- **Output Formats** - XML, CSV, and other export formats
- **Stealth Scanning** - SYN scanning and other advanced techniques
- **Rate Limiting** - Built-in throttling to avoid network congestion
- **Web Dashboard** - Browser-based UI with IDE-inspired design
- **Scan Profiles** - Predefined scan configurations (fast, comprehensive, stealth)
- **IPv6 Support** - Full support for IPv6 addresses

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

MIT License - feel free to use this project for learning, portfolios, or professional work.

## Author

**Nick Barwick**

This project was created to demonstrate clean Python coding practices and cybersecurity tool development for potential employers and collaborators.

---

**Disclaimer**: This tool is provided for educational and authorized security testing purposes only. The author assumes no liability for misuse or damage caused by this program.
