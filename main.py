'''
Name: Chuangyi Zhang, Homero Vazquez, Eric Zavala 
Project Three -- ECE 366
Univeristy of Illinois at Chicago 
system: OnlineGDB, Macbook Pro
The goal of this project is building our own ISA with its relevant software and hardware. 
This will be a processor with 8 bit instructions and 8 bit data (registers and memory),
which we optimize for the PRPG program we have worked on in previous project, and showcase our result with a Python simulator.
'''

import numpy as np
import array as ar


def hexdecode(char):
    return {
        '0':0,
        '1':1,
        '2':2,
        '3':3,
        '4':4,
        '5':5,
        '6':6,
        '7':7,
        '8':8,
        '9':9,
        'a':10,
        'b':11,
        'c':12,
        'd':13,
        'e':14,
        'f':15,
        }[char]

def hextobin(hexitem):
    binary =ar.array('I',[0])
    hexterms = hexitem.split('\n')
    c=0
    for term in hexterms:
    #select only the last 2 characters in each line
        hexterms[c] = term[-2:]
        c+=1  
    k=0
    for term in hexterms:
        c = 0
        for char in term:
            num = hexdecode(char)
            binary[k] += num * 16**(1-c)
            c+=1
        binary.append(0)
        k+=1    
    if binary[k]==0:
        binary.pop()
    return binary

