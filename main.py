# main.py - Entry point for running the Python Port Scanner

from port_scanner import scan_port, parse_ports  # Import necessary functions from port_scanner.py
from concurrent.futures import ThreadPoolExecutor, as_completed

# Lists to store scan results
open_ports = []  # Stores open ports along with their detected service names
closed_ports = []  # Stores closed/filtered ports along with their detected service names


def main():
    # Ask user for the target host (IP or domain)
    target = input("Enter target (IP or domain): ")

    # Ask user for ports to scan (single ports or port ranges)
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