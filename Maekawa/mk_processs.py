import threading
import time
import queue
import constants

class procThread (threading.Thread):
  
    def __init__(self, threadID, name, row, column, threads, voting_set_size ):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.rcv_msg_queue = queue.Queue(1000)
      self.simulation_msg_queue = queue.Queue(1000)
      self.msg_buffer = queue.Queue(1000)
      self.row = row
      self.column = column
      self._state = constants.RELEASED
      self._heldCondition = threading.Condition()
      self._voted = False
      self.threads = threads
      self._my_votes = 0
      self._voting_set_size = 2*voting_set_size-1


    def handle_internal_event_loop(self): #this method works like the internal life of a process
          print(self.name + "-- internal worker thread starting....")
          while True:
                if self._state == constants.RELEASED : 
                  event = self.simulation_msg_queue.get(block = True)
                  if event == constants.EVENT_CS_REQ :
                        print(self.name , " -- Requesting to access Critical Section."  )
                        self._state = constants.WANTED
                        for i in range(len(self.threads)):
                              for j in range(len(self.threads[i])):
                                    if i == self.row or j == self.column:
                                          self.threads[i][j].rcv_msg_queue.put([constants.MSG_CS_ACCESS_WANTED,self.row,self.column])
                                          print("Thread -", self.row,",",self.column," sending WANTED msg to ",i, j, " | q size ",self.threads[i][j].rcv_msg_queue.qsize() )
                    
                elif  self._state != constants.RELEASED :
                  self._heldCondition.acquire()
                  if self._my_votes < self._voting_set_size :
                        print(self.name, " Still not recieved enough vote to enter CS. only ",self._my_votes)
                        self._heldCondition.wait()
                        continue
                  if self._my_votes ==self._voting_set_size :
                        self._state=constants.HELD
                        print(self.name," ACCESS to CS granted")
                        self._my_votes = 0
                  self._heldCondition.notify()
                  self._heldCondition.release()  
                  print("Condition released")  
                elif self._state == constants.HELD : 
                  event = self.simulation_msg_queue.get(block = True)
                  if event == constants.EVENT_CS_REL :
                        print(self.name," CS ACCESS is being released")
                        self._state = constants.RELEASED
                        for i in range(len(self.threads)):
                              for j in range(len(self.threads[i])):
                                    if i == self.row:
                                          print("Thread -", self.row,",",self.column," sending RELEASE msg to ",i, j)
                                          self.threads[i][j].rcv_msg_queue.put([constants.MSG_CS_ACCESS_RELEASED,self.row,self.column])
                                    if j == self.column:
                                          print("Thread -", self.row,",",self.column," sending RELEASE msg to ",i, j)
                                          self.threads[i][j].rcv_msg_queue.put([constants.MSG_CS_ACCESS_RELEASED,self.row,self.column])
                continue
          

    def run(self):  #This function behaves as a thread that controlling the incoming socket
      print ( self.name+" Starting msg receiver thread ... " )
      worker_t = threading.Thread(target=self.handle_internal_event_loop)
      worker_t.start()
      while True:
            msg = self.rcv_msg_queue.get(block = True)
            #print("Received a message , ", msg)

            if msg[0] == constants.MSG_CS_ACCESS_WANTED:
                  print("Thread -", self.row,",",self.column," Received WANTED msg from ",msg[1],msg[2])
                  if self._state == constants.HELD or self._voted == True:
                        self.msg_buffer.put(msg)
                  else:
                        print()
                        self.threads[msg[1]][msg[2]].rcv_msg_queue.put([constants.MSG_CS_ACCESS_REPLY,self.row,self.column])
                        self._voted = True
            if msg[0] == constants.MSG_CS_ACCESS_REPLY:
                  print("Thread -", self.row,",",self.column," Received REPLY msg from ",msg[1],msg[2])
                  self._heldCondition.acquire()
                  self._my_votes = self._my_votes + 1
                  print("Received a vote from members of voting set: ", self.threads[msg[1]][msg[2]], " Vote rcvd =",self._my_votes )
                  self._heldCondition.notify()
                  self._heldCondition.release()
                  print("Condition released")  
            if msg[0] == constants.MSG_CS_ACCESS_RELEASED:
                  print("Thread -", self.row,",",self.column," Received RELEASED msg from ",msg[1],msg[2])
                  try:
                    bfrd_msg = self.msg_buffer.get_nowait()
                    self.threads[bfrd_msg[1]][bfrd_msg[2]].rcv_msg_queue.put([constants.MSG_CS_ACCESS_REPLY,self.row,self.column])
                    self._voted  = True
                  except queue.Empty:
                    self._voted  = False
                    print("No msg is buffered in queue")


     

      
    

    
          

    