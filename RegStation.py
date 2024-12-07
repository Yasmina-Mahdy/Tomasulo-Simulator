class RegStation():
    # create a list of reg entries for the RegStation
    regs = [{"Reg" : i, "ROB" : 0} for i in range(16)]

    # return if a certain reg is busy
    @staticmethod
    def isBusy(reg_num):
        # return whether the ROB entry for this reg is not empty
        return RegStation.regs[reg_num]['ROB'] != 0
    
    # set the ROB entry for a specific Reg
    @staticmethod
    def setROB(reg_num, ROB):
        # reg[0] never has an ROB entry
        if(reg_num == 0):
            return
        # set the ROB entry
        RegStation.regs[reg_num]['ROB'] = ROB

    # free a reg's ROB entry
    @staticmethod
    def freeReg(ROB):
        # any reg waiting on the ROB entry is freed
        for reg in RegStation.regs:
            if reg['ROB'] == ROB:
                reg['ROB'] = 0