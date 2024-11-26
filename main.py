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
        self.open_door_counter = 0
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
        print("Select which thermostat yoo want")
        print("s  | simple : For the simple thermostat")
        print("b  | bursts : For Activating the compressor in bursts")
        print("a  | ai     : For Letting the AI do the hard work")
        print()
        print("Other functions")
        print("p  | price  : Plot price plot")
        print("pb | bounds : Generate and plot bounds for burst. Warning takes a long time")
        print("pa | aibound: slow")
        match input().lower():
            case "bursts" | "b":
                thermostat_caller = self.bursts
            case "ai" | "a":
                thermostat_caller = self.ai_enhanced
            case "price" | "p":
                self.plot_price()
            case "bounds" | "bp":
                self.generate_plot_bound()
            case "aibound" | "pa":
                self.generate_ai_values()
            case "simple" | "s" | _: # Also acts as default
                thermostat_caller = self.simple

        # Run the user selected thermostat
        if thermostat_caller != 0:
            avg_cost = 0
            runs = 20
            for i in range(runs):
                self.open_door_counter = 0
                avg_cost += thermostat_caller()
            avg_cost = avg_cost / runs
            print(avg_cost)
        return

#=======================================
# Random functions that does something
#=======================================
    def generate_plot_bound(self):
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
                threads[index] = threading.Thread(target=self.t_start_plot_bound, args=(lowerbound, upperbound, index))
            
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            all_test_runs.append(self.thread_results)
            print(f"progress: {upperbound} of {given_upbound}, time taken: {(datetime.now() - time_stamp).seconds} seconds")
        self.plot_bound(all_test_runs, given_lowbound/10, given_upbound/10)
        return

    def t_start_plot_bound(self, lowerbound, upperbound, index):
        avg_cost = 0
        runs = 20
        for i in range(runs):
            avg_cost += self.bursts(lowerbound=(lowerbound/10), upperbound=(upperbound/10)) 
        avg_cost = avg_cost / runs 
        self.thread_results[index] = avg_cost
        return

    def generate_ai_values(self):
        self.import_price()

        given_low_thres = 1
        given_high_thres = 50
        time_stamp = 0
        
        all_test_runs = []
        for high_thres in range(given_low_thres, given_high_thres):
            time_stamp = datetime.now()
            test_runs = []
            for low_thres in range(given_low_thres, given_high_thres):
                avg_cost = 0
                runs = 20
                for i in range(runs):
                    avg_cost += self.ai_enhanced(low_thres/10, high_thres/10)

                test_runs.append(avg_cost/runs)
            print(f"progress: {high_thres} of {given_high_thres}, time taken: {(datetime.now() - time_stamp).microseconds} microseconds")
            all_test_runs.append(test_runs)
        self.plot_bound(all_test_runs, given_low_thres/10, given_high_thres/10)
        return    

#=============
# Thermostats
#=============
    def simple(self, threshold = 6):
        my_fridge = fridge(electric_price=self.price)
        for i in range(8640):
            enable_comprssor = my_fridge.tempeture > threshold # The simple thermostat logic
            is_door_open = random.randrange(10) == 0 # 1 in 10 chance of door being open
            my_fridge.update_tempeture(i, is_door_open, enable_comprssor)
            self.open_door_counter += 1 if is_door_open else 0
        print(self.open_door_counter / 8640)
        return my_fridge.cost      

    def bursts(self, lowerbound = 6.4, upperbound = 6.4):
        my_fridge = fridge(electric_price=self.price)
        enable_comprssor = False
        for i in range(8640):
            enable_comprssor = my_fridge.tempeture > lowerbound if enable_comprssor else my_fridge.tempeture > upperbound 
            is_door_open = random.randrange(9) == 0 # 1 in 10 chance of door being open
            my_fridge.update_tempeture(i, is_door_open, enable_comprssor)
        return my_fridge.cost      

    def ai_enhanced(self, price_threshold_1:float = 1.3, price_threshold_2:float = 2.8):
        my_fridge = fridge(electric_price=self.price)
        for i in range(8640):
            enable_comprssor = False
            if (my_fridge.tempeture > 6 
                or my_fridge.tempeture > 3.5 and self.price[i] < price_threshold_1
                or my_fridge.tempeture > 5 and self.price[i] < price_threshold_2):
                enable_comprssor = True
            is_door_open = random.randrange(9) == 0 # 1 in 10 chance of door being open
            my_fridge.update_tempeture(i, is_door_open, enable_comprssor)
            self.open_door_counter += 1 if is_door_open else 0
        print(self.open_door_counter / 8640)
        return my_fridge.cost

#=================
# Plotting utils
#=================
    def plot_price(self):
        x = self.dates
        y = self.price
        plt.plot(x,y)
        plt.show()
        return

    def plot_bound(self, data, given_lowbound, given_upbound):
        plt.imshow(data, extent=[given_lowbound,given_upbound, given_upbound,given_lowbound])
        plt.gca().invert_yaxis()
        plt.xlabel("Lowerbound [celcius]")
        plt.ylabel("Upperbound [celcius]")
        plt.colorbar()
        plt.show()
        return

if __name__ == "__main__":
    starter = your_mom()
    #starter.generate_plot_bound() # Better known as bursts graphing
    starter.start()
