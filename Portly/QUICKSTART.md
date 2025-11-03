# PortScanPy - Quick Start Guide

## Running the CLI Tool

### Basic Usage

```bash
# Scan default ports (1-1024)
python3 main.py 192.168.1.10

# Scan specific ports
python3 main.py localhost -p 22,80,443

# Scan a range
python3 main.py scanme.nmap.org -p 1-1000

# JSON output
python3 main.py localhost -p 1-1024 --json

# Verbose mode
python3 main.py example.com -p 80-443 -v
```

### Running Tests

```bash
# Run all tests
python3 -m unittest discover tests -v

# Or with pytest (if installed)
pytest tests/ -v
```

## Running the Web UI (Optional)

### Setup

1. Install Flask:
```bash
pip install -r requirements.txt
```

2. Start the web server:
```bash
cd web
python3 app.py
```

3. Open your browser to:
```
http://localhost:5000
```

The web UI features an IDE-inspired dark theme with:
- Clean, panel-based layout
- Real-time scan execution
- Terminal-style output
- Developer-friendly aesthetics

## Project Structure

```
PortScanPy/
├── portscanpy/           # Main package
│   ├── __init__.py       # Package initialization
│   ├── scanner.py        # Core scanning logic
│   ├── cli.py            # CLI interface
│   └── services.py       # Port-to-service mapping
├── web/                  # Optional web UI
│   ├── app.py            # Flask backend
│   ├── templates/        # HTML templates
│   └── static/           # CSS and JavaScript
├── tests/                # Unit tests
│   └── test_scanner.py
├── main.py               # CLI entry point
├── requirements.txt      # Python dependencies
└── README.md             # Full documentation
```

## Future Enhancement Ideas

### Quick Wins
1. **Add color output** - Use the `rich` library for beautiful terminal output
2. **Save results** - Add flags to save results to CSV/XML files
3. **Port range presets** - Add common scan profiles (--fast, --full, --top-100)
4. **Banner grabbing** - Capture service banners for better fingerprinting

### Advanced Features
1. **UDP scanning** - Add support for UDP port scanning
2. **SYN scanning** - Implement stealth scanning techniques (requires raw sockets)
3. **Service version detection** - Identify specific software versions
4. **OS fingerprinting** - Detect operating system based on scan results
5. **Web dashboard** - Expand the web UI with:
   - Scan history and saved results
   - Multiple concurrent scans
   - Real-time progress updates
   - Network topology visualization
   - Scheduled/recurring scans

### Integration & Automation
1. **Python library** - Make it pip-installable
2. **CI/CD integration** - Use for automated security testing
3. **API mode** - Run as a REST API service
4. **Notifications** - Alert on open ports via email/Slack
5. **Database backend** - Store scan history in SQLite/PostgreSQL

## Code Style Notes

- Uses type hints throughout for better IDE support
- Follows PEP 8 style guidelines
- Clean separation of concerns (scanning, CLI, services)
- Comprehensive docstrings
- Error handling for edge cases
- Thread-safe concurrent scanning

## Security Reminder

**Always get permission before scanning!**

Only scan:
- Your own systems
- Systems you have written authorization to test
- Practice ranges like `scanme.nmap.org`

Unauthorized scanning may be illegal in your jurisdiction.

## Making it Your Own

To customize for your portfolio:
1. Update the author name in `__init__.py` and `README.md`
2. Add your GitHub username to the clone URL in `README.md`
3. Consider adding your own features to make it unique
4. Take screenshots of the web UI for your portfolio
5. Write a blog post about building it

---

**Happy scanning!** 🚀
