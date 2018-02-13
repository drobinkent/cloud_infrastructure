import csv
import sys
import numpy as np 
from copy import deepcopy
 
ALGO_MIN_MIN = "min-min"
ALGO_MAX_MIN = "max-min"
ALGO_SUFFERAGE = "sufferage "
min_min_task_machine_mapping = {}
max_min_task_machine_mapping = {}
sufferage_min_task_machine_mapping = {}

def second_smallest(numbers):
    a1, a2 = float('inf'), float('inf')
    i1 = -1
    i2 = -1 
    i=0
    for i in range(len(numbers)):
        if numbers[i] <= a1:
            a1, a2 = numbers[i], a1
            i1 = i
        elif numbers[i] < a2:
            a2 = numbers[i]
            i2 = i
    return a1, a2 , i1 , i2 

def print_data(dt):
    print("Rest of the taks to scheduled")
    for i in range(len(dt)):
        for j in range(len(dt[i])):
            if (dt[i][0] != -1) and (j == 0):
                print("\t", dt[i][j], " , ", end = "")
            elif(dt[i][0] != -1) and (j != len(dt[i])):
                print(dt[i][j]," , ",end="")
            elif (dt[i][0] != -1) and (j == len(dt[i])):
                print(dt[i][j])
            
        if dt[i][0] != -1 :
            print("\n",end="")

def readMyFile(filename="data.csv" ):
    datas = []
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        i=0
        temp = []
        for row in csvReader:
            datas.append(row[0:len(row)])
    stripped_data = datas[1:len(datas)]
    #print (stripped_data)
    return stripped_data


def process_invalid_Data(data, algo):
    new_data = []
    for i in range(len(data)):
        #print("i is ", i )
        new_row = []
        for j in range(len(data[0])):
            #print("j is ", j)
            if algo == ALGO_MIN_MIN and data[i][j] == '-':
                new_row.append(sys.maxsize)
            elif algo == ALGO_MAX_MIN and data[i][j] == '-':
                new_row.append(-sys.maxsize -1)
            else:
                new_row.append(int(data[i][j]))  
        new_data.append(new_row)
    return new_data
    

def get_min_sort_data(data, algo):
    temp = []
    min_data = []
    for i in range(len(data)):
        if data[i][0] == -1:
            continue;
        else:
            minimum = min(data[i][1:len(data[i])]) #first index is task number. so we are skipping that
            machine_idx = data[i].index(minimum) -1  # -1 because first index is for task number
            temp = []
            task_number = i
            temp.append(task_number)
            temp.append(minimum)
            temp.append(machine_idx)
            min_data.append(temp)
    if algo == ALGO_MIN_MIN:
        dt = sorted(min_data, key=lambda x: x[1])
        print("Task --Minimum length time -- on Machine in MIN-MIN sorted format ")
    if algo == ALGO_MAX_MIN:
        dt = sorted(min_data, key=lambda x: x[1],  reverse=True)
        print("Task --Minimum length time -- on Machine in MAX-MIN sorted format ")
    print(dt)
    return dt


def get_min_sufferage_sort_data(data):
    sufrg_data = []
    print("inside get_min_sufferage_sort_data")
    for i in range(len(data)):
        if data[i][0] == -1:
            continue;
        else:
            temp = deepcopy(data[i])
            sorted(temp)
            min_1, min_2, min_1_idx, min_2_idx  = second_smallest(temp[1:len(temp)]) #skip first column becuse it is task id
            sufferage = min_2 - min_1 
            p = [i, sufferage,min_1, min_2, min_1_idx+1, min_2_idx+1 ]
            sufrg_data.append(p)
            # print("Data ", data[i] )
            # print("sfrg: ", p)
    dt = sorted(sufrg_data, key=lambda x: x[1],  reverse=True)
    print ("Sufferge data calculated in format : task -- suffergae -- first minimum-- second minimum -- index of first minimum -- index of second minimum")
    print(dt)
    return dt
   



