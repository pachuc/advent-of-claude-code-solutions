#!/usr/bin/env python3
"""Test individual instruction types"""

from solution import execute_instruction

print("Testing individual instruction types:")
print("="*60)

# Test hlf
print("\n1. Testing hlf (halve):")
registers = {"a": 10, "b": 0}
pc = execute_instruction({"op": "hlf", "reg": "a"}, registers, 0)
print(f"   hlf a: 10 -> {registers['a']} (expected 5), PC: 0 -> {pc}")
assert registers['a'] == 5 and pc == 1, "hlf failed"

registers = {"a": 7, "b": 0}
pc = execute_instruction({"op": "hlf", "reg": "a"}, registers, 0)
print(f"   hlf a: 7 -> {registers['a']} (expected 3, integer division), PC: 0 -> {pc}")
assert registers['a'] == 3 and pc == 1, "hlf integer division failed"

# Test tpl
print("\n2. Testing tpl (triple):")
registers = {"a": 5, "b": 0}
pc = execute_instruction({"op": "tpl", "reg": "a"}, registers, 0)
print(f"   tpl a: 5 -> {registers['a']} (expected 15), PC: 0 -> {pc}")
assert registers['a'] == 15 and pc == 1, "tpl failed"

# Test inc
print("\n3. Testing inc (increment):")
registers = {"a": 0, "b": 0}
pc = execute_instruction({"op": "inc", "reg": "a"}, registers, 0)
print(f"   inc a: 0 -> {registers['a']} (expected 1), PC: 0 -> {pc}")
assert registers['a'] == 1 and pc == 1, "inc failed"

# Test jmp
print("\n4. Testing jmp (unconditional jump):")
pc = execute_instruction({"op": "jmp", "offset": 5}, {}, 10)
print(f"   jmp +5 at PC=10 -> PC={pc} (expected 15)")
assert pc == 15, "jmp positive failed"

pc = execute_instruction({"op": "jmp", "offset": -3}, {}, 10)
print(f"   jmp -3 at PC=10 -> PC={pc} (expected 7)")
assert pc == 7, "jmp negative failed"

# Test jie (jump if even)
print("\n5. Testing jie (jump if even):")
registers = {"a": 4, "b": 0}
pc = execute_instruction({"op": "jie", "reg": "a", "offset": 3}, registers, 5)
print(f"   jie a, +3 at PC=5 with a=4 (even) -> PC={pc} (expected 8, jump taken)")
assert pc == 8, "jie with even failed"

registers = {"a": 5, "b": 0}
pc = execute_instruction({"op": "jie", "reg": "a", "offset": 3}, registers, 5)
print(f"   jie a, +3 at PC=5 with a=5 (odd) -> PC={pc} (expected 6, no jump)")
assert pc == 6, "jie with odd failed"

registers = {"a": 0, "b": 0}
pc = execute_instruction({"op": "jie", "reg": "a", "offset": 3}, registers, 5)
print(f"   jie a, +3 at PC=5 with a=0 (even) -> PC={pc} (expected 8, 0 is even)")
assert pc == 8, "jie with 0 failed"

# Test jio (jump if one)
print("\n6. Testing jio (jump if one):")
registers = {"a": 1, "b": 0}
pc = execute_instruction({"op": "jio", "reg": "a", "offset": 10}, registers, 5)
print(f"   jio a, +10 at PC=5 with a=1 -> PC={pc} (expected 15, jump taken)")
assert pc == 15, "jio with 1 failed"

registers = {"a": 2, "b": 0}
pc = execute_instruction({"op": "jio", "reg": "a", "offset": 10}, registers, 5)
print(f"   jio a, +10 at PC=5 with a=2 -> PC={pc} (expected 6, no jump)")
assert pc == 6, "jio with 2 failed"

registers = {"a": 0, "b": 0}
pc = execute_instruction({"op": "jio", "reg": "a", "offset": 10}, registers, 5)
print(f"   jio a, +10 at PC=5 with a=0 -> PC={pc} (expected 6, no jump)")
assert pc == 6, "jio with 0 failed"

print("\n" + "="*60)
print("✓ ALL INSTRUCTION TYPE TESTS PASSED")
print("="*60)
