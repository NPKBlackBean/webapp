FROM ghcr.io/astral-sh/uv:alpine

COPY . /backend

WORKDIR /backend

RUN ["uv", "sync"]

EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "app/main.py"]