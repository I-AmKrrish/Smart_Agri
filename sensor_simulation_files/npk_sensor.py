import random
import time

class NPKSensor:
    def __init__(self, pin):
        self.pin = pin
        
    def read_nitrogen(self):
        # Simulate JXBS-3001 nitrogen reading (mg/kg)
        return random.randint(10, 200)
        
    def read_phosphorus(self):
        # Simulate JXBS-3001 phosphorus reading (mg/kg)
        return random.randint(5, 150)
        
    def read_potassium(self):
        # Simulate JXBS-3001 potassium reading (mg/kg)
        return random.randint(20, 300)