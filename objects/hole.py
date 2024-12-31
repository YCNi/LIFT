from config import LENGTH, REACTION

class Hole():
    def __init__(self, location):
        self.location = location
        self.wave_speed = LENGTH/REACTION
