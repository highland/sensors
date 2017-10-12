"""
A module to facilitate taking measurements using the DHT22 Temperature and Humidity Sensor
using the Raspberry Pi

12/10/2017
"""
from dht import DHT
import RPIO as GPIO


class DHT22(DHT):
    """
    Represents a DHT22 temperature/humidity sensor
    connected to a specified GPIO pin
    """

    def __init__(self, pin=4, mode=GPIO.BCM):
        super().__init__(pin, mode)

    @staticmethod
    def _decode_message(message_bytes):
        humidity_high, humidity_low, temperature_high, temperature_low, check_sum = message_bytes
        if (humidity_high + humidity_low + temperature_high + temperature_low) % 256 == check_sum:  # confirmed
            humidity = ((humidity_high << 8) + humidity_low) / 10
            temperature = ((temperature_high << 8) + temperature_low) / 10
            return humidity, temperature
        else:
            return 0.0, 0.0


if __name__ == '__main__':
    sensor = DHT22()
    print(sensor.take_measurement())
