#!/usr/bin/env python3
"""Test the solution with the example from the problem statement."""

from solution import parse_instructions, execute

# Example from problem statement
example_input = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""

instructions = parse_instructions(example_input.strip().split('\n'))
result = execute(instructions)

print(f"Example test result: {result}")
print(f"Expected: 42")
print(f"Test {'PASSED' if result == 42 else 'FAILED'}")
