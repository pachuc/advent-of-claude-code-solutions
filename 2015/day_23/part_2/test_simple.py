#!/usr/bin/env python3
"""Test with the example program from problem description"""

from solution import execute_instruction

# Example program:
# inc a
# jio a, +2
# tpl a
# inc a
# With a=0, should result in a=2, b=0

instructions = [
    {"op": "inc", "reg": "a"},
    {"op": "jio", "reg": "a", "offset": 2},
    {"op": "tpl", "reg": "a"},
    {"op": "inc", "reg": "a"}
]

# Test with a=0 (as in example)
registers = {"a": 0, "b": 0}
pc = 0

print("Testing example program with a=0, b=0:")
print(f"Initial: PC={pc}, a={registers['a']}, b={registers['b']}")

iteration = 0
while 0 <= pc < len(instructions):
    inst = instructions[pc]
    print(f"[{iteration}] PC={pc} | a={registers['a']}, b={registers['b']} | {inst}")
    pc = execute_instruction(inst, registers, pc)
    iteration += 1

print(f"Final: PC={pc}, a={registers['a']}, b={registers['b']}")

# Expected: a=2, b=0
if registers['a'] == 2 and registers['b'] == 0:
    print("✓ PASSED: Example program works correctly")
else:
    print(f"✗ FAILED: Expected a=2, b=0, got a={registers['a']}, b={registers['b']}")

# Test with a=1 (Part 2 condition)
print("\n" + "="*50)
print("Testing same program with a=1, b=0:")
registers = {"a": 1, "b": 0}
pc = 0

print(f"Initial: PC={pc}, a={registers['a']}, b={registers['b']}")

iteration = 0
while 0 <= pc < len(instructions):
    inst = instructions[pc]
    print(f"[{iteration}] PC={pc} | a={registers['a']}, b={registers['b']} | {inst}")
    pc = execute_instruction(inst, registers, pc)
    iteration += 1

print(f"Final: PC={pc}, a={registers['a']}, b={registers['b']}")
print("With a=1, jio jumps over tpl instruction, so a becomes 2")
