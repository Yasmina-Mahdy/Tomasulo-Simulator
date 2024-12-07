from collections import deque
from dataclasses import dataclass
from ReservationStation import RegStation as rs
import RegFile 

@dataclass
class buff_entry:
    Type: str
    Dest: str
    Value: int
    Addr: int
    Ready: bool


class Reorderbuffer:

    def __init__(self):
        self.buffer = deque(maxlen = 6)
        for b in self.buffer:
            b.Ready = False
    
    @staticmethod
    # adds a new instruction to the end of the reorder buffer and returns its index
    # you create the entry 
    def addInst(self, inst:buff_entry):
        self.buffer.append(inst)
        self.robEntry(inst.dest)

    @staticmethod
    # removes and returns the instruction at the top of the reorder buffer
    def commitInst(self,rd,res,addr,pc, offset):

        #rs.freeReg(self.robEntry(dest))
        match self.Type:
            case 'AL' | 'LD':
                RegFile.RegFile.regWrite(rd,res)
            case 'SW':
                RegFile.Memory.memWrite(addr,res)
            case 'BEQ' | 'RET' | 'CALL':
                return pc + offset
        #rs.freeReg(self.robEntry(dest))
        self.buffer.popleft()
    
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
    def setReady(self, dest, value):
        for inst in self.buffer:
            if inst.Dest == dest:
                inst.Ready = True
                inst.Value = value
                

    def setAddr(self, dest, Addr):
        for inst in self.buffer:
            if inst.Dest == dest:
                inst.Addr = Addr

    
    @staticmethod
    # returns the ready value
    def isReady(self, dest):
        for inst in self.buffer:
            if inst.Dest == dest:
                return inst.Ready
        

    @staticmethod
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


