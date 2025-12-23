import sys
r = [0] * 32
r[2] = 380

def funct1(dec):
    """Convert decimal to uppercase hexadecimal without '0x' prefix"""
    map = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
    if dec == 0:
        return '0'
    h = ''
    while dec > 0:
        rem = dec % 16
        if rem < 10:
            h = str(rem) + h
        else:
            h = map[rem] + h
        dec = dec // 16
    return h

def Print_mem():
    start = 65536  
    for i in range(32):
        addr = start + 4 * i
        addr2= funct1(addr) 
        mem_key = addr2.upper()
        val = memory.get(mem_key, 0)
        line = f"0x000{addr2}:0b{twos(val)}\n"
        file.write(line)

memory={}
start = 65536
for i in range(32):
    memory[funct1(start + 4*i)] = 0

x = {"PC" : 0}
cycle = x["PC"]//4
def funct2(num, bits): #to bin
    if int(num) < 0:
        num = (1 << bits) + int(num) 
    s = ""
    for i in range(bits):
        s = str(int(num) % 2) + s
        num //= 2
    return "0b" + s

def twos(num):
  if num >= 0:
    return format(num, '032b')
  else:
    pos = format(-num, '032b')
    flip = ''.join('0' if bit == '1' else '1'
                           for bit in pos)
    ans = format(int(flip, 2) + 1, '032b')
    return ans
  
def db(num, bits):
  if int(num) < 0:
      num = (1 << bits) + int(num) 
  
  s = ""
  
  for i in range(bits):
      s = str(int(num) % 2) + s
      num //= 2
  return "0b" + s

def funct4(bin): 
    pow = len(bin)-2
    dec = -int(bin[0]) * 2**(pow+1)
    for i in bin[1:]:
        if i == '1':
            dec += 2**pow
        pow -= 1
    return dec

def funct5(val): 
    neg = val < 0
    if neg:
        val = -val
    bins = bin(val)[2:] #bin_str
    if neg:
        str1 = ''.join('1' if bit == '0' else '0' for bit in bins) #inverted str
        ans = list(str1)
        for i in range(len(str1) - 1, -1, -1):
            if ans[i] == '0':
                ans[i] = '1'
                break
            else:
                ans[i] = '0'
        else:
            ans.insert(0, '1')

        return ''.join(ans)
    else:
        return bins

def funct6(val,bits): #sign ext
    if val[0]=='1':
        return int(val,2)-(1<<bits)
    return int(val,2)

def funct8(bins):
  if bins[0] == '1':
    a = ''.join('1' if bit == '0' else '0' for bit in bins) 
    dec = -1 * (int(a, 2) + 1)
  else:
    dec= int(bins, 2)
  return dec

def Type_R(I):
    funct7 = I[:7]
    rs2 = int(I[7:12], 2)
    rs1 = int(I[12:17], 2)
    funct3 = I[17:20]
    rd = int(I[20:25], 2)
    if funct7 == "0000000": 
        if funct3 == "000":
            r[rd] = r[rs1] + r[rs2]
        elif funct3 == "010":  
            r[rd] = 1 if r[rs1] < r[rs2] else 0
        elif funct3 == "101": #slt
            sh= r[rs2] & 0b11111
            r[rd] = r[rs1] >>sh
        elif funct3 == "110": 
            r[rd] = r[rs1] | r[rs2]
        elif funct3 == "111": 
            r[rd] = r[rs1] & r[rs2]


    elif funct7 == "0100000":
        if funct3 == "000":
            if (rs1 == 0):
              r[rd] = 0 - r[rs2]
            else:
              r[rd] = r[rs1] - r[rs2]
        else:
          print("Invalid Instruction")

def Load(I):
    rs1 = int(I[-20:-15], 2)
    rd = int(I[-12:-7], 2)
    imm = I[:-20]
    immf=funct4(imm)
    funct3 = I[-15:-12]
    if funct3 == "010": #lw
        offset = immf + r[rs1]
        addr = 0x00010000 + offset
        r[rd] = memory[hex(addr)[2:].upper()]

def Type_I(I):
    opcode = I[-7:]
    rs1 = int(I[-20:-15], 2)
    rd = int(I[-12:-7], 2)
    imm = I[:-20]
    funct3 = I[-15:-12]
    if opcode == "0010011": 
        if funct3 == "000":  
            r[rd] = r[rs1] + funct8(imm)
    elif opcode == "1100111": 
        if funct3 == "000":
            immd = funct8(imm) #imm_dec
            target = (r[rs1] + immd) & ~1 
            r[rd] = x["PC"] + 4  
            x["PC"] = target-4
            return

def Type_B(I):
    if(I[-32:-7]=="0"*25):
        return x["PC"]
    imm = I[-32] + I[-8] + I[-31:-25] + I[-12:-8]
    rs1 = int(I[-20:-15], 2)
    rs2 = int(I[-25:-20], 2)
    funct3 = I[-15:-12]
    if funct3 == "000": 
        if r[rs1] == r[rs2]:
            x["PC"] += funct8(imm[-12:]+"0")
            x["PC"]-=4
    elif funct3 == "001": 
        if r[rs1] != r[rs2]:
            x["PC"] += funct8(imm[-12:]+"0")
            x["PC"]-=4
            return

def Type_S(I):

    imm1 = I[-32:-25]
    imm2 = I[-12:-7]
    imm = imm1 + imm2  
    rs2 = int(I[-25:-20], 2)
    rs1 = int(I[-20:-15], 2)
    immf=funct4(imm)
    funct3 = I[-15:-12]
    if funct3 == "010":
        offset = immf + r[rs1]
        addr = 0x00010000 + offset
        memory[hex(addr)[2:].upper()] = r[rs2]

file = open(sys.argv[2], "w")
# file = open("output.txt", "w")
    
def Print_reg():
        file.write(db(x["PC"], 32) + " ")
        for i in range(32):
            ans = db(r[i], 32)
            file.write(ans + " ") 
        file.write("\n")


def Type_J(I):
    imm = I[0] + I[12:20] + I[11] + I[1:11]
    rd = int(I[20:25], 2) 
    r[rd] = x["PC"] + 4 
    x["PC"] =x["PC"]+funct8(imm+"0")
    x["PC"]-=4
 
# f = open("input.txt", "r")
f = open(sys.argv[1], "r") 
machine_code = f.read().splitlines()
max_pc = len(machine_code)*4
while x["PC"] < max_pc:
    # print(memory)
    I = machine_code[int(x["PC"]/4)]
    opcode = I[-7:]
    # print(opcode)
    
    # print(instruction)
    if  I == "00000000000000000000000001100011":
        break
    if opcode == "0110011":
        Type_R(I)
        # x["PC"]+=4
    elif opcode == "0000011":
        Load(I)
        # x["PC"]+=4
    elif opcode == "0010011" or opcode == "1100111":
        Type_I(I)
        # continue 
        # x["PC"]+=4
    elif opcode == "0100011":
        # print(opcode)
        Type_S(I)
        # print('s')
        # x["PC"]+=4
    elif opcode == "1100011":
        Type_B(I)
        # x[="PC"]+=4
    elif opcode == "1101111":
        Type_J(I)
        # x["PC"]+=4
    elif I == "11100110000000000000000000000000":  # halt
        print("Program halted.")
    else:
        print("Invalid instruction")
        # x["PC"]+=4
    r[0] = 0
    x["PC"] += 4
    # print(x["PC"])
    Print_reg()
Print_reg()
Print_mem()
file.close()
