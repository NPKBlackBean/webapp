FROM python:3.12-alpine

# Install uv
RUN pip install uv

COPY ./external/.env /database/docker/.env
COPY . /backend

WORKDIR /backend

RUN ["uv", "sync"]

EXPOSE 8000
CMD ["uv", "run", "fastapi", "run", "app/main.py"]