# import pycurl
# import io
#
#
# def measure_dns_resolve_time(url):
#     c = pycurl.Curl()
#     c.setopt(c.URL, url)
#     c.setopt(c.FOLLOWLOCATION, True)
#     c.setopt(c.CONNECTTIMEOUT, 10)
#     c.setopt(c.TIMEOUT, 15)
#
#     buffer = io.BytesIO()
#     c.setopt(c.WRITEDATA, buffer)
#
#     c.perform()
#
#     # Get DNS resolution time (in seconds)
#     dns_resolve_time = c.getinfo(pycurl.NAMELOOKUP_TIME) * 1000  # Convert to milliseconds
#
#     c.close()
#
#     print(f"DNS Resolve Time for {url}: {dns_resolve_time:.2f} ms")
#     return dns_resolve_time
#
#
# url = "https://www.python.org/"
# measure_dns_resolve_time(url)


import time
import socket
import urllib.request


def get_dns_resolution_time(hostname):
    try:
        # Start timer for DNS resolution
        dns_start = time.time()
        ip_address = socket.gethostbyname(hostname)
        dns_end = time.time()

        # Calculate DNS resolution time
        dns_time = (dns_end - dns_start) * 1000  # Convert to milliseconds
        print(f"DNS Resolution Time for {hostname}: {dns_time:.2f} ms")

        return dns_time
    except socket.gaierror as e:
        print(f"Error resolving DNS for {hostname}: {e}")
        return None


def fetch_page(hostname):
    url = f'https://{hostname}/'

    # Measure DNS resolution time
    dns_time = get_dns_resolution_time(hostname)

    # Start timer for the HTTP request after DNS resolution
    request_start = time.time()

    try:
        # Make a request to fetch the page
        with urllib.request.urlopen(url) as response:
            content = response.read()

        request_end = time.time()
        request_time = (request_end - request_start) * 1000  # Convert to milliseconds
        print(f"Total Request Time (excluding DNS): {request_time:.2f} ms")

        return content, dns_time, request_time
    except urllib.error.URLError as e:
        print(f"Error fetching page for {hostname}: {e}")
        return None, dns_time, None


# Example usage:
hostname = 'python.org'
content, dns_time, request_time = fetch_page(hostname)
