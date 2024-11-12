import pycurl
import io


def measure_connect_time(url):
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.FOLLOWLOCATION, True)
    c.setopt(c.CONNECTTIMEOUT, 10)
    c.setopt(c.TIMEOUT, 15)

    buffer = io.BytesIO()
    c.setopt(c.WRITEDATA, buffer)

    # Execute the request
    c.perform()

    # Get connection time (in seconds)
    connect_time = c.getinfo(pycurl.CONNECT_TIME) * 1000  # Convert to milliseconds

    c.close()

    print(f"Connect Time for {url}: {connect_time:.2f} ms")
    return connect_time


url = "https://www.python.org/"
measure_connect_time(url)


# import time
# import socket
# import urllib.request
#
# def get_connection_time(url):
#     # Parse the URL to get the hostname and port
#     parsed_url = urllib.parse.urlparse(url)
#     hostname = parsed_url.hostname
#     port = parsed_url.port if parsed_url.port else 443  # Default to HTTPS port 443
#
#     # Start the connection time measurement
#     start_time = time.time()
#
#     # Create a socket connection to the server
#     with socket.create_connection((hostname, port)) as sock:
#         # This just ensures the connection is established
#         sock.sendall(b"GET / HTTP/1.1\r\nHost: " + hostname.encode() + b"\r\n\r\n")
#         sock.recv(1)  # Receiving at least one byte to establish the connection is active
#
#     # Calculate the connection time in milliseconds
#     connection_time = (time.time() - start_time) * 1000  # Convert to milliseconds
#     print(f"Connection time for {url}: {connection_time:.2f} ms")
#     return connection_time
#
# # Example usage
# url = "https://www.python.org/"
# connection_time = get_connection_time(url)
