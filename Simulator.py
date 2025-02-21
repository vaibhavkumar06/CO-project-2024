import sys
import keyword

Registers={"00000":"00000000000000000000000000000000",
           "00001":"00000000000000000000000000000000",
           "00010":"00000000000000000000000100000000",
           "00011":"00000000000000000000000000000000",
           "00100":"00000000000000000000000000000000",
           "00101":"00000000000000000000000000000000",
           "00110":"00000000000000000000000000000000",
           "00111":"00000000000000000000000000000000",
           "01000":"00000000000000000000000000000000",
           "01000":"00000000000000000000000000000000",
           "01001":"00000000000000000000000000000000",
           "01010":"00000000000000000000000000000000",
           "01011":"00000000000000000000000000000000",
           "01100":"00000000000000000000000000000000",
           "01101":"00000000000000000000000000000000",
           "01110":"00000000000000000000000000000000",
           "01111":"00000000000000000000000000000000",
           "10000":"00000000000000000000000000000000",
           "10001":"00000000000000000000000000000000",
           "10010":"00000000000000000000000000000000",
           "10011":"00000000000000000000000000000000",
           "10100":"00000000000000000000000000000000",
           "10101":"00000000000000000000000000000000",
           "10110":"00000000000000000000000000000000",
           "10111":"00000000000000000000000000000000",
           "11000":"00000000000000000000000000000000",
           "11001":"00000000000000000000000000000000",
           "11010":"00000000000000000000000000000000",
           "11011":"00000000000000000000000000000000",
           "11100":"00000000000000000000000000000000",
           "11101":"00000000000000000000000000000000",
           "11110":"00000000000000000000000000000000",
           "11111":"00000000000000000000000000000000"}

def decimal_to_binary_32(decimal):
    decimal=int(decimal)
    return bin(decimal)[2:].zfill(32) 

def binary_to_decimal(binary):
    return int(binary, 2)

def twos_to_decimal(binary):
    if binary[0] == '1':
        inverted_bits = ''.join('1' if bit == '0' else '0' for bit in binary)
        binary = bin(int(inverted_bits, 2) + 1)[2:]
        binary = binary.zfill(len(inverted_bits))
        return -int(binary, 2)
    return int(binary, 2)

def decimal_to_binary_with_sign_extension(decimal, num_bits=32):
        if decimal < 0:
            binary = bin(decimal & int("1"*num_bits, 2))[2:]
        else:
            binary = bin(decimal)[2:]
        if len(binary) < num_bits:
            binary = "0" * (num_bits - len(binary)) + binary
        elif len(binary) > num_bits:
            binary = binary[-num_bits:]
        return binary

mem_address = {}
for i in range(32):
    bin_str = "0x"+hex(65536+(4*i))[2:].zfill(8) 
    mem_address[bin_str] ="00000000000000000000000000000000"
input = []
for i in sys.stdin:
    i = i.rstrip() 
    words = i.split()
    input.append(words)
