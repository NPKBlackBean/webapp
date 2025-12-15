import fastapi
from fastapi.middleware.cors import CORSMiddleware
import logging

from utils import get_ip_address
from services import get_sensor_readings

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

@app.get("/sensor_readings")
async def sensor_readings() -> dict[str, str]:
    # TODO:
    # Replace this placeholder (which is to create a mental image of what we want)
    # with objects created from data received from sensor.
    # {
    #     "controls": {
    #         0: {
    #             "pH": 7,
    #             "temp": 20,
    #             "humidity": 80,
    #             "N": 10,
    #             "P": 7,
    #             "K": 6,
    #         }
    #     },
    #     "treatments": {
    #         0: {
    #             "pH": 7,
    #             "temp": 20,
    #             "humidity": 80,
    #             "N": 10,
    #             "P": 7,
    #             "K": 6,
    #         },
    #         1: {
    #             "pH": 7,
    #             "temp": 20,
    #             "humidity": 80,
    #             "N": 10,
    #             "P": 7,
    #             "K": 6,
    #         }
    #     }
    # }

    received_sensor_readings = get_sensor_readings()
    return received_sensor_readings