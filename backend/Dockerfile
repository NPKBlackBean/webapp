FROM python:3.13-alpine

# Install uv
RUN pip install uv

COPY . /backend

WORKDIR /backend

RUN ["uv", "sync"]

EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "app/main.py"]