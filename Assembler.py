import sys
input_file = sys.argv[1]
output_file = sys.argv[2]

f_ans = [] 
with open(input_file, 'r') as file:
    lines = file.readlines()

with open(output_file, 'w') as file:
    for output in f_ans:
        file.write(output + '\n')

Registers = {
    "zero": "00000",
    "ra": "00001",  
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "fp": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111"
}

B_type = {
    "beq": {"opcode": "1100011", "funct3": "000"},
    "bne": {"opcode": "1100011", "funct3": "001"},
}

S_Type = {
        "sw": {"opcode": "0100011", "funct3": "010"}
}

R_Type = {
        "add": {"opcode": "0110011", "funct3": "000", "funct7": "0000000"},
        "sub": {"opcode": "0110011", "funct3": "000", "funct7": "0100000"},
        "slt": {"opcode": "0110011", "funct3": "010", "funct7": "0000000"},
        "srl": {"opcode": "0110011", "funct3": "101", "funct7": "0000000"},
        "or": {"opcode": "0110011", "funct3": "110", "funct7": "0000000"},
        "and": {"opcode": "0110011", "funct3": "111", "funct7": "0000000"}

}

I_Type = {
        "lw": {"opcode": "0000011", "funct3": "010"},
        "addi": {"opcode": "0010011", "funct3": "000"},
        "jalr": {"opcode": "1100111", "funct3": "000"}
}

def funct1(a: str, b: str) -> str: #2's complement
    s = []
    carry = 0
    i = len(a) - 1
    j = len(b) - 1
    while i >= 0 or j >= 0 or carry:
        if i >= 0:
            carry += int(a[i])
            i -= 1
        if j >= 0:
            carry += int(b[j])
            j -= 1
        s.append(str(carry % 2))
        carry //= 2
    return ''.join(reversed(s))


def funct2(lines): #parse_mips
    labels = {}
    for idx, line in enumerate(lines, 1):
        if ':' in line:
            label = line.split(':')[0].strip()
            labels[label] = idx
    return labels


def funct3(lines): #remove labels
    l = []
    for line in lines:
        if ':' in line:
            label, statement = line.split(':', 1)
            l.append(statement.strip())
        else:
            l.append(line.strip())
    return l


with open(input_file, 'r') as file:
    lines = file.readlines()

labels = funct2(lines)
l = funct3(lines)

z = 0

