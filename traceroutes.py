import subprocess
import sys


def traceroute(destination):
    try:
        # Determine the command based on the OS
        command = ["tracert", destination] if sys.platform == "win32" else ["traceroute", destination]
        print(command)

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate()

        if process.returncode != 0:
            print("Error running traceroute:")
            print(error)
            return

        print(f"Traceroute to {destination}:\n")
        print(output)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    destination = "smartops-di05.ustdev.com"
    traceroute(destination)
