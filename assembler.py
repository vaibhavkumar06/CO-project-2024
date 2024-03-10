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










































data = []
for inst in sys.stdin:
    inst = inst.rstrip()
    if inst == "":
        break  
    if comment_empty(inst):
        continue
    else:
        words = inst.split()
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
    binary.append(opcode[i[0]][0] + Registers[i[1]] +opcode[i[0]][1] + Registers[i[2]] + decimal_to_binary_12(i[3]))

    #type S
    elif i[0]=="sw":
    imm = decimal_to_binary_12 (i[2])
    imm1 = imm[:4]
    imm2 = imm[5:11]
    binary.append(opcode[i[0]][0] + imm1 + opcode[i[0]][1] + Registers[i[3]] + Registers[i[1]] + imm2)
