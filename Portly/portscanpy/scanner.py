"""
Core port scanning functionality.

This module provides the main port scanning logic using concurrent socket
connections to check if ports are open or closed on a target host.
"""

import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Set, TypedDict

from .services import get_service_name


class ScanResult(TypedDict):
    """Type definition for a single port scan result."""
    port: int
    status: str  # "open" or "closed"
    service: Optional[str]


def scan_single_port(host: str, port: int, timeout: float) -> ScanResult:
    """
    Scan a single port on the target host.

    Args:
        host: The hostname or IP address to scan
        port: The port number to check
        timeout: Socket timeout in seconds

    Returns:
        A ScanResult dictionary containing port, status, and service name
    """
    result: ScanResult = {
        "port": port,
        "status": "closed",
        "service": None,
    }

    try:
        # Create a TCP socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            # Attempt to connect
            connection_result = sock.connect_ex((host, port))

            if connection_result == 0:
                result["status"] = "open"
                result["service"] = get_service_name(port)
    except socket.gaierror:
        # DNS resolution failed
        pass
    except socket.timeout:
        # Connection timed out
        pass
    except Exception:
        # Any other exception, treat as closed
        pass

    return result


def scan_ports(
    host: str,
    ports: List[int],
    timeout: float = 0.5,
    max_workers: int = 100,
) -> List[ScanResult]:
    """
    Scan multiple ports on a host using concurrent connections.

    Args:
        host: The hostname or IP address to scan
        ports: List of port numbers to scan
        timeout: Socket timeout in seconds (default: 0.5)
        max_workers: Maximum number of concurrent worker threads (default: 100)

    Returns:
        A list of ScanResult dictionaries, one for each port scanned

    Raises:
        socket.gaierror: If the hostname cannot be resolved
    """
    # First, verify the host is resolvable
    try:
        socket.gethostbyname(host)
    except socket.gaierror as e:
        raise socket.gaierror(f"Cannot resolve hostname: {host}") from e

    results: List[ScanResult] = []

    # Use ThreadPoolExecutor for concurrent scanning
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all port scan tasks
        future_to_port = {
            executor.submit(scan_single_port, host, port, timeout): port
            for port in ports
        }

        # Collect results as they complete
        for future in as_completed(future_to_port):
            try:
                result = future.result()
                results.append(result)
            except Exception:
                # If individual scan fails, skip it
                port = future_to_port[future]
                results.append({
                    "port": port,
                    "status": "closed",
                    "service": None,
                })

    # Sort results by port number
    results.sort(key=lambda x: x["port"])
    return results


def parse_ports(port_spec: str) -> List[int]:
    """
    Parse a port specification string into a list of port numbers.

    Supports:
    - Single port: "80"
    - Comma-separated: "80,443,8080"
    - Range: "20-1024"
    - Mixed: "22,80-90,443"

    Args:
        port_spec: The port specification string

    Returns:
        A sorted list of unique port numbers

    Raises:
        ValueError: If the port specification is invalid
    """
    ports: Set[int] = set()

    # Split by comma
    parts = port_spec.split(",")

    for part in parts:
        part = part.strip()

        if "-" in part:
            # Handle range
            try:
                start_str, end_str = part.split("-", 1)
                start = int(start_str.strip())
                end = int(end_str.strip())

                if start < 1 or end > 65535 or start > end:
                    raise ValueError(
                        f"Invalid port range: {part}. "
                        "Ports must be 1-65535 and start <= end."
                    )

                ports.update(range(start, end + 1))
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError(f"Invalid port range format: {part}") from e
                raise
        else:
            # Handle single port
            try:
                port = int(part)
                if port < 1 or port > 65535:
                    raise ValueError(
                        f"Invalid port number: {port}. "
                        "Ports must be 1-65535."
                    )
                ports.add(port)
            except ValueError as e:
                if "invalid literal" in str(e):
                    raise ValueError(f"Invalid port number: {part}") from e
                raise

    return sorted(list(ports))
