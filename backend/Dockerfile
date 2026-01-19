FROM python:3.13-slim

# Install system dependencies for psycopg2 and other packages
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . /backend

WORKDIR /backend

# Install dependencies using pip (Debian has much better ARM wheel availability)
RUN pip install --upgrade pip && \
    pip install -e .

EXPOSE 8000
CMD ["python", "-m", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]