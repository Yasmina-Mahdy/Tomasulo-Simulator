import ReservationStation as rs
import ROB
import RegFile as rf

Load1 = rs.LoadRS('Load1','LOAD')
Load2 = rs.LoadRS('Load2','LOAD')
Store = rs.StoreRS('Store','STORE')
BEQ = rs.BEQRS('BEQ','BEQ')
CALLRET = rs.CallRetRS('CALLRET')
ADD1 = rs.ALRS('ADD1','ADD')
ADD2 = rs.ALRS('ADD2','ADD')
ADD3 = rs.ALRS('ADD3','ADD')
ADD4 = rs.ALRS('ADD4','ADD')
NAND1 = rs.ALRS('NAND1','NAND')
NAND2 = rs.ALRS('NAND2','NAND')
MUL = rs.ALRS('MUL','MUL')

def instructions(inst):

    try:
        if inst[0] == 'RET' or inst[0] == 'CALL':
            rd_temp = 'R1'
        else:
            rd_temp = inst[1]
            
    except:
        rd_temp = None

    try:
        if inst[0] == 'LOAD' or inst[0] == 'STORE':
            rs_temp = inst[4]
        elif inst[0] == 'BEQ':
            rs_temp = inst[1]
        else:
            rs_temp = inst[2]
    except:
        rs_temp = None

    try:
        if inst[0] == 'STORE':
            rt_temp = inst[1]
        elif inst[0] == 'BEQ':
            rt_temp = inst[2]
        else:
            rt_temp = inst[3]
    except:
        rt_temp = None

    try:
        if inst[0] == 'LOAD' or inst[0] == 'STORE':
            imm_temp = inst[2]
        elif inst[0] == 'CALL':
            imm_temp = inst[1]
        else:
            imm_temp = inst[3]
    except:
        imm_temp = None

    insts = {
        'op': inst[0],
        'rd': rd_temp,
        'rs': rs_temp,
        'rt': rt_temp,
        'imm':imm_temp
        }
    return insts

def parseinsts(inst,filename):
    inst = []
    with open(filename, 'r') as file:
        for line in file:
            inst.append(line.strip())  # .strip() removes leading/trailing whitespace

    parsed_insts = [ist.split(' ') for ist in inst ]
    instruction = [instructions(inst) for inst in parsed_insts]
    return instruction


# while loop representing each cycle meow
# checking to see if the instructions all have been issued and that the ROB is empty 
# cycle counter and instruction counter
# for rs in list  if rs.isbusy rs.proceed
# match case to check which reservation station to issue too
# handels the writes 
# create the memory and the parsing function 
# write it as a dictonary for the gui and pandas   