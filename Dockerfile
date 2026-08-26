FROM python:3.11-slim

# Set working directory di dalam kontainer
WORKDIR /app

# Install dependensi sistem jika diperlukan (misal: poppler-utils)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dan install dependensi Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh kode aplikasi ke dalam kontainer
COPY app/ ./app/

# Port yang dibuka oleh aplikasi FastAPI
EXPOSE 8000

# Perintah untuk menjalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]