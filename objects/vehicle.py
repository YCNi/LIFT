#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 20:28:24 2024
"""

from config import LENGTH, SPEED, REACTION

class Vehicle():
    def __init__(self, v_id, path, link, entry_time):
        
        self.id = v_id
        self.path = path
        self.link = link
        self.entry_time = entry_time
        
        self.length = LENGTH
        self.v = SPEED
        self.reaction = REACTION

        self.remaining_distance = None

        # self._initiate_remaining_distance()
        # self._calculate_remaining_distance()
        
    def calculate_wave_speed(self):
        return self.length / self.reaction
    
    def _initiate_remaining_distance(self):
        remaining_distance = self.link.link_length
        return remaining_distance


    def _calculate_remaining_distance(self):
        remaining_distance = self.remaining_distance - step_size * self.v
        return remaining_distance()
    
    
        