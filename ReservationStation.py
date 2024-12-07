from enum import Enum
from ROB import Reorderbuffer as rob
import RegStation
from ROB import buff_entry as be
from RegFile import RegFile as RF
from RegFile import Memory as mem


# add the rest
# unit to define functional units: their operations and execution cycles
class FU(Enum):
    ADD = {
           'op' : 'ADD',
           'execution_cycles': 2,
           }
    
    ADDI = {
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
    LOAD = {
            'op' : 'LOAD',
            'execution_cycles': 6
           }
    STORE = {
            'op' : 'STORE',
            'execution_cycles': 2
            }
    BEQ =   {
              'op' : 'BEQ',
              'execution_cycles': 1
             }
    CALL =   {
              'op' : 'CALL',
              'execution_cycles': 1
             }
    RET =   {
              'op' : 'RET',
              'execution_cycles': 1
             }
    
# create enum for stages
class State(Enum):
    IDLE = 'idle'
    ISSUED = 'issued'
    EXECUTING = 'executing'
    EXECUTED = 'executed'
    WRITTEN = 'written'


class ReservationStation():
    def __init__(self, name, unit, op):
        # names like load1, load2, mul3, etc.
        self.name = name
        # initially not busy
        self.busy = False 
        self.total_execution_cycles = FU[unit].value['execution_cycles']
        self.op = op
        # number of cycles the instr has been executed, initially zero (to be compared with total_execution_cycles variable of the child class)
        self.current_execution_cycle = 0 
        # we should store a pair/dict that indicates for each state, what it's next state is
        self.current_state = State.IDLE
        # value stored after execution is done
        self.result = None   
        # other values that may not necessarily be needed by all children
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.Dest = None
        self.Addr = None
        self.pc = None
        
    # returns if the reservation station is busy
    def isBusy(self):
        return self.busy
    
    # resets everything in the case of a branch misprediction 
    def flush(self):
        self.busy = False 
        self.current_execution_cycle = 0 
        self.current_state = State.IDLE
        self.result = None   
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.Dest = None
        self.Addr = None
        self.pc = None

    # could be "extended" [not overriden] in child case if needed [make sure to call the super version in child regardless]
    def issue (self, rs):
        self.current_state = State.ISSUED
        # in the child class, set ROB
        # stores any of the following that is needed
         # set rs
        if(RegStation.isBusy(rs)):
            if(rob.isReady(rs)):
                # get value from ROB
                self.Vj = rob.getValue(rs)
                # reset Qj
                self.Qj = 0
            # else
            # assiging the correct ROB for Qj
            else:
                self.Qj = rob.robEntry(rs)
        else:
            # get the value from RF
            self.Vj = RF.regRead(rs)
            self.Qj = 0

        self.busy = True

    # function to set Vj
    def setVj(self, result):
        self.Vj = result
        self.Qj = 0

     # function to set Vj
    def setVk(self, result):
        self.Vk = result
        self.Qk = 0
  
    # override this method if no Qk or other conditions are needed (like in load/store)
    def readyToExec(self):
        return (self.Qj == 0) and (self.Qk == 0)
    
    # extend in child classes
    def execute(self):
        # ExecutionCycles should be a variable in each child as needed
        self.current_state = State.EXECUTING
        #if(self.current_execution_cycle == self.total_execution_cycles - 1):
            #self.current_state = 'executed'
            # set self.result = the result of whatever operation you need to do if applicable

    # if a function does not "write", still keep this to reset the values
    # kind of the trickiest to implement since needs to access all other RSs + ROB
    # as well as check that no other instr is writing
    # extended in child class
    def write(self, rd):
        # maybe return a signal, along with the value, and it can be handled outside?
        self.busy = False
        self.execution_cycles = 0 

        # if(self.readyToWrite):
        #     self.readyToWrite = False
        #     self.current_state = 'written'
        #     rob.setReady(rd, )
        
        # add logic to write and what to return

    # override in child class
    def proceed(self):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        pass


# Arithmetic and Logic RS
class ALRS(ReservationStation): 

    # calls parent constructor
    def __init__(self, name, unit):
        super().__init__(name, unit)
    
    # issue implementation for Arith & logic
    def issue (self, rd, rs, rt, type):

        # call parent issue function
        super().issue(rs)
        self.type = type

        # if addi, assume rt has the imm
        if(self.type == 'ADDI'):
            self.Vk = rt
            self.Qk = 0
        else:    
            if(RegStation.isBusy(rt)):
                if(rob.isReady(rt)):
                    # get value from ROB
                    self.Vk = rob.getValue(rt)
                    # reset Qk
                    self.Qk = 0
                # else
                # assiging the correct ROB for Qk
                else:
                    self.Qk = rob.robEntry(rt)
            else:
                # get the value from RF
                self.Vk = RF.regRead(rt)
                self.Qk = 0
                
        # create an entry in the ROB
        self.Dest = rob.addInst(be('AL', rd, None, None, False))
        # set the regStat entry  
        RegStation.setROB(rd, self.Dest)


    # execute implementation for Arith & logic
    def __execute(self):
        # call parent issue function
        super().execute()
        # increment number of execution cycles
        self.current_execution_cycle += 1 

        # if this is the last cycle to be executed
        if(self.current_execution_cycle == self.total_execution_cycles - 1):
            # compute the result and signal that it is ready to be written     
            # fix the lower bit issues       
            match self.op:
                case 'ADD': self.result = (self.Vj + self.Vk)
                case 'NAND': self.result = ~(self.Vj & self.Vk)
                case 'MUL': self.result = (self.Vj * self.Vk)
            self.readyToWrite = True
            self.current_state = State.EXECUTED

    # write implementation for Arith & logic
    def __write(self, rd):
        super().write()

        if(self.readyToWrite):
            self.readyToWrite = False
            self.current_state = State.WRITTEN
            rob.setReady(rd,self.name,self.result)
        # what to do...?

    # the function that is called from the main
    def proceed(self, can_write):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        match self.current_state:
            # if free and there's a free ROB -> issue
            # case ('written'|  'idle') if (rob.isFree() & new_inst): self.__issue(rd, rs, rt)
            # if issued and ready to execute or already executing but not done -> execute
            case  ('executing' | 'issued') if self.readyToExec(): 
                self.__execute()
                return False
            # if ready to write and there's an available bus, write
            case  'executed' if can_write : 
                self.__write() 
                return True


# class for the load and stor reservation stations
class LRS(ReservationStation):
     def __init__(self, name, unit):
          super().__init__(name, unit)
    

     def issue(self, rs, rd, offset):
         super().issue(rs)
         # add imm to addr field
         self.Addr = offset
         # create an entry in the ROB
         self.Dest = rob.addinst(be(self.op, rd, None, None, False))
         # set the regStat entry  
         RegStation.setROB(rd, self.Dest)
         
     def __readyToExec(self):
            return (self.Qj == 0)

     def __execute(self):
         super().execute()
         # increment number of execution cycles
         self.current_execution_cycle += 1

         if self.current_execution_cycle == 2:
             self.Addr +=  self.Vj

         elif self.current_execution_cycle == self.total_execution_cycles - 1:
            # compute the result and signal that it is ready to be written     
            self.current_state = State.EXECUTED
            # getting the value stored in the memory at a specific address 
            self.result =  mem.memRead(self.Addr)
            self.readyToWrite = True

     def __write(self, rd, offset):
        super().write()
        # writing value from execution to the regs 
        if(self.readyToWrite):
            self.readyToWrite = False
            self.current_state = State.WRITTEN
            rob.setReady(rd, self.name,self.result)
        

     def proceed(self, can_write):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        match self.current_state:
            # if free and there's a free ROB -> issue
            # case ('written'|  'idle') if (rob.isFree() & new_inst): self.__issue(rs,rd, offset)
            # if issued and ready to execute or already executing but not done -> execute
            case  ('executing' | 'issued') if self.__readyToExec(): 
                self.__execute()
                return False
            # if ready to write and there's an available bus, write
            case  'executed' if can_write : 
                self.__write()
                return True   


class SRS(ReservationStation):
    def __init__(self, name, unit):
          super().__init__(name, unit)

    def issue(self, rs,rt, offset):
        super().issue(rs)

        self.Addr = offset

        if(RegStation.isBusy(rt)):
            if(rob.isReady(rt)):
                # get value from ROB
                self.Vk = rob.getValue(rt)
                # reset Qj
                self.Qk = 0
                
            self.Qk = rob.robEntry(rt) 
        else: 
            self.Qk = 0
            self.Vk = RF.regRead(rt) 

        self.Dest = rob.addinst(be(self.op, 'mem', None, None, False))

    def __readyToExec(self):
        return self.Qj == 0
    
    def __readyToWrite(self):
        return self.Qk == 0
    
    def __execute(self):
         super().execute()

         # increment number of execution cycles
         self.current_execution_cycle += 1

         if self.current_execution_cycle == 2:
             rob.setAddr('mem', self.Addr +  self.Vj)

         elif self.current_execution_cycle == self.total_execution_cycles - 1:
            # compute the result and signal that it is ready to be comitted     
            self.current_state = State.EXECUTED

    def __write(self, rd, offset):
        super().write()
        # writing value from execution to the regs 
        self.current_state = State.WRITTEN
        rob.setReady(rd,self.name, self.Vk)

    def proceed(self, can_write):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        match self.current_state:
            # if free and there's a free ROB -> issue
            # case ('written'|  'idle') if (rob.isFree() & new_inst): self.__issue(rs,rd, offset)
            # if issued and ready to execute or already executing but not done -> execute
            case  ('executing' | 'issued') if self.__readyToExec(): 
                self.__execute()
                return False
            # if ready to write and there's an available bus, write
            case  'executed' if can_write and self.__readyToWrite(): 
                self.__write()   
                return True
 

class BRS(ReservationStation):
    def __init__(self, name, unit):
          super().__init__(name, unit)

    def issue(self, rs, rt, pc, imm):
        super().issue(rs)

        self.pc = pc
        self.Addr = imm

        if(RegStation.isBusy(rt)):
            if(rob.isReady(rt)):
                # get value from ROB
                self.Vk = rob.getValue(rt)
                # reset Qj
                self.Qk = 0
                
            self.Qk = rob.robEntry(rt)
            
        else: 
            self.Qk = 0
            self.Vk = RF.regRead(rt) 

        self.Dest = rob.addinst(be(self.op, 'beq', None, None, False))
    

    def __execute(self, pc):
         super().write()
         if(self.Vj == self.Vk):
             # flushing handled in the main flush all the reservation stations
             rob.setAddr(pc + 1 + self.Addr) 
             # assuming pc + 1 is implicit
        # writing value from execution to the regs 
         self.current_state = State.WRITTEN    
         rob.setReady('beq',self.name, self.Vj == self.Vk)

         

    def proceed(self, can_write):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        match self.current_state:
            # if free and there's a free ROB -> issue
            # case ('written'|  'idle') if (rob.isFree() & new_inst): self.__issue(rs,rt,offset) 
            # if issued and ready to execute or already executing but not done -> execute
            case  ('executing' | 'issued') if self.readyToExec(): 
                self.__execute()
                return False



class CRRS(ReservationStation):

    def __init__(self, name, unit):
          super().__init__(name, unit)

    def issue(self, type, pc, imm):

        self.pc = pc
        self.type = type
        if(self.type == 'RET'):
            super().issue(1)
            self.Dest = rob.addinst(be(self.op,'ret', None, None, False))  
        else:
            self.current_state = State.ISSUED
            self.busy = True
            self.Addr = imm
            self.Dest = rob.addinst(be(self.op, 1, None, None, False))  

    def __readyToExec(self):
        return self.type == 'CALL' or self.Qj == 0

    def __execute(self):
         self.current_state = State.EXECUTED
         if self.op == 'RET':
             rob.setAddr('ret', self.Vj)
             rob.setReady('ret',self.name, self.Vj)
             super().write()
             self.current_state = State.WRITTEN
         else:
            self.result =  self.pc + 1
            rob.setAddr(1, self.Addr)
    

    def __write(self):
        super().write()
        # writing value from execution to the regs 
        self.current_state = State.WRITTEN
        rob.setReady(1, self.name,self.result)
    

    def proceed(self, can_write):
        # looks at current state and if the conditions to move to next state are satisified
        # call one of following function (issue, execute, write) [committing handles by ROB]
        match self.current_state:
            # if free and there's a free ROB -> issue
            # case ('written'|  'idle') if (rob.isFree() & new_inst): self.__issue(rs,rt,offset) 
            # if issued and ready to execute or already executing but not done -> execute
            case  ('executing' | 'issued') if self.__readyToExec(): 
                self.__execute()
                return False
            # if ready to write and there's an available bus, write
            case  'executed' if can_write : 
                self.__write()
                return True   

    
 

