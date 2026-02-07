FROM python:3.11-slim-bookworm

RUN useradd -m asmuser

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER asmuser

EXPOSE 5000

CMD ["python", "main.py"]

