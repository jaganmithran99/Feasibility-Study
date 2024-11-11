import requests
import time


def calculate_download_time(url):
    start_time = time.time()

    # Send an HTTP request to the URL and get the response
    response = requests.get(url)

    end_time = time.time()

    total_time = (end_time - start_time) * 1000

    content_size = len(response.content)

    print(f"Downloaded {content_size / 1024:.2f} KB in {total_time:.2f} ms")
    return total_time


url = "https://www.python.org/"
download_time = calculate_download_time(url)
