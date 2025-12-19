import fastapi
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import asdict
import logging

from utils import get_ip_address
from services import get_sensor_reading
from domain import SensorReading

app = fastapi.FastAPI()
logger = logging.getLogger(__name__)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.get("/backend_ip")
async def backend_ip() -> dict[str, str]:
    backend_ip_address = get_ip_address()
    return {"ip_address": backend_ip_address}

@app.get("/sensor_reading")
async def sensor_reading() -> dict[str, str]:
    sensor_reading: SensorReading = get_sensor_reading()
    return asdict(sensor_reading)