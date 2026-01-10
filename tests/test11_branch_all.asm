# Test 11: Branch Instructions (All Types)
# Tests beq, bne, blt, bge
addi t0, zero, 10        # t0 = 10
addi t1, zero, 20        # t1 = 20
addi t2, zero, 10        # t2 = 10 (equal to t0)
addi s0, zero, 0         # s0 = result counter

# Test blt (signed less than): 10 < 20 should branch
blt t0, t1, blt_pass
addi s0, zero, 99
blt_pass: addi s0, s0, 1

# Test bge (signed greater or equal): 20 >= 10 should branch  
bge t1, t0, bge_pass
addi s0, zero, 99
bge_pass: addi s0, s0, 1

# Test beq (equal): 10 == 10 should branch
beq t0, t2, beq_pass
addi s0, zero, 99
beq_pass: addi s0, s0, 1

# Test bne (not equal): 10 != 20 should branch
bne t0, t1, bne_pass
addi s0, zero, 99
bne_pass: addi s0, s0, 1

beq zero, zero, 0
