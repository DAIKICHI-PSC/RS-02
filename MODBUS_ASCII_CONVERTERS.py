# TOOLS TO CONVERT DATA
#
# DECIMAL_TO_HEX(decimal, desired number of digits)
# Input example　255, 4
# Output example 00FF
# ret=0 Processed without any problem.
# ret=1 Length of input data greater than specified digits.
#
# TWO_HEX_TO_BYTES(upper HEX, lower HEX, desired number of digits)
# Input example　'0x01', '0x03', '0x02', '0x30', '0x88', '0x42'
# ('0x02' above means 2bytes(16bit) takes 2 hex '0x30' and '0x88'.)
# Output example 0000000011111111(16bit).
# ret=0 Processed without any problem.
# ret=1 Length of input data greater than specified digits.


#####CONVERT DECIMAL TO HEX AND ADD ZEROS TO BE DESIRED DIGITS.#####
def DECIMAL_TO_HEX(decimal=255, digits = 4):
    hexadecimal = hex(decimal) #Convert decimal to hex.
    hex_Str = str(hexadecimal) #Convert hex to string.
    hex_Str = hex_Str.replace("0x", "") #Delete the header.
    hex_Str = hex_Str.upper() #Convert all charactors to learge text.
    if len(hex_Str) > digits: #Check the length of the string smaller than specified digits.
        ret = 1
        hex_Str = "0"
        return ret, hex_Str
    for _ in range(digits - len(hex_Str)): #Add zeros up to specified digits.
        hex_Str = "0" + hex_Str
    ret = 0
    return ret, hex_Str


#####CONVERT HEX TO BYTES AND ADD ZEROS.#####
#The reason to add zeros is because zeros from the head are lost after converting from bytes to string.
def RESPONSE_TO_BYTES(response = ['0x01', '0x03', '0x02', '0x30', '0x88', '0x42']):
    data = []
    for x in range(3, 3 + int(response[2], 0)): #Get the data part indicated in recieved data(third hex).
        data.append(response[x])
    digits = len(data) * 8
    byte_Str = ""
    for x in data:
        x = x.replace("0x", "") #Delete the header part.
        byte_Str = byte_Str + x
    byte_Str = "0x" + byte_Str
    byte_Str = int(byte_Str, 0) #convert string to hex.
    byte_Str = bin(byte_Str) #Convert hex to bytes.
    byte_Str = str(byte_Str) #Convert bytes to string.
    byte_Str = byte_Str.replace("0b", "") #Delete the header part.
    if len(byte_Str) > digits: #Check the length of the string smaller than specified digits.
        ret = 1
        byte_Str = "0"
        return ret, byte_Str
    for _ in range(digits - len(byte_Str)): #Add zeros up to specified digits.
        byte_Str = "0" + byte_Str
    ret = 0
    return ret, byte_Str


if __name__ == '__main__':
    print()
    print()
    ret, result = DECIMAL_TO_HEX()
    print("############################################################")
    print(">Result of testing DECIMAL_TO_HEX()")
    print("ret = " + str(ret))
    print(result)
    print("############################################################")
    print()
    print()

    ret, result = RESPONSE_TO_BYTES()
    print("############################################################")
    print(">Result of testing RESPONSE_TO_BYTES()")
    print("ret = " + str(ret))
    print(result)
    print("############################################################")
    print()
    print()
    