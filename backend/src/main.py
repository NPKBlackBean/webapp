from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}

@app.get("/begin_reading")
async def begin_reading() -> dict[str, str]:
    return {"message": "This endpoint should return sensor data for all pots"}