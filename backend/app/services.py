import roslibpy  # type: ignore[import-untyped]
from roslibpy import ServiceResponse
import logging

logger = logging.getLogger(__name__)

client = roslibpy.Ros(host='localhost', port=9090)

REQ_SENSOR_NUMBER_TO_NAME = {
    6: "EC",
    7: "pH",
    8: "N",
    9: "P",
    10: "K",
}

def get_sensor_readings():
    """
    Talk ROSBridge with the ROS sensor server to get soil sensor readings.
    :return: a dict of SensorReadings with "control", "treatment" keys.
    :raise: TimeoutError when no readings are received from the server in >30 seconds.
    """

    client.run()
    service = roslibpy.Service(client, 'sensors_server', 'external/Sensors')

    request = roslibpy.ServiceRequest()

    readings: dict[str, str] = {}
    for sensor_number, reading_name in REQ_SENSOR_NUMBER_TO_NAME.items():
        logging.info(f"Calling sensor {sensor_number} for {reading_name}")

        request.sensor_number = sensor_number
        result = ServiceResponse(service.call(request))

        readings[reading_name] = result["sensor_reading"]

        logging.info(f"Reading is {result['sensor_reading']}")

    client.terminate()

    #TODO: remove after integration with ROS backend
    # with respect to SensorReading dataclass
    print(readings)
    print(type(readings))
    # {'EC': '544', 'pH': '527', 'N': '524', 'P': '534', 'K': '515'}
    # <class 'dict'>

    return readings