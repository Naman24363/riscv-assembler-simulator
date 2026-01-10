# Test 9: Shift Operations
# Tests sll, srl, sra, slli, srli, srai instructions
addi t0, zero, 8         # t0 = 8 (binary: 1000)
addi t1, zero, 2         # t1 = 2 (shift amount)
sll t2, t0, t1           # t2 = 8 << 2 = 32
srl t3, t0, t1           # t3 = 8 >> 2 = 2
addi s0, zero, -16       # s0 = -16 (for arithmetic shift test)
addi s1, zero, 2         # s1 = 2
sra s2, s0, s1           # s2 = -16 >> 2 = -4 (arithmetic)
slli t4, t0, 3           # t4 = 8 << 3 = 64
srli t5, t0, 1           # t5 = 8 >> 1 = 4
srai s3, s0, 1           # s3 = -16 >> 1 = -8 (arithmetic)
beq zero, zero, 0
