"""
A module containing the abstract superclass for DHTxx Temperature and Humidity Sensors
using the Raspberry Pi

12/10/2017
"""
import RPIO as GPIO
import time
from abc import ABCMeta, abstractmethod
from dht_typing import Message, Data

class DHT(metaclass=ABCMeta):
    """
    Represents a DHT22 temperature/humidity sensor
    connected to a specified GPIO pin
    """

    def __init__(self, pin: int = 4, mode=GPIO.BCM) -> None:
        self._pin = pin
        GPIO.setmode(mode)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
        time.sleep(0.025)

    def take_measurement(self, retries: 'int > 0' = 5) -> Data:
        """
        Takes a measurement from the sensor.
        Repeat if unsuccessful <retries> times.
        This is a Template Method which reads the message
        from the device, and then delegates to
        subclasses which must provide specific
        behaviour for the _decode_message() method.

        Returns:
            Relative Humidity: float,
            Temperature in Centigrade: float

            if the reading was unsuccessful, zeroes are returned
        """
        if retries < 1:
            retries = 1
        result = (0.0, 0.0)  # initial value
        first_time = True
        while retries > 0 and result == (0.0, 0.0):
            if not first_time:
                time.sleep(1)  # min re-sample time
            GPIO.output(self._pin, GPIO.LOW)  # send start signal
            time.sleep(0.02)  # min 0.018 specified

            GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Change to Input & pull up

            message_bytes = [0] * 5  # accumulator for the individual bits of the 5 bytes of the message

            # skip the high bits to look for start of data
            while GPIO.input(self._pin) == 1:
                pass

            for i in range(40):  # each measurement message is 40 bits (5 x 8 bytes)
                byte_number = i // 8

                # count the low samples (0's and 1's both start low)
                low_sample_count = 1  # used for timing 0's vs 1's. The low of each bit is 50 µs.
                while GPIO.input(self._pin) == 0:
                    low_sample_count += 1

                # count the high samples
                high_sample_count = 1  # starting at 1 as the first high reading terminated the low loop
                while GPIO.input(self._pin) == 1:
                    high_sample_count += 1

                # here's the timing test: 0's are 26-28 µs high, 1's are 70 µs high
                #                         the low_sample_count corresponds to 50 µs
                bit = 1 if high_sample_count > low_sample_count else 0
                message_bytes[byte_number] = (message_bytes[byte_number] << 1) + bit
            # finished reading all 40 bits of the message

            result = self._decode_message(message_bytes)
            retries -= 1
            first_time = False
        return result

    @staticmethod
    @abstractmethod
    def _decode_message(message_bytes: Message) -> Data:
        pass
