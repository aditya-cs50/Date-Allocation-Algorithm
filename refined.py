# who has done which type of day in the previous month

# ensure the lists are mutually exclusive (each person belongs to only 1 list)
# ensure the lists, when combined, have the names of everyone
# put ASICs under dn_wknd, not dn_wkday
dn_wknd = ["PTE EUGENE (HQ)","LCP CHING KAI (HQ)","LCP ERNEST (HQ)","PTE JINGZE (A)","CPL ADRIAN (A)","CPL XINBO (A)","PTE WINSON (B)","LCP DARYL (HQ)","PTE CHRISTIAN (HQ)"]
dn_fri = ["PTE YANNIAN (HQ)","LCP ELIAS (B)","PTE SRI (C)"]
dn_wkday = ["PTE MIN QUAN (B)","LCP JUN LONG (ME)","LCP AVIER (HQ)","CPL LEONARD (B)","PTE HAIKAL (HQ)","PTE RUSYAIDI (HQ)","PTE SHAFIQ (HQ)","PTE EDMUND (C)"]

# put ASICs in the following list also. 
# Only if it is possible, it will remove them from weekends and fridays for MAIN DC only (not RESERVE DC)
dont_give_wknd_or_fri = ["LCP CHING KAI (HQ)", "PTE EUGENE (HQ)"]

#for the month you are planning for, input weekend dates, friday dates, number of days in month and name of blockout date csv file

no_wknd = [4,11,18,25,5,12,19,26]
no_fri = [3,10,17,24]
no_days_in_month = 28

"""
no_wknd = [1,2,3,4,5]
no_fri = [6,7]
no_days_in_month = 8
"""
csv_name = "DC Blockout Dates (Jan 23).csv"


# NO NEED TO EDIT THE REST

import csv
from helper import function
from collections import OrderedDict
from copy import deepcopy
import random
from math import ceil
#import matplotlib.pyplot as plt

names = list(set(dn_wknd+dn_fri+dn_wkday)) 

#creating list of days, and sets for weekends, weekdays and fridays
days = []
for i in range(no_days_in_month):
    days.append(str(i+1))
    
weekends = set([str(x) for x in no_wknd])
fridays = set([str(x) for x in no_fri])
weekdays = set([i for i in days if int(i) not in no_wknd+no_fri])


dictionary = function(dn_wknd, dn_fri, dn_wkday, no_wknd, no_fri, no_days_in_month, dont_give_wknd_or_fri)
can_do = {}

for name in dictionary["do_wkday"]:
    try:
        can = can_do[name]
        can_do[name].update(weekdays)
    except:
        can_do[name] = weekdays

for name in dictionary["do_fri"]:
    try:
        can = can_do[name]
        can_do[name].update(fridays)
    except:
        can_do[name] = fridays


for name in dictionary["do_wknd"]:
    try:
        can = can_do[name]
        can_do[name].update(weekends)
    except:
        can_do[name] = weekends

