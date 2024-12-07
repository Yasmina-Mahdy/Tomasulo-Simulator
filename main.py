import ReservationStation as rs
import ROB
import RegFile as rf

Load1 = rs.LRS('Load1','LOAD')
Load2 = rs.LRS('Load2','LOAD')
Store = rs.SRS('Store','STORE')
BEQ = rs.BRS('BEQ','BEQ')
CALLRET = rs.CRRS('CALLRET')
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
        'imm':imm_temp,
        'state': 'idle',
        }
    return insts

def parseinsts(filename):
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


def issue(pc, inst):
    match inst['op']:
        case 'ADD' | 'ADDI':
            rt = inst['rt'] if inst['op'] == 'ADD' else inst['imm']
            for r in RS:
                if r.op == 'ADD' and not r.isBusy():
                    r.issue(inst['rd'], inst['rs'], inst['rt'], inst['op'])
                    return True
            return False

        case 'NAND':
            for r in RS:
                if r.op == 'NAND' and not r.isBusy():
                    r.issue(inst['rd'], inst['rs'], inst['rt'], inst['op'])
                    return True
            return False
        
        case 'MUL':
            for r in RS:
                if r.op == 'MUL' and not r.isBusy():
                    r.issue(inst['rd'], inst['rs'], inst['rt'], inst['op'])
                    return True
            return False
        
        case 'LOAD':
            for r in RS:
                if r.op == 'LOAD' and not r.isBusy():
                    r.issue(inst['rs'], inst['rd'], inst['imm'])
                    return True
            return False
        
        case 'STORE':
            for r in RS:
                if r.op == 'STORE' and not r.isBusy():
                    r.issue(inst['rs'], inst['rt'], inst['imm'])
                    return True
                
            return False
        case 'BEQ':
            for r in RS:
                if r.op == 'BEQ' and not r.isBusy():
                    r.issue(inst['rs'], inst['rt'], pc, inst['imm'])
                    return True
            return False
        
        case 'CALL' | 'RET':
            for r in RS:
                if r.op == 'CR' and not r.isBusy():
                    r.issue(inst['op'], pc, inst['imm'])
                    return True
            return False

instList = parseinsts(filename)
RS = [Load1, Load2, Store, BEQ, CALLRET, ADD1, ADD2, ADD3, ADD4, NAND1, NAND2, MUL]
cycles = 0
pc = 0 # actually modify it to be the value passed at the beginning
offset = pc
while(instList and not ROB.Reorderbuffer.isEmpty()):
    can_issue = ROB.Reorderbuffer.isFree()

    # we have a free bus
    can_write = True

    ROB.Reorderbuffer.commit()

    # try to advance every RS
    for r in RS:
        # if an RS is writing, it blocks all proceeding RSs
        # note that once can_write is set, we know that this rs is writing
        prev_state = r.current_state
        can_write = not r.proceed(can_write)
        if r.current_state == 'written' and r.current_state != prev_state:
            written = r
        # handle writing
    

    for r in RS:
        if r.Qj == written.Dest:
            r.Qj = 0
            r.Vj = ROB.Reorderbuffer.getValueself(written.Dest, written.name)

        if r.Qk == written.Dest:
            r.Qk = 0
            r.Vk = ROB.Reorderbuffer.getValueself(written.Dest, written.name)

    


    inst = instList[pc - offset] # how to deal with the offset for the list


    # trying to issue
    if can_issue:
        if issue(pc, inst):
            pc += 1
    
    cycles += 1

