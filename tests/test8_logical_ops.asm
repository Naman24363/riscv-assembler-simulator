# Test 8: XOR and Logical Operations
# Tests xor, ori, andi, xori instructions
addi t0, zero, 10        # t0 = 10 (binary: 1010)
addi t1, zero, 12        # t1 = 12 (binary: 1100)
xor t2, t0, t1           # t2 = 10 ^ 12 = 6 (0110)
ori t3, zero, 255        # t3 = 255
andi t4, t3, 15          # t4 = 255 & 15 = 15
xori t5, t0, 15          # t5 = 10 ^ 15 = 5
beq zero, zero, 0
