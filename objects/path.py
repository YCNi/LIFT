#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
from config import DEMAND, T
from statistics import mean

class Path():
    def __init__(self, path_id, ordered_link_list):
        self.id = path_id
        self.link_list = ordered_link_list
        self.links = []
        self.demand = None
        self.path_length = None

        self.finished_trips = []
        self.mean_speeds = []

        self._fill_demand()
        
    def add_links(self, link_objs, link_list):
        for link in link_list:
            self.links.append(link_objs[link])

    def calculate_path_length(self):
        self.path_length = sum([link.link_length for link in self.links if not link.external])
            
    def _fill_demand(self):
        self.demand = DEMAND[self.id]
        
    def find_next_link(self, link_id, link_objs):
        next_link = None
        for ind, link_id_in_link_list in enumerate(self.link_list):
            if link_id == link_id_in_link_list:
                try:
                    next_link = link_objs[self.link_list[ind+1]]
                except:
                    next_link = None
                return next_link
        return next_link

    def calculate_mean_speed(self, interval):
        for interval_id in range(int(T / interval)):
            v_list = []
            for trip in self.finished_trips:
                if trip.finish_time >= interval_id * interval and trip.finish_time < (interval_id + 1) * interval:
                    v_list.append(trip.mean_speed)
            if len(v_list) > 0:
                self.mean_speeds.append(mean(v_list))
            else:
                if len(self.mean_speeds) == 0:
                    self.mean_speeds.append(None)
                else:
                    self.mean_speeds.append(self.mean_speeds[-1])

        
        
                
        
            