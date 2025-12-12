import roslibpy

client = roslibpy.Ros(host='localhost', port=9090)

# plantroid repo
# class SensorReader(Node):
#     def __init__(self, node_name):
#         super().__init__(node_name)
#         self.cli = self.create_client(Sensors, 'sensors_server')
#         while not self.cli.wait_for_service(timeout_sec=5.0):
#             self.get_logger().info('Sensor service not available, waiting again...')
#         self.req = Sensors.Request()
#         self.future = None
#
#     def send_request(self, num):
#         self.req.sensor_number = num
#         self.future = self.cli.call_async(self.req)

def get_sensor_readings():
    """
    Talk ROSBridge with the ROS sensor server to get soil sensor readings.
    :return: a dict of SensorReadings with "control", "treatment" keys.
    :raise: TimeoutError when no readings are received from the server in >30 seconds.
    """

    client.run()
    service = roslibpy.Service(client, 'sensors_server', 'rooted_msgs/srv/Sensors')

    # TODO: send request with sensor ID, like in Plantroid repo
    request = roslibpy.ServiceRequest()

    print('Calling service...')
    result = service.call(request)
    print('Service response: {}'.format(result['loggers']))

    client.terminate()