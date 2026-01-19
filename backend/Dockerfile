FROM python:3.13-alpine

# Install system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev

COPY . /backend

WORKDIR /backend

# Install dependencies using pip (better wheel availability for ARM)
RUN pip install --upgrade pip && \
    pip install -e .

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]