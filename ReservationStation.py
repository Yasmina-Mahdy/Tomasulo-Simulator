from enum import Enum

class RegStation():
    # create a list of reg entries for the RegStation
    regs = [{"Reg" : i, "ROB" : 0} for i in range(16)]

    # return if a certain reg is busy
    @staticmethod
    def isBusy(reg_num):
        # return whether the ROB entry for this reg is not empty
        return RegStation.regs[reg_num]['ROB'] != 0
    
    # set the ROB entry for a specific Reg
    @staticmethod
    def setROB(reg_num, ROB):
        # reg[0] never has an ROB entry
        if(reg_num == 0):
            return
        # set the ROB entry
        RegStation.regs[reg_num]['ROB'] = ROB

    # free a reg's ROB entry
    @staticmethod
    def freeReg(ROB):
        for reg in RegStation.regs:
            if reg['ROB'] == ROB:
                
                reg['ROB'] = 0


# add the rest
# unit to define functional units: their operations and execution cycles
class FU(Enum):
    ADD = {
           'op' : 'ADD',
           'execution_cycles': 2,
           }
    
    ADD = {
           'op' : 'ADDI',
           'execution_cycles': 2,
           }
    
    NAND = {
           'op' : 'NAND',
           'execution_cycles': 1,
           }
    MUL = {
           'op' : 'MUL',
           'execution_cycles': 8,
          }


class ReservationStation():
    def __init__(self, name, unit):
        # names like load1, load2, mul3, etc.
        self.name = name
        # initially not busy
        self.busy = False 
        self.total_execution_cycles = FU[unit].value['execution_cycles']
        self.op = FU[unit].value['op']
        # number of cycles the instr has been executed, initially zero (to be compared with total_execution_cycles variable of the child class)
        self.current_execution_cycle = 0 
        # doesn't matter what the nextState is when not busy but still, we can have it be idle
        # we should store a pair/dict that indicates for each state, what it's next state is
        self.current_state = 'idle'
        # value stored after execution is done
        self.result = None   
        # other values that may not necessarily be needed by all children
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.Dest = None
        self.Addr = None
        

    def isBusy(self):
        return self.busy
    
    # how to implement this?
    def flush(self):
        # resets everything in the case of a branch misprediction 
        pass

    # should also receive other data like Vj or Qj
    def issue (self, ROB):
        self.current_state = 'issued'
        # stores any of the following that is needed
        # Vj/k, Qj/K, A (imm)
        self.busy = True
        self.Dest = ROB

    def readyToExec(self):
        # override this method if no Qk or other conditions are needed (like in load/store)
        return (self.Qj == 0) and (self.Qk == 0)
    
    def execute(self):
        # ExecutionCycles should be a variable in each child as needed
        self.current_state = 'executing'
        #if(self.current_execution_cycle == self.total_execution_cycles):
            #self.current_state = 'executed'
            # set self.result = the result of whatever operation you need to do if applicable


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

    def proceed(self):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        pass


# Arithmetic and Logic RS
class ALRS(ReservationStation): 

    def __init__(self, name, unit):
        super.__init__(self, name, unit)
    
    def __issue (self, ROB, rd, rs, rt):
        # call parent issue function
        super().issue(self, ROB)

        # set rs
        if(RegStation.isBusy(rs)):
            # check if ROB head is ready
                # set Vj = ROB[ROB].value
                # set Qj = 0
            # else
            self.Qj = ROB
        else:
            # get the value from the actual registers (HOW)? and put it in Vj
            self.Qj = 0
            
        # if addi, assume rt has the imm
        if(self.op == 'ADDI'):
            self.Vk = rt
            self.Qk = 0
        # set rt    
        else:    
            if(RegStation.isBusy(rt)):
                # check if ROB head is ready
                    # set Vk = ROB[ROB].value
                    # set Qk = 0
                # else
                self.Qk = ROB
            else:
                # get the value from the actual registers (HOW)? and put it in Vj
                self.Qk = 0
                
        RegStation.setROB(rd, ROB)


    def __execute(self):
        super().execute()
        self.current_execution_cycle += 1 
        if(self.current_execution_cycle == self.total_execution_cycles):
            self.readyToWrite = True
            match self.op:
                case 'ADD' | 'ADDI': self.result = self.Vj + self.Vk
                case 'NAND': self.result = ~(self.Vj & self.Vk)
                case 'MUL': self.result = (self.Vj * self.Vk) & 0xFFFF # only store lower 16 bits


    def __write(self):
        super().write()
        # what to do...?

    # the fun
    def proceed(self, ROB, rd, rs, rt, can_write):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        match self.current_state:
            # if free and there's a free ROB -> issue
            case 'idle' if ROB != None: self.__issue(self, ROB, rd, rs, rt)
            # if issued and ready to execute or already executing but not done -> execute
            case 'issued' if self.__readyToExec() | 'executing': self.__execute()
            # if ready to write and there's an available bus, write
            case  'executed' if can_write : self.__write() 

            

            
    
    