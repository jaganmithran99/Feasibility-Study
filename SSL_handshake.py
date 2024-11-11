import ssl
import socket
import time


def measure_ssl_handshake_time(hostname, port):
    context = ssl.create_default_context()

    start_time = time.time()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            handshake_time_ms = (time.time() - start_time) * 1000

    print(f"SSL Handshake Time: {handshake_time_ms:.2f} ms")


measure_ssl_handshake_time(hostname="smartops-qa04.eastus.cloudapp.azure.com", port=443)

