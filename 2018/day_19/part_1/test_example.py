#!/usr/bin/env python3
"""Test with the example from the problem"""

from solution import parse_input, execute_program

# Example from problem.md
example_input = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

# Parse and execute
ip_register, instructions = parse_input(example_input)
result = execute_program(ip_register, instructions, debug=True)

print(f"\nFinal result: {result}")
print(f"Expected: 6")
print(f"Test {'PASSED' if result == 6 else 'FAILED'}!")
