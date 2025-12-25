from dataclasses import dataclass
from pydantic import BaseModel

class SensorReading(BaseModel):
    """Class for storing sensor reading data."""
    EC: float
    pH: float
    N: float
    P: float
    K: float
