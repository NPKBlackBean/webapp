import fastapi
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import asdict
import logging

from utils import get_ip_address
from services import get_sensor_reading, save_sensor_reading
from domain import SensorReading

app = fastapi.FastAPI()
logger = logging.getLogger(__name__)

# TODO: switch to allow_origin_regex
origins = [
    "*"
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
async def sensor_reading() -> dict[str, float]:
    _sensor_reading: SensorReading = get_sensor_reading()
    return _sensor_reading.model_dump()

@app.post("/accepted_readings")
async def accepted_readings(readings: dict[str, list[SensorReading]]) -> None:
    for i, reading in enumerate(readings["readings"]):
        save_sensor_reading(plant_id=(i + 1), sensor_reading=reading)