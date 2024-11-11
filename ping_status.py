import subprocess
import sys


def ping_check(hostname):
    try:
        # Run the ping command
        command = ["ping", "-c", "1", hostname] if sys.platform != "win32" else ["ping", "-n", "1", hostname]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return "Status: Okay"
        elif "Name or service not known" in result.stderr or "cannot resolve" in result.stderr:
            return "Status: DNS failure"
        else:
            return f"Status: Failure ({result.stderr.strip()})"

    except Exception as e:
        return f"Status: Error ({str(e)})"


# Usage example
if __name__ == "__main__":
    hostname = "smartops-qa04.eastus.cloudapp.azure.com"
    print(ping_check(hostname))
