# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 15:07:49 2024

@author: yingni
"""
#%%
import numpy as np
import math
from statistics import mean
import pickle
from LIFT_model import LIFT

#%%
n_seed = 5 # number of ramdom seeds

#%% Network info
n_link = 10 # number of links
L = {1:125,2:125,3:125,4:125,5:125,6:125,7:125,8:125,9:125,10:125,10001:120,10002:120,10003:120,10004:120,10005:120,10006:120} # all link lengths
EL = [10001,10002,10003,10004,10005,10006] # external origin links
w_intersection = 12 # intersection width
In = {1:[10001,7],2:[1,8],3:[2,9],4:[10002,10003],5:[10004,4],6:[10005,5],7:[10002,10003],8:[10004,4],9:[10005,5],10:[10006,6]} # inflow links of each link
cycle = 60 # signal cycle length
start_in_cycle_exit = {1:55,2:50,3:45,4:0,5:55,6:50,7:30,8:25,9:20,10:15,10001:0,10002:5,10003:35,10004:30,10005:25,10006:20} # signal offset
green_exit = {1:25,2:25,3:20,4:25,5:25,6:25,7:25,8:25,9:25,10:20,10001:25,10002:25,10003:25,10004:25,10005:25,10006:25} # green length of the downstream signal

#%% Model parameters
l_eff = 7.5 # effective vehicle length
v = 12.5 # free-flow speed
reaction = 1 # start-up reaction time
w = 7.5 / reaction # backward wave speed
q_straight = 0.625 # saturation flow rate of straight going movement
q_turn = 0.4 # saturation flow rate of turning movement
q_second = 0.33 # saturation flow rate of straight going movement of the second vehicle due to acceleration dynamics
q_third = 0.5 # saturation flow rate of straight going movement of the third vehicle due to acceleration dynamics

#%% Demand info (OD paths and their inflow loading)
T = 10800 # total simulation time
n_path = 13 # number of paths
path = {1:[10001,1,2,3],2:[10002,4,5,6],3:[10002,4,5,6,10],4:[10003,7,1,2,3],5:[10003,7],6:[10003,4,5,6,10],7:[10004,8,2,3],8:[10004,8],9:[10004,5,6,10],10:[10005,9,3],11:[10005,9],12:[10005,6,10],13:[10006,10]} # ordered link list of each path
p_exit_turn = {1:[],2:[],3:[],4:[],5:[],6:[3,6,9,12],7:[4],8:[7],9:[10],10:[],10001:[],10002:[],10003:[6],10004:[9],10005:[12],10006:[]} # turning paths on each link
time_window = 900 # time window length
d = [50, 75, 100, 150, 75, 50, 50, 50, 50, 25, 25, 25] # base demand profile
demand = {
    1:[int(d[i]*1) for i in range(len(d))],
    2:[int(d[i]*1/5) for i in range(len(d))],
    3:[int(d[i]*4/5) for i in range(len(d))],
    4:[int(d[i]*3/5) for i in range(len(d))],
    5:[int(d[i]*1/5) for i in range(len(d))],
    6:[int(d[i]*1/5) for i in range(len(d))],
    7:[int(d[i]*3/5) for i in range(len(d))],
    8:[int(d[i]*1/5) for i in range(len(d))],
    9:[int(d[i]*1/5) for i in range(len(d))],
    10:[int(d[i]*3/5) for i in range(len(d))],
    11:[int(d[i]*1/5) for i in range(len(d))],
    12:[int(d[i]*1/5) for i in range(len(d))],
    13:[int(d[i]*1) for i in range(len(d))]
    }

#%% Computed info
L_jam = {} # link length with the intersection width deducted
for i in L:
    L_jam[i] = L[i] - w_intersection
jam_num = {} # jam number of vehicles on each link
for i in L:
    jam_num[i] = math.floor(L_jam[i] / l_eff)
    if (i in EL) == True:
        jam_num[i] = 99999
PL = {} # path lengths
for i in path:
    PL[i] = sum([L[j] for j in path[i]])
    PL[i] = PL[i] - L[path[i][0]]
p_end = {} # exiting paths at each link
for i in L:
    p_end[i] = []
    for j in path:
        if path[j][-1] == i:
            p_end[i].append(j)
min_interval_s = round(1/q_straight,2) # straight going headway
min_interval_t = round(1/q_turn,2) # turning headway
second_interval = round(1/q_second,2) # straight going headway of the second vehicle
third_interval = round(1/q_third,2) # straight going headway of the third vehicle

#%% Generating entries
def generate_entry():
    entry = {} 
    for i in L:
        entry[i] = []
    distribution_type = 1 # 0: uniform entry interval, 1: exponentially-distributed interval
    if distribution_type == 0:
        for i in path:
            e = path[i][0] # entrance link
            veh_id = i * 10000
            for j in range(len(demand[i])):
                for k in range(demand[i][j]):
                    if len(entry[e]) == 0 or entry[e][-1][2] != i:
                        entry[e].append([0,veh_id,i,0]) # t, id, path, entry time
                        tc = 0
                        veh_id += 1
                    else:
                        interval = time_window / demand[i][j]
                        entry[e].append([round(tc + interval,1),veh_id,i,round(tc + interval,1)])
                        tc = tc + interval
                        veh_id += 1
    else:
        for i in path:
            e = path[i][0]
            veh_id = i * 10000
            for j in range(len(demand[i])):
                avg = round(time_window / demand[i][j],2)
                headway = np.random.exponential(scale=avg,size=demand[i][j])
                while sum(headway) >= 900:
                    headway = np.random.exponential(scale=avg,size=demand[i][j])
                for k in range(len(headway)):
                    headway[k] = round(headway[k],2)
                point = []
                start = time_window * j
                for k in range(len(headway)):
                    point.append(round(start+headway[k].item(),2))
                    start += headway[k].item()
                for k in range(len(point)):
                    entry[e].append([point[k],veh_id,i,point[k]])
                    veh_id += 1
    for i in L:
        entry[i].sort()
    return entry

#%% Simulation
den = {}
speed = {}
for rs in range(1,n_seed+1):
    entries = generate_entry()
    TT, accum_link, time, step = LIFT(T,L,EL,v,w,min_interval_s,min_interval_t,second_interval,third_interval,L_jam,jam_num,path,In,p_end,p_exit_turn,cycle,start_in_cycle_exit,green_exit,
                                      entries)
    # Analyze path speeds
    exp_v = {}
    for i in path:
        exp_v[i] = [] # finish time, mean speed
    for i in range(len(TT)):
        exp_v[TT[i][2]].append([TT[i][0],round(PL[TT[i][2]] / TT[i][1],2)])
    mean_exp_v_300 = {}
    for i in path:
        mean_exp_v_300[i] = []
    v_list = []
    for i in path:
        for c in range(36):
            v_list = []
            for j in range(len(exp_v[i])):
                if exp_v[i][j][0] >= c*300 and exp_v[i][j][0] < (c+1)*300:
                    v_list.append(exp_v[i][j][1])
            if len(v_list) > 0:
                mean_exp_v_300[i].append(mean(v_list))
            else:
                if len(mean_exp_v_300[i]) == 0:
                    mean_exp_v_300[i].append(None)
                else:
                    mean_exp_v_300[i].append(mean_exp_v_300[i][-1])
    # Analyze link densities
    den_300 = {}
    for i in L:
        den_300[i] = []
    for l in L:
        for c in range(36):
            n_list = []
            total_time = 0
            for i in range(len(accum_link[l])-1):
                if time[i] >= c * 300 and time[i] < (c+1) * 300:
                    n_list.append(accum_link[l][i]*step[i+1])
                    total_time += step[i+1]
            den_300[l].append(sum(n_list)/total_time*1000/L_jam[l])
    # Store the outputs
    den[rs] = den_300
    speed[rs] = mean_exp_v_300
# Save the outputs
with open('den.pickle', 'wb') as handle:
    pickle.dump(den, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('speed.pickle', 'wb') as handle:
    pickle.dump(speed, handle, protocol=pickle.HIGHEST_PROTOCOL)