class mipsMachine:
    def __init__(self, arra):
        self.reg = np.int32([0]*16)
        self.specialreg = np.int32([0]*3)
        self.mem = np.int32([0]*65)
        self.code = arra
        self.pc = 0
        self.numInstr = 0
      
    def execute(self):
        bottom = len(self.code.tolist())
        rd = 2
        rs = 3
        rt = 4
        overflow = 0
        overflowReg = 9
        totalReg = 10
        while self.pc < bottom:
            command = self.code[self.pc]
            types = command >> 4 
            if command == 0xa0:
                self.pc += 1
                self.numInstr += 1
                self.reg[1] = 251
                outfile.write("Seed " + str(self.reg[1]) + "\n")
            if command == 0xa1:
                self.pc += 1
                self.numInstr += 1
                self.reg[1] = 118
                outfile.write("Seed " + str(self.reg[1]) + "\n")
            if command == 0xa2:
                self.pc += 1
                self.numInstr += 1
                self.reg[1] = 79
                outfile.write("Seed " + str(self.reg[1]) + "\n")
            if command == 0xa3ECE:
                self.pc += 1
                self.numInstr += 1
                self.reg[1] = 69
                outfile.write("Seed " + str(self.reg[1]) + "\n")
                
                
            if types == 0x0: # ADD
                self.pc += 1
                self.numInstr += 1
                num = command & 0xf
                self.reg[rd] = self.reg[rs] + self.reg[num]
                outfile.write("Add $" + str(num) + "\n")
            elif types == 0x1: # ADDI check 
                self.pc += 1
                self.numInstr += 1
                imm = command & 0x0f
                self.reg[rd] = self.reg[rs] + imm
                outfile.write("Addi " + str(imm) + "\n")
            elif types == 0x2: # mult & drop check this
                self.pc += 1
                self.numInstr += 1
                num = command & 0x0f
                square = self.reg[num]*self.reg[num]
                square = square & 0xf00f
                top = square >> 8
                square = square & 0x000f
                result = square | top
                self.reg[num] = result
                outfile.write("Muiltdrop $" + str(num) + "\n")
                
            elif types == 0x3: # check ones 
                self.pc += 1
                self.numInstr += 1
                num = command & 0x0f
                count = 0
                result = self.reg[num]
                temp = result
                count += (temp & 0x80)>>7
                count += (temp & 0x40)>>6
                count += (temp & 0x20)>>5
                count += (temp & 0x10)>>4
                count += (temp & 0x08)>>3
                count += (temp & 0x04)>>2
                count += (temp & 0x02)>>1
                count += (temp & 0x01)
                self.reg[rd] = count
                outfile.write("HammingWeight " + str(num) + "\n")
                #print(count)
            elif types == 0x4: # sbadding
                self.pc += 1
                self.numInstr += 1
                Setnumber = (command & 0x0f)
                
                if(Setnumber != 0 ):
                    self.reg[totalReg] = 0
                    outfile.write("StoreAdding " + str(Setnumber) + "\n")

                else:
                    self.mem[(self.reg[rs])] = self.reg[rd]
                    self.reg[totalReg] = self.reg[totalReg] + self.mem[(self.reg[rs])]
                    
                    outfile.write("StoreAdding " + str(Setnumber) + "\n")
                #print(self.reg[totalReg])
            elif types == 0x5: # lb
                self.pc += 1
                self.numInstr += 1
                imm = command & 0x0f
                newRs = self.reg[rs]
                self.reg[rd] = self.mem[newRs]
                outfile.write("Lb " + str(imm) + "\n")
            elif types == 0x6: # MoveD
                self.pc += 1
                self.numInstr += 1
                num = command & 0x0f
                self.reg[num] = self.reg[rd]
                outfile.write("MoveD $" + str(num) + "\n")
            elif types == 0x7: # MoveT
                self.pc += 1
                self.numInstr += 1
                num = command & 0x0f
                self.reg[num] = self.reg[rt]
                outfile.write("MoveT $" + str(num) + "\n")
            elif types == 0x8: # MoveS
                self.pc += 1
                self.numInstr += 1
                num = command & 0x0f
                self.reg[num] = self.reg[rs]
                outfile.write("MoveS $" + str(num) + "\n")
            elif types == 0x9: # checkoverflow
                self.pc += 1
                self.numInstr += 1
                imm = (command & 0x0f)
                temp = self.reg[totalReg]
                while (temp > 256) :
                    temp = temp - 256
                    overflow += 1
                self.reg[overflowReg] = overflow
                outfile.write("Checkoverflow " + str(overflowReg) + "\n")
                
                    
            elif types == 0xb: # RmoveD
                self.pc += 1
                self.numInstr += 1
                num = command & 0x0f
                self.reg[rd] = self.reg[num]
                outfile.write("RmoveD $" + str(num) + "\n")
            elif types == 0xc: # RmoveT
                self.pc += 1
                self.numInstr += 1
                num = command & 0x0f
                self.reg[rt] = self.reg[num]
                outfile.write("RmoveT $" + str(num) + "\n")
            elif types == 0xd: # RmoveS
                self.pc += 1
                self.numInstr += 1
                num = command & 0x0f
                self.reg[rs] = self.reg[num]
                outfile.write("RmoveS $" + str(num) + "\n")
            elif types == 0xe: # Average
                self.pc += 1
                self.numInstr += 1
                imm = command & 0x0f

                if(overflow == 1):
                    self.reg[totalReg] = self.reg[totalReg] + 256
                if(overflow == 2):
                    self.reg[totalReg] = self.reg[totalReg] + 512
                if(overflow == 3):
                    self.reg[totalReg] = self.reg[totalReg] + 1024
                self.reg[imm] = self.reg[totalReg]/16
                overflow = 0;
                outfile.write("Average $" + str(imm) + "\n")
                    
            elif types == 0xf: # bneb
                self.pc += 1
                self.numInstr += 1
                imm = (command & 0x0f) 
                if self.reg[rt] != self.reg[rs]:
                    self.pc -= imm
                outfile.write("Bneb " + str(imm) + "\n")
                    
                
            self.reg[0] = 0 #reg0 is always 0
        self.result()
    
    def result(self):

        print("\n------------------ 4dollar Instructions file compile successfully ------------------\n")
        print("Here is your first seed of your PRPG program: " + str(self.mem[8]))
        print("Here is the number of instruction in the MIPS instructions file: " + str(self.numInstr))
        print("Here is the total number of the instructions of the program: " + str(self.pc) + "\n") 
        
        print( "------------------ Register Content ------------------")
        print("Register" + "             " + "Int" + "               " +" Hex" )

        i = 0
        
        for thing in self.reg:
            print( "$" + str('{:>2}'.format(i)) + str('{:>20}'.format(thing)) + str('{:>20}'.format(hex(thing))))
            #print(str(i) + ': ' + str(hex(thing & 0xff)))
            i += 1
        c=0
        print( "PC:"  + str('{:>20}'.format(self.pc)) + str('{:>20}'.format(hex(self.pc))))
        print( "------------------ Memory Content ------------------")
        print("Memory" + "                 " + "Int" + "               " +" Hex" )
        
        
        for thing in self.mem:
            print( "[M" + str('{:>2}'.format(c)) + "]" + str('{:>20}'.format(thing)) + str('{:>20}'.format(hex(thing))))
            #print(str(c) + ': ' + str(thing))
            c += 1
        
#end mipsMachine class
infile = open("4dollar.txt", 'r')
outfile = open("instrfile.txt", 'w')

mipshex = infile.read()
binary = hextobin(mipshex)

order66 = mipsMachine(binary)
order66.execute()
