class Trip():
    def __init__(self, finish_time, travel_time):
        self.finish_time = finish_time
        self.travel_time = travel_time
        self.mean_speed = None

    def calculate_mean_speed(self, path_obj):
        self.mean_speed = round(path_obj.path_length/self.travel_time, 2)
