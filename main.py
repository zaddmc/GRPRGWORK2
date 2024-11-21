from fridge import fridge
import csv
from datetime import datetime
import random

class your_mom:
    def __init__(self):
        self.dates = []
        self.price = []
        return

    def import_price(self):
        with open("elpris.csv", "r") as file:
            reader = csv.reader(file)
            for line in reader:
                try:
                    self.dates.append(datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S'))
                    self.price.append(float(line[1]))
                except:
                    pass
        return

    def start(self):
        
        self.import_price()
        
        for _ in range(20):
            print(self.simple()) 
        return
    
    def simple(self):
        my_fridge = fridge()
        for _ in range(8640):
            enable_comprssor = my_fridge.tempeture > 5
            my_fridge.update_tempeture(random.randrange(9) == 0, enable_comprssor)
        return my_fridge.tempeture       


if __name__ == "__main__":
    starter = your_mom()
    starter.start()
