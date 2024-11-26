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
        args_to_give = {}
        print("Select which thermostat yoo want")
        print("s  | simple : For the simple thermostat")
        print("b  | bursts : For Activating the compressor in bursts")
        print("a  | ai     : For Letting the AI do the hard work")
        print()
        print("Other functions")
        print("pp | price  : Plot price plot")
        print("ps | plotsimple : Plot best values for simple thermostat")
        print("pb | bounds : Generate and plot bounds for burst. Warning takes a long time")
        print("pa | aibound: slow")
        match input().lower():
            case "bursts" | "b":
                thermostat_caller = self.bursts
                args_to_give = {"lowerbound" : 6.4, "upperbound" : 6.4, "prior_state" : False}
            case "ai" | "a":
                thermostat_caller = self.ai_enhanced
                args_to_give = {"threshold_1" : 1.3, "threshold_2" : 2.8}
            case "price" | "p":
                self.plot_simple(given_title="Electricity prices", given_x_label="Date", given_y_label="Pris [kr./kWh]")
            case "plotsimple" | "ps":
                self.find_simple_vals()
            case "bounds" | "pb":
                self.generate_plot_bound()
            case "aibound" | "pa":
                self.generate_ai_values()
            case "t": # For testing and development
                self.plot_simple()
            case "simple" | "s" | _: # Also acts as default
                thermostat_caller = self.simple
                args_to_give = {"threshold" : 5}

        if thermostat_caller != 0:
            print(self.run_simulations(thermostat_caller, args_to_give))
        return

    def run_simulations(self, thermostat_caller, args_to_give, runs:int = 20) -> float:
        avg_cost = 0
        for i in range(runs):
            avg_cost += self.run(thermostat_caller, args_to_give)
        avg_cost = avg_cost / runs
        return avg_cost

    def run(self, thermostat_caller, args_to_give) -> float:
        self.open_door_counter = 0
        my_fridge = fridge(electric_price=self.price)
        for i in range(8640):
            args_to_give["tempeture"] = my_fridge.tempeture 
            args_to_give["i"] = i
            enable_comprssor = thermostat_caller(args_to_give)
            is_door_open = random.randrange(10) == 0 # 1 in 10 chance of door being open
            my_fridge.update_tempeture(i, is_door_open, enable_comprssor)
            args_to_give["prior_state"] = enable_comprssor
            #self.open_door_counter += 1 if is_door_open else 0
        #print(self.open_door_counter / 8640)
        return my_fridge.cost

#=============
# Thermostats
#=============
    def simple(self, args) -> bool:
        return args["tempeture"] > args["threshold"] 

    def bursts(self, args) -> bool:
        return args["tempeture"] > args["lowerbound"] if args["prior_state"] else args["tempeture"] > args["upperbound"] 

    def ai_enhanced(self, args) -> bool: 
        return (args["tempeture"] > 6
                or args["tempeture"] > 3.5 and self.price[args["i"]] < args["threshold_1"]
                or args["tempeture"] > 5 and self.price[args["i"]] < args["threshold_2"]) 

#================================================================
# Helper functions to find best values for different thermostats 
#================================================================
    def find_simple_vals(self):
        print("Beginning to find best values for simple thermostat")
        start_val = 1
        end_val = 7
        check_progress = start_val
        
        tempeture_to_test = start_val
        tempetures_tested = []
        results = []
        while True:
            tempetures_tested.append(tempeture_to_test)
            results.append(self.run_simulations(self.simple, {"threshold" : tempeture_to_test}, 50))
            tempeture_to_test += 0.1
            if tempeture_to_test > end_val:
                break
            if tempeture_to_test > check_progress:
                print(f"Progress: {(tempeture_to_test-start_val)/(end_val-start_val)*100:.2f}%")
                check_progress += start_val
            
        best_temp = 0
        best_cost = results[0]
        for cost, temp in zip(results, tempetures_tested):
            if cost < best_cost:
                best_cost = cost
                best_temp = temp
        print(f"Best Tempeture for simple is: {best_temp:.4f} celcius with only a cost of: {best_cost:.2f} kr.")
        self.plot_simple(tempetures_tested, results, "Tempetures tested [celcius]", "Avg Cost [kr.]", "Simple thermostat Test")
        return

#=================
# Plotting utils
#=================
    def plot_simple(self, given_x_val = 0, given_y_val = 0, given_x_label = "X Label", given_y_label = "Y Label", given_title = "Graph Title"):
        x = self.dates if given_x_val == 0 else given_x_val
        y = self.price if given_y_val == 0 else given_y_val
        plt.title(given_title)
        plt.xlabel(given_x_label)
        plt.ylabel(given_y_label)
        plt.plot(x,y)
        plt.show()
        return

    def plot_fancy(self, data, given_x_vals = [1,5], given_y_vals = [1,5], given_x_label = "X Label", given_y_label = "Y Label", given_title = "Graph Titile"):
        given_y_vals.reverse()
        given_x_vals.extend(given_y_vals)
        plt.imshow(data, extent=given_x_vals)
        plt.gca().invert_yaxis()
        plt.title(given_title)
        plt.xlabel(given_x_label)
        plt.ylabel(given_y_label)
        plt.colorbar()
        plt.show()
        return

if __name__ == "__main__":
    starter = your_mom()
    starter.start()
