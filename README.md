# Cloud_infrastructure
Assignments of cloud_infrastrcuture course 


# Maekawa folder contains code for Maekawa algorithm. 
  This folder has 4 python files
  
    1) mm.py this is the file where execution starts. Here you can change the value of variable "n" to change the number of process you want to simulate
    
    2) constant.py contaiins declaration of some constant
    
    3) Simulator.py contains code to simulate mutual exclusion request and release events by the processes.
    
    4) mk_process.py this file has 2 threads and one class. procThread class simulates behavior of a process. It first thread simulates message reciver behaviour from other classes. and another thread simulates mutual exclusion request and release event of a process
    
    
 #   How to Run
 
 $ python3 mm.py
    
# Schedulng folder

This folder contains implementation of 

a) Min-Min b) Max-Min c) Sufferage scheduling algorithm 

all the 3 algo's are implemented in mk.py file. it uses data.csv file's data 

# How to tun

$python3 mk.py

It will show you on which machines all the tasks are asigned and why they are assigned with details explanation. A sample outout is listed in out.txt file 
