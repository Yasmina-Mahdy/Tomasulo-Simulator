
class ReservationStation():
    def __init__(self):
        # initially not busy
        self.busy = False 
        # number of cycles the instr has been executed, initially zero (to be compared with static variable of the child class)
        self.execution_cycles = 0 
        # doesn't matter what the nextState is when not busy but still, we can have it be idle
        # we should store a pair/dict that indicates for each state, what it's next state is
        self.current_state = 'idle'
        # signal to indicate that execution is done and ready to write
        self.readyToWrite = False
        # value stored after execution is done
        self.result = None   
        

    def isBusy(self):
        return self.busy
    
    def flush(self):
        # resets everything in the case of a branch misprediction 
        pass

    def proceed(self):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        pass

    # should also receive other data like Vj or Qj
    def issue (self, ROB):
        # stores any of the following that is needed
        # Vj/k, Qj/K, A (imm)
        self.busy = True
        self.Dest = ROB

    def readyToExec(self):
        # override this method if no Qk or other conditions are needed (like in load/store)
        return (self.Qj == 0) and (self.Qk == 0)
    
    def execute(self):
        # ExecutionCycles should be a static variable in each child as needed
        if(self.execution_cycles == ExecutionCycles):
            # set self.readyToWrite = true if applicable
            # set self.result = the result of whatever operation you need to do if applicable

            pass

    # if a function does not "write", still keep this to reset the values
    # kind of the trickiest to implement since needs to access all other RSs + ROB
    # as well as check that no other instr is writing
    def write(self):
        # maybe return a signal, along with the value, and it can be handled outside?
        self.busy = False
        self.execution_cycles = 0 

        if(self.readyToWrite):
            self.readyToWrite = False
            self.current_state = 'idle'
        
        # add logic to write and what to return

        