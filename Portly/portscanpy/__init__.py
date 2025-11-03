"""
PortScanPy - A lightweight Python port scanner.

This package provides port scanning functionality with a clean CLI interface
and support for concurrent scanning of multiple ports.
"""

__version__ = "1.0.0"
__author__ = "Nick Barwick"

from .scanner import scan_ports, parse_ports, ScanResult
from .services import get_service_name, COMMON_PORTS

__all__ = [
    "scan_ports",
    "parse_ports",
    "ScanResult",
    "get_service_name",
    "COMMON_PORTS",
]