for line in lines:
    data = line.strip()
    if not data:
        continue

    for i, char in enumerate(data):
        if char == ':':
            data = data[i + 1:]

    z += 1
    if data.split()[0] in B_type:
        data = data.replace(",", " ")
        if data.split()[3] in labels.keys():
            data_list = list(data.split())
            j = str(4 * (labels[data_list[3]] - z))
            data_list[3] = j
            data = ' '.join(data_list)
        
        decimal_num = int(data.split()[3])
        if decimal_num >= 0:
            bina = bin(decimal_num)[2:].zfill(13) 
        else:
            bina = bin(abs(decimal_num))[2:].zfill(13)
            bina = bina.replace("0", "X").replace("1", "0").replace("X", "1")  
            bina = funct1(bina, "1")
        bina = bina[-13:]
        # print(bina)

        imm12 = bina[0]    
        imm10_5 = bina[1:7]  
        imm4_1 = bina[8:12]  
        # print(imm4_1)
        imm11 = bina[1]   

        opcode = B_type[data.split()[0]]["opcode"]
        funct3 = B_type[data.split()[0]]["funct3"]
        if data.split()[2] not in Registers or data.split()[1] not in Registers:
            f_ans.append("Error: Invalid register")
            continue 
        output = (
            imm12 + imm10_5 + Registers[data.split()[2]] +
            Registers[data.split()[1]] + funct3 + imm4_1 + imm11 + opcode
        )

        f_ans.append(output)

        # R-Type Instruction
    elif data.split()[0] in R_Type:
        opcode = R_Type[data.split()[0]]["opcode"]
        funct3 = R_Type[data.split()[0]]["funct3"]
        funct7 = R_Type[data.split()[0]]["funct7"]
        data = data.replace(",", " ")

        if data.split()[2] not in Registers or data.split()[1] not in Registers or data.split()[3] not in Registers:
            f_ans.append("Error: Invalid register")
            continue

        output = funct7 + Registers[data.split()[3]] + Registers[data.split()[2]] + funct3 + Registers[data.split()[1]] + opcode
        f_ans.append(output)

        # I-Type Instruction
    elif data.split()[0] in I_Type:
        opcode = I_Type[data.split()[0]]["opcode"]
        funct3 = I_Type[data.split()[0]]["funct3"]
        data = data.replace(",", " ")

        if len(data.split()) == 3:
            input_str = data.split()[2]
            opening_index = input_str.find('(')
            number_string = input_str[:opening_index]
            decimal = int(number_string)
            opening_index = input_str.find('(')
            closing_index = input_str.find(')')
            fin_reg = input_str[opening_index + 1:closing_index]
        else:
            decimal = int(data.split()[3])
            fin_reg = data.split()[2]

        if decimal < 0:
            bina = bin(abs(decimal))[2:].zfill(12)
            bina = bina.replace("0", "X").replace("1", "0").replace("X", "1")
            result = funct1(bina, "1")
            imm = result
        else:
            imm = bin(decimal)[2:].zfill(12)

        if fin_reg not in Registers or data.split()[1] not in Registers:
            f_ans.append("Error: Invalid register")
            continue

        output = imm + Registers[fin_reg] + funct3 + Registers[data.split()[1]] + opcode
        f_ans.append(output)
    
        # S-Type Instruction
    elif data.split()[0] in S_Type:
        opcode = S_Type[data.split()[0]]["opcode"]
        funct3 = S_Type[data.split()[0]]["funct3"]
        data = data.replace(",", " ")
        input_str = data.split()[2]
        opening_index = input_str.find('(')
        num_str = input_str[:opening_index]
        result = int(num_str)
        opening_index = input_str.find('(')
        closing_index = input_str.find(')')
        substring = input_str[opening_index + 1:closing_index]

        if result >= 0:
            bina = bin(result)[2:].zfill(12)
        else:
            bina = bin(abs(result))[2:].zfill(12)
            bina = bina.replace("0", "X").replace("1", "0").replace("X", "1")
            result = funct1(bina, "1")
            bina = result

        if substring not in Registers or data.split()[1] not in Registers:
            f_ans.append("Error: Invalid register")
            continue

        output = bina[0:7] + Registers[data.split()[1]] + Registers[substring] + funct3 + bina[7:] + opcode
        f_ans.append(output)

        # J-TYPE INSTRUCTION
    elif data.split()[0] == "jal":
        data = data.replace(",", " ")
        opcode = "1101111"

        target = data.split()[2]

        if target in labels:
            decimal_num = (labels[target] - z) * 4
        else:
            decimal_num = int(target)

        if decimal_num >= 0:
            bina = bin(decimal_num)[2:].zfill(21)
        else:
            bina = bin(abs(decimal_num))[2:].zfill(21)
            bina = bina.replace("0", "X").replace("1", "0").replace("X", "1")
            result = funct1(bina, "1")
            bina = result.zfill(21)

        immm = []
        immm.append(bina[0])      # imm[20]
        immm.extend(bina[10:20])  # imm[10:1]
        immm.append(bina[9])      # imm[11]
        immm.extend(bina[1:9])    # imm[19:12]
        im = ''.join(immm)

        if data.split()[1] not in Registers:
            f_ans.append("Error: Invalid register")
            continue

        output = im + Registers[data.split()[1]] + opcode
        f_ans.append(output)

with open(output_file, 'w') as file:
    for output in f_ans:
        file.write(output + '\n')