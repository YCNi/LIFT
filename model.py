#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 17:25:20 2024
"""

from create_objects import Object
from objects.vehicle import Vehicle
from objects.event import Event
from objects.trip import Trip
from objects.hole import Hole
from config import T, MIN_HEADWAY_STRAIGHT, MIN_HEADWAY_TURN, SECOND_HEADWAY, THIRD_HEADWAY
from matplotlib import pyplot as plt


def check_no_vehicle(object):
    for link in object.Links.values():
        if len(link.entry):
            return False
        elif len(link.remain):
            return False
    return True

def LIFT(object):
    t = 0

    step = []
    time = []

    while t <= T:
        # print('-------------------- new event --------------------')
        if check_no_vehicle(object):
            break;
        ############################## find the next link event ##########################################################
        for link in object.Links.values():
            if len(link.entry) >0 and len(link.remain)==0: # if no vehicle inside and there are entry requests
                entry_time_temp = max(t, link.entry[0].entry_time)
                link.next_event = Event(entry_time_temp,'entry') # time, 0:entry, 1:exit, 2:both, 3:nothing
            elif len(link.entry) == 0 and len(link.remain) == 0: # if nothing to do for this link
                link.next_event = Event(99999,'nothing')
            else: # if there are vehicles inside
                ############################## calculate the next entry time ############################################
                if len(link.entry) != 0: # if there are entry requests
                    entry_time_temp = max(t, link.entry[0].entry_time)
                    next_entry_time = max(entry_time_temp, link.time_entry_supply)
                else: # if there is no entry request
                    next_entry_time = 99999
                ############################## calculate the next exit time ############################################
                exit_time_temp = round(t + link.remain[0].remaining_distance / link.remain[0].v , 2)
                green, wait_time = link.in_green_exit(exit_time_temp)
                if green == False: # if that exit time is in red
                    link.next_exit_seq= 0
                    exit_time_temp = exit_time_temp + wait_time
                next_exit_time = max(exit_time_temp, link.time_exit_supply)
                ############################## determine next event ####################################################
                if len(link.entry) == 0: # if no more entry
                    link.next_event = Event(next_exit_time, 'exit')
                else:
                    if next_entry_time < next_exit_time:
                        link.next_event = Event(next_entry_time, 'entry')
                    elif next_entry_time == next_exit_time:
                        link.next_event = Event(next_entry_time, 'both')
                    else:
                        link.next_event = Event(next_exit_time, 'exit')
        ############################## Find those event links #############################################################
        event_link = []
        next_time_temp = 99999
        for link in object.Links.values():
            if link.next_event.time < next_time_temp:
                event_link = []
                next_time_temp = link.next_event.time
                event_link.append(link)
            elif link.next_event.time == next_time_temp:
                event_link.append(link)
            else:
                pass
        ############################## update time and delta t and time-in_cycle ###########################################
        delta_t = round(next_time_temp - t, 2)
        t = round(t + delta_t, 2)
        ############################## update the remaining distance and segment for every circulating vehicles ###########
        for link in object.Links.values():
            for vehicle in link.remain:
                move_length = 0
                if vehicle.remaining_distance > 0: # remaining distance
                    move_length = min(vehicle.v * delta_t , vehicle.remaining_distance)
                else:
                    move_length = 0
                vehicle.remaining_distance = vehicle.remaining_distance - move_length
        ############################## recording ##########################################################################
        step.append(delta_t)
        time.append(t)
        for link in object.Links.values():
            link.accumulation.append(len(link.remain))
        ############################## read the next event and execute them ###############################################
        for link in event_link:
            if link.next_event.event_type == 'entry': # only new entry, assign a trip length
                veh_interest = link.entry[0]
                veh_interest.remaining_distance = link.link_length
                veh_interest.entry_time = t
                link.remain.append(veh_interest)
                link.previous_entry_all = t
                link.entry.pop(0)
            elif link.next_event.event_type == 'exit': # only exit
                if (link.remain[0].path.id in link.exiting_path.keys()) == False: # have next link
                    next_link = link.remain[0].path.find_next_link(link.id, object.Links)
                    if link.external == True:
                        veh_interest = link.remain[0]
                        veh_interest.remaining_distance = next_link.link_length
                        veh_interest.entry_time = t
                        next_link.remain.append(veh_interest)
                    else:
                        veh_interest = link.remain[0]
                        veh_interest.remaining_distance = next_link.link_length
                        next_link.remain.append(veh_interest)
                    next_link.previous_entry_all = t
                else:
                    link.remain[0].path.finished_trips.append(Trip(t, t-link.remain[0].entry_time))
                link.previous_exit_all= t
                link.next_exit_seq += 1
                link.remain.pop(0)
            elif link.next_event.event_type == 'both':
                # entry
                veh_interest = link.entry[0]
                veh_interest.remaining_distance = link.link_length
                veh_interest.entry_time = t
                link.remain.append(veh_interest)
                link.previous_entry_all = t
                link.entry.pop(0)
                # exit
                if (link.remain[0].path.id in link.exiting_path.keys()) == False: # have next link
                    next_link = link.remain[0].path.find_next_link(link.id, object.Links)
                    if link.external == True:
                        veh_interest = link.remain[0]
                        veh_interest.remaining_distance = next_link.link_length
                        veh_interest.entry_time = t
                        next_link.remain.append(veh_interest)
                    else:
                        veh_interest = link.remain[0]
                        veh_interest.remaining_distance = next_link.link_length
                        next_link.remain.append(veh_interest)
                    next_link.previous_entry_all = t
                else:
                    link.remain[0].path.finished_trips.append(Trip(t, t-link.remain[0].entry_time))
                link.previous_exit_all = t
                link.next_exit_seq += 1
                link.remain.pop(0)
            else:
                pass
            # print('link: ',link.id,', time: ',t,', remain: ',len(link.remain),', situation processed: ',link.next_event.event_type)
        ############################## update hole conditions #############################################################
        for link in object.Links.values():
            if not link.external:
                new_holes_in_link = []
                for hole in link.holes_in_link: # update hole loc
                    hole.location = round(hole.location + delta_t * hole.wave_speed,2)
                    if hole.location < link.length_jam:
                        new_holes_in_link.append(hole) # keep holes that are not done
                link.holes_in_link = new_holes_in_link # remove done holes
                if (link in event_link) == True and (link.next_event.event_type == 'exit' or link.next_event.event_type == 'both'): # add holes if exit
                    link.holes_in_link.append(Hole(0))
        ############################## update entry supply time ###########################################################
        for link in object.Links.values():
            if not link.external:
                if len(link.holes_in_link) > 0: # if there are holes
                    link.spill_num = link.jam_num - len(link.holes_in_link) # update spill num
                    if len(link.remain) >= link.spill_num: # if spill
                        link.temp_time_entry_supply = t + (link.length_jam - link.holes_in_link[0].location) / link.holes_in_link[0].wave_speed # next time of arrival of a hole
                        for upstream_link in link.upstream_links.values():
                            if len(upstream_link.remain) > 0 and upstream_link.in_green_exit(t)[0] == True:
                                if (upstream_link.remain[0].path in upstream_link.exiting_path) == False:
                                    if upstream_link.remain[0].path.find_next_link(upstream_link.id, object.Links) == link:
                                        upstream_link.next_exit_seq = 0
                    else:
                        link.temp_time_entry_supply = -1
                else:
                    if len(link.remain) >= link.jam_num:
                        for upstream_link in link.upstream_links.values():
                            if len(upstream_link.remain) > 0 and upstream_link.in_green_exit(t)[0] == True:
                                if (upstream_link.remain[0].path in upstream_link.exiting_path) == False:
                                    if upstream_link.remain[0].path.find_next_link(upstream_link.id, object.Links) == link:
                                        upstream_link.next_exit_seq = 0
                        link.temp_time_entry_supply = 99999
                    else:
                        link.temp_time_entry_supply = -1
            else:
                link.temp_time_entry_supply = -1
            link.time_entry_supply = round(max(link.temp_time_entry_supply, link.previous_entry_all + MIN_HEADWAY_STRAIGHT), 2)
        ############################## update exit supply time ###############################################################
        for link in object.Links.values():
            if len(link.remain) == 0:
                link.time_exit_supply = -1
            elif (link.remain[0].path.id in link.exiting_path.keys()) == False: # have next link
                next_link = link.remain[0].path.find_next_link(link.id, object.Links) # next link id
                if link.next_exit_seq == 1:
                    link.time_exit_supply = max(link.previous_exit_all + SECOND_HEADWAY, next_link.time_entry_supply)
                elif link.next_exit_seq == 2 and (link.remain[0].path in link.turning_exiting_path) == False:
                    link.time_exit_supply = max(link.previous_exit_all + THIRD_HEADWAY, next_link.time_entry_supply)
                else:
                    if (link.remain[0].path in link.turning_exiting_path) == True:
                        link.time_exit_supply = max(link.previous_exit_all + MIN_HEADWAY_TURN, next_link.time_entry_supply)
                    else:
                        link.time_exit_supply = max(link.previous_exit_all + MIN_HEADWAY_STRAIGHT, next_link.time_entry_supply)
            else:
                if link.next_exit_seq == 1:
                    link.time_exit_supply = link.previous_exit_all + SECOND_HEADWAY
                elif link.next_exit_seq == 2 and (link.remain[0].path in link.turning_exiting_path) == False:
                    link.time_exit_supply = link.previous_exit_all + THIRD_HEADWAY
                else:
                    if (link.remain[0].path in link.turning_exiting_path) == True:
                        link.time_exit_supply = link.previous_exit_all + MIN_HEADWAY_TURN
                    else:
                        link.time_exit_supply = link.previous_exit_all + MIN_HEADWAY_STRAIGHT

        ################################ simulation ended #########################################################

    object.time = time
    object.step = step

    return object










