#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from objects.trip import Trip
from objects.hole import Hole
from config import T, MIN_HEADWAY_STRAIGHT, MIN_HEADWAY_TURN, SECOND_HEADWAY, THIRD_HEADWAY


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
            break
        ############################## find the next link event ########################################################
        for link in object.Links.values():
            link.next_event_time = 99999
            link.next_event = []
            link.possible_event_time = {1:99999,2:99999,3:99999}
            if len(link.entry) > 0: # if there are entry requests (1)
                link.possible_event_time[1] = max(t, link.entry[0].entry_time, link.time_entry_supply)
            if len(link.remain) > 0: # if there are exit requests (2)
                exit_time_temp = max(t, link.remain[0].link_exit_time, link.time_exit_supply)
                green, wait_time = link.in_green_exit(exit_time_temp)
                if green == False:
                    link.next_exit_seq= 0
                    link.possible_event_time[2] = exit_time_temp + wait_time
                else:
                    link.possible_event_time[2] = exit_time_temp
            if link.external == False:
                if len(link.holes_in_link) > 0: # if there are holes traveling, the next arrival (3)
                    link.possible_event_time[3] = link.holes_in_link[0].link_arrival_time
            ############################## determine next event ########################################################
            link.next_event_time = min([link.possible_event_time[e] for e in link.possible_event_time.keys()])
            for e in link.possible_event_time.keys():
                if link.possible_event_time[e] == link.next_event_time:
                    link.next_event.append(e)
        ############################## Find those event links ##########################################################
        event_link = []
        next_event_time_all_temp = 99999
        for link in object.Links.values():
            if link.next_event_time < next_event_time_all_temp:
                event_link = []
                next_event_time_all_temp = link.next_event_time
                event_link.append(link)
            elif link.next_event_time == next_event_time_all_temp:
                event_link.append(link)
            else:
                pass
        ############################## update time and delta t and time-in_cycle ###########################################
        if next_event_time_all_temp > T:
            break
        delta_t = round(next_event_time_all_temp - t, 2)
        t = round(t + delta_t, 2)
        ############################## recording ##########################################################################
        step.append(delta_t)
        time.append(t)
        for link in object.Links.values():
            link.accumulation.append(len(link.remain))
        ############################## read the next event and execute them ###############################################
        for link in event_link:
            if (1 in link.next_event) == True: # entry
                veh_interest = link.entry[0]
                veh_interest.link = link
                veh_interest.calculate_link_exit_time(t)
                veh_interest.entry_time = link.entry[0].entry_time
                link.remain.append(veh_interest)
                link.previous_entry_all = t
                link.entry.pop(0)
            if (2 in link.next_event) == True: # exit
                if (link.remain[0].path.id in link.exiting_path.keys()) == False:  # have next link
                    next_link = link.remain[0].path.find_next_link(link.id, object.Links)
                    veh_interest = link.remain[0]
                    next_link.remain.append(veh_interest)
                    veh_interest.link = next_link
                    veh_interest.calculate_link_exit_time(t)
                    next_link.previous_entry_all = t
                else:
                    link.remain[0].path.finished_trips.append(Trip(t, t - link.remain[0].entry_time))
                link.previous_exit_all = t
                link.next_exit_seq += 1
                if link.external == False:
                    link.holes_in_link.append(Hole(link, t))
                link.remain.pop(0)
            if (3 in link.next_event) == True: # hole arrive
                link.holes_in_link.pop(0)
            # print('link: ',link.id,', time: ',t,', remain: ',len(link.remain),', situation processed: ',link.next_event.event_type)
        ############################## update entry supply time ########################################################
        for link in object.Links.values():
            if not link.external:
                if len(link.holes_in_link) > 0:  # if there are holes
                    link.spill_num = link.jam_num - len(link.holes_in_link)  # update spill num
                    if len(link.remain) >= link.spill_num:  # if spill
                        link.temp_time_entry_supply =  link.holes_in_link[0].link_arrival_time # next time of arrival of a hole
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
            link.time_entry_supply = round(
                max(link.temp_time_entry_supply, link.previous_entry_all + MIN_HEADWAY_STRAIGHT), 2)
        ############################## update exit supply time #########################################################
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
        ################################ simulation ended ##############################################################
    object.time = time
    object.step = step
    return object
