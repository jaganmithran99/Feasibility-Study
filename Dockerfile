# Use an official Ubuntu base image
FROM ubuntu:20.04

# Set environment variable to suppress interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary dependencies, tools, and Python 3.10
RUN apt-get update && \
    apt-get install -y software-properties-common wget gnupg unzip xvfb dbus && \
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

# Install dbus to avoid the bus error (optional)
RUN apt-get install -y dbus-x11


# Install Google Chrome
#RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list' && \
#    apt-get update && \
#    apt-get install -y google-chrome-stable

# Install ChromeDriver to match the installed Chrome version
#RUN CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+') && \
#    wget -q -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip" && \
#    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
#    rm /tmp/chromedriver.zip

#RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

# Add Chrome to PATH and set necessary flags for running in Docker
ENV PATH="/usr/local/bin:$PATH"
ENV CHROME_BIN="/usr/bin/google-chrome"
ENV CHROME_OPTIONS="--no-sandbox --disable-dev-shm-usage --headless"

# Verify installations
#RUN python3.10 --version && google-chrome --version && chromedriver --version

# Optional: Install Selenium or other packages
RUN pip install selenium

# Set default command (you can change this based on your needs)
#CMD ["python3.10"]

# Ensure Chrome runs without sandbox
#ENTRYPOINT ["google-chrome", "--no-sandbox", "--disable-gpu", "--disable-extensions"]
ENTRYPOINT ["xvfb-run", "--auto-servernum", "--server-args='-screen 0 1920x1080x24'", "google-chrome", "--no-sandbox", "--disable-gpu", "--headless"]

#CMD ["sleep","3600"]