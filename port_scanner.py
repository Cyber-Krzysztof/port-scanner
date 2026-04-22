import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

# Lists to store scan results
open_ports = []     # Stores open ports along with their detected service names
closed_ports = []   # Stores closed/filtered ports along with their detected service names

# ----------------------------
# Function to get the service name for a port
# e.g., 22 -> ssh, 80 -> http
# If the port is non-standard, returns "Unknown"
# ----------------------------
def get_service_name(port):
    try:
        return socket.getservbyport(port)
    except:
        return "Unknown"

# ----------------------------
# Function to scan a single port
# Attempts to connect to the target host on the specified port
# Records whether it is OPEN or CLOSED/FILTERED
# ----------------------------
def scan_port(target, port):
    try:
        # Create a TCP socket (IPv4)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout in seconds to prevent hanging on unresponsive ports
        sock.settimeout(5)
        # Attempt connection; returns 0 if connection succeeds (port is open)
        result = sock.connect_ex((target, port))
        # Close the socket after use
        sock.close()

        # Get human-readable service name
        service = get_service_name(port)

        # Check result and return the status
        if result == 0:
            return port, service, "OPEN"
        else:
            return port, service, "CLOSED/FILTERED"

    except Exception as e:
        # Catch unexpected errors and return the port as closed/unknown
        return port, "Unknown", "CLOSED/FILTERED"

# ----------------------------
# Function to parse user input for ports
# Allows user to input multiple ports separated by commas or port ranges (e.g. 22,80,443,500-600)
# ----------------------------
def parse_ports(port_input):
    ports = []
    for part in port_input.split(","):
        part = part.strip()  # Remove whitespace
        if "-" in part:  # Handle ranges (e.g., 500-600)
            try:
                start_port, end_port = part.split("-")
                start_port, end_port = int(start_port), int(end_port)
                if start_port > end_port:
                    print(f"Invalid range skipped: {part}")
                else:
                    ports.extend(range(start_port, end_port + 1))  # Add all ports in the range
            except ValueError:
                print(f"Invalid range skipped: {part}")
        elif part.isdigit():  # Handle individual ports
            ports.append(int(part))
        else:
            print(f"Invalid port skipped: {part}")
    return sorted(ports)  # Sort the ports in ascending order

# ----------------------------
# Main function that runs the scanner
# ----------------------------
def main():
    # Ask user for the target host (IP or domain)
    target = input("Enter target (IP or domain): ")
    # Ask user for ports to scan
    port_input = input("Enter port(s) (e.g. 22,80,443 or 500-600): ")
    # Parse the input into a list of integers
    ports = parse_ports(port_input)

    # Exit if no valid ports were entered
    if not ports:
        print("No valid ports provided. Exiting.")
        return

    print(f"\nScanning {target} on ports: {ports}\n")

    # ----------------------------
    # Use ThreadPoolExecutor to scan multiple ports in parallel
    # This makes scanning faster compared to scanning ports sequentially
    # ----------------------------
    with ThreadPoolExecutor(max_workers=50) as executor:
        # Start scanning for each port and collect results
        futures = {executor.submit(scan_port, target, port): port for port in ports}

        # Dictionary to store results indexed by port
        results = {}

        # Wait for all threads to complete and store the results in the dictionary
        for future in as_completed(futures):
            port, service, status = future.result()
            results[port] = (service, status)  # Store the result by port number

    # ----------------------------
    # Print results in the correct order
    # ----------------------------
    print("\nScan Results:")
    for port in ports:
        service, status = results.get(port, ("Unknown", "CLOSED/FILTERED"))
        print(f"Port {port} ({service}) {status}")

    # ----------------------------
    # Ask user if they want to save the results
    # If yes, ask for a filename and save both open and closed ports
    # ----------------------------
    save_option = input("\nDo you want to save results? (y/n): ").lower()
    if save_option in ["y", "yes"]:
        filename = input("Enter filename (default: results.txt): ").strip()
        if filename == "":
            filename = "results.txt"
        # Ensure the file has a .txt extension
        if not filename.endswith(".txt"):
            filename += ".txt"

        # Write results to file
        with open(filename, "w") as f:
            for port in ports:
                service, status = results.get(port, ("Unknown", "CLOSED/FILTERED"))
                f.write(f"Port {port} ({service}) {status}\n")

        print(f"Results saved to {filename}")
    else:
        print("Results not saved.")

    print("\nScan complete.")

# ----------------------------
# Entry point: ensures main() runs only when script is executed directly
# ----------------------------
if __name__ == "__main__":
    main()