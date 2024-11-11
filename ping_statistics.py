import subprocess
import sys
import re


def ping_statistics(hostname, count=4):
    try:
        command = ["ping", "-c", str(count), hostname] if sys.platform != "win32" else ["ping", "-n", str(count),
                                                                                        hostname]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Ping check failed. Error: {result.stderr.strip()}")
            return

        output = result.stdout
        sent, received, lost = None, None, None

        # Extract RTT statistics and packet counts based on the OS
        if sys.platform == "win32":
            # Windows packet statistics pattern
            packet_match = re.search(r"Packets: Sent = (\d+), Received = (\d+), Lost = (\d+)", output)
            rtt_match = re.search(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms", output)
            if packet_match:
                sent, received, lost = map(int, packet_match.groups())
            if rtt_match:
                min_rtt, max_rtt, avg_rtt = map(int, rtt_match.groups())

        else:
            # Linux/macOS packet statistics pattern
            packet_match = re.search(r"(\d+) packets transmitted, (\d+) received, (\d+)% packet loss", output)
            rtt_match = re.search(r"min/avg/max/mdev = ([\d.]+)/([\d.]+)/([\d.]+)/[\d.]+ ms", output)
            if packet_match:
                sent, received = map(int, packet_match.groups()[:2])
                lost = sent - received
            if rtt_match:
                min_rtt, avg_rtt, max_rtt = map(float, rtt_match.groups())

        print(f"Ping Packet Statistics for {hostname}:")
        print(f"Packets Sent: {sent}")
        print(f"Packets Received: {received}")
        print(f"Packets Lost: {lost}")

        if 'min_rtt' in locals():
            print(f"\nRTT Statistics:")
            print(f"Minimum RTT: {min_rtt} ms")
            print(f"Maximum RTT: {max_rtt} ms")
            print(f"Average RTT: {avg_rtt} ms")

    except Exception as e:
        print(f"An error occurred: {e}")


# Usage example
if __name__ == "__main__":
    hostname = "smartops-qa04.eastus.cloudapp.azure.com"
    ping_statistics(hostname)
