import sys
import keyword

opcode={
    "add":"0110011",
    "sub":"0110011",
    "sll":"0110011",
    "slt":"0110011",
    "sltu":"0110011",
    "xor":"0110011",
    "srl":"0110011",
    "or":"0110011",
    "and":"0110011",
    "lw":"0000011",
    "addi":"0010011",
    "sltiu":"0010011",
    "jalr":"1100111",
    "sw":"0100011",
    "beq":"1100011",
    "bne":"1100011",
    "blt":"1100011",
    "bge":"1100011",
    "bltu":"1100011",
    "bgeu":"1100011",
    "lui":"0110111",
    "auipc":"0010111",
    "jal":"1101111",
}
Registers={"zero":"00000",
           "ra":"00001",
           "sp":"00010",
           "gp":"00011",
           "tp":"00100",
           "t0":"00101",
           "t1":"00110",
           "t2":"00111",
           "s0":"01000",
           "fp":"01000",
           "s1":"01001",
           "a0":"01010",
           "a1":"01011",
           "a2":"01100",
           "a3":"01101",
           "a4":"01110",
           "a5":"01111",
           "a6":"10000",
           "a7":"10001",
           "s2":"10010",
           "s3":"10011",
           "s4":"10100",
           "s5":"10101",
           "s6":"10110",
           "s7":"10111",
           "s8":"11000",
           "s9":"11001",
           "s10":"11010",
           "s11":"11011",
           "t3":"11100",
           "t4":"11101",
           "t5":"11110",
           "t6":"11111"}





def comment_empty(inst):
    if inst.strip() == "" or inst.strip()[0] == "#":
        return True
    return False
    
def empty(inst):
    if not inst.strip():
        return True
    return False
    
def decimal_to_binary_12(decimal):
    binary_str = bin(int(decimal))[2:]
    return binary_str.zfill(12)

def decimal_to_binary_32(decimal):
    binary_str = bin(int(decimal))[2:]
    return binary_str.zfill(32)

def decimal_to_binary_201(decimal):
    binary_str = bin(int(decimal))[2:]
    return binary_str.zfill(20)
    
def hlt_last(data):
    length=len(data)-1
    if data[length][-1]=="0x00000000":
        return True
    else:
        print("ERROR: at inst no.",length+1, "halt instruction missing from last of program")
        sys.exit()

def hlt_only_in_last(data):
    for i in range(len(data)-1):
        if data[i][3]=="0x00000000":
            print("ERROR:  at inst no. ",i+1, " can't execute after hlt, hlt instruction present in a inst other than the last one")
            sys.exit()
    return True  
    
def valid(data):
    for i in range(len(data)):
        if data[i][0] in opcode.keys():
            continue
        elif data[i][0][-1]==":":
            continue
        else:
            print("Syntax ERROR,at",i+1,"not a valid opcode/literal/label")
            sys.exit()
    return True

