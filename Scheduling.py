import web_scrubbing as ws
import numpy as np
import datetime



def int2time(integer):
    ''' Documentation:
        function that converts a decimal value to a time structured d:hr:min converted based on minutes
        Assumption:
        - 0 = Monday:00:00
        - 1 = Monday:00:01
        - 1440 = Tuesday:00:00
        - 7199 = Friday:23:59

        input:
        - integer = integer value with units in min

        output:
        - result = tuple in form (day,hour,min)
    '''

    return


def days2interval(days,times):
    ''' Documentation:
        function that takes in days and times and converts it into a time interval with units of min
        multiple intervals for multple days


        inputs:
        - days = list of strings abreviations for days of the set {'M','T','W','R','F'}
        - times = string of time interval 'hr:min am - hr:min pm'

        output:
        - result = list of intervals as tuples [(0,1),(1440,1490),...] 
    '''
    interval = times.split(' - ')

    start_t = datetime.datetime.strptime(interval[0],'%I:%M%p')
    start = (start_t - datetime.datetime(1900,1,1)).total_seconds()/60

    end_t = datetime.datetime.strptime(interval[1],'%I:%M%p')
    end = (end_t - datetime.datetime(1900,1,1)).total_seconds()/60

    result = []
    d_dict = {'M':0,'T':1440,'W':2880,'R':4320,'F':5760}
    for day in days:
        d = d_dict[day]

        result.append((start+d,end+d)) 

    return result

# - test of days2interval - #
    # d2i = days2interval(['M','W','F'],'10:10am - 11:00am')
    # print(d2i)

# - datetime tests - #
    # time = '3:45pm'

    # t = datetime.datetime.strptime(time,'%I:%M%p')
    # print(t.strftime('%H:%M%p'))
    # print(t)
    # delta = t-datetime.datetime(1900,1,1)
    # print(delta.total_seconds()/60)

    # tt = '2:40pm - 3:30pm'

    # print(tt.split(' - '))


def conflictCheck(s,n):
    '''
    Function to check if there are any conflicts between the current schedule and the new classes

    Returns False if there are no conflicts True if there is at least one conflict

    inputs:
     - s = schedule that has already been created, list
     - n = list of intervals to be added to the schedule
    '''

    for sec in s:
        for interval in n:
            if interval[0] < sec[1] and interval[1] > sec[0]:
                return True
    return False

def getClassIntervals(sections):
    intervals = []

    for section in sections:
        sec = days2interval(section['days'],section['time'])
        intervals.extend(sec)

    return intervals

def scheduler():

    classes = ws.WS_main()
    
    #make a big list of all sections
        # secs = []
        # necessary_types = []
        # all_intervals = []
        # for c in classes:
        #     sections4c = c['sections']
        #     for key in sections4c.keys():
        #         priority = len(sections4c[key])
        #         for s in sections4c[key]:
        #             name = c['code'] + ': ' + s['number']
        #             intervals = days2interval(s['days'],s['time'])
        #             typ = c['code'] + ': ' + key
        #             secs.append((name,priority,intervals,typ))
        #             if typ not in necessary_types:
        #                 necessary_types.append(typ)

        # print(secs)
        # print(necessary_types)


        # print(c)
        # print(classes)

    return


def nextCombo(current,maximum):
    '''
    Function that iterates the indices of each type of section in a dictionary to get a new combination
    Returns -1 if there are no more combinations left

    inputs:
     - current = dict that contains the current indicies of the sections to be iterated
     - maximum = dict that contains the number of sections each type contains for this course

    output:
     - either returns current iterated by one combination or -1

    '''
    num = len(current) 
    keys_list = list(current.keys()) 

    current[keys_list[num-1]] = current[keys_list[num-1]] + 1 # iterate last section type
    
    okay = False
    carry = False
    while not okay:
        for i in range(num): ##can maybe change to backwards loop

            if current[keys_list[i]] >= maximum[keys_list[i]]: # iterated past the max of the section 
                current[keys_list[i]] = 0
                if (i-1) < 0 : # went through all the combinations
                    return -1

                else: 
                    current[keys_list[i-1]] = current[keys_list[i-1]] + 1
                    carry = True #added 1 to next section type (need to check if overflow)

        if carry == False:
            okay = True

    return current

def recScheduler(current,classes,index,current_names):
    '''
    Function (used recursively) that takes a list of classes and tries to create a schedule
    Uses a Depth First Search esque method by resursively going through each class in the list.   
    '''
    test_mode = False

    # -- grab class to add -- #
    new_class = classes[index]
    
    secs = new_class['sections']

    sec_totals = dict()
    sec_counters = dict()
    for t in secs.keys():
        sec_totals[t] = len(secs[t])
        sec_counters[t] = 0

    # print(secs)
    # print(sec_totals)

    num_types = len(sec_totals)
    

    worked = False
    while worked == False:   
        # -- Getting the intervals for this class -- #
        new_intervals = []
        new_sections = []
        for key,ind in sec_counters.items():
            intervals = days2interval(secs[key][ind]['days'],secs[key][ind]['time'])
            new_sections.append(new_class['code'] + ': ' + secs[key][ind]['number'])
            new_intervals.extend(intervals)                                                     ### Do something with this ###

        # -- Checking if the intervals conflict with the current schedule -- #
        conflict = conflictCheck(current,new_intervals)

        if test_mode:
            if conflict:
                print('there is a conflict')
            else:
                print('no conflict -- Adding class')
        
        if not conflict:

            temp_intervals = [] #temporarily create a schedule with the new sections
            temp_intervals.extend(current)
            temp_intervals.extend(new_intervals)

            temp_sections = []
            temp_sections.extend(current_names)
            temp_sections.extend(new_sections)
            
            # -- recursion -- #
            if index < len(classes)-1: # this is not the last class in the list
                # print('recursion', index)
                next_intervals,next_sections = recScheduler(temp_intervals,classes,index+1,temp_sections)
                if next_intervals == -1: # if it could not schedule the next class(es)
                    worked = False
                    sec_counters = nextCombo(sec_counters,sec_totals) # increment sections
                    if sec_counters == -1:
                        break
                    # if no sec_counters left break

                else: # recursion returned a schedule
                    result = new_intervals
                    result.extend(next_intervals)

                    result_sections = new_sections
                    result_sections.extend(next_sections)
                    if index == 0 and current != []:
                        current.extend(result)
                        current_names.extend(result_sections)
                        return current,current_names
                    return result,result_sections

            else: # last class to schedule (no recursion)
                worked = True ## possibly redundant
                if index == 0 and current != []:
                        current.extend(new_intervals)
                        current_names.extend(new_sections)
                        return current,current_names
                return new_intervals,new_sections


        else: # there was a conflict
            worked = False
            sec_counters = nextCombo(sec_counters,sec_totals)
            # - if we tried every combination - #
            if sec_counters == -1:
                break
                

    if worked: ##possibly redundant
        print('I used this!')
        return current,current_names

    # - if 'worked' is false after the while loop that means every combo was tried - #
    else:
        return -1,-1



# classes = ws.WS_main()
# first = classes[0]
# [(880.0, 890.0),(2320.0,2330.0),(3760.0,3770.0)]
# i,s = recScheduler([],classes,0,[]) 
# print(i)
# print()
# print(s)
