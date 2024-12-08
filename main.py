import ReservationStation as rs
import ROB
import RegFile as rf

Load1 = rs.LRS('Load1','LOAD','LOAD')
Load2 = rs.LRS('Load2','LOAD','LOAD')
Store = rs.SRS('Store','STORE','STORE')
BEQ = rs.BRS('BEQ','BEQ','BEQ')
CALLRET = rs.CRRS('CR', 'CR', 'CR')
ADD1 = rs.ALRS('ADD1','ADD', 'ADD')
ADD2 = rs.ALRS('ADD2','ADD', 'ADD')
ADD3 = rs.ALRS('ADD3','ADD', 'ADD')
ADD4 = rs.ALRS('ADD4','ADD', 'ADD')
NAND1 = rs.ALRS('NAND1','NAND', 'NAND')
NAND2 = rs.ALRS('NAND2','NAND', 'NAND')
MUL = rs.ALRS('MUL','MUL', 'MUL')

def instructions(inst):

    try:
        if inst[0] == 'RET' or inst[0] == 'CALL':
            rd_temp = 1
        else:
            rd_temp = int(inst[1].split('r')[1])
        
            
    except:
        rd_temp = None

    try:
        if inst[0] == 'LOAD' or inst[0] == 'STORE':
            rs_temp = int(inst[4].split('r')[1])
        elif inst[0] == 'BEQ':
            rs_temp = int(inst[1].split('r')[1])
        else:
            rs_temp = int(inst[2].split('r')[1])
    except:
        rs_temp = None

    try:
        if inst[0] == 'STORE':
            rt_temp = int(inst[1].split('r')[1])
        elif inst[0] == 'BEQ':
            rt_temp = int(inst[2].split('r')[1])
        else:
            rt_temp = int(inst[3].split('r')[1])
    except:
        rt_temp = None

    try:
        if inst[0] == 'LOAD' or inst[0] == 'STORE':
            imm_temp = int(inst[2])
        elif inst[0] == 'CALL':
            imm_temp = int(inst[1])
        else:
            imm_temp = int(inst[3])
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


def issue(pc, inst):
    match inst['op']:
        case 'ADD' | 'ADDI':
            rt = inst['rt'] if inst['op'] == 'ADD' else inst['imm']
            for r in RS:
                if r.op == 'ADD' and not r.isBusy():
                    r.issue(inst['rd'], inst['rs'], rt, inst['op'])
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

instList = parseinsts('parse.txt')
RS = [Load1, Load2, Store, BEQ, CALLRET, ADD1, ADD2, ADD3, ADD4, NAND1, NAND2, MUL]
cycles = 0
pc = 2 # actually modify it to be the value passed at the beginning
offset = pc
instcount = 0
print(instList)
while(pc != len(instList) or not ROB.Reorderbuffer.isEmpty()):
    can_issue = ROB.Reorderbuffer.isFree()

    # we have a free bus
    free_bus = True

    if cycles != 0:
        flush, pc= ROB.Reorderbuffer.commit(pc)

    # in case of Branch misprediction or call or return
        if flush:
            for r in RS:
                r.flush()

    # try to advance every RS
        for r in RS:
            # if an RS is writing, it blocks all proceeding RSs
            # note that once can_write is set, we know that this rs is writing
            if(r.isBusy()):
                prev_state = r.current_state
                if free_bus:
                    free_bus = not r.proceed(free_bus)
                else:
                    r.proceed(free_bus)
                if r.current_state == rs.State.WRITTEN and r.current_state != prev_state:
                    written = r
            # handle writing
    

    if not free_bus:
        for r in RS:
            if(r.isBusy()):
                if r.Qj == written.rd:
                    r.Qj = 0
                    r.Vj = ROB.Reorderbuffer.getValueself(written.rd, written.name)

                if r.Qk == written.rd:
                    r.Qk = 0
                    r.Vk = ROB.Reorderbuffer.getValueself(written.rd, written.name)

    print(cycles)


    # trying to issue
    if can_issue and pc < len(instList):
        inst = instList[pc] # how to deal with the offset for the list
        if issue(pc, inst):
            instcount += 1
            pc += 1

    
    cycles += 1

