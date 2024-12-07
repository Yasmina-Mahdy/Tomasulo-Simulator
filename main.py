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




# while loop representing each cycle meow
# checking to see if the instructions all have been issued and that the ROB is empty 
# cycle counter and instruction counter
# for rs in list  if rs.isbusy rs.proceed
# match case to check which reservation station to issue too
# handels the writes 
# create the memory and the parsing function 
# write it as a dictonary for the gui and pandas   