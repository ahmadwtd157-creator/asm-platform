FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt



RUN apt-get update \
    && apt-get install -y --no-install-recommends wget unzip ca-certificates \
    && apt-get install -y golang \
    && apt-get install -y nmap \
    \
    && wget https://github.com/projectdiscovery/subfinder/releases/download/v2.12.0/subfinder_2.12.0_linux_amd64.zip \
    && unzip -o subfinder_2.12.0_linux_amd64.zip \
    && mv subfinder /usr/local/bin/ \
    && chmod +x /usr/local/bin/subfinder \
    \
    && wget https://github.com/projectdiscovery/dnsx/releases/download/v1.2.3/dnsx_1.2.3_linux_amd64.zip \
    && unzip -o dnsx_1.2.3_linux_amd64.zip \
    && mv dnsx /usr/local/bin/ \
    && chmod +x /usr/local/bin/dnsx

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]