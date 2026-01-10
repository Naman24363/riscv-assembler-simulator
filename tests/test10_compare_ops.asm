# Test 10: Comparison Instructions
# Tests slt, sltu, slti, sltiu instructions
addi t0, zero, 10        # t0 = 10
addi t1, zero, 20        # t1 = 20
addi s4, zero, -5        # s4 = -5 (unsigned: large positive)
slt t2, t0, t1           # t2 = (10 < 20) = 1
slt t3, t1, t0           # t3 = (20 < 10) = 0
slt t4, s4, t0           # t4 = (-5 < 10) signed = 1
sltu t5, s4, t0          # t5 = (large > 10) unsigned = 0
slti s0, t0, 15          # s0 = (10 < 15) = 1
slti s1, t0, 5           # s1 = (10 < 5) = 0
sltiu s2, t0, 15         # s2 = (10 < 15) unsigned = 1
beq zero, zero, 0
