#!/usr/bin/env python3
"""Verify critical execution flow of the actual input"""

from solution import parse_instructions, simulate

# Parse the actual input
instructions = parse_instructions("input.md")

print("Verifying critical execution flow:")
print(f"Total instructions: {len(instructions)}")
print()

# Check first instruction
print(f"Instruction 0: {instructions[0]}")
print(f"Expected: jio a, +22 (should jump to PC=22 when a=1)")
print()

# Check instruction at PC=22
print(f"Instruction 22: {instructions[22]}")
print(f"Expected: jmp +19 (should jump to PC=41)")
print()

# Check instruction at PC=41
print(f"Instruction 41: {instructions[41]}")
print(f"Expected: jio a, +8 (jumps to PC=49 when a=1, terminating the program)")
print()

# Run simulation with verbose mode for first 20 iterations
print("="*60)
print("Running simulation with verbose output (first 20 iterations):")
print("="*60)

registers = simulate(instructions, initial_a=1, initial_b=0, verbose=True, max_iterations=1_000_000)

print()
print("="*60)
print(f"FINAL RESULT: b = {registers['b']}")
print("="*60)

# Verify answer
expected_answer = 334
if registers['b'] == expected_answer:
    print(f"✓ PASSED: Got expected answer {expected_answer}")
else:
    print(f"✗ FAILED: Expected {expected_answer}, got {registers['b']}")
