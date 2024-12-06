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
    # adds a new instruction to the end of the reorder buffer
    def addinstruction(self, inst:ROB):
        self.buffer.append(inst)

    @staticmethod
    # removes and returns the instruction at the top of the reorder buffer
    def removeinst(self):
        return self.buffer.popleft()
    
    @staticmethod
    # returns the position of an instruction in the ROB
    def instindex(self,dest):
       index = 0
       for inst in self.buffer:
            index += 1
            if inst.Dest == dest:
                return index
    

    @staticmethod
    # changes the ready of an instruction 
    def changeready(self,dest):
        for inst in self.buffer:
            if inst.Dest == dest:
                inst.Ready = True
                rs.freeReg(self.instindex(dest))

    
    @staticmethod
    # returns the ready value
    def Isready(self, dest):
        for inst in self.buffer:
            if inst.Dest == dest:
                return inst.Ready
            
    def setvalue(self, dest, value):
        for inst in self.buffer:
            if inst.Dest == dest:
                inst.Value = value

    def getvalue(self, dest):
        for inst in self.buffer:
            if inst.Dest == dest:
                return self.inst.Value





