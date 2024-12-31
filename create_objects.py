#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 23:12:41 2024
"""

from config import (LINKS, EXTERNAL_LINKS, PATH, PATH_EXIT_TURN,
                    START_IN_CYCLE_EXIT, GREEN_EXIT, TIME_INTERVAL)
from objects.link import Link
from objects.path import Path
from objects.vehicle import Vehicle
import numpy as np


class Object():
    def __init__(self):
        self.Links = self._create_link_objects()
        self.Paths = self._create_path_objects()
        self.time = []
        self.step = []
        
        self._add_upstream_links()
        self._add_links_to_path()
        self._calculate_path_length()
        self._add_exiting_path_to_link()
        self._add_turning_existing_path_to_link()
        


    def _create_vehicle_objects(self):
        pass
    
    def _create_link_objects(self):
        link_objs = {}
        for link_id in LINKS.keys():
            # first, check the link is external or not
            if link_id in EXTERNAL_LINKS:
                is_external = True
            else:
                is_external = False
            link_objs[link_id] = Link(link_id = link_id, 
                                      link_length = LINKS[link_id],
                                      is_external = is_external,
                                      start_in_cycle_exit = START_IN_CYCLE_EXIT[link_id],
                                      green_exit = GREEN_EXIT[link_id])
        return link_objs
    
    def _create_path_objects(self):
        path_objs = {}
        for path_id in PATH.keys():
            path_objs[path_id] = Path(path_id = path_id,
                                      ordered_link_list = PATH[path_id])
        return path_objs
    
    def _add_upstream_links(self):
        for link_id in self.Links.keys():
            self.Links[link_id].get_upstream_links(self.Paths, self.Links)
        
    
    def _add_links_to_path(self):
        for path_id in self.Paths.keys():
            self.Paths[path_id].add_links(self.Links, PATH[path_id])
            
    def _add_exiting_path_to_link(self):
        for link_id in self.Links.keys():
            self.Links[link_id].get_exiting_paths(self.Paths)
            
    def _add_turning_existing_path_to_link(self):
        for link_id in self.Links.keys():
            self.Links[link_id].get_turning_exiting_paths(self.Paths, PATH_EXIT_TURN[link_id])

    def _calculate_path_length(self):
        for path in self.Paths.values():
            path.calculate_path_length()

    def generate_uniform_entry(self):
        previous_path = None
        for path in self.Paths.values():
            entrance_link = self.Links[path.link_list[0]]
            vehicle_id = path.id * 10000
            for demand in path.demand:
                interval = TIME_INTERVAL/demand
                for veh in range(demand):
                    if len(entrance_link.entry)==0 or path!= previous_path:
                        entry_time = 0
                        entrance_link.entry.append(Vehicle(vehicle_id, path, entrance_link, entry_time))
                        tc = 0
                        vehicle_id += 1
                        previous_path = path
                    else:
                        entry_time = round(tc + interval,1)
                        entrance_link.entry.append(Vehicle(vehicle_id, path, entrance_link, entry_time))
                        tc = tc + interval
                        vehicle_id += 1
                        previous_path = path
        for link in self.Links.values():
            link.entry.sort(key=lambda x: x.entry_time)

    def generate_exponential_entry(self):
        for path in self.Paths.values():
            entrance_link = self.Links[path.link_list[0]]
            vehicle_id = path.id * 10000
            for j, demand in enumerate(path.demand):
                avg = round(TIME_INTERVAL / demand, 2)
                headway = np.random.exponential(scale=avg, size=demand)
                while sum(headway) >= TIME_INTERVAL:  # or sum(headway) <= 800
                    headway = np.random.exponential(scale=avg, size=demand)
                #for k in range(len(headway)):
                    #headway[k] = round(headway[k], 2)
                point = []
                start = TIME_INTERVAL * j
                for k in range(len(headway)):
                    point.append(round(start + headway[k].item(), 2))
                    start += headway[k].item()
                for k in range(len(point)):
                    entrance_link.entry.append(Vehicle(vehicle_id, path, entrance_link, point[k]))
                    vehicle_id += 1
        for link in self.Links.values():
            link.entry.sort(key=lambda x: x.entry_time)



        

if __name__ == "__main__":                
    Object = Object()
    print('done')
    