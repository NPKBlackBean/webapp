from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import get_ip_address
from services import get_sensor_readings

app = FastAPI()

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
async def sensor_readings() -> dict[str, dict]:
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