from dataclasses import dataclass

@dataclass
class SensorReading:
    """Class for storing sensor reading data."""
    EC: float
    pH: float
    N: float
    P: float
    K: float
