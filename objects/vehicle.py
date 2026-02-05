#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

        self.link_exit_time = None

    def calculate_link_exit_time(self,t):
        self.link_exit_time = t + self.link.link_length / self.v
    
    
        