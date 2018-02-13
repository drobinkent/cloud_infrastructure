import threading
import time
import queue
from random import *
import math 
import constants
import time 

class eventSimulator (threading.Thread):
    def __init__(self, threadID, name, number_of_processes, threads ):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.number_of_processes = number_of_processes
      self.voting_set_size = math.ceil(math.sqrt(number_of_processes))
      self.threads = threads

    def run(self):
      print ("Starting " + self.name)
      print("Create a method that will create a random rrquest event and will put in process's queue")
      while True:
          x = randint(0, self.voting_set_size-1)
          y = randint(0, self.voting_set_size-1)
          self.threads[x][y].simulation_msg_queue.put(constants.EVENT_CS_REQ, block = True)
          time.sleep(25)
          self.threads[x][y].simulation_msg_queue.put(constants.EVENT_CS_REL, block = True)
          time.sleep(constants.DELAY_IN_CS_REQ_CREATION)
      return

    