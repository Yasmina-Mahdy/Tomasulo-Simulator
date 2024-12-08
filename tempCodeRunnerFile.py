while(pc != len(instList) or not ROB.Reorderbuffer.isEmpty()):
    can_issue = ROB.Reorderbuffer.isFree()
    cycles += 1

    # we have a free bus
    free_bus = True

    if cycles != 1:
        flush, pc, branched, temp_cycle, commited = ROB.Reorderbuffer.commit(pc,cycles)
        if commited and len(PCs) > 0:
            comm = instList[PCs.pop(0)]
            instList[PCs[0]]['Commiting cycle'] = temp_cycle
            #print(comm)
            commited_inst.append(comm) 

    # in case of Branch misprediction or call or return
        if flush:
            PCs.clear()
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
                try:
                    inst['Written cycle'] = cycles
                    written = r
                except:
                    pass

            if r.current_state == rs.State.EXECUTING and r.current_state != prev_state:
                try:
                    instList[r.pc]['Started Execution cycle'] = cycles
                except:
                    pass

            if r.current_state == rs.State.EXECUTED and r.current_state != prev_state:
                try:
                    instList[r.pc]['Last execution cycle'] = cycles
                except:
                    pass

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
        if inst['op'] == 'BEQ':
            total_branch += 1
        if issue(pc, inst):
            inst['issuing cycle'] = cycles
            print(inst['op'])
            PCs.append(pc)
            instcount += 1
            pc += 1




print(f"The total number of cycles: {cycles}")
print(f"The IPC: {instcount / cycles}")
print(f"The branch misprediction percentage: {(branched_total/total_branch) * 100}")
df = pd.DataFrame(commited_inst)
print(df)