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
    if decimal >= 0:
        binary_str = bin(decimal)[2:].zfill(12)
    else:
        binary_str = bin(2**12 + decimal)[2:]
    return binary_str[-12:]

def decimal_to_binary_32(decimal):
    if decimal >= 0:
        binary_str = bin(decimal)[2:].zfill(32)
    else:
        binary_str = bin(2**32 + decimal)[2:]
    return binary_str[-32:]

def decimal_to_binary_20(decimal):
    if decimal >= 0:
        binary_str = bin(decimal)[2:].zfill(20)
    else:
        binary_str = bin(2**20 + decimal)[2:]
    return binary_str[-20:]

    
def hlt_last(data):
    length=len(data)-1
    if data[length][0]=="beq" and data[length][1]=="zero" and data[length][2]=="zero" and data[length][3]=="0":
        return True
    else:
        print("ERROR: at inst no.",length+1, "halt instruction missing from last of program")
        sys.exit()

def hlt_only_in_last(data):
    for i in range(len(data)-1):
        if data[i][0]=="beq" and data[i][1]=="zero" and data[i][2]=="zero" and data[i][3]=="0":
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
        if data[i][0][-1] == ":":
            words = data[i][1:]
        else:
            words = data[i]
        instruction = words[0]
        
        # R type 
        if instruction in ["add", "sub", "sll", "slt", "or", "and" , "srl" , "xor" , "sltu"]:
            if len(words) == 4:
                for word in words[1:]:
                    if word not in Registers:
                        print("Syntax ERROR: at inst no. ", i+1, word + " is not a valid register name")
                        sys.exit()
            else:
                print("Syntax ERROR: at inst no.", i+1, instruction + " supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()
        
        # I type
        if instruction in ["lw", "addi", "sltiu", "jalr"]:
            if len(words) == 4:
                if words[1] not in Registers:
                    print("Syntax ERROR: at inst no. ", i+1, words[1] + " is not a valid register name")
                    sys.exit()
                if instruction == "addi" or instruction == "sltiu" or instruction == "jalr":
                    if words[2] not in Registers:
                        print("Syntax ERROR: at inst no. ", i+1, words[2] + " is not a valid register name")
                        sys.exit()
                    if not words[3].isdigit():
                        print("Syntax ERROR: at inst no. ", i+1, words[3] + " is not a valid digit")
                        sys.exit()     
                if instruction == "lw":
                    if not words[2].isdigit():
                        print("Syntax ERROR: at inst no. ", i+1, words[2] + " is not a valid digit")
                        sys.exit()
                    if words[3] not in Registers:
                        print("Syntax ERROR: at inst no. ", i+1, words[3] + " is not a valid register name")
                        sys.exit()
            else:
                print("Syntax ERROR: at inst no.", i+1, instruction + " supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()
        
        # S type
        if instruction == "sw":
            if len(words) == 4:
                if words[1] not in Registers:
                    print("Syntax ERROR: at inst no. ", i+1, words[1] + " is not a valid register name")
                    sys.exit()
                if not words[2].isdigit():
                    print("Syntax ERROR: at inst no. ", i+1, words[2] + " is not a digit")
                    sys.exit()
                if words[3] not in Registers:
                    print("Syntax ERROR: at inst no. ", i+1, words[3] + " is not a valid register name")
                    sys.exit()
            else:
                print("Syntax ERROR: at inst no.", i+1, instruction + " supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()
        
        # B type
        if instruction in ["beq", "bne", "blt", "bge", "bltu", "bgeu"]:
            if len(words) == 4:
                if words[1] not in Registers:
                    print("Syntax ERROR: at inst no. ", i+1, words[1] + " is not a valid register name")
                    sys.exit()
                if words[2] not in Registers:
                    print("Syntax ERROR: at inst no. ", i+1, words[2] + " is not a valid register name")
                    sys.exit()
                if not words[3].isdigit():
                    print("Syntax ERROR: at inst no. ", i+1, words[3] + " is not a valid digit")
                    sys.exit()
            else:
                print("Syntax ERROR: at inst no.", i+1, instruction + " supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()
        
        # U type
        if instruction in ["lui", "auipc"]:
            if len(words) == 3:
                if words[1] not in Registers:
                    print("Syntax ERROR: at inst no. ", i+1, words[1] + " is not a valid register name")
                    sys.exit()
                if not words[2].isdigit():
                    print("Syntax ERROR: at inst no. ", i+1, words[2] + " is not a valid digit")
                    sys.exit()
            else:
                print("Syntax ERROR: at inst no.", i+1, instruction + " supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()
        
        # J type
        if instruction == "jal":
            if len(words) == 3:
                if words[1] not in Registers:
                    print("Syntax ERROR: at inst no. ", i+1, words[1] + " is not a valid register name")
                    sys.exit()
                if not words[2].isdigit():
                    print("Syntax ERROR: at inst no. ", i+1, words[2] + " is not a valid digit")
                    sys.exit()  
            else:
                print("Syntax ERROR: at inst no.", i+1, instruction + " supports three operands, " + str(len(words)-1) + " were given")
                sys.exit()











        elif elif words[i][0]=="beq" and words[i][1]=="zero" and words[i][2]=="zero" and words[i][3]=="0": 
            continue         
        elif instruction[-1]==":":
            continue
        else:
            print("Syntax ERROR:  at inst no. ",i+1, "Invalid instruction! ",words[0],"is not an instruction")
            sys.exit()
    return True



































data = []
for inst in sys.stdin:
    inst = inst.rstrip()
    if inst == "":
        break  
    if comment_empty(inst):
        continue
    if "(" in inst:
        words=[]
        current_component = ""
        for char in inst:
            if char == ' ' or char == ',' or char == '(' or char == ')':
                if current_component:
                    words.append(current_component)
                    current_component = ""
                if char != ' ':
                    words.append(char)
            else:
                current_component += char
        if current_component:
            words.append(current_component)
        data.append(words)
    else:
        words = inst.split()
        comma=words[1].split(",")
        words=[words[0]]+comma
        data.append(words)

if hlt_only_in_last(data):
    pass
if hlt_last(data):
    pass
if valid(data):
    pass
if is_valid_syntax(data):
    pass
    
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
