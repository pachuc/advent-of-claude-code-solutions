#!/usr/bin/env python3
"""Test with actual input and measure performance"""

import time
from solution import parse_input, execute_program

# Read actual input
with open('input.md', 'r') as f:
    input_text = f.read()

# Parse input
ip_register, instructions = parse_input(input_text)
print(f"IP bound to register: {ip_register}")
print(f"Number of instructions: {len(instructions)}")
print()

# Execute with timing
start_time = time.time()
result = execute_program(ip_register, instructions, debug=False)
end_time = time.time()

execution_time = end_time - start_time
print(f"Final result: {result}")
print(f"Execution time: {execution_time:.3f} seconds")
print()

if execution_time < 1:
    print("Performance: EXCELLENT (< 1 second)")
elif execution_time < 5:
    print("Performance: GOOD (1-5 seconds)")
elif execution_time < 30:
    print("Performance: ACCEPTABLE (5-30 seconds)")
else:
    print("Performance: WARNING (> 30 seconds)")
