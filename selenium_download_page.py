from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")


def measure_spa_load_time(url):
    driver = webdriver.Chrome()

    start_time = time.time()

    try:
        # Load the page
        driver.get(url)

        # Wait for the page to fully load (this may need adjustment based on the site)
        driver.implicitly_wait(10)

        load_time = time.time() - start_time
        print(f"Total page load time for {url}: {load_time * 1000:.2f} ms")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser
        driver.quit()


if __name__ == "__main__":
    url = "https://www.python.org/"
    measure_spa_load_time(url)
