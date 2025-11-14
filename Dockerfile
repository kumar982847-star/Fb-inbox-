# Example Dockerfile for Render + Selenium + Chrome
FROM python:3.11

# Install Chrome
RUN apt-get update && apt-get install -y wget gnupg2 \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y

# Install ChromeDriver
RUN apt-get install -y unzip \
  && wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/119.0.6045.105/chromedriver_linux64.zip \
  && unzip /tmp/chromedriver.zip -d /usr/bin

# Set ChromeDriver path
ENV PATH="/usr/bin:${PATH}"

# Install Python dependecies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
CMD ["streamlit", "run", "app.py", "--server.port=10000"]
