from fridge import fridge

import csv
from datetime import datetime
import random
import numpy as np
import threading
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
        print("Select which thermostat yoo want\ns | simple : For the simple thermostat \nb | bursts : For Activating the compressor in bursts")
        match input().lower():
            case "simple" | "s":# | _: # Also acts as default
                thermostat_caller = self.simple
            case "bursts" | "b" | _:
                thermostat_caller = self.bursts

        # Run the user selected thermostat
        avg_cost = 0
        runs = 20
        for i in range(runs):
            avg_cost += thermostat_caller()
        avg_cost = avg_cost / runs 
        

        print(avg_cost)

        #self.plot_price()
        return
    
    def tester(self):
        self.import_price()
        
        given_lowbound = 25
        given_upbound = 75
        time_stamp = 0

        threads = [0 for _ in range(given_lowbound, given_upbound)]
        all_test_runs = []
        for upperbound in range(given_lowbound, given_upbound):
            time_stamp = datetime.now()
            self.thread_results = [0 for _ in range(given_lowbound, given_upbound)]
            for lowerbound in range(given_lowbound, given_upbound):
                index = lowerbound - given_lowbound 
                threads[index] = threading.Thread(target=self.t_start_tester, args=(lowerbound, upperbound, index))
            
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            all_test_runs.append(self.thread_results)
            print(f"progress: {upperbound} of {given_upbound}, time taken: {(datetime.now() - time_stamp).seconds} seconds")

        self.plottest(all_test_runs, given_lowbound/10, given_upbound/10)

    def t_start_tester(self, lowerbound, upperbound, index):
        avg_cost = 0
        runs = 20
        for i in range(runs):
            avg_cost += self.bursts(lowerbound=(lowerbound/10), upperbound=(upperbound/10)) 
        avg_cost = avg_cost / runs 
        self.thread_results[index] = avg_cost

    def simple(self):
        my_fridge = fridge(electric_price=self.price)
        for i in range(8640):
            enable_comprssor = my_fridge.tempeture > 5 # The simple thermostat logic
            is_door_open = random.randrange(9) == 0 # 1 in 10 chance of door being open
            my_fridge.update_tempeture(i, is_door_open, enable_comprssor)
        return my_fridge.cost      

    def bursts(self, lowerbound = 6.4, upperbound = 6.4):
        my_fridge = fridge(electric_price=self.price)
        enable_comprssor = False
        for i in range(8640):
            enable_comprssor = my_fridge.tempeture > lowerbound if enable_comprssor else my_fridge.tempeture > upperbound 
            is_door_open = random.randrange(9) == 0 # 1 in 10 chance of door being open
            my_fridge.update_tempeture(i, is_door_open, enable_comprssor)
        return my_fridge.cost      


    def plot_price(self):
        x = self.dates
        y = self.price
        plt.plot(x,y)
        plt.show()

    def plot_bounds(self, data):
        npoints = 500
        x = np.random.uniform(low=0, high=3, size=npoints)
        y = np.random.uniform(low=-3, high=3, size=npoints)
        
        print(x)

        # Make the plot
        plt.hist2d(x, y)
        plt.colorbar()
        plt.show()
        
    def plottest(self, data, given_lowbound, given_upbound):
        plt.imshow(data, extent=[given_lowbound,given_upbound, given_upbound,given_lowbound])
        plt.gca().invert_yaxis()
        plt.xlabel("Lowerbound [celcius]")
        plt.ylabel("Upperbound [celcius]")
        plt.colorbar()
        plt.show()
        return

if __name__ == "__main__":
    starter = your_mom()
    #starter.tester() # Better known as bursts graphing
    starter.start()
