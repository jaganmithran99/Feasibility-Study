# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set environment variable to suppress interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies, tools, and Python 3.10
RUN apt-get update && \
    apt-get install -y software-properties-common wget gnupg && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-distutils && \
    apt-get install -y curl unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.10
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.10 get-pip.py && \
    rm get-pip.py

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable

# Install ChromeDriver to match the installed Chrome version
RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
    wget -q -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Add Chrome to PATH and set necessary flags for running in Docker
ENV PATH="/usr/local/bin:$PATH"
ENV CHROME_BIN="/usr/bin/google-chrome"
ENV CHROME_OPTIONS="--no-sandbox --disable-dev-shm-usage --headless"

# Verify installations
RUN python3.10 --version && google-chrome --version && chromedriver --version

# Optional: Install Selenium or other packages
RUN pip install selenium

# Set default command (you can change this based on your needs)
CMD ["python3.10"]
