# Test 14: Complex Arithmetic Expression
# Computes: result = (a + b) * 2 - c using available ops
# a=15, b=10, c=5 -> result = (15+10)*2-5 = 45
addi t0, zero, 15        # a = 15
addi t1, zero, 10        # b = 10
addi t2, zero, 5         # c = 5
add t3, t0, t1           # t3 = a + b = 25
slli t4, t3, 1           # t4 = (a+b) * 2 = 50
sub t5, t4, t2           # t5 = (a+b)*2 - c = 45
beq zero, zero, 0
