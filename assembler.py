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

def decimal_to_binary_12(decimal):
    binary_str = bin(int(decimal))[2:]
    return binary_str.zfill(12)

binary_code=[]

#assumption that opcode tuple mei 0th index pe theres opcode and 1st index theres funct3

#type I
if i[0]== "addi" or "sltiu" or "jalr" or "lw":
    binary_code.append(opcode[i[0]][0] + Registers[i[1]] +opcode[i[0]][1] + Registers[i[2]] + decimal_to_binary_12(i[3]))

#type S
if i[0]=="sw":
    imm = decimal_to_binary_12 (i[2])
    imm1 = imm[:4]
    imm2 = imm[5:11]
    binary_code.append(opcode[i[0]][0] + imm1 + opcode[i[0]][1] + Registers[i[3]] + Registers[i[1]] + imm2)

    

