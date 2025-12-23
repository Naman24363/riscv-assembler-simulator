"""
Test Script for RISC-V Assembler and Simulator
Runs all test cases and verifies the results
"""
import subprocess
import os

# Paths
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TESTS_DIR = os.path.join(ROOT_DIR, "tests")
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
    asm_file = os.path.join(TESTS_DIR, test["asm_file"])
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
