"""
A module to facilitate taking measurements using the DHT11 Temperature and Humidity Sensor
using the Raspberry Pi

10/10/2017
"""
import RPi.GPIO as GPIO
import time


class DHT11:
    """
    Represents a DHT11 temperature/humidity sensor
    connected to a specified GPIO pin
    """
    def __init__(self, pin=4, mode=GPIO.BCM):
        self._pin = pin
        GPIO.setmode(mode)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
        time.sleep(0.025)

    def take_measurement(self):
        """
        Takes a measurement from the sensor.

        Returns:
            Relative Humidity: float,
            Temperature in Centigrade: float

            if the reading was unsuccessful, zeroes are reurened
        """

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
            high_sample_count = 1
            while GPIO.input(self._pin) == 1:
                high_sample_count += 1

            # here's the timing test: 0's are 26-28 µs high, 1's are 70 µs high
            #                         the low_sample_count corresponds to 50 µs
            bit = 1 if high_sample_count > low_sample_count else 0
            message_bytes[byte_number] = (message_bytes[byte_number] << 1) + bit
        # finished reading all 40 bits of the message

        humidity, humidity_dec, temperature, temperature_dec, check_sum = message_bytes

        if (humidity + humidity_dec + temperature + temperature_dec) % 256 == check_sum:  # confirmed
            return (humidity + humidity_dec / 256), (temperature + temperature_dec / 256)
        else:
            return 0.0, 0.0

if __name__ == '__main__':
    sensor = DHT11()
    print(sensor.take_measurement())