FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Utilisez main_simple.py pour tester rapidement la connexion
CMD ["python", "main_simple.py"]
