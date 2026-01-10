"""
Test Script for RISC-V Assembler and Simulator
Runs all test cases and verifies the results
"""
import subprocess
import os

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

# Test configurations
tests = [
    {
        "name": "Test 1: Basic Arithmetic (R-type & I-type)",
        "asm_file": "test1_arithmetic.asm",
        "expected_registers": {
            5: 10,   # t0 = 10
            6: 5,    # t1 = 5
            7: 15,   # t2 = 10 + 5
            28: 5,   # t3 = 10 - 5
        },
        "description": "Tests addi, add, sub, and, or instructions"
    },
    {
        "name": "Test 2: Memory Operations (S-type & Load)",
        "asm_file": "test2_memory.asm",
        "expected_registers": {
            5: 100,  # t0 = 100
            6: 200,  # t1 = 200
            7: 100,  # t2 = loaded value of t0
            28: 200, # t3 = loaded value of t1
            29: 300, # t4 = t2 + t3
        },
        "description": "Tests sw and lw instructions"
    },
    {
        "name": "Test 3: Branch Operations (B-type)",
        "asm_file": "test3_branch.asm",
        "expected_registers": {
            5: 5,    # t0 = 5
            6: 5,    # t1 = 5
            7: 1,    # t2 = 1 (branch taken because t0 == t1)
        },
        "description": "Tests beq with labels"
    },
    {
        "name": "Test 4: Jump Operations (J-type)",
        "asm_file": "test4_jump.asm",
        "expected_registers": {
            1: 8,    # ra = return address (PC + 4 at jal)
            5: 10,   # t0 = 10 (not overwritten with 99)
            6: 20,   # t1 = 20
            7: 30,   # t2 = 10 + 20
        },
        "description": "Tests jal with labels"
    },
    {
        "name": "Test 5: Loop with bne",
        "asm_file": "test5_loop.asm",
        "expected_registers": {
            5: 5,    # t0 = 5 (after 5 iterations)
            6: 5,    # t1 = 5
            7: 100,  # t2 = 100
        },
        "description": "Tests bne for looping"
    },
    {
        "name": "Test 6: Negative Numbers",
        "asm_file": "test6_negative.asm",
        "expected_registers": {
            5: -5,   # t0 = -5
            6: 10,   # t1 = 10
            7: 5,    # t2 = -5 + 10 = 5
            28: -10, # t3 = -10
            29: 15,  # t4 = 10 - (-5) = 15
        },
        "description": "Tests negative immediates and two's complement"
    },
    {
        "name": "Test 7: Compare and Shift",
        "asm_file": "test7_compare_shift.asm",
        "expected_registers": {
            5: 8,    # t0 = 8
            6: 3,    # t1 = 3
            7: 1,    # t2 = slt(3, 8) = 1
            28: 0,   # t3 = slt(8, 3) = 0
            29: 1,   # t4 = srl(8, 3) = 1
        },
        "description": "Tests slt and srl instructions"
    },
    {
        "name": "Test 8: Logical Operations (XOR, ORI, ANDI, XORI)",
        "asm_file": "test8_logical_ops.asm",
        "expected_registers": {
            5: 10,   # t0 = 10 (1010)
            6: 12,   # t1 = 12 (1100)
            7: 6,    # t2 = 10 ^ 12 = 6 (0110)
            28: 255, # t3 = ori(0, 255)
            29: 15,  # t4 = 255 & 15
            30: 5,   # t5 = 10 ^ 15 = 5
        },
        "description": "Tests xor, ori, andi, xori instructions"
    },
    {
        "name": "Test 9: Shift Operations (SLL, SRL, SRA, SLLI, SRLI, SRAI)",
        "asm_file": "test9_shift_ops.asm",
        "expected_registers": {
            5: 8,    # t0 = 8
            6: 2,    # t1 = 2
            7: 32,   # t2 = 8 << 2 = 32
            28: 2,   # t3 = 8 >> 2 = 2
            29: 64,  # t4 = 8 << 3 = 64
            30: 4,   # t5 = 8 >> 1 = 4
            8: -16,  # s0 = -16
            9: 2,    # s1 = 2
            18: -4,  # s2 = -16 >> 2 = -4 (arithmetic)
            19: -8,  # s3 = -16 >> 1 = -8 (arithmetic)
        },
        "description": "Tests sll, srl, sra, slli, srli, srai instructions"
    },
    {
        "name": "Test 10: Comparison Operations (SLT, SLTU, SLTI, SLTIU)",
        "asm_file": "test10_compare_ops.asm",
        "expected_registers": {
            5: 10,   # t0 = 10
            6: 20,   # t1 = 20
            20: -5,  # s4 = -5
            7: 1,    # t2 = (10 < 20) = 1
            28: 0,   # t3 = (20 < 10) = 0
            29: 1,   # t4 = (-5 < 10) signed = 1
            30: 0,   # t5 = unsigned compare (large > 10) = 0
            8: 1,    # s0 = (10 < 15) = 1
            9: 0,    # s1 = (10 < 5) = 0
            18: 1,   # s2 = (10 < 15) unsigned = 1
        },
        "description": "Tests slt, sltu, slti, sltiu instructions"
    },
    {
        "name": "Test 11: All Branch Types (BEQ, BNE, BLT, BGE)",
        "asm_file": "test11_branch_all.asm",
        "expected_registers": {
            5: 10,   # t0 = 10
            6: 20,   # t1 = 20
            7: 10,   # t2 = 10
            8: 4,    # s0 = 4 (all 4 branches taken)
        },
        "description": "Tests beq, bne, blt, bge branch instructions"
    },
    {
        "name": "Test 12: LUI and AUIPC Instructions",
        "asm_file": "test12_lui_auipc.asm",
        "expected_registers": {
            5: 4096,   # t0 = 1 << 12
            6: 8192,   # t1 = 2 << 12
            7: 65536,  # t2 = 16 << 12
            28: 4196,  # t3 = 4096 + 100
            29: 16,    # t4 = PC at auipc instruction
        },
        "description": "Tests lui and auipc U-type instructions"
    },
    {
        "name": "Test 13: JALR Instruction",
        "asm_file": "test13_jalr.asm",
        "expected_registers": {
            5: 20,   # t0 = 20 (target address)
            1: 8,    # ra = return address (PC+4 after jalr)
            6: 50,   # t1 = 50 (executed after jump)
            7: 100,  # t2 = 100
        },
        "description": "Tests jalr (jump and link register) instruction"
    },
    {
        "name": "Test 14: Complex Arithmetic Expression",
        "asm_file": "test14_complex_expr.asm",
        "expected_registers": {
            5: 15,   # t0 = a = 15
            6: 10,   # t1 = b = 10
            7: 5,    # t2 = c = 5
            28: 25,  # t3 = a + b = 25
            29: 50,  # t4 = (a+b) * 2 = 50
            30: 45,  # t5 = (a+b)*2 - c = 45
        },
        "description": "Tests computing (a+b)*2-c using add, slli, sub"
    },
    {
        "name": "Test 15: Fibonacci Sequence",
        "asm_file": "test15_fibonacci.asm",
        "expected_registers": {
            5: 0,    # t0 = fib(0) = 0
            6: 1,    # t1 = fib(1) = 1
            7: 1,    # t2 = fib(2) = 1
            28: 2,   # t3 = fib(3) = 2
            29: 3,   # t4 = fib(4) = 3
            30: 5,   # t5 = fib(5) = 5
            8: 8,    # s0 = fib(6) = 8
        },
        "description": "Computes first 7 Fibonacci numbers"
    },
]

