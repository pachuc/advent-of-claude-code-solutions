#!/usr/bin/env python3
"""Test instruction parsing"""

from solution import parse_instructions

print("Testing instruction parsing:")
print("="*60)

instructions = parse_instructions("input.md")

print(f"Total instructions parsed: {len(instructions)}")
print()

# Test first few instructions
print("First 5 instructions:")
for i in range(5):
    print(f"  {i}: {instructions[i]}")

print()

# Test key instructions mentioned in test plan
print("Key instructions:")
print(f"  0: {instructions[0]} (should be jio a, +22)")
print(f"  21: {instructions[21]} (should be jmp +19)")
print(f"  40: {instructions[40]} (should be jio a, +8)")
print(f"  41: {instructions[41]} (should be inc b)")
print(f"  42: {instructions[42]} (should be jie a, +4)")
print(f"  46: {instructions[46]} (should be hlf a)")
print(f"  47: {instructions[47]} (should be jmp -7)")

print()

# Verify specific parsing
assert instructions[0] == {"op": "jio", "reg": "a", "offset": 22}, "Parsing of jio failed"
assert instructions[21] == {"op": "jmp", "offset": 19}, "Parsing of jmp failed"
assert instructions[40] == {"op": "jio", "reg": "a", "offset": 8}, "Parsing of jio failed"
assert instructions[41] == {"op": "inc", "reg": "b"}, "Parsing of inc failed"
assert instructions[42] == {"op": "jie", "reg": "a", "offset": 4}, "Parsing of jie failed"
assert instructions[46] == {"op": "hlf", "reg": "a"}, "Parsing of hlf failed"
assert instructions[47] == {"op": "jmp", "offset": -7}, "Parsing of jmp with negative offset failed"

print("="*60)
print("✓ ALL PARSING TESTS PASSED")
print("="*60)
