# import pycurl
# import io
#
#
# def get_detailed_timings(url):
#     curl = pycurl.Curl()
#     curl.setopt(curl.URL, url)
#     curl.setopt(curl.FOLLOWLOCATION, True)
#
#     buffer = io.BytesIO()
#     curl.setopt(curl.WRITEDATA, buffer)
#
#     curl.perform()
#
#     # Retrieve timing details in milliseconds
#     dns_time = curl.getinfo(pycurl.NAMELOOKUP_TIME) * 1000
#     connect_time = curl.getinfo(pycurl.CONNECT_TIME) * 1000
#     ssl_time = curl.getinfo(pycurl.APPCONNECT_TIME) * 1000  # SSL/TLS handshake time
#     start_transfer_time = curl.getinfo(pycurl.STARTTRANSFER_TIME) * 1000  # TTFB
#     total_time = curl.getinfo(pycurl.TOTAL_TIME) * 1000  # Total request time
#
#     curl.close()
#
#     print(f"DNS Resolution Time: {dns_time:.2f} ms")
#     print(f"TCP Connection Time: {connect_time - dns_time:.2f} ms")
#     print(f"SSL Handshake Time: {ssl_time - connect_time:.2f} ms")
#     print(f"TTFB (Time to First Byte): {start_transfer_time:.2f} ms")
#     print(f"Total Download Time: {total_time:.2f} ms")
#
#     return {
#         "dns_time": dns_time,
#         "connect_time": connect_time - dns_time,
#         "ssl_time": ssl_time - connect_time,
#         "ttfb": start_transfer_time,
#         "total_time": total_time
#     }
#
#
# url = "https://www.python.org/"
# timings = get_detailed_timings(url)


import time
import urllib.request


def get_ttfb(url):
    try:
        # Start timing before the request
        start_time = time.time()

        # Open the URL but do not read the response body
        with urllib.request.urlopen(url) as response:
            # TTFB is the time from the start to when headers are received
            ttfb = (time.time() - start_time) * 1000  # Convert to milliseconds

        print(f"TTFB for {url}: {ttfb:.2f} ms")
        return ttfb
    except urllib.error.URLError as e:
        print(f"Error accessing {url}: {e}")
        return None


# Example usage
url = "https://www.python.org/"
ttfb = get_ttfb(url)
