from collections import deque
from dataclasses import dataclass
from RegStation import RegStation as rs
import RegFile 

@dataclass
class buff_entry:
    Type: str
    Unit: str
    Dest: str
    Value: int
    Addr: int
    Ready: bool


class Reorderbuffer:

    buffer = deque(maxlen = 6)
    for b in buffer:
        b.Ready = False
    
    @staticmethod
    # adds a new instruction to the end of the reorder buffer and returns its index
    # you create the entry 
    def addInst(inst:buff_entry):
        Reorderbuffer.buffer.append(inst)
        Reorderbuffer.robEntry(inst.dest)

    @staticmethod
    # removes and returns the instruction at the top of the reorder buffer
    def commit():
        match Reorderbuffer.buffer[0].Type:
            case 'AL' | 'LD':
                RegFile.RegFile.regWrite(Reorderbuffer.buffer[0].Dest,Reorderbuffer.buffer[0].Value)
            case 'SW':
                RegFile.Memory.memWrite(Reorderbuffer.buffer[0].Addr,Reorderbuffer.buffer[0].Value)
            case 'BEQ':
                if Reorderbuffer.buffer[0].Value == 1:
                    Reorderbuffer.flush()
                return Reorderbuffer.buffer[0].Adder
            case 'RET' | 'CALL':
                Reorderbuffer.flush()
                return Reorderbuffer.buffer[0].Adder
            
        rs.freeReg(Reorderbuffer.robEntry(Reorderbuffer.buffer[0].Dest))
        Reorderbuffer.buffer.popleft()
    
    @staticmethod
    # returns the position of an instruction in the ROB
    def robEntryself(dest,unit):
       index = 0
       for inst in Reorderbuffer.buffer:
            index += 1
            if inst.Dest == dest and inst.Unit == unit:
                return index

    @staticmethod       
    def robEntry(dest):
       index = 0
       for inst in Reorderbuffer.buffer:
            index += 1
            if inst.Dest == dest :
                actindex = index
       return actindex
    

    @staticmethod
    # changes the ready and value of an instruction 
    def setReady(dest,unit, value):
        for inst in Reorderbuffer.buffer:
            if inst.Dest == dest and inst.Unit == unit:
                inst.Ready = True
                inst.Value = value
                
    @staticmethod
    def setAddr(dest, unit, Addr):
        for inst in Reorderbuffer.buffer:
            if inst.Dest == dest and inst.Unit == unit:
                inst.Addr = Addr

    
    @staticmethod
    # returns the ready value
    def isReady(dest):
        for inst in Reorderbuffer.buffer:
            if inst.Dest == dest:
                ready = inst.Ready
        return ready
            
    @staticmethod        
    def isReadyself(dest , unit):
        for inst in Reorderbuffer.buffer:
            if inst.Dest == dest and inst.Unit == unit:
                return inst.Ready
        

    @staticmethod
    def getValueself(dest, unit):
        for inst in Reorderbuffer.buffer:
            if inst.Dest == dest and inst.Unit == unit:
                return Reorderbuffer.inst.Value
            
    @staticmethod
    def getValue(dest):
        for inst in Reorderbuffer.buffer:
            if inst.Dest == dest:
                val = Reorderbuffer.inst.Value
        return val
            

    @staticmethod
    # checks if the buffer has free space or not
    def isFree():
        if len(Reorderbuffer.buffer) == 6:
            return False
        return True
    
    def isEmpty():
        if len(Reorderbuffer.buffer) == 0:
            return True
        else:
            return False
    
    @staticmethod
    # flushes the ROB
    def flush():
        for b in Reorderbuffer.buffer:
            b = None


