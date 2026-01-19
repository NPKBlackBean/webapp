FROM python:3.13-alpine

# Install system dependencies for building Rust packages on ARM
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    cargo \
    rust

# Install uv
RUN pip install uv

COPY . /backend

WORKDIR /backend

RUN ["uv", "sync"]

EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "app/main.py"]