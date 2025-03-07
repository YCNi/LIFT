from config import LENGTH, REACTION

class Hole():
    def __init__(self,link,start_time):
        self.link = link
        self.start_time = start_time
        self.wave_speed = LENGTH/REACTION

        self.link_arrival_time = None

        self._calculate_link_arrival_time()

    def _calculate_link_arrival_time(self):
        self.link_arrival_time = self.start_time + self.link.link_length / self.wave_speed