def update_task_lengths(data,task_number_to_be_deleted, task_length, machine_number):
    data[task_number_to_be_deleted][0] = -1
    for row in data : 
        row[machine_number+1] = row[machine_number+1]+task_length
    return data
    
def update_task_lengths_for_sufferage(data,task_number_to_be_deleted, task_length, machine_number):
    data[task_number_to_be_deleted][0] = -1
    for row in data : 
        row[machine_number] = row[machine_number]+task_length
    return data

def min_min_and_max_minmapping(data, total_tasks, algo):
    dtx = data 
    mapping = {}
    if algo == ALGO_MIN_MIN:
        mapping = min_min_task_machine_mapping
    if algo == ALGO_MAX_MIN:
        mapping = max_min_task_machine_mapping
    for i in range(total_tasks):
        print_data(dtx)
        dt = get_min_sort_data(dtx,algo )
        task = dt[0][0]
        length = dt[0][1]
        machine = dt[0][2]
        print("Task --", task," with time length ", length," is scheduled on Machine ", machine)
        
        
        if machine in mapping:
            l = mapping[machine]
            l.append([task,length])
            mapping[machine] = l
        else:
            l = []
            l.append([task,length])
            mapping[machine] = l
        dtx = update_task_lengths(dtx,task,length, machine  )
    if algo == ALGO_MIN_MIN:
        print("Final Result using Min-Min scheduling in [ Machine : Task , Aggregated length] format is follwoing : ")
        print(mapping)
    if algo == ALGO_MAX_MIN:
        print("Final Result using Max-Min scheduling in [ Machine : Task , Aggregated length] format is follwoing : ")
        print(mapping)
    #print("Final Result using Min-Min scheduling in  Machine : Task , Aggregated length] format is follwoing : ")
    #print(mapping)
        
   
def sufferage_minmapping(data, total_tasks):
    dtx = data 
    mapping = sufferage_min_task_machine_mapping
    
    for i in range(total_tasks):
        print_data(dtx)
        dt = get_min_sufferage_sort_data(dtx)
        task = dt[0][0]
        sufferage = dt[0][1]
        min_1 = dt[0][2]
        min_2 = dt[0][3]
        min_1_idx = dt[0][4]
        min_2_idx = dt[0][5]
        print("Task --", task,"sufferage " , sufferage, " with time length ", min_1," is scheduled on Machine ", min_1_idx-1)
        if min_1_idx in mapping:
            l = mapping[min_1_idx]
            l.append([task,min_1])
            mapping[min_1_idx] = l
        else:
            l = []
            l.append([task,min_1])
            mapping[min_1_idx] = l
        dtx = update_task_lengths_for_sufferage(dtx,task,min_1, min_1_idx  )
    
    print("Final Result using Sufferage scheduling in [ Machine : Task , Aggregated length] format is follwoing : ")
    print(mapping)
    #print("Final Result using Min-Min scheduling in  Machine : Task , Aggregated length] format is follwoing : ")
    #print(mapping)
  

unprocessed_data = readMyFile()
num_of_task = len(unprocessed_data)
num_of_machine = len(unprocessed_data[0])
processed_data = process_invalid_Data(unprocessed_data, ALGO_MIN_MIN)
min_min_and_max_minmapping(processed_data,num_of_task, ALGO_MIN_MIN)


print("\n\n===========================================\n\n")
unprocessed_data = readMyFile()
num_of_task = len(unprocessed_data)
num_of_machine = len(unprocessed_data[0])
processed_data = process_invalid_Data(unprocessed_data, ALGO_MIN_MIN)
min_min_and_max_minmapping(processed_data,num_of_task, ALGO_MAX_MIN)



print("\n\n===========================================\n\n")
unprocessed_data = readMyFile()
num_of_task = len(unprocessed_data)
num_of_machine = len(unprocessed_data[0])
processed_data = process_invalid_Data(unprocessed_data, ALGO_MIN_MIN)
sufferage_minmapping(processed_data,num_of_task)