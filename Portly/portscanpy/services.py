"""
Common port-to-service name mappings for network services.

This module provides a dictionary mapping well-known port numbers to their
corresponding service names, useful for annotating port scan results.
"""

from typing import Dict, Optional

COMMON_PORTS: Dict[int, str] = {
    20: "ftp-data",
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    111: "rpcbind",
    135: "msrpc",
    139: "netbios-ssn",
    143: "imap",
    443: "https",
    445: "microsoft-ds",
    993: "imaps",
    995: "pop3s",
    1723: "pptp",
    3306: "mysql",
    3389: "ms-wbt-server",
    5432: "postgresql",
    5900: "vnc",
    6379: "redis",
    8080: "http-proxy",
    8443: "https-alt",
    27017: "mongodb",
}


def get_service_name(port: int) -> Optional[str]:
    """
    Get the service name for a given port number.

    Args:
        port: The port number to look up

    Returns:
        The service name if known, otherwise None
    """
    return COMMON_PORTS.get(port)
