# function to convert any number to an int 16
def int16(value):
    value = value & 0xFFFF  # Mask to 16 bits (for any number)
    # If the number is greater than 32,767, convert to negative values
    if value >= 0x8000:  # If the value is >= 32,768, it's negative in two's complement
        value -= 0x10000   # Subtract 65536 (0x10000) to convert to negative
    return value


class RegFile:
    # initialize regs to zero
    regs = [0 for i in range(8)]

    @staticmethod
    def regWrite(rd,res):
        if rd != 0:
            RegFile.regs[rd] = int16(res)

    @staticmethod
    def regRead(rs):

        return RegFile.regs[rs]
          

class Memory:
    Mem = [0 for i in range(65537)]

    @staticmethod
    def memWrite(addr,res):
        Memory.Mem[addr] = int16(res)

    def memRead(addr):
        return Memory.Mem[addr]
