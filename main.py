from create_objects import Object
from post_processing import post_processing
from model import LIFT
from plot import plot
from config import N_SEED, AGG_INTERVAL, UNIFORM


simulations = []

for rs in range(N_SEED):
    object = Object()
    if UNIFORM == True:
        object.generate_uniform_entry()
    else:
        object.generate_exponential_entry()
    object = LIFT(object)
    print("simulation done")
    object = post_processing(object, AGG_INTERVAL)
    print("post-processing done")
    simulations.append(object)
    print("simulation stored")

#plot(simulations, AGG_INTERVAL, N_SEED)
#print("plotted")
