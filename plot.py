from matplotlib import pyplot as plt
import math
from config import T


def plot(simulation_objects, interval, n_seed):
    num_t = int(T / interval)
    time_x = [interval * i for i in range(1, num_t)]
    n_path = len(simulation_objects[0].Paths)
    n_link = sum([1 for link in simulation_objects[0].Links.values() if not link.external])

    # create dictionary for plotting
    speed = {}
    den = {}

    for i, object in enumerate(simulation_objects):
        speed[i] = {}
        den[i] = {}
        for path in object.Paths.values():
            speed[i][path.id] = path.mean_speeds
        for link in object.Links.values():
            den[i][link.id] = link.densities

    #%% Fill empty data
    for j in range(n_seed):
        for i in range(1, n_link+1):
            for k in range(num_t):
                if den[j][i][k] == None:
                    den[j][i][k] = 0
        for i in range(1, n_path+1):
            for k in range(num_t):
                if speed[j][i][k] == None:
                    speed[j][i][k] = 0

    #%% Calculate max and min for the range
    den_max = {}
    den_min = {}
    for i in range(1, n_link+1):
        den_max[i] = []
        den_min[i] = []
        for k in range(num_t):
            den_max[i].append(max([den[j][i][k] for j in range(n_seed)]))
            den_min[i].append(min([den[j][i][k] for j in range(n_seed)]))
    speed_max = {}
    speed_min = {}
    for i in range(1, n_path+1):
        speed_max[i] = []
        speed_min[i] = []
        for k in range(num_t):
            speed_max[i].append(max([speed[j][i][k] for j in range(n_seed)]))
            speed_min[i].append(min([speed[j][i][k] for j in range(n_seed)]))

    #%% Density plot
    fig, axs = plt.subplots(math.ceil(n_link/2), 2,sharex=True,sharey=False, figsize=(15, math.ceil(n_link/2)*4))
    r = 0
    c = 0
    for i in range(n_link):
        print(r,c)
        axs[r][c].fill_between(time_x, den_max[i+1][1:], den_min[i+1][1:], color = 'tab:red', alpha=0.5)
        axs[r][c].plot(time_x, den_max[i+1][1:], c='tab:red', linewidth=3)
        axs[r][c].plot(time_x, den_min[i+1][1:], c='tab:red', linewidth=3)
        axs[r][c].set_ylabel('density (veh/km)',fontname="Arial",fontsize=22)
        axs[r][c].set_xlim([0, T])
        axs[r][c].set_ylim([0, 140])
        axs[r][c].set_title('link '+repr(i+1),fontname="Arial",fontsize=22)
        r = r + i%2
        c = (i+1)%2
    plt.savefig('den.png',bbox_inches='tight')
    #plt.show()

    #%% Speed plot
    fig, axs = plt.subplots(math.ceil(n_path/2), 2,sharex=True,sharey=False, figsize=(15, math.ceil(n_path/2)*4))
    r = 0
    c = 0
    for i in range(n_path):
        axs[r][c].fill_between(time_x, speed_max[i+1][1:], speed_min[i+1][1:], color = 'tab:red', alpha=0.5)
        axs[r][c].plot(time_x, speed_max[i+1][1:], c='tab:red', linewidth=3)
        axs[r][c].plot(time_x, speed_min[i+1][1:], c='tab:red', linewidth=3)
        axs[r][c].set_ylabel('speed (m/s)',fontname="Arial",fontsize=22)
        axs[r][c].set_xlim([0, T])
        axs[r][c].set_ylim([0, 14])
        axs[r][c].set_title('path '+repr(i+1),fontname="Arial",fontsize=22)
        r = r + i%2
        c = (i+1)%2
    plt.savefig('speed.png',bbox_inches='tight')
    #plt.show()