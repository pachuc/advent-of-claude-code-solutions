#!/usr/bin/env python3
"""Test the example from the problem statement."""

from solution import calculate_severity, is_caught

# Test the provided example
example_layers = [(0, 3), (1, 2), (4, 4), (6, 4)]
result = calculate_severity(example_layers)
print(f"Example test result: {result}")
print(f"Expected: 24")
print(f"Match: {result == 24}")

# Test is_caught function with specific cases from test plan
print("\n--- Testing is_caught function ---")
test_cases = [
    (0, 3, True),   # 0 % 4 = 0
    (1, 2, False),  # 1 % 2 = 1
    (2, 2, True),   # 2 % 2 = 0
    (6, 4, True),   # 6 % 6 = 0
    (4, 4, False),  # 4 % 6 = 4
    (8, 3, True),   # 8 % 4 = 0
    (10, 3, False), # 10 % 4 = 2
]

all_passed = True
for depth, range_val, expected in test_cases:
    result = is_caught(depth, range_val)
    match = result == expected
    all_passed = all_passed and match
    print(f"is_caught({depth}, {range_val}) = {result}, expected {expected}: {'PASS' if match else 'FAIL'}")

print(f"\nAll is_caught tests passed: {all_passed}")
