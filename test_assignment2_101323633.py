"""
Unit Tests for Assignment 2 — Port Scanner
"""

import unittest



from assignment2_101323633 import PortScanner, common_ports

class TestPortScanner(unittest.TestCase):

    def test_scanner_initialization(self):
        """Test that PortScanner initializes with correct target and empty results list."""
       # Create object
        scanner = PortScanner("127.0.0.1")
        
        # Check target value
        self.assertEqual(scanner.target, "127.0.0.1")
        
        # Check scan_results is empty list
        self.assertEqual(scanner.scan_results, [])

    def test_get_open_ports_filters_correctly(self):
        """Test that get_open_ports returns only Open ports."""

         # Create object
        scanner = PortScanner("127.0.0.1")
        
        # Add fake data
        scanner.scan_results = [
            (22, "Open", "SSH"),
            (23, "Closed", "Telnet"),
            (80, "Open", "HTTP")
        ]
        
        # Call function
        result = scanner.get_open_ports()
        
        # Expect only 2 open ports
        self.assertEqual(len(result), 2)

    def test_common_ports_dict(self):
        """Test that common_ports dictionary has correct entries."""

        # Check HTTP
        self.assertEqual(common_ports[80], "HTTP")
        
        # Check SSH
        self.assertEqual(common_ports[22], "SSH")

    def test_invalid_target(self):
        """Test that setter rejects empty string target."""
      
        # Create object
        scanner = PortScanner("127.0.0.1")
        
        # Try invalid value
        scanner.target = ""
        
        # Should NOT change
        self.assertEqual(scanner.target, "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
