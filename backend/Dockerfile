FROM ghcr.io/astral-sh/uv:alpine

COPY . /backend
WORKDIR /backend

COPY backend/pyproject.toml /backend/pyproject.toml
RUN ["uv", "sync"]

EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "app/main.py"]