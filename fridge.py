import numpy as np

class fridge:
    def __init__(self, start_temp:float = 5, room_temp:float = 20, compressor_temp:float = -5, electric_price = []):
        self.tempeture:float = start_temp
        self.room_tempeture:float = room_temp
        self.compressor_tempeture:float = compressor_temp
        self.tempeture_change = []
        self.door_val = {False : 5 * 10**-7, True : 3 * 10**-5} # Same as c1
        self.comp_val = {False : 0, True : 8 * 10**-6} # Same as c2
        self.electricity_price = electric_price
        self.cost_change = []
        self.cost:float = 0
        return

    def update_tempeture(self, n:int , is_door_open:bool, is_compressor_on:bool):
        new_temp = self.tempeture + (self.door_val[is_door_open]*(self.room_tempeture - self.tempeture) + self.comp_val[is_compressor_on]*(self.compressor_tempeture - self.tempeture)) * 300
        self.tempeture = new_temp
        self.tempeture_change.append(new_temp)
        
        self.calculate_cost(n, is_compressor_on)
        return

    def calculate_cost(self, n:int, compressor_state:bool, tempeture:float = 0):
        tempeture = self.tempeture if tempeture == 0 else 0
        add_cost:float = 0
        if compressor_state:
            add_cost += self.electricity_price[n]
        add_cost += self.food_cost(tempeture)

        self.cost_change.append(add_cost)
        self.cost += add_cost
        return

    def food_cost(self, T:float):
        if T < 3.5:
            #print("under caled " + str(self.tempeture))
            return 4.39 * np.exp(-0.49 * T)
        elif 3.5 <= T and T < 6.5:
            return 0
        else:
            #print("over called " + str(self.tempeture))
            return 0.11 * np.exp(0.31 * T)
