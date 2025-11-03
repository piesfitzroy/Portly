"""
Unit tests for PortScanPy scanner module.

These tests verify port parsing logic and basic scanning functionality.
"""

import socket
import unittest
from unittest.mock import patch, MagicMock

from portscanpy.scanner import parse_ports, scan_ports, scan_single_port
from portscanpy.services import get_service_name


class TestPortParsing(unittest.TestCase):
    """Test cases for port specification parsing."""

    def test_single_port(self):
        """Test parsing a single port number."""
        result = parse_ports("80")
        self.assertEqual(result, [80])

    def test_comma_separated_ports(self):
        """Test parsing comma-separated port list."""
        result = parse_ports("80,443,8080")
        self.assertEqual(result, [80, 443, 8080])

    def test_port_range(self):
        """Test parsing a port range."""
        result = parse_ports("20-25")
        self.assertEqual(result, [20, 21, 22, 23, 24, 25])

    def test_mixed_specification(self):
        """Test parsing mixed port specification."""
        result = parse_ports("22,80-82,443")
        self.assertEqual(result, [22, 80, 81, 82, 443])

    def test_ports_with_spaces(self):
        """Test parsing ports with extra whitespace."""
        result = parse_ports("22, 80 - 82 , 443")
        self.assertEqual(result, [22, 80, 81, 82, 443])

    def test_duplicate_ports(self):
        """Test that duplicate ports are handled correctly."""
        result = parse_ports("80,80,80")
        self.assertEqual(result, [80])

    def test_invalid_port_number(self):
        """Test that invalid port numbers raise ValueError."""
        with self.assertRaises(ValueError):
            parse_ports("99999")

    def test_invalid_port_zero(self):
        """Test that port 0 raises ValueError."""
        with self.assertRaises(ValueError):
            parse_ports("0")

    def test_invalid_range(self):
        """Test that invalid ranges raise ValueError."""
        with self.assertRaises(ValueError):
            parse_ports("100-50")

    def test_invalid_format(self):
        """Test that invalid format raises ValueError."""
        with self.assertRaises(ValueError):
            parse_ports("abc")


class TestServiceLookup(unittest.TestCase):
    """Test cases for service name lookup."""

    def test_known_service(self):
        """Test lookup of a known service."""
        self.assertEqual(get_service_name(80), "http")
        self.assertEqual(get_service_name(443), "https")
        self.assertEqual(get_service_name(22), "ssh")

    def test_unknown_service(self):
        """Test lookup of an unknown service."""
        self.assertIsNone(get_service_name(12345))


class TestScanSinglePort(unittest.TestCase):
    """Test cases for single port scanning."""

    @patch("socket.socket")
    def test_open_port(self, mock_socket_class):
        """Test scanning an open port."""
        # Mock socket to return success (0) on connect_ex
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 0
        mock_socket.__enter__ = MagicMock(return_value=mock_socket)
        mock_socket.__exit__ = MagicMock(return_value=False)
        mock_socket_class.return_value = mock_socket

        result = scan_single_port("localhost", 80, 0.5)

        self.assertEqual(result["port"], 80)
        self.assertEqual(result["status"], "open")
        self.assertEqual(result["service"], "http")

    @patch("socket.socket")
    def test_closed_port(self, mock_socket_class):
        """Test scanning a closed port."""
        # Mock socket to return failure on connect_ex
        mock_socket = MagicMock()
        mock_socket.connect_ex.return_value = 1
        mock_socket.__enter__ = MagicMock(return_value=mock_socket)
        mock_socket.__exit__ = MagicMock(return_value=False)
        mock_socket_class.return_value = mock_socket

        result = scan_single_port("localhost", 9999, 0.5)

        self.assertEqual(result["port"], 9999)
        self.assertEqual(result["status"], "closed")
        self.assertIsNone(result["service"])

    @patch("socket.socket")
    def test_timeout_port(self, mock_socket_class):
        """Test scanning a port that times out."""
        # Mock socket to raise timeout
        mock_socket = MagicMock()
        mock_socket.connect_ex.side_effect = socket.timeout
        mock_socket.__enter__ = MagicMock(return_value=mock_socket)
        mock_socket.__exit__ = MagicMock(return_value=False)
        mock_socket_class.return_value = mock_socket

        result = scan_single_port("localhost", 80, 0.1)

        self.assertEqual(result["port"], 80)
        self.assertEqual(result["status"], "closed")


class TestScanPorts(unittest.TestCase):
    """Test cases for multi-port scanning."""

    def test_invalid_host(self):
        """Test that scanning an invalid host raises socket.gaierror."""
        with self.assertRaises(socket.gaierror):
            scan_ports("this-host-does-not-exist-12345.invalid", [80], 0.5, 10)

    def test_empty_port_list(self):
        """Test scanning with an empty port list."""
        result = scan_ports("localhost", [], 0.5, 10)
        self.assertEqual(result, [])

    @patch("portscanpy.scanner.scan_single_port")
    @patch("socket.gethostbyname")
    def test_results_sorted_by_port(self, mock_gethostbyname, mock_scan_single):
        """Test that results are sorted by port number."""
        mock_gethostbyname.return_value = "127.0.0.1"

        # Mock scan results in random order
        def mock_scan(host, port, timeout):
            return {
                "port": port,
                "status": "closed",
                "service": None,
            }

        mock_scan_single.side_effect = mock_scan

        result = scan_ports("localhost", [443, 22, 80], 0.5, 10)

        # Results should be sorted by port
        self.assertEqual([r["port"] for r in result], [22, 80, 443])


if __name__ == "__main__":
    unittest.main()
