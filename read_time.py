import http.client
import ssl
import time
from urllib.parse import urlparse


def calculate_pure_read_time(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    path = parsed_url.path if parsed_url.path else '/'
    port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)

    context = ssl.create_default_context() if parsed_url.scheme == 'https' else None

    if parsed_url.scheme == 'https':
        conn = http.client.HTTPSConnection(hostname, port, context=context)
    else:
        conn = http.client.HTTPConnection(hostname, port)

    conn.request("GET", path)

    # Receive the response headers (this is where SSL handshake and initial response time happen)
    response = conn.getresponse()

    # Read the entire response body
    read_start = time.time()
    data = response.read()  # This will only time the reading of the body, not the headers or SSL handshake
    read_end = time.time()

    conn.close()

    read_time_ms = (read_end - read_start) * 1000
    content_size_kb = len(data) / 1024

    print(f"Read time for {url}: {read_time_ms:.2f} ms")
    print(f"Downloaded {content_size_kb:.2f} KB")
    return read_time_ms


url = "https://www.python.org/"
read_time = calculate_pure_read_time(url)
