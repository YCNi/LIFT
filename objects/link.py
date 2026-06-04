#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from config import LENGTH, INTERSECTION_WIDTH, CYCLE, T

class Link():
    def __init__(self, link_id, link_length, lane_num, is_external,
                 cycle, start_in_cycle_exit, green_exit):
        self.id = link_id
        self.link_length = link_length
        self.lane_num = lane_num
        self.external = is_external
        self.intersection_width = INTERSECTION_WIDTH
        self.upstream_links = None
        self.cycle = cycle
        self.start_in_cycle_exit = start_in_cycle_exit
        self.green_exit = green_exit
        
        self.length_jam = None
        self.jam_num = None
        self.entry = []
        self.remain = []
        self.spill_num = None

        self.next_event = []
        self.next_event_time = None
        self.possible_event_time = {}
        
        self.time_entry_supply = -1
        self.temp_time_entry_supply = -1
        self.time_exit_supply = -1
        self.previous_entry_all = -1
        self.previous_exit_all = -1

        self.next_exit_seq = 0
        self.accumulation = []
        self.holes_in_link = []
        self.exiting_path = None
        self.turning_exiting_path = []

        self.exit_stamp = []

        self.flows = []
        self.densities = []
        
        self._calculate_length_jam()
        self._calculate_jam_num()
          
    def _calculate_length_jam(self):
        self.length_jam = self.link_length - self.intersection_width
    
    def _calculate_jam_num(self):
        if self.external == True:
            self.jam_num = float('inf')
        else:
            self.jam_num = math.floor(self.length_jam * self.lane_num/LENGTH)
            
    def get_upstream_links(self, path_objs, link_objs):
        self.upstream_links = {}
        for path in path_objs.values():
            if self.id in path.link_list:
                ind = path.link_list.index(self.id)
                upstream_ind = ind-1
                if upstream_ind>=0:
                    upstream_link_id = path.link_list[upstream_ind]
                    self.upstream_links[upstream_link_id] = link_objs[upstream_link_id]
            
    def get_exiting_paths(self, path_objs):
        self.exiting_path = {}
        for path in path_objs.values():
            if path.link_list[-1] == self.id:
                self.exiting_path[path.id] = path
                
    def get_turning_exiting_paths(self, path_objs, path_list):
        for path in path_list:
            self.turning_exiting_path.append(path_objs[path])
            
    def in_green_exit(self, request_time):
        in_green = False
        delay = 0
        if (self.start_in_cycle_exit + request_time) % self.cycle <= self.green_exit:
            in_green = True
        else:
            delay = round(self.cycle - (self.start_in_cycle_exit + request_time) % self.cycle, 2)
        return in_green, delay

    def calculate_density(self, interval, time, step):
        # check length of time, step, accumulation:
        if len(time) != len(step):
            raise Exception("len(time) != len(step)")
        elif len(self.accumulation) != len(time):
            raise Exception("len(number of accumulated vehicles for a link) != len(time)")
        elif len(self.accumulation) != len(step):
            raise Exception("len(number of accumulated vehicles for a link) != len(step)")

        for interval_id in range(int(T/interval)):
            n_list = []
            total_time = 0
            for i, t in enumerate(time):
                if i != len(time)-1: # if not the last one
                    if t >= interval_id * interval and t < (interval_id + 1) * interval:
                        n_list.append(self.accumulation[i] * step[i + 1])
                        total_time += step[i + 1]
            if self.lane_num > 0:
                self.densities.append(sum(n_list) / total_time * 1000 / (self.length_jam * self.lane_num))
            else:
                self.densities.append(0)

    def calculate_flow(self, interval):
        for interval_id in range(int(T / interval)):
            exit_count = 0
            for i, t in enumerate(self.exit_stamp):
                if t >= interval_id * interval and t < (interval_id + 1) * interval:
                    exit_count += 1
            if self.lane_num > 0:
                self.flows.append(exit_count*(3600/interval)/self.lane_num)
            else:
                self.flows.append(0)
        