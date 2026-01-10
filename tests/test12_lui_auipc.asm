# Test 12: LUI and AUIPC Instructions
# Tests lui and auipc U-type instructions
lui t0, 1                # t0 = 1 << 12 = 4096
lui t1, 2                # t1 = 2 << 12 = 8192
lui t2, 16               # t2 = 16 << 12 = 65536
addi t3, t0, 100         # t3 = 4096 + 100 = 4196
auipc t4, 0              # t4 = PC (should be 16 at this point)
beq zero, zero, 0