# update can_do by removing blockout dates
with open(csv_name, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        name = row[1]
        dates = row[2]
        format_dates = dates.split(', ')
        try:
            can_do[name] = can_do[name] - set(format_dates)
        except:
            continue

allocation = OrderedDict()
for element in names:
    allocation[element] = set()

x = []
days_copy = deepcopy(days)
can_do_copy = deepcopy(can_do)

no_wkdays = no_days_in_month - len(weekends) - len(fridays)
no_people_doing_weekdays = len(dictionary["do_wkday"])
a = ceil(no_wkdays/no_people_doing_weekdays)

while len(days) !=0:
    random.shuffle(names)
    allocation = OrderedDict()
    for element in names:
        allocation[element] = set()
    days = deepcopy(days_copy)
    can_do = deepcopy(can_do_copy)
    # a is the maximum number of duties that should be allocated to a person. number should be round up value of no_wkdays/no_people_doing_weekdays 
    for i in range(a):
        for element in names:
            for day in days:
                try:
                    if day in can_do[element]:
                        allocation[element].update({day})
                        days.remove(day)
                        can_do[element] = can_do[element] - {str(int(day)+1),str(int(day)-1)}
                        if day in weekends or day in fridays:
                            can_do[element] = can_do[element]-weekends-fridays
                        break
                except:
                    continue
    x.append(len(days))

print("Main DC:\n")
dic = OrderedDict(sorted(allocation.items()))
for element in dic:
    print(f"{element}: {str(allocation[element])}")
print("\n")

#RESERVE
can_do = {}
days = []

for i in range(no_days_in_month):
    days.append(str(i+1))

dn_wknd = []
dn_fri = []
dn_wkday =[] 

for name in allocation:
    if allocation[name] == set():
        dn_wkday.append(name)        
    for element in allocation[name]:
        if element in fridays:
            dn_fri.append(name)
        elif element in weekends:
            dn_wknd.append(name)
        else:
            dn_wkday.append(name)
            
dn_wkday = list(set(dn_wkday))

dictionary = function(dn_wknd, dn_fri, dn_wkday, no_wknd, no_fri, no_days_in_month, [])

can_do = {}

for name in dictionary["do_wkday"]:
    try:
        can = can_do[name]
        can_do[name].update(weekdays)
    except:
        can_do[name] = weekdays

for name in dictionary["do_fri"]:
    try:
        can = can_do[name]
        can_do[name].update(fridays)
    except:
        can_do[name] = fridays


for name in dictionary["do_wknd"]:
    try:
        can = can_do[name]
        can_do[name].update(weekends)
    except:
        can_do[name] = weekends

# update can_do by removing blockout dates
with open(csv_name, "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        name = row[1]
        dates = row[2]
        format_dates = dates.split(', ')
        try:
            can_do[name] = can_do[name] - set(format_dates)
        except:
            continue

#won't be allocated reserve on same day +- 1 day, where you are main DC
for name in can_do:
    temp_set = set()
    for element in allocation[name]:
        temp_set.update({str(int(element) + 1), str(int(element) - 1)})
    can_do[name] = can_do[name] - allocation[name] - temp_set


allocation = OrderedDict()
for element in names:
    allocation[element] = set()

y = []
can_do_copy = deepcopy(can_do)
days_copy = deepcopy(days)

no_people_doing_weekdays = len(dictionary["do_wkday"])
b = ceil(no_wkdays/no_people_doing_weekdays)

while len(days) !=0:
    random.shuffle(names)
    allocation = OrderedDict()
    for element in names:
        allocation[element] = set()
    days = deepcopy(days_copy)
    can_do = deepcopy(can_do_copy)
    # b is the maximum number of duties that should be allocated to a person
    for i in range(b):
        for element in names:
            for day in days:
                try:
                    if day in can_do[element]:
                        allocation[element].update({day})
                        days.remove(day)
                        can_do[element] = can_do[element] - {str(int(day)+1),str(int(day)-1)}
                        if day in weekends or day in fridays:
                            can_do[element] = can_do[element]-weekends-fridays
                        break
                except:
                    continue
    y.append(len(days))
        

print("Reserve DC:\n")
dic = OrderedDict(sorted(allocation.items()))
for element in dic:
    print(f"{element}: {str(allocation[element])}")


#for debugging

"""
# dictionary of date : people who can do on that date, sorted from dates with least people to most people
counts = {}
counts_names = {}

for i in range(31):
    counts[str(i+1)] = 0
    counts_names[str(i+1)] = []

for day in days:
    for element in can_do:
        if day in can_do[element]:
            counts[day] += 1
            counts_names[day].append(element)

counts_new = []

for element in counts:
    counts_new.append(counts[element])
counts_new.sort()

new_dict = {}

for element in counts_new:
    for x in counts:
        if counts[x] == element:
            new_dict[x] = counts_names[x] #counts_new[x]
            
#print(new_dict, len(new_dict))
"""

"""
# dictionary of names against number of days that name can do
numbers = []
for name in can_do:
    numbers.append(len(can_do[name]))
numbers.sort()

new_names = {}

for number in numbers:
    for name in names:
        if len(can_do[name]) == number:
            new_names[name] = number
            names.remove(name)
            break
print(new_names, len(new_names))
"""

