"""
Flask web application for PortScanPy.

Provides a web-based interface with an IDE-inspired aesthetic for
running port scans and viewing results.
"""

import os
import sys
import time
from pathlib import Path

from flask import Flask, render_template, request, jsonify

# Add parent directory to path to import portscanpy
sys.path.insert(0, str(Path(__file__).parent.parent))

from portscanpy.scanner import scan_ports, parse_ports

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main web interface."""
    return render_template("index.html")


@app.route("/api/scan", methods=["POST"])
def scan():
    """
    API endpoint to perform a port scan.

    Expected JSON payload:
    {
        "target": "hostname or IP",
        "ports": "port specification (e.g., '1-1024' or '22,80,443')",
        "timeout": 0.5,
        "workers": 100
    }

    Returns:
    {
        "success": true/false,
        "target": "hostname",
        "ports_scanned": "port specification",
        "results": [...],
        "scan_time_seconds": 1.23,
        "error": "error message if failed"
    }
    """
    try:
        data = request.get_json()

        target = data.get("target", "").strip()
        port_spec = data.get("ports", "1-1024").strip()
        timeout = float(data.get("timeout", 0.5))
        workers = int(data.get("workers", 100))

        # Validate inputs
        if not target:
            return jsonify({
                "success": False,
                "error": "Target hostname or IP is required"
            }), 400

        # Parse ports
        try:
            ports = parse_ports(port_spec)
        except ValueError as e:
            return jsonify({
                "success": False,
                "error": f"Invalid port specification: {str(e)}"
            }), 400

        if not ports:
            return jsonify({
                "success": False,
                "error": "No valid ports to scan"
            }), 400

        # Perform scan
        start_time = time.time()
        results = scan_ports(
            host=target,
            ports=ports,
            timeout=timeout,
            max_workers=workers
        )
        scan_time = time.time() - start_time

        # Filter to open ports only
        open_results = [r for r in results if r["status"] == "open"]

        return jsonify({
            "success": True,
            "target": target,
            "ports_scanned": port_spec,
            "results": open_results,
            "total_ports": len(ports),
            "open_ports": len(open_results),
            "scan_time_seconds": round(scan_time, 2)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
