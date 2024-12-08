class RegStation():
    # create a list of reg entries for the RegStation
    regs = [{"Reg" : i, "ROB" : 0, "Unit": None} for i in range(8)]

    # return if a certain reg is busy
    @staticmethod
    def isBusy(reg_num):
        # return whether the ROB entry for this reg is not empty
        return RegStation.regs[reg_num]['ROB'] != 0, RegStation.regs[reg_num]['Unit']
    
    # set the ROB entry for a specific Reg
    @staticmethod
    def setReg(reg_num, ROB, Unit):
        # reg[0] never has an ROB entry
        if(reg_num == 0):
            return
        # set the ROB entry
        RegStation.regs[reg_num]['ROB'] = ROB
        RegStation.regs[reg_num]['Unit'] = Unit

    # free a reg's ROB entry
    @staticmethod
    def freeReg(ROB, Unit):
        # any reg waiting on the ROB entry is freed
        for reg in RegStation.regs:
            if reg['ROB'] == ROB and reg['Unit'] == Unit:
                reg['ROB'] = 0

    def flushRegs():
        for reg in RegStation.regs:
                reg['ROB'] = 0
                reg['Unit'] = None