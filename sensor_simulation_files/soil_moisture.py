import random
import time

class SoilMoistureSensor:
    def __init__(self, pin):
        self.pin = pin
        
    def read_moisture(self):
        # Simulate FC-28 sensor reading (0-1023, lower is drier)
        moisture_value = random.randint(200, 800)
        moisture_percent = (1023 - moisture_value) * 100 / 1023
        return round(moisture_percent, 2)