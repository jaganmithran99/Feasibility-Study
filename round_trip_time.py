import subprocess
import sys
import re


def ping_rtt_statistics(hostname, count=4):
    try:
        # Define the ping command based on the operating system
        command = ["ping", "-c", str(count), hostname] if sys.platform != "win32" else ["ping", "-n", str(count),
                                                                                        hostname]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Ping check failed. Error: {result.stderr.strip()}")
            return

        # Extract RTT statistics from the output
        output = result.stdout
        if sys.platform == "win32":
            # Windows ping statistics pattern
            match = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", output)
            if match:
                min_rtt, max_rtt, avg_rtt = map(int, match.groups())
        else:
            # Linux/macOS ping statistics pattern
            match = re.search(r"min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/[\d.]+ ms", output)
            if match:
                min_rtt, avg_rtt, max_rtt = map(float, match.groups())

        # Print RTT statistics
        print(f"Ping RTT Statistics for {hostname}:")
        print(f"Minimum RTT: {min_rtt} ms")
        print(f"Maximum RTT: {max_rtt} ms")
        print(f"Average RTT: {avg_rtt} ms")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    hostname = "smartops-qa04.eastus.cloudapp.azure.com"
    ping_rtt_statistics(hostname)
