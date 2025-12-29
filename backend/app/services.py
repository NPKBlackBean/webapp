import roslibpy  # type: ignore[import-untyped]
from roslibpy import ServiceResponse
import logging

from utils import REQ_SENSOR_NUMBER_TO_NAME
from domain import SensorReading
from database import PostgresDatabase

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

ros_client = roslibpy.Ros(host='localhost', port=9090)
db = PostgresDatabase()

def get_sensor_reading() -> SensorReading:
    """
    Talk ROSBridge with the ROS sensor server to get current soil sensor reading.
    :return: a SensorReading containing all the data.
    :raise: TimeoutError when no readings are received from the server in >30 seconds.
    """

    if not ros_client.is_connected:
        ros_client.run()
    service = roslibpy.Service(ros_client, 'sensors_server', 'external/Sensors')

    request = roslibpy.ServiceRequest()

    readings: dict[str, float] = {}
    for sensor_number, reading_name in REQ_SENSOR_NUMBER_TO_NAME.items():
        logger.info(f"Calling sensor {sensor_number} for {reading_name}")

        request.sensor_number = sensor_number
        result = ServiceResponse(service.call(request))

        readings[reading_name] = float(result["sensor_reading"])

        logger.info(f"Reading is {result['sensor_reading']}")

    return SensorReading(
        EC=readings["EC"],
        pH=readings["pH"],
        N=readings["N"],
        P=readings["P"],
        K=readings["K"],
    )

def save_sensor_reading(plant_id: int, sensor_reading: SensorReading) -> None:
    try:
        db.save_reading(plant_id, sensor_reading)
    except RuntimeError as e:
        print(f"Error when saving to database: {e}")