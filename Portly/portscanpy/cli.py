"""
Command-line interface for PortScanPy.

This module handles argument parsing, output formatting, and the main
CLI execution flow.
"""

import argparse
import json
import socket
import sys
import time
from typing import Any

from .scanner import parse_ports, scan_ports, ScanResult


def format_human_output(
    target: str,
    port_spec: str,
    timeout: float,
    workers: int,
    results: list[ScanResult],
    scan_time: float,
    verbose: bool = False,
) -> None:
    """
    Format and print scan results in human-readable format.

    Args:
        target: The target hostname or IP
        port_spec: The port specification string
        timeout: Socket timeout used
        workers: Number of workers used
        results: List of scan results
        scan_time: Total scan time in seconds
        verbose: Whether to show verbose output
    """
    print(f"\nPortScanPy - scanning host: {target}")

    if verbose:
        try:
            resolved_ip = socket.gethostbyname(target)
            if resolved_ip != target:
                print(f"Resolved to: {resolved_ip}")
        except socket.gaierror:
            pass

    print(f"Ports: {port_spec} | Timeout: {timeout}s | Workers: {workers}\n")

    # Filter to show only open ports
    open_ports = [r for r in results if r["status"] == "open"]

    if not open_ports:
        print("No open ports found.")
    else:
        for result in open_ports:
            port = result["port"]
            status = result["status"]
            service = result["service"] or "unknown"
            print(f"[+] {port}/tcp   {status:8s} {service}")

    print(f"\nScan complete in {scan_time:.2f} seconds.")
    print(f"Open ports: {len(open_ports)}")


def format_json_output(
    target: str,
    port_spec: str,
    timeout: float,
    results: list[ScanResult],
    scan_time: float,
) -> None:
    """
    Format and print scan results in JSON format.

    Args:
        target: The target hostname or IP
        port_spec: The port specification string
        timeout: Socket timeout used
        results: List of scan results
        scan_time: Total scan time in seconds
    """
    # For JSON output, include only open ports by default
    # (can be modified to include all if needed)
    open_results = [r for r in results if r["status"] == "open"]

    output: dict[str, Any] = {
        "target": target,
        "ports_scanned": port_spec,
        "timeout": timeout,
        "results": open_results,
        "summary": {
            "open_ports": len(open_results),
            "scan_time_seconds": round(scan_time, 2),
        },
    }

    print(json.dumps(output, indent=2))


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PortScanPy - A lightweight Python port scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s 192.168.1.10
  %(prog)s scanme.nmap.org -p 20-1024
  %(prog)s scanme.nmap.org -p 22,80,443 --json
  %(prog)s example.com -p 1-65535 -w 500 -t 1.0

Note: Only scan hosts you own or have explicit permission to test.
        """,
    )

    parser.add_argument(
        "target",
        help="Target hostname or IP address to scan",
    )

    parser.add_argument(
        "-p",
        "--ports",
        default="1-1024",
        help='Port specification: single (80), list (22,80,443), or range (1-1024). Default: "1-1024"',
    )

    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0.5,
        help="Socket timeout in seconds (default: 0.5)",
    )

    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=100,
        help="Maximum number of concurrent workers (default: 100)",
    )

    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output results in JSON format",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    # Parse port specification
    try:
        ports = parse_ports(args.ports)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nUse -h or --help for usage information.", file=sys.stderr)
        sys.exit(1)

    if not ports:
        print("Error: No valid ports to scan.", file=sys.stderr)
        sys.exit(1)

    # Perform the scan
    try:
        start_time = time.time()

        if args.verbose and not args.json:
            print(f"Starting scan of {len(ports)} ports...")

        results = scan_ports(
            host=args.target,
            ports=ports,
            timeout=args.timeout,
            max_workers=args.workers,
        )

        scan_time = time.time() - start_time

        # Output results
        if args.json:
            format_json_output(
                target=args.target,
                port_spec=args.ports,
                timeout=args.timeout,
                results=results,
                scan_time=scan_time,
            )
        else:
            format_human_output(
                target=args.target,
                port_spec=args.ports,
                timeout=args.timeout,
                workers=args.workers,
                results=results,
                scan_time=scan_time,
                verbose=args.verbose,
            )

    except socket.gaierror:
        print(f"Error: Cannot resolve hostname '{args.target}'", file=sys.stderr)
        print("Please check the hostname or IP address and try again.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
