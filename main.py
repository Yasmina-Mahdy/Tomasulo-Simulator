import ReservationStation as rs
import ROB
import RegFile as rf

# INPUTS HERE
pc = 0
path = 'parse.txt'
# input the memoryy
# unit counts
load_units = 2
store_units = 1
beq_units = 1
cr_units = 1
add_units = 4
nand_units = 4
mul_units = 1
# cycle lengths
load_addr_cycles = 2
load_cycles = 4
store_addr_cycles = 2
store_cycles = 4
beq_cycles = 1
cr_cycles = 1
add_cycles = 2
nand_cycles = 1
mul_cycles = 8

RS = []
for i in range(load_units):
    RS.append(rs.LRS(f'Load{i+1}','LOAD','LOAD', load_addr_cycles, load_cycles))

for i in range(store_units):
    RS.append(rs.SRS(f'Store{i+1}','STORE','STORE', store_addr_cycles, store_cycles))

for i in range(beq_units):
    RS.append(rs.BRS(f'BEQ{i+1}','BEQ','BEQ', beq_cycles))

for i in range(cr_units):
    RS.append(rs.CRRS(f'CR{i+1}', 'CR', 'CR', cr_cycles))

for i in range(add_units):
    RS.append(rs.ALRS(f'ADD{i+1}','ADD', 'ADD', add_cycles))

for i in range(nand_units):
    RS.append(rs.ALRS(f'NAND{i+1}','NAND', 'NAND', nand_cycles))

for i in range(mul_units):
    RS.append(rs.ALRS(f'MUL{i+1}','MUL', 'MUL', mul_cycles))

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

instList = parseinsts(path)
cycles = 0
instcount = 0
total_branch = 0
branched = False
branched_total = 0
print(instList)
while(pc < len(instList) or not ROB.Reorderbuffer.isEmpty()):
    cycles += 1
    print(cycles)
    can_issue = ROB.Reorderbuffer.isFree()
    # we have a free bus
    free_bus = True

    if cycles != 1:
        flush, pc, branched= ROB.Reorderbuffer.commit(pc)

    # in case of Branch misprediction or call or return
        if flush:
            can_issue = False
            for r in RS:
                r.flush()

    if branched:
        branched_total += 1

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
                if r.Qj == written.Dest:
                    r.Qj = 0
                    r.Vj = ROB.Reorderbuffer.getValueself(written.rd, written.name)

                if r.Qk == written.Dest:
                    r.Qk = 0
                    r.Vk = ROB.Reorderbuffer.getValueself(written.rd, written.name)



    # trying to issue
    if can_issue and pc < len(instList):
        inst = instList[pc] # how to deal with the offset for the list
        if inst['op'] == 'BEQ':
            # total_branch += 1
            pass
        if issue(pc, inst):
            # print(f'issued {inst['op']} at cycle {cycles}')
            # instcount += 1
            pc += 1



print(f"The total number of cycles: {cycles}")
print(f"The IPC: {instcount / cycles}")
print(f"The branch misprediction percentage: {(branched_total/total_branch) * 100}")

