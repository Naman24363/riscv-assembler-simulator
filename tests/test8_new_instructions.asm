# Test new instructions: xor, sll, slli, srli, ori, andi, blt, lui
addi t0, zero, 12
addi t1, zero, 5
xor t2, t0, t1
sll t3, t0, t1
ori t4, zero, 255
andi t5, t4, 15
lui s0, 1
addi s1, zero, 3
slli s2, t0, 2
srli s3, t0, 2
blt t1, t0, skip
addi s4, zero, 99
skip: addi s4, zero, 42
beq zero, zero, 0