def is_valid_syntax(data):
    for i in range(len(data)):
        if data[i][0][-1]==":":
            words=data[i][1:]
        else:
            words=data[i]
        instruction= words[0]
        if instruction in ["add", "sub", "sll", "slt", "or", "and" , "srl" , "xor" , "sltu"]:
            if len(words) == 4:
                for word in words[1:]:
                    if word not in Registers:
                        print("Syntax ERROR:  at inst no. ", i+1, ""  + word+" is not a valid register name")
                        sys.exit()
            else:
                print("Syntax ERROR: at inst no.",i+1, +   instruction + " supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()











        elif words[3]=="0x00000000" :
            continue         
        elif instruction[-1]==":":
            continue
        else:
            print("Syntax ERROR:  at inst no. ",i+1, "Invalid instruction! ",words[0],"is not an instruction")
            sys.exit()
    return True

































if hlt_only_in_last(data):
    pass
if hlt_last(data):
    pass
if valid(data):
    pass
if is_valid_syntax(data):
    pass

data = []
for inst in sys.stdin:
    inst = inst.rstrip()
    if inst == "":
        break  
    if comment_empty(inst):
        continue
    else:
        words = inst.split()
        comma=words[1].split(",")
        words=[words[0]]+comma
        data.append(words)
binary=[]  
for i in range(len(data)):
    if data[i][0][-1]==":":
        data[i].remove(data[i][0])   
for i in data:
   
    ## R type instructions
    if i[0]=="add":
        bin="0000000"+Registers[i[3]]+Registers[i[2]]+"000"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)
    
    elif i[0]=="sub":
        bin="0100000"+Registers[i[3]]+Registers[i[2]]+"000"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)
    
    elif i[0]=="sll":
        bin="0000000"+Registers[i[3]]+Registers[i[2]]+"001"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)

    elif i[0]=="slt":
        bin="0000000"+Registers[i[3]]+Registers[i[2]]+"010"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)

    elif i[0]=="sltu":
        bin="0000000"+Registers[i[3]]+Registers[i[2]]+"011"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)
        
    elif i[0]=="xor":
        bin="0000000"+Registers[i[3]]+Registers[i[2]]+"100"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)

    elif i[0]=="srl":
        bin="0000000"+Registers[i[3]]+Registers[i[2]]+"101"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)
        
    elif i[0]=="or":
        bin="0000000"+Registers[i[3]]+Registers[i[2]]+"110"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)

    elif i[0]=="and":
        bin="0000000"+Registers[i[3]]+Registers[i[2]]+"111"+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)
        
    #type I
    elif i[0]== "addi" or "sltiu" or "jalr" or "lw":
        binary.append(decimal_to_binary_12(i[3])+Registers[i[2]]+"010"+Registers[i[1]]+opcode[i[0])

    elif i[0]== "sltiu":
        binary.append(decimal_to_binary_12(i[3])+Registers[i[2]]+"000"+Registers[i[1]]+opcode[i[0])

    elif i[0]== "jalr":
        binary.append(decimal_to_binary_12(i[3])+Registers[i[2]]+"011"+Registers[i[1]]+opcode[i[0])

    elif i[0]== "lw":
        binary.append(decimal_to_binary_12(i[3])+Registers[i[2]]+"000"+Registers[i[1]]+opcode[i[0])

    

    #type S
    elif i[0]=="sw":
        imm = decimal_to_binary_12 (i[2])
        imm1 = imm[7:12]
        imm2 = imm[0:7]
        binary.append( imm2 + Registers[i[1]] + Registers[i[3]] + "010" + imm1 + opcode[i[0])
    #type B
    elif i[0]== "beq":
        rs1 = Registers[i[1]]
        rs2 = Registers[i[2]]
        imm_binary = decimal_to_binary_12(int(i[3]))
        imm1 = imm_binary[0]+imm_binary[2:8]
        imm2 = imm_binary[8:12]+imm_binary[1]
        binary.append(imm1+rs2+rs1+"000"+imm2+opcode[i[0]])

    elif i[0]== "bne":
        rs1 = Registers[i[1]]
        rs2 = Registers[i[2]]
        imm_binary = decimal_to_binary_12(int(i[3]))
        imm1 = imm_binary[0]+imm_binary[2:8]
        imm2 = imm_binary[8:12]+imm_binary[1]
        binary.append(imm1+rs2+rs1+"001"+imm2+opcode[i[0]])

    elif i[0]== "blt":
        rs1 = Registers[i[1]]
        rs2 = Registers[i[2]]
        imm_binary = decimal_to_binary_12(int(i[3]))
        imm1 = imm_binary[0]+imm_binary[2:8]
        imm2 = imm_binary[8:12]+imm_binary[1]
        binary.append(imm1+rs2+rs1+"100"+imm2+opcode[i[0]])

    elif i[0]== "bge":
        rs1 = Registers[i[1]]
        rs2 = Registers[i[2]]
        imm_binary = decimal_to_binary_12(int(i[3]))
        imm1 = imm_binary[0]+imm_binary[2:8]
        imm2 = imm_binary[8:12]+imm_binary[1]
        binary.append(imm1+rs2+rs1+"101"+imm2+opcode[i[0]])

    elif i[0]== "bltu":
        rs1 = Registers[i[1]]
        rs2 = Registers[i[2]]
        imm_binary = decimal_to_binary_12(int(i[3]))
        imm1 = imm_binary[0]+imm_binary[2:8]
        imm2 = imm_binary[8:12]+imm_binary[1]
        binary.append(imm1+rs2+rs1+"110"+imm2+opcode[i[0]])
 

    elif i[0]== "bgeu":
        rs1 = Registers[i[1]]
        rs2 = Registers[i[2]]
        imm_binary = decimal_to_binary_12(int(i[3]))
        imm1 = imm_binary[0]+imm_binary[2:8]
        imm2 = imm_binary[8:12]+imm_binary[1]
        binary.append(imm1+rs2+rs1+"111"+imm2+opcode[i[0]])
        
    elif i[0]=="lui":
        bin=decimal_to_binary_32(i[2])[0:20]+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)
        
    elif i[0]=="auipc":
        bin=decimal_to_binary_32(i[2])[0:20]+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)
        
    elif i[0]=="jal":
        bin=decimal_to_binary_20(i[2])[0]+decimal_to_binary_20(i[2])[10:20]+decimal_to_binary_21(i[2])[9]+decimal_to_binary_21(i[2])[1:9]+Registers[i[1]]+opcode[i[0]]
        binary.append(bin)


for i in binary:
    print(i)
