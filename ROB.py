from collections import deque
from dataclasses import dataclass
from RegStation import RegStation as rs
import RegFile 

@dataclass
class buff_entry:
    Type: str
    Unit: str
    Dest: int
    Value: int
    Addr: int
    Ready: bool
    index: int


class Reorderbuffer:

    buffer = deque(maxlen = 6)
    commit_cycles = 0

    @staticmethod
    # adds a new instruction to the end of the reorder buffer and returns its index
    # you create the entry 
    def addInst(inst:buff_entry):
        inst.index = len(Reorderbuffer.buffer)
        Reorderbuffer.buffer.append(inst)
        return inst.index

    @staticmethod
    # removes and returns the instruction at the top of the reorder buffer
    def commit(pc):
        if(Reorderbuffer.buffer[0].Ready):
            match Reorderbuffer.buffer[0].Type:
                case 'AL' | 'LD':
                    RegFile.RegFile.regWrite(Reorderbuffer.buffer[0].Dest,Reorderbuffer.buffer[0].Value)
                    rs.freeReg(Reorderbuffer.buffer[0].index)
                    Reorderbuffer.buffer.popleft()
                case 'SW':
                    Reorderbuffer.commit_cycles += 1
                    if(Reorderbuffer.commit_cycles == 4):
                        RegFile.Memory.memWrite(Reorderbuffer.buffer[0].Addr,Reorderbuffer.buffer[0].Value)
                        Reorderbuffer.commit_cycles = 0
                        Reorderbuffer.buffer.popleft()
                case 'BEQ':
                    if Reorderbuffer.buffer[0].Value == True:
                        Addr = Reorderbuffer.buffer[0].Addr
                        Reorderbuffer.flush()
                        rs.flushRegs()
                        return (True, Addr,True)
                    
                    Reorderbuffer.buffer.popleft()
                    
                case 'RET' | 'CALL':
                    Addr = Reorderbuffer.buffer[0].Addr
                    if Reorderbuffer.buffer[0].Type == 'CALL':
                        RegFile.RegFile.regWrite(Reorderbuffer.buffer[0].Dest, Reorderbuffer.buffer[0].Value)
                    Reorderbuffer.flush()
                    rs.flushRegs()
                    return (True, Addr, False)
        return (False, pc, False)    
        
    
    @staticmethod
    # returns the position of an instruction in the ROB
    def robEntryself(dest, unit):
       index = 0
       for inst in Reorderbuffer.buffer:
            if inst.Dest == dest and inst.Unit == unit:
                return index
            index += 1

    @staticmethod       
    def robEntry(dest):
       index = 0
       for inst in Reorderbuffer.buffer:
            if inst.Dest == dest :
                actindex = index
            index += 1
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
                return inst.Value
            
    @staticmethod
    def getValue(dest):
        for inst in Reorderbuffer.buffer:
            if inst.Dest == dest:
                val = inst.Value
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
        Reorderbuffer.buffer.clear()
