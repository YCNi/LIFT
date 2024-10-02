# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 11:40:53 2024

@author: yingni
"""

def LIFT(T,
         L,EL,
         v,w,min_interval_s,min_interval_t,second_interval,third_interval,
         L_jam,jam_num,
         path,In,p_end,p_exit_turn,
         cycle,start_in_cycle_exit,green_exit,
         entry,):
    # Initialize all the variables
    remain = {} # the remaining vehicles on each link with their information
    for i in L:
        remain[i] = [] # id, remaining distance, path type, entry time
    next_event = {}
    for i in L:
        next_event[i] = None # time, 0:entry, 1:exit, 2:both
    entry_time_supply = {}
    entry_time_supply_temp = {}
    for i in L:
        entry_time_supply[i] = -1
        entry_time_supply_temp[i] = -1
    exit_time_supply = {}
    for i in L:
        exit_time_supply[i] = -1
    previous_entry_all = {}
    for i in L:
        previous_entry_all[i] = -1
    previous_exit_all = {}
    for i in L:
        previous_exit_all[i] = -1
    accum_link = {}
    for i in L:
        accum_link[i] = []
    step = []
    time = []
    TT = [] # finished trip: finish time, travel time, path
    def find_next_link(path_id,link_id):
        next_link_order = 0
        for i in range(len(path[path_id])):
            if link_id == path[path_id][i]:
                next_link_order = i+1
                break
            else:
                pass
        return path[path_id][next_link_order]
    def in_green_exit(request_time, link):
        in_green = False
        delay = 0
        if (start_in_cycle_exit[link] + request_time) % cycle <= green_exit[link]:
            in_green = True
        else:
            delay = round(cycle - (start_in_cycle_exit[link] + request_time) % cycle,2)
        return [in_green,delay]
    hole_loc = {} # list, add when one exit
    num_pop_hole = {}
    for i in L:
        if (i in EL) == False:
            hole_loc[i] = []
    spill_num = {} # dynamic variable
    next_exit_seq = {}
    for i in L:
        next_exit_seq[i] = 0
    t = 0
    delta_t = 0
    # Run the simulation
    while t <= T:
        #print('-------------------- new event --------------------')
        if sum([len(entry[i]) for i in L]) == 0 and sum([len(remain[i]) for i in L]) == 0:
            break
        ############################## find the next link event ##########################################################
        for i in L:
            if len(entry[i]) > 0 and len(remain[i]) == 0: # if no vehicle inside and there are entry requests
                entry_time_temp = max(t,entry[i][0][0])
                next_event[i] = [entry_time_temp,0] # time, 0:entry, 1:exit, 2:both, 3:nothing
            elif len(entry[i]) == 0 and len(remain[i]) == 0: # if nothing to do for this link
                next_event[i] = [99999,3]
            else: # if there are vehicles inside
                ############################## calculate the next entry time ############################################
                if len(entry[i]) != 0: # if there are entry requests
                    entry_time_temp = max(t,entry[i][0][0])
                    next_entry_time = max(entry_time_temp , entry_time_supply[i])
                else: # if there is no entry request
                    next_entry_time = 99999
                ############################## calculate the next exit time ############################################
                exit_time_temp = round(t + remain[i][0][1] / remain[i][0][4] , 2)
                green, wait_time = in_green_exit(exit_time_temp,i)
                if green == False: # if that exit time is in red
                    next_exit_seq[i] = 0
                    exit_time_temp = exit_time_temp + wait_time
                next_exit_time = max(exit_time_temp , exit_time_supply[i])
                ############################## determine next event ####################################################
                if len(entry[i]) == 0: # if no more entry
                    next_event[i] = [next_exit_time,1]
                else:
                    if next_entry_time < next_exit_time:
                        next_event[i] = [next_entry_time,0]
                    elif next_entry_time == next_exit_time:
                        next_event[i] = [next_entry_time,2]
                    else:
                        next_event[i] = [next_exit_time,1]
        ############################## Find those event links #############################################################
        event_link = []
        next_time_temp = 99999
        for i in L:
            if next_event[i][0] < next_time_temp:
                event_link = []
                next_time_temp = next_event[i][0]
                event_link.append(i)
            elif next_event[i][0] == next_time_temp:
                event_link.append(i)
            else:
                pass
        ############################## update time and delta t and time-in_cycle ###########################################
        delta_t = round(next_time_temp - t,2)
        t = round(t + delta_t,2)
        ############################## update the remaining distance and segment for every circulating vehicles ###########
        # Do not keep updating remaining distance, if smaller than 0, = 0
        for i in L:
            for veh in remain[i]:
                move_length = 0
                if veh[1] > 0: # remaining distance
                    move_length = min(veh[4] * delta_t , veh[1])
                else:
                    move_length = 0
                veh[1] = veh[1] - move_length
        ############################## recording ##########################################################################
        step.append(delta_t)
        time.append(t)
        for i in L:
            accum_link[i].append(len(remain[i]))
        ############################## read the next event and execute them ###############################################
        for i in event_link:
            if next_event[i][1] == 0: # only new entry, assign a trip length
                remain[i].append([entry[i][0][1],L[i],entry[i][0][2],t,v]) # id, remaining distance, path type, entry time, speed
                previous_entry_all[i] = t
                entry[i].pop(0)
            elif next_event[i][1] == 1: # only exit
                if (remain[i][0][2] in p_end[i]) == False: # have next link
                    j = find_next_link(remain[i][0][2],i) # next link id
                    if (i in EL) == True:
                        remain[j].append([remain[i][0][0],L[j],remain[i][0][2],t,v]) # id, remaining distance, path type, entry time, speed
                    else:
                        remain[j].append([remain[i][0][0],L[j],remain[i][0][2],remain[i][0][3],v]) # id, remaining distance, path type, entry time, speed
                    previous_entry_all[j] = t
                else:
                    TT.append([t,t - remain[i][0][3],remain[i][0][2]])
                previous_exit_all[i] = t
                next_exit_seq[i] += 1
                remain[i].pop(0)
            elif next_event[i][1] == 2:
                # entry
                remain[i].append([entry[i][0][1],L[i],entry[i][0][2],t,v]) # id, remaining distance, path type, entry time, speed
                previous_entry_all[i] = t
                entry[i].pop(0)
                # exit
                if (remain[i][0][2] in p_end[i]) == False: # have next link
                    j = find_next_link(remain[i][0][2],i) # next link id
                    if (i in EL) == True:
                        remain[j].append([remain[i][0][0],L[j],remain[i][0][2],t,v]) # id, remaining distance, path type, entry time, speed
                    else:
                        remain[j].append([remain[i][0][0],L[j],remain[i][0][2],remain[i][0][3],v]) # id, remaining distance, path type, entry time, speed
                    previous_entry_all[j] = t
                else:
                    TT.append([t,t - remain[i][0][3],remain[i][0][2]])
                previous_exit_all[i] = t
                next_exit_seq[i] += 1
                remain[i].pop(0)
            else:
                pass
            #print('link: ',i,', time: ',t,', remain: ',len(remain[i]),', den: ',round(len(remain[i])/(L_jam[i]/1000),1),', situation processed: ',next_event[i][1])
        ############################## update hole conditions #############################################################
        for i in L:
            if (i in EL) == False:
                num_pop_hole[i] = 0
                for j in range(len(hole_loc[i])): # update hole loc
                    hole_loc[i][j] = round(hole_loc[i][j] + delta_t * w,2)
                    if hole_loc[i][j] >= L_jam[i]:
                        num_pop_hole[i] += 1
                # remove done holes
                for j in range(num_pop_hole[i]):
                    hole_loc[i].pop(0)
                # add holes if exit
                if (i in event_link) == True and (next_event[i][1] == 1 or next_event[i][1] == 2):
                    hole_loc[i].append(0)
                #print('link: ',i,' hole loc: ',hole_loc[i])
        ############################## update entry supply time ###########################################################
        for i in L:
            if (i in EL) == False:
                if len(hole_loc[i]) > 0: # if there are holes
                    spill_num[i] = jam_num[i] - len(hole_loc[i]) # update spill num
                    if len(remain[i]) >= spill_num[i]: # if spill
                        entry_time_supply_temp[i] = t + (L_jam[i] - hole_loc[i][0]) / w # next time of arrival of a hole
                        #print('link: ',i,' is spilled, remain: ',len(remain[i]),', extra delay: ',round((L_jam[i] - hole_loc[i][0]) / w,2))
                        for j in In[i]:
                            if len(remain[j]) > 0 and in_green_exit(t,j)[0] == True:
                                if (remain[j][0][2] in p_end[j]) == False:
                                    if find_next_link(remain[j][0][2],j) == i:
                                        next_exit_seq[j] = 0
                                        #print('next exit veh on link ',j,' is blocked.')
                    else:
                        entry_time_supply_temp[i] = -1
                else:
                    if len(remain[i]) >= jam_num[i]:
                        #print('link: ',i,' is jammed.')
                        for j in In[i]:
                            if len(remain[j]) > 0 and in_green_exit(t,j)[0] == True:
                                if (remain[j][0][2] in p_end[j]) == False:
                                    if find_next_link(remain[j][0][2],j) == i:
                                        next_exit_seq[j] = 0
                                        #print('next exit veh on link ',j,' is blocked.')
                        entry_time_supply_temp[i] = 99999
                    else:
                        entry_time_supply_temp[i] = -1
            else:
                entry_time_supply_temp[i] = -1
            entry_time_supply[i] = round(max(entry_time_supply_temp[i],previous_entry_all[i] + min_interval_s),2)
        ############################## update exit supply time ###############################################################
        for i in L:
            if len(remain[i]) == 0:
                exit_time_supply[i] = -1
            elif (remain[i][0][2] in p_end[i]) == False: # have next link
                j = find_next_link(remain[i][0][2],i) # next link id
                if next_exit_seq[i] == 1:
                    exit_time_supply[i] = max(previous_exit_all[i] + second_interval , entry_time_supply[j])
                elif next_exit_seq[i] == 2 and (remain[i][0][2] in p_exit_turn[i]) == False:
                    exit_time_supply[i] = max(previous_exit_all[i] + third_interval , entry_time_supply[j])
                else:
                    if (remain[i][0][2] in p_exit_turn[i]) == True:
                        exit_time_supply[i] = max(previous_exit_all[i] + min_interval_t , entry_time_supply[j])
                    else:
                        exit_time_supply[i] = max(previous_exit_all[i] + min_interval_s , entry_time_supply[j])
            else:
                if next_exit_seq[i] == 1:
                    exit_time_supply[i] = previous_exit_all[i] + second_interval
                elif next_exit_seq[i] == 2 and (remain[i][0][2] in p_exit_turn[i]) == False:
                    exit_time_supply[i] = previous_exit_all[i] + third_interval
                else:
                    if (remain[i][0][2] in p_exit_turn[i]) == True:
                        exit_time_supply[i] = previous_exit_all[i] + min_interval_t
                    else:
                        exit_time_supply[i] = previous_exit_all[i] + min_interval_s
    return TT, accum_link, time, step