def parse_register_value(binary_str):
    """Parse a binary string like 0b00000000000000000000000000001010 to integer"""
    if binary_str.startswith('0b'):
        binary_str = binary_str[2:]
    # Handle two's complement for negative numbers
    if binary_str[0] == '1':
        return int(binary_str, 2) - (1 << 32)
    return int(binary_str, 2)

def run_test(test):
    """Run a single test case"""
    asm_file = os.path.join(SCRIPT_DIR, test["asm_file"])
    bin_file = os.path.join(OUTPUT_DIR, test["asm_file"].replace('.asm', '_output.bin'))
    result_file = os.path.join(OUTPUT_DIR, test["asm_file"].replace('.asm', '_result.txt'))
    
    print(f"\n{'='*60}")
    print(f"Running: {test['name']}")
    print(f"Description: {test['description']}")
    print(f"{'='*60}")
    
    # Run assembler
    result = subprocess.run(['python', os.path.join(ROOT_DIR, 'Assembler.py'), asm_file, bin_file], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ASSEMBLER ERROR: {result.stderr}")
        return False
    
    # Check if binary was generated
    if not os.path.exists(bin_file):
        print(f"ERROR: Binary file {bin_file} was not created")
        return False
    
    print(f"Assembled {test['asm_file']} -> {os.path.basename(bin_file)}")
    
    # Run simulator
    result = subprocess.run(['python', os.path.join(ROOT_DIR, 'Simulator.py'), bin_file, result_file],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"SIMULATOR ERROR: {result.stderr}")
        return False
    
    print(f"Simulated {os.path.basename(bin_file)} -> {os.path.basename(result_file)}")
    
    # Parse results
    with open(result_file, 'r') as f:
        lines = f.readlines()
    
    # Get the last register state line (before memory dump)
    reg_line = None
    for line in reversed(lines):
        if line.startswith('0b') and 'x' not in line.lower():
            reg_line = line.strip()
            break
    
    if not reg_line:
        print("ERROR: Could not find register state")
        return False
    
    # Parse register values (format: PC r0 r1 r2 ... r31)
    values = reg_line.split()
    registers = {}
    for i in range(33):  # PC + 32 registers
        if i == 0:
            registers['PC'] = parse_register_value(values[i])
        else:
            registers[i-1] = parse_register_value(values[i])
    
    # Verify expected values
    passed = True
    for reg, expected in test["expected_registers"].items():
        actual = registers.get(reg, None)
        if actual == expected:
            print(f"  ✓ Register {reg}: {actual} (expected {expected})")
        else:
            print(f"  ✗ Register {reg}: {actual} (expected {expected})")
            passed = False
    
    return passed

def main():
    print("="*60)
    print("RISC-V Assembler and Simulator Test Suite")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test in tests:
        if run_test(test):
            passed += 1
            print(f"\n✓ {test['name']} PASSED")
        else:
            failed += 1
            print(f"\n✗ {test['name']} FAILED")
    
    print("\n" + "="*60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0

if __name__ == "__main__":
    main()