pc=0
for j in input:
    i=j[0]
    op=i[25:32]

    #R type
    if op=="0110011": 
        p=pc
        reg=i[20:25]
        reg1=i[12:17]
        reg2=i[7:12]

        # add
        if i[17:20]=="000" and i[0:7]=="0000000":
           Registers[reg]=decimal_to_binary_with_sign_extension( binary_to_decimal(Registers[reg1])  +   binary_to_decimal(Registers[reg2])   )
           pc=pc+4

        # sub
        elif i[0:7]=="0100000":
            if reg1=="00000":
                Registers[reg]= decimal_to_binary_with_sign_extension(-1*twos_to_decimal(Registers[reg2]))
                pc=pc+4
            else:
                if Registers[reg1][0]=="1":
                      r1=-1*twos_to_decimal(Registers[reg1][1:])
                else:
                      r1=twos_to_decimal(Registers[reg1][1:])
                if Registers[reg2][0]=="1":
                      r2=-1*twos_to_decimal(Registers[reg2][1:])
                else:
                      r2=twos_to_decimal(Registers[reg2][1:])
                if (twos_to_decimal(r1) - twos_to_decimal(r2))<0:
                      Registers[reg]="1"+bin(twos_to_decimal(r1) - twos_to_decimal(r2))[2:].zfill(31)
                else:
                      Registers[reg]="0"+bin(twos_to_decimal(r1) - twos_to_decimal(r2))[2:].zfill(31)
                pc=pc+4
        #slt
        elif i[17:20]=="010":
            if twos_to_decimal(Registers[reg1]) < twos_to_decimal(Registers[reg2]):
                Registers[reg]=decimal_to_binary_32(1)
            pc=pc+4

        #sltu
        elif i[17:20]=="011":
            if twos_to_decimal(Registers[reg1]) < twos_to_decimal(Registers[reg2]):
                Registers[reg]=decimal_to_binary_32(1)
            pc=pc+4

        #xor
        elif i[17:20]=="100":
            Registers[reg] = str(int(Registers[reg1]) ^ int(Registers[reg2])).zfill(32)
            pc=pc+4
        #or
        elif i[17:20]=="110":
            Registers[reg] = str(int(Registers[reg1]) | int(Registers[reg2])).zfill(32)
            pc=pc+4
        #and
        elif i[17:20]=="111":
            Registers[reg] = str(int(Registers[reg1]) & int(Registers[reg2])).zfill(32)
            pc=pc+4
        #sll
        elif i[17:20]=="001":
            r2=Registers[reg2][27:32]
            Registers[reg] = decimal_to_binary_32(binary_to_decimal(Registers[reg1]) << binary_to_decimal(r2))
            pc=pc+4
        #srl
        elif i[17:20]=="101":
            r2=Registers[reg2][27:32]
            Registers[reg] = decimal_to_binary_32(binary_to_decimal(Registers[reg1]) >> binary_to_decimal(r2))
            pc=pc+4


    #U type
    # auipc
    elif op == "0010111":
        p = pc
        reg = i[20:25]
        imm = i[0:20]
        Registers[reg]= decimal_to_binary_with_sign_extension(p + binary_to_decimal(imm+"000000000000"))
        pc=pc+4

    # lui
    elif op == "0110111":
        p = pc
        reg = i[20:25]
        imm = i[0:20]
        Registers[reg] = imm+"000000000000"
        pc=pc+4
    
    #B type
    elif op == "1100011":
        p=pc
        reg1=i[12:17]
        reg2=i[7:12]
        imm = i[0] + i[24] + i[1:7] + i[20:24]
        #beq
        if i[17:20]=="000":
            if reg1==reg2:
                print("0b"+decimal_to_binary_32(pc),end=" ")
                for j in Registers.values():
                    print("0b"+j,end=" ")
                print()
                break
            elif twos_to_decimal(Registers[reg1])==twos_to_decimal(Registers[reg2]):
                pc = pc + twos_to_decimal(imm+"0") 
            else:
                pc=pc+4
        #bne
        elif i[17:20]=="001":
            if twos_to_decimal(Registers[reg1])!=twos_to_decimal(Registers[reg2]):
                pc = pc + twos_to_decimal(imm+"0")
            else:
                pc=pc+4
        #blt
        elif i[17:20]=="100":
            if twos_to_decimal(Registers[reg1]) < twos_to_decimal(Registers[reg2]):
                pc = pc + twos_to_decimal(imm+"0")
            else:
                pc=pc+4
        #bge
        elif i[17:20]=="101":
            if twos_to_decimal(Registers[reg1]) >= twos_to_decimal(Registers[reg2]):
                pc = pc + twos_to_decimal(imm+"0")
            else:
                pc=pc+4
        #bltu
        elif i[17:20]=="110":
            if binary_to_decimal(Registers[reg1]) < binary_to_decimal(Registers[reg2]):
                pc = pc + twos_to_decimal(imm+"0")
            else:
                pc=pc+4
        #bgeu
        elif i[17:20]=="111":
            if binary_to_decimal(Registers[reg1]) >= binary_to_decimal(Registers[reg2]):
                pc = pc + twos_to_decimal(imm+"0")
            else:
                pc=pc+4

    #I type 
    elif op=="0000011" or op=="0010011" or op=="1100111 ":
        p=pc
        reg=i[20:25]
        reg1=i[12:17]
        imm=i[0:12]
        #lw
        if i[17:20]=="010":
            Registers[reg]=mem_address["0x" + hex(twos_to_decimal(Registers[reg1]) + twos_to_decimal(imm))[2:].zfill(8)]
            pc=pc+4
        #addi
        elif i[17:20]=="000":
            Registers[reg]= decimal_to_binary_with_sign_extension( twos_to_decimal(Registers[reg1]) + twos_to_decimal(imm) )
            pc=pc+4
        #sltiu
        elif i[17:20]=="011":
            if binary_to_decimal(Registers[reg1]) < binary_to_decimal(imm):
                Registers[reg] = decimal_to_binary_32(1)
            pc=pc+4
        #jalr
        elif i[17:20]=="000":
            Registers[reg]= decimal_to_binary_32(pc+4)
            pc = binary_to_decimal(decimal_to_binary_with_sign_extension(twos_to_decimal(imm) + twos_to_decimal(reg1))[0:31] + "0")
    
    #S type
    elif op=="0100011":
        p=pc
        reg1=i[12:17]
        reg2=i[7:12]
        imm = i[0:7] + i[20:25]
        if i[17:20]=="010":
            mem_address["0x" + hex(twos_to_decimal(Registers[reg1]) + twos_to_decimal(imm))[2:].zfill(8)] = Registers[reg2] 
            pc=pc+4
            

    #J type
    elif op=="1101111":
        p=pc
        reg=i[20:25]
        imm=i[0] + i[12:20] + i[11] + i[1:11]
        Registers[reg]=decimal_to_binary_32( pc+4 )
        pc = binary_to_decimal( decimal_to_binary_with_sign_extension( pc + twos_to_decimal(imm+"0"))[0:31] + "0")
    else:
        continue
   


    print("0b"+decimal_to_binary_32(pc),end=" ")
    for j in Registers.values():
        print("0b"+j,end=" ")
    print()
for k in mem_address:
    print(k,end=":")
    print("0b" + mem_address[k])
