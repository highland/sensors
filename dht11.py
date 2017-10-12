"""
A module to facilitate taking measurements using the DHT11 Temperature and Humidity Sensor
using the Raspberry Pi

10/10/2017
"""
from dht import DHT
import RPIO as GPIO


class DHT11(DHT):
    """
    Represents a DHT11 temperature/humidity sensor
    connected to a specified GPIO pin
    """

    def __init__(self, pin=4, mode=GPIO.BCM):
        super().__init__(pin, mode)

    @staticmethod
    def _decode_message(message_bytes):
        humidity, _, temperature, _, check_sum = message_bytes
        if (humidity + temperature) % 256 == check_sum:  # confirmed
            return float(humidity), float(temperature)
        else:
            return 0.0, 0.0


if __name__ == '__main__':
    sensor = DHT11()
    print(sensor.take_measurement())
