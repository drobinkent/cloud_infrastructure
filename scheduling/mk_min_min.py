import csv
import sys
import numpy as np 
 
ALGO_MIN_MIN = "min-min"
ALGO_MAX_MIN = "max-min"
ALGO_SUFFERAGE = "sufferage "
min_min_task_machine_mapping = {}
max_min_task_machine_mapping = {}
sufferage_min_task_machine_mapping = {}

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

def update_task_lengths(data,task_number_to_be_deleted, task_length, machine_number):
    data[task_number_to_be_deleted][0] = -1
    for row in data : 
        #print("old ",row[machine_number+1])
        row[machine_number+1] = row[machine_number+1]+task_length
        #print("new ",row[machine_number+1])

    return data
    
def min_min_mapping(data, total_tasks, algo):
    dtx = data 
    for i in range(total_tasks):
        print_data(dtx)
        dt = get_min_sort_data(dtx,algo )
        task = dt[0][0]
        length = dt[0][1]
        machine = dt[0][2]
        print("Task --", task," with time length ", length," is scheduled on Machine ", machine)
        mapping = {}
        if algo == ALGO_MIN_MIN:
            mapping = min_min_task_machine_mapping
        if algo == ALGO_MAX_MIN:
            mapping = max_min_task_machine_mapping
        if machine in mapping:
            l = mapping[machine]
            l.append([task,length])
            mapping[machine] = l
        else:
            l = []
            l.append([task,length])
            mapping[machine] = l
        dtx = update_task_lengths(dtx,task,length, machine  )
    print("Final Result using Min-Min scheduling in  Machine : Task , Aggregated length] format is follwoing : ")
    print(mapping)
        
   


unprocessed_data = readMyFile()
num_of_task = len(unprocessed_data)
num_of_machine = len(unprocessed_data[0])
processed_data = process_invalid_Data(unprocessed_data, ALGO_MIN_MIN)
min_min_mapping(processed_data,num_of_task, ALGO_MIN_MIN)