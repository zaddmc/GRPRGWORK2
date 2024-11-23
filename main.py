from fridge import fridge

import csv
from datetime import datetime
import random
import numpy as np

import matplotlib.pyplot as plt

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
        # Setup
        self.import_price()
        
         
        # Get the thermostat type from user
        thermostat_caller = 0
        print("Select which thermostat yoo want\ns | simple : For the simple thermostat")
        match input().lower():
            case "simple" | "s" | _:
                thermostat_caller = self.simple
        
        # Run the user selected thermostat
        avg_cost = 0
        runs = 20
        for i in range(runs):
            avg_cost += thermostat_caller()
        avg_cost = avg_cost / runs 
        

        print(avg_cost)

        #self.plot_price()
        return
    
    def simple(self):
        my_fridge = fridge(electric_price=self.price)
        for i in range(8640):
            enable_comprssor = my_fridge.tempeture > 5 # The simple thermostat logic
            is_door_open = random.randrange(9) == 0 # 1 in 10 chance of door being open
            my_fridge.update_tempeture(i, is_door_open, enable_comprssor)
        return my_fridge.cost      

    def plot_price(self):
        x = self.dates
        y = self.price
        plt.plot(x,y)
        plt.show()

if __name__ == "__main__":
    starter = your_mom()
    starter.start()
