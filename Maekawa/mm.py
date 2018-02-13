import threading
import time
import mk_processs as mkp
import math
import Simulator as sim

N = 16
K = 4 
threads = [] # list for storing all threads. each thared for one process
threadlocks = [] # list for storing locks for all threads. lock to control synchronous read wrtie in buffer of each process


def create_processes(number_of_processes):
    print(math.sqrt(number_of_processes) )
    print(math.ceil(math.sqrt(number_of_processes)))
    voting_set_size = math.ceil(math.sqrt(number_of_processes))
    for i in range(voting_set_size):
        temp_thrd_list = []
        for j in range(voting_set_size):
            id = i*voting_set_size+j
            temp_thrd_list.append(mkp.procThread(id, "Process-"+str(id), i, j, threads,voting_set_size))
        threads.append(temp_thrd_list)
    simulator_thread = sim.eventSimulator(N+1, "simulator", number_of_processes, threads)
    
    for i in range(voting_set_size):
        for j in range(voting_set_size):
            threads[i][j].start()
    simulator_thread.start()

    for i in range(voting_set_size):
        for j in range(voting_set_size):
            threads[i][j].join()
    simulator_thread.join()
    



create_processes(N)



