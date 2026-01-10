# Test 13: JALR Instruction
# Tests jalr (jump and link register)
addi t0, zero, 20        # t0 = 20 (target address)
jalr ra, t0, 0           # Jump to address 20, ra = PC+4 (8)
addi t1, zero, 99        # Should be skipped (addr 8)
addi t1, zero, 99        # Should be skipped (addr 12)
addi t1, zero, 99        # Should be skipped (addr 16)
addi t1, zero, 50        # This is at address 20, should execute
addi t2, zero, 100       # t2 = 100
beq zero, zero, 0
