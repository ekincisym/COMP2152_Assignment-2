"""
Author: Seyma Sibel Ekinci
Assignment: #2
Description: Port Scanner — A tool that scans a target machine for open network ports
"""


# socket, threading, sqlite3, os, platform, datetime
import socket
import threading
import sqlite3
import os
import platform
import datetime


# Print Python version and OS name (Step iii)


print("Python Version:", platform.python_version())
print("Operating System:", os.name)

# the common_ports dictionary (Step iv)

common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}

# the NetworkTool parent class (Step v)




class NetworkTool:
    def __init__(self, target):
        self.__target = target
        
# Q3: What is the benefit of using @property and @target.setter?
    # Using @property and setter allows controlled access to the variable.
    # It prevents direct modification and allows validation.
    # This helps protect the data and improve code structure.

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        if value == "":
            print("Error: Target cannot be empty")
        else:
            self.__target = value

    def __del__(self):
        print("NetworkTool instance destroyed")

# Q1: How does PortScanner reuse code from NetworkTool?
# PortScanner reuses code from NetworkTool by inheriting from it.
# For example, it uses the target property from the parent class instead of creating it again.
# This reduces repeated code and makes the program easier to organize and maintain.
class PortScanner(NetworkTool):
    def __init__(self, target):
        super().__init__(target)
        self.scan_results = []
        self.lock = threading.Lock()

    def __del__(self):
        print("PortScanner instance destroyed")
        super().__del__()

    def scan_port(self, port):
        sock = None

        # Q4: What would happen without try-except here?
        # Without try-except, the program could stop if a socket error happens while scanning.
        # For example, if the machine is unreachable, the method may raise an error and crash the scanner.
        # Using try-except lets the program handle the error and continue scanning other ports.
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))

            if result == 0:
                status = "Open"
            else:
                status = "Closed"

            service_name = common_ports.get(port, "Unknown")

            self.lock.acquire()
            self.scan_results.append((port, status, service_name))
            self.lock.release()

        except socket.error as e:
            print(f"Error scanning port {port}: {e}")

        finally:
            if sock:
                sock.close()

    def get_open_ports(self):
        return [result for result in self.scan_results if result[1] == "Open"]

    # Q2: Why do we use threading instead of scanning one port at a time?
    # We use threading so multiple ports can be scanned at the same time.
    # If 1024 ports were scanned one by one, the program would be much slower because each scan waits for a response or timeout.
    # Threading makes the scanner faster and more efficient.
    def scan_range(self, start_port, end_port):
        threads = []

        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()







def save_results(target, results):
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            port INTEGER,
            status TEXT,
            service TEXT,
            scan_date TEXT
        )
        """)

        for port, status, service in results:
            cursor.execute("""
            INSERT INTO scans (target, port, status, service, scan_date)
            VALUES (?, ?, ?, ?, ?)
            """, (target, port, status, service, str(datetime.datetime.now())))

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        print(f"Database error: {e}")


def load_past_scans():
    conn = None
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scans")
        rows = cursor.fetchall()

        for row in rows:
            print(f"[{row[5]}] {row[1]} : Port {row[2]} ({row[4]}) - {row[3]}")

    except sqlite3.Error:
        print("No past scans found.")

    finally:
        if conn:
            conn.close()


# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
    try:
        target = input("Enter target IP address (default 127.0.0.1): ").strip()
        if target == "":
            target = "127.0.0.1"

        start_port = int(input("Enter start port (1-1024): "))
        end_port = int(input("Enter end port (1-1024): "))

        if start_port < 1 or start_port > 1024 or end_port < 1 or end_port > 1024:
            print("Port must be between 1 and 1024.")
        elif end_port < start_port:
            print("End port must be greater than or equal to start port.")
        else:
            scanner = PortScanner(target)
            print(f"Scanning {target} from port {start_port} to {end_port}...")
            scanner.scan_range(start_port, end_port)

            open_ports = scanner.get_open_ports()

            print(f"--- Scan Results for {target} ---")
            for port, status, service in open_ports:
                print(f"Port {port}: {status} ({service})")

            print("------")
            print(f"Total open ports found: {len(open_ports)}")

            save_results(target, scanner.scan_results)

            history_choice = input("Would you like to see past scan history? (yes/no): ").strip().lower()
            if history_choice == "yes":
                load_past_scans()

    except ValueError:
        print("Invalid input. Please enter a valid integer.")
   

   


# Q5: New Feature Proposal
# One new feature I would add is a filter option to show only open ports for a selected service type.
# This could use a list comprehension to return only ports that match a service name like HTTP or SSH.
# It would make the scanner easier to use when the user wants specific results only.
# Diagram: See diagram_101323633.png in the repository root