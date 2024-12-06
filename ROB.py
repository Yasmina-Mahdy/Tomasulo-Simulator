from collections import deque
from dataclasses import dataclass
from ReservationStation import RegStation as rs

@dataclass
class ROB:
    Type: str
    Dest: str
    Value: int
    Ready: bool


class Reorderbuffer:

    def __init__(self):
        self.buffer = deque(maxlen = 6)
        for b in self.buffer:
            b.Ready = False
    
    @staticmethod
    # adds a new instruction to the end of the reorder buffer and returns its index
    def addInst(self, inst:ROB):
        self.buffer.append(inst)
        self.instindex(inst.dest)

    @staticmethod
    # removes and returns the instruction at the top of the reorder buffer
    def commitInst(self):
        match self.Type:
            case 'AL' | 'LD' # add value to register
            case 'SW' # add to the memory
            case 'BEQ' | 'RET' | 'CALL' # pc + offset
        return self.buffer.popleft()
    
    @staticmethod
    # returns the position of an instruction in the ROB
    def robEntry(self, dest):
       index = 0
       for inst in self.buffer:
            index += 1
            if inst.Dest == dest:
                return index
    

    @staticmethod
    # changes the ready and value of an instruction 
    def setReady(self,dest, value):
        for inst in self.buffer:
            if inst.Dest == dest:
                inst.Ready = True
                inst.Value = value
                rs.freeReg(self.instindex(dest))

    
    @staticmethod
    # returns the ready value
    def isReady(self, dest):
        for inst in self.buffer:
            if inst.Dest == dest:
                return inst.Ready
        

    @staticmethod
    # returns the value of a certain instruction
    def getValue(self, dest):
        for inst in self.buffer:
            if inst.Dest == dest:
                return self.inst.Value
            

    @staticmethod
    # checks if the buffer has free space or not
    def isFree(self):
        if len(self.buffer) == 6:
            return False
        return True
    
    @staticmethod
    # flushes the ROB
    def flush(self):
        for b in self.buffer:
            b = None