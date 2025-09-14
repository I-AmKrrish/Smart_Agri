import random
import time

class DHT11Sensor:
    def __init__(self, pin):
        self.pin = pin
        
    def read_temperature(self):
        # Simulate DHT11 temperature reading
        return round(random.uniform(10, 40), 2)
        
    def read_humidity(self):
        # Simulate DHT11 humidity reading
        return round(random.uniform(20, 90), 2)