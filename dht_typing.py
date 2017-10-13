"""
A module to define the type hints for the DHT classes

13/10/2017
"""
from typing import Tuple, List

Humidity = float
Temperature = float
Data = Tuple[Humidity, Temperature]
Message = List[int]
