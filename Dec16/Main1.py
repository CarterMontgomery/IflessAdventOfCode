filename = "Input.txt"
#Let's try an object oriented approach
#Appraoch:
#Parse hexadecimal into big long binary string
#Pass binary string into a packet tester
#Packet tester takes string of binary values
#Determines the version and type of packet.

#Every time a new packet starts, pass it 6 bits.
#Each packet will have a 'done' variable
#While that packet is not done, pass it a new bit




hexDict = {"0":"0000","1":"0001","2":"0010","3":"0011",
           "4":"0100","5":"0101","6":"0110","7":"0111",
           "8":"1000","9":"1001","A":"1010","B":"1011",
           "C":"1100","D":"1101","E":"1110","F":"1111"}
def binToVal(val):
    rev = val[::-1]
    temp = 0
    mult = 1
    for i in rev:
        temp += (i == "1") * mult
        mult = mult * 2
    return temp

#With IF statements:
def parsePacket(index,string):
    #print("STARTING NEW PACKET: ",string[index:])
    onIndex = index
    version = binToVal(string[onIndex:onIndex+3])
    onIndex +=3
    ptype = binToVal(string[onIndex:onIndex+3])
    onIndex += 3
    endIndex = len(string)-1
    #print("VERSION: ",version, " TYPE: ",ptype)
    options = {True:parseLiteral,False:parseOperator}
    endIndex,addV = options[ptype == 4](onIndex,string)
    
    version += addV
    return version,endIndex

def parseOperator(onIndex,string):
    #onIndex += 1
    version = 0
    #print("ON INDEX: ",onIndex)
    options = {True:parseOpLength,False:parseOpPackets}
    endIndex,addV = options[string[onIndex]=="0"](onIndex,string)
    version += addV
    
    return endIndex,version

def parseOpPackets(onIndex,string):
    version = 0
    onIndex += 1
    packets = binToVal(string[onIndex:onIndex+11])
    onIndex += 11
    donepackets = 0
    #print("SUB PACKETS: ",packets)
    while (donepackets < packets):
        newVersion, nextIndex = parsePacket(onIndex,string)
        version += newVersion
        onIndex = nextIndex
        donepackets += 1
        endIndex = onIndex
    return endIndex,version
def parseOpLength(onIndex,string):
    #Get 15 bits for length
    version = 0
    onIndex += 1
    length = binToVal(string[onIndex:onIndex+15])
    onIndex += 15
    ending = onIndex + length
    #print("LENGTH : ",length)
    while (onIndex != ending):
        newVersion, nextIndex = parsePacket(onIndex,string)
        version += newVersion
        onIndex = nextIndex
    endIndex = onIndex
    return endIndex,version

def parseLiteral(onIndex,string):
    #Literal packet
    done = False
    while (not(done)):
        #print("CHECKING: ",string[onIndex:onIndex+5])
        done = string[onIndex] == "0"
        onIndex += 5
            
    endIndex = onIndex
    return endIndex, 0



if __name__ == "__main__":
    text = ""
    with open(filename) as f:
        text = f.read()
    #print(text)
    binText = ""
    for letter in text:
        binText += hexDict[letter]
    versionNum,index = (parsePacket(0,binText))
    print(versionNum)