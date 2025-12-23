# RISC-V Assembler & Simulator

A complete RISC-V assembler and simulator built in Python. This project assembles RISC-V assembly code into 32-bit machine code and simulates its execution with full register and memory state tracking.

---

## Features

- Converts RISC-V assembly to 32-bit binary machine code
- Executes machine code with cycle-accurate register updates
- Supports labels for branches and jumps
- Simulates load/store with memory state tracking
- Handles negative numbers with two's complement
- Includes automated test suite with 7 test cases

---

## Project Structure

```
CO-Assignment/
├── Assembler.py          # RISC-V Assembler
├── Simulator.py          # RISC-V Simulator
├── run_tests.py          # Automated test runner
├── README.md
├── tests/                # Assembly test files
│   ├── test1_arithmetic.asm
│   ├── test2_memory.asm
│   ├── test3_branch.asm
│   ├── test4_jump.asm
│   ├── test5_loop.asm
│   ├── test6_negative.asm
│   └── test7_compare_shift.asm
└── output/               # Generated binaries & results
```

---

## Usage

### Prerequisites
- Python 3.x

### Assemble a Program
```bash
python Assembler.py <input.asm> <output.bin>
```

### Run the Simulator
```bash
python Simulator.py <input.bin> <output.txt>
```

### Run All Tests
```bash
python run_tests.py
```

---

## Supported Instructions

| Type | Instructions | Format |
|------|-------------|--------|
| R-Type | `add`, `sub`, `and`, `or`, `slt`, `srl` | `op rd, rs1, rs2` |
| I-Type | `addi`, `lw`, `jalr` | `op rd, rs1, imm` |
| S-Type | `sw` | `sw rs2, offset(rs1)` |
| B-Type | `beq`, `bne` | `op rs1, rs2, label/offset` |
| J-Type | `jal` | `jal rd, label/offset` |

---

## Instruction Encoding

### R-Type (Register)
```
| funct7 (7) | rs2 (5) | rs1 (5) | funct3 (3) | rd (5) | opcode (7) |
```

### I-Type (Immediate)
```
| imm[11:0] (12) | rs1 (5) | funct3 (3) | rd (5) | opcode (7) |
```

### S-Type (Store)
```
| imm[11:5] (7) | rs2 (5) | rs1 (5) | funct3 (3) | imm[4:0] (5) | opcode (7) |
```

### B-Type (Branch)
```
| imm[12|10:5] (7) | rs2 (5) | rs1 (5) | funct3 (3) | imm[4:1|11] (5) | opcode (7) |
```

### J-Type (Jump)
```
| imm[20|10:1|11|19:12] (20) | rd (5) | opcode (7) |
```

---

## Register Map

| Register | ABI Name | Description |
|----------|----------|-------------|
| x0 | zero | Hardwired zero |
| x1 | ra | Return address |
| x2 | sp | Stack pointer |
| x5-x7 | t0-t2 | Temporaries |
| x8 | s0/fp | Saved register / Frame pointer |
| x10-x17 | a0-a7 | Function arguments |
| x18-x27 | s2-s11 | Saved registers |
| x28-x31 | t3-t6 | Temporaries |

---

## Test Cases

| Test | Description | Instructions Tested |
|------|-------------|---------------------|
| 1 | Basic Arithmetic | `addi`, `add`, `sub`, `and`, `or` |
| 2 | Memory Operations | `sw`, `lw` |
| 3 | Branch with Labels | `beq` |
| 4 | Jump Operations | `jal` |
| 5 | Loop Construct | `bne` |
| 6 | Negative Numbers | Two's complement |
| 7 | Compare & Shift | `slt`, `srl` |

---

## Output Format

### Assembler Output
Each line contains a 32-bit binary instruction:
```
00000000101000000000001010010011
00000000010100000000001100010011
00000000011000101000001110110011
```

### Simulator Output
Each line shows PC and all 32 registers in binary format, followed by memory dump.

---

## Example

### Input Assembly
```asm
addi t0, zero, 10
addi t1, zero, 5
add t2, t0, t1
beq zero, zero, 0
```

### Result
- `t0` = 10
- `t1` = 5  
- `t2` = 15

---

## Team

| Name | Roll Number |
|------|-------------|
| Anoushka Malik | 2024086 |
| Cho Hnin Lwin | 2024165 |
| Naman Chug | 2024363 |
| Parth Kumar | 2024404 |

---

Computer Organization Course Assignment