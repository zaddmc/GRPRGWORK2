class fridge:
    def __init__(self, start_temp:float = 5, room_temp:float = 20, compressor_temp:float = -5):
        self.tempeture:float = start_temp
        self.room_tempeture:float = room_temp
        self.compressor_tempeture:float = compressor_temp
        self.tempeture_change = []
        self.door_val = {False : 5 * 10**-7, True : 3 * 10**-5} # Same as c1
        self.comp_val = {False : 0, True : 8 * 10**-6} # Same as c2
        return

    def update_tempeture(self, is_door_open:bool, is_compressor_on:bool):
        new_temp = self.tempeture + (self.door_val[is_door_open]*(self.room_tempeture - self.tempeture) + self.comp_val[is_compressor_on]*(self.compressor_tempeture - self.tempeture)) * 300
        self.tempeture = new_temp
        self.tempeture_change.append(new_temp)
        return
    
