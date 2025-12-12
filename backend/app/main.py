from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils import get_ip_address

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

@app.get("/begin_reading")
async def begin_reading() -> dict[str, str]:
    return {"message": "This endpoint should return sensor data for all pots"}