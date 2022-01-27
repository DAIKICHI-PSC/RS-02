# LRC Tools for Modbus ASCII

# LRC_CREATE(Output command to the instrument)
# Add LRC to the command.
# Output exanple 0105040B0000
# Output example :0105040B0000EB\r\n
# ret=0 Processed without any problem.
# ret=1 Command is not 2bytes paires.
#
# LRC_CHECK(Input command from the instrument)
# Check LRC.
# Input example :0105040B0000EB\r\n
# Output example ['0x01', '0x05', '0x04', '0x0B', '0x00', '0x00']
# ret=0 Processed without any problem.
# ret=1 Command is not 2bytes paires.
# ret=2 Received LRC and caluculated LRC do not match.

import re

#####Calculate LRC and add to the command.#####
def LRC_CREATE(command = "0105040B0000"):
    command = command.replace(" ", "")
    com_Length = len(command) #Get length of body part.
    if (com_Length % 2) == 0: #Check the commands are 2-bit pair or not.
        command_List = SPLIT_COMMAND(command) #Get list of the body part. e.g.['0x01', '0x05', '0x04', '0x0B', '0x00', '0x00']
        LRC = LRC_CALUCULATE(command_List) #Calculate LRC from the body part.
        output = ":" + command + LRC + "\r\n"
        ret = 0
        return ret, output
    else:
        ret = 1
        return ret, command

#####CHeck received LRC and Calculated LRC.#####
def LRC_CHECK(command = ":010302308842\r\n"):
    command_Body = command.replace(":", "")
    command_Body = command_Body.replace("\r\n", "")
    com_Length = len(command_Body) #Get length of body part.
    if (com_Length % 2) == 0: #Check the commands are 2-bit pair or not.
        LRC = command_Body[com_Length - 2:com_Length] #Get the LRC part.
        command_Body = command_Body[0:com_Length - 2] #Get the body part.
        command_List = SPLIT_COMMAND(command_Body) #Get list of the body part. e.g.['0x01', '0x05', '0x04', '0x0B', '0x00', '0x00']
        caluculated_LRC = LRC_CALUCULATE(command_List) #Calculate LRC from the body part.
        if LRC == caluculated_LRC: #Match two LRC
            ret = 0
            return ret, command_List
        else:
            ret = 2
            return ret, command
    else:
        ret = 1
        return ret, command


def SPLIT_COMMAND(command = "010302308842"):
    indivisual_Command = re.split("(..)", command)[1::2] #Split the command by two charactors
    command_List = []
    for x in indivisual_Command:
        command_List.append("0x" + x) #Add hexadecimal charactor
    return command_List


def LRC_CALUCULATE(command_List = ['0x01', '0x03', '0x02', '0x30', '0x88']):
    sum = 0
    for x in command_List:
        sum += int(x, 0) #Sum all value(Decimal number)
    LRC = sum ^ 0xffffffff #Two's complement(8-bit length) 
    LRC += 1 #Two's complement(Add 1) 
    LRC = hex(LRC) #Convert from decimal number to hexadecimal
    LRC = str(LRC) #Convert to strings
    LRC = LRC.upper() #Convert to uppercase letter
    LRC = LRC[8:10] #Get the last tow charactors
    return LRC


if __name__ == '__main__':
    print()
    print()
    ret, result = LRC_CREATE()
    print("############################################################")
    print(">Result of testing LRC_CREATE()")
    print("ret = " + str(ret))
    print(result)
    print("############################################################")
    print()
    print()

    ret, result = LRC_CHECK()
    print("############################################################")
    print(">Result of testing LRC_CKECK()")
    print("ret = " + str(ret))
    print(result)
    print("############################################################")
    print()
    print()

    ret = SPLIT_COMMAND()
    print("############################################################")
    print(">Result of testing SPLIT_COMMAND()")
    print("ret = " + str(ret))
    print("############################################################")
    print()
    print()

    ret = LRC_CALUCULATE()
    print("############################################################")
    print(">Result of testing LRC_CALUCULATE()")
    print("ret = " + str(ret))
    print("############################################################")
    print()
    print()