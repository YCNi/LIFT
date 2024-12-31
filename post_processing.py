
def post_processing(object, interval):
    # path mean speed
    for path in object.Paths.values():
        # calculate mean speed per trip
        for trip in path.finished_trips:
            trip.calculate_mean_speed(path)
        # calculate mean speed per path per 300 seconds
        path.calculate_mean_speed(interval)

    # link density
    for link in object.Links.values():
        link.calculate_density(interval, object.time, object.step)

    return object