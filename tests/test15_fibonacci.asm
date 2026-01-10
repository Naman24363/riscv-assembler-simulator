# Test 15: Fibonacci Sequence (First 7 numbers)
# Computes fib(0)=0, fib(1)=1, fib(2)=1, fib(3)=2, fib(4)=3, fib(5)=5, fib(6)=8
addi t0, zero, 0         # fib(0) = 0
addi t1, zero, 1         # fib(1) = 1
add t2, t0, t1           # fib(2) = 0+1 = 1
add t3, t1, t2           # fib(3) = 1+1 = 2
add t4, t2, t3           # fib(4) = 1+2 = 3
add t5, t3, t4           # fib(5) = 2+3 = 5
add s0, t4, t5           # fib(6) = 3+5 = 8
beq zero, zero, 0
