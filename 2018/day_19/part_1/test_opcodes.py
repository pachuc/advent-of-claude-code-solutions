#!/usr/bin/env python3
"""Quick tests for opcodes"""

from solution import create_opcode_functions

# Get opcode functions
ops = create_opcode_functions()

def test_opcode(name, regs_initial, A, B, C, expected_reg, expected_value):
    """Test a single opcode"""
    regs = regs_initial.copy()
    ops[name](regs, A, B, C)
    actual = regs[expected_reg]
    status = "PASS" if actual == expected_value else "FAIL"
    print(f"{status}: {name} {A} {B} {C} -> reg[{expected_reg}]={actual} (expected {expected_value})")
    return actual == expected_value

print("Testing opcodes:")
print()

# Addition
test_opcode('addr', [5, 3, 0, 0, 0, 0], 0, 1, 2, 2, 8)
test_opcode('addi', [5, 0, 0, 0, 0, 0], 0, 10, 1, 1, 15)

# Multiplication
test_opcode('mulr', [4, 3, 0, 0, 0, 0], 0, 1, 2, 2, 12)
test_opcode('muli', [7, 0, 0, 0, 0, 0], 0, 5, 1, 1, 35)

# Bitwise AND
test_opcode('banr', [12, 10, 0, 0, 0, 0], 0, 1, 2, 2, 8)
test_opcode('bani', [15, 0, 0, 0, 0, 0], 0, 7, 1, 1, 7)

# Bitwise OR
test_opcode('borr', [12, 10, 0, 0, 0, 0], 0, 1, 2, 2, 14)
test_opcode('bori', [8, 0, 0, 0, 0, 0], 0, 5, 1, 1, 13)

# Assignment
test_opcode('setr', [0, 42, 0, 0, 0, 0], 1, 999, 2, 2, 42)
test_opcode('seti', [0, 0, 0, 0, 0, 0], 123, 999, 3, 3, 123)

# Greater-than
test_opcode('gtir', [0, 5, 0, 0, 0, 0], 10, 1, 2, 2, 1)  # 10 > 5
test_opcode('gtir', [0, 10, 0, 0, 0, 0], 5, 1, 2, 2, 0)  # 5 > 10 is false
test_opcode('gtri', [10, 0, 0, 0, 0, 0], 0, 5, 1, 1, 1)  # 10 > 5
test_opcode('gtri', [5, 0, 0, 0, 0, 0], 0, 10, 1, 1, 0)  # 5 > 10 is false
test_opcode('gtrr', [10, 5, 0, 0, 0, 0], 0, 1, 2, 2, 1)  # 10 > 5
test_opcode('gtrr', [5, 10, 0, 0, 0, 0], 0, 1, 2, 2, 0)  # 5 > 10 is false

# Equality
test_opcode('eqir', [0, 7, 0, 0, 0, 0], 7, 1, 2, 2, 1)  # 7 == 7
test_opcode('eqir', [0, 5, 0, 0, 0, 0], 7, 1, 2, 2, 0)  # 7 == 5 is false
test_opcode('eqri', [7, 0, 0, 0, 0, 0], 0, 7, 1, 1, 1)  # 7 == 7
test_opcode('eqri', [5, 0, 0, 0, 0, 0], 0, 7, 1, 1, 0)  # 5 == 7 is false
test_opcode('eqrr', [7, 7, 0, 0, 0, 0], 0, 1, 2, 2, 1)  # 7 == 7
test_opcode('eqrr', [7, 5, 0, 0, 0, 0], 0, 1, 2, 2, 0)  # 7 == 5 is false

print()
print("All opcode tests completed!")
