#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:37:25 2024
"""

#vehicle & driving behavioral parameters
LENGTH = 7.5 # effective vehicle length (including minimum gap)
SPEED = 12.5 # desired speed
REACTION = 1 # reaction time
Q_STRAIGHT = 0.625 # saturation flow rate for straight movements
Q_TURN = 0.4 # saturation flow rate for turning movements
MIN_HEADWAY_STRAIGHT = round(1 / Q_STRAIGHT, 2) # headway of straight movements
MIN_HEADWAY_TURN = round(1 / Q_TURN, 2) # headway of turning movements
Q_SECOND = 0.33 # saturation flow rate for the second exiting vehicle considering start-up delay
Q_THIRD = 0.5 # saturation flow rate for the third exiting vehicle considering start-up delay
SECOND_HEADWAY = round(1 / Q_SECOND, 2) # headway for the second exiting vehicle considering start-up delay
THIRD_HEADWAY = round(1 / Q_THIRD, 2) # headway for the third exiting vehicle considering start-up delay

#Link and path parameters
INTERSECTION_WIDTH = 12
NUM_LINK = 10
NUM_PATH = 13

# link length
LINKS = {1: 125,
         2: 125,
         3: 125,
         4: 125,
         5: 125,
         6: 125,
         7: 125,
         8: 125,
         9: 125,
         10: 125,
         10001: 120,
         10002: 120,
         10003: 120,
         10004: 120,
         10005: 120,
         10006: 120} 

EXTERNAL_LINKS = [10001, 10002, 10003, 10004, 10005, 10006]

# ordered link list of each path
PATH = {1:[10001,1,2,3],
        2:[10002,4,5,6],
        3:[10002,4,5,6,10],
        4:[10003,7,1,2,3],
        5:[10003,7],
        6:[10003,4,5,6,10],
        7:[10004,8,2,3],
        8:[10004,8],
        9:[10004,5,6,10],
        10:[10005,9,3],
        11:[10005,9],
        12:[10005,6,10],
        13:[10006,10]
        }

# turning exit paths at each link
PATH_EXIT_TURN = {1:[],
                  2:[],
                  3:[],
                  4:[],
                  5:[],
                  6:[3,6,9,12],
                  7:[4],
                  8:[7],
                  9:[10],
                  10:[],
                  10001:[],
                  10002:[],
                  10003:[6],
                  10004:[9],
                  10005:[12],
                  10006:[]
                } 

#simulation parameters
T = 10800 # total simulation period
N_SEED = 5 # number of random scenarios
AGG_INTERVAL = 300 # aggregation time interval for post-processing

#demand parameters
UNIFORM = False
if UNIFORM == True:
    N_SEED = 1
TIME_INTERVAL = 900 # time interval for different demand values
D = [50, 75, 100, 150, 75, 50, 50, 50, 50, 25, 25, 25] # base demand
DEMAND = {
            1:[int(D[i]*1) for i in range(len(D))],
            2:[int(D[i]*1/5) for i in range(len(D))],
            3:[int(D[i]*4/5) for i in range(len(D))],
            4:[int(D[i]*3/5) for i in range(len(D))],
            5:[int(D[i]*1/5) for i in range(len(D))],
            6:[int(D[i]*1/5) for i in range(len(D))],
            7:[int(D[i]*3/5) for i in range(len(D))],
            8:[int(D[i]*1/5) for i in range(len(D))],
            9:[int(D[i]*1/5) for i in range(len(D))],
            10:[int(D[i]*3/5) for i in range(len(D))],
            11:[int(D[i]*1/5) for i in range(len(D))],
            12:[int(D[i]*1/5) for i in range(len(D))],
            13:[int(D[i]*1) for i in range(len(D))]
        } # demand of each path

#signal timing parameters
CYCLE = 60
START_IN_CYCLE_EXIT = {1:55,2:50,3:45,4:0,5:55,6:50,7:30,8:25,9:20,10:15,10001:0,10002:5,10003:35,10004:30,10005:25,10006:20} # time in the signal cycle of the exit of ech link at the beginning of the simulation
GREEN_EXIT = {1:25,2:25,3:20,4:25,5:25,6:25,7:25,8:25,9:25,10:20,10001:25,10002:25,10003:25,10004:25,10005:25,10006:25} # green length of the exit of each link
