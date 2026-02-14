FROM python:3.11-slim-bookworm

RUN useradd -m asmuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER root

EXPOSE 5000

CMD ["python", "main.py"]

RUN apt update && apt install -y wget unzip
RUN wget https://github.com/projectdiscovery/subfinder/releases/download/v2.12.0/subfinder_2.12.0_linux_amd64.zip \
    && unzip subfinder_2.12.0_linux_amd64.zip \
    && mv subfinder /usr/local/bin/ \
    && chmod +x /usr/local/bin/subfinder