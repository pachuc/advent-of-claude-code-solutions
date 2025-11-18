#!/usr/bin/env python3
"""Test edge cases from the test plan."""

from solution import calculate_severity, is_caught

print("--- Edge Case Tests ---\n")

# Test 3.1: Range = 1 (Division by Zero Edge Case)
print("Test 3.1: Range = 1 (all scanners always at position 0)")
layers = [(0, 1), (5, 1), (10, 1)]
result = calculate_severity(layers)
expected = 0*1 + 5*1 + 10*1  # = 15
print(f"Result: {result}, Expected: {expected}, Match: {result == expected}")
# Also verify no division by zero errors occur
for depth in [0, 5, 10, 100]:
    caught = is_caught(depth, 1)
    print(f"  is_caught({depth}, 1) = {caught} (should be True)")

# Test 3.2: Depth = 0 Only
print("\nTest 3.2: Depth = 0 only")
layers = [(0, 5)]
result = calculate_severity(layers)
expected = 0 * 5  # = 0
print(f"Result: {result}, Expected: {expected}, Match: {result == expected}")

# Test 3.3: No Layers Caught
print("\nTest 3.3: No layers caught")
layers = [(1, 3), (3, 5)]
result = calculate_severity(layers)
expected = 0
print(f"Result: {result}, Expected: {expected}, Match: {result == expected}")
# Verify manually:
# Layer 1, range 3: period = 4, 1 % 4 = 1 (not caught)
# Layer 3, range 5: period = 8, 3 % 8 = 3 (not caught)
print(f"  Layer 1: caught={is_caught(1, 3)} (should be False)")
print(f"  Layer 3: caught={is_caught(3, 5)} (should be False)")

# Test 3.4: All Layers Caught
print("\nTest 3.4: All layers caught")
layers = [(0, 2), (2, 2), (4, 3)]
result = calculate_severity(layers)
expected = 0*2 + 2*2 + 4*3  # = 0 + 4 + 12 = 16
print(f"Result: {result}, Expected: {expected}, Match: {result == expected}")
# Verify manually:
# Layer 0: always caught
# Layer 2, range 2: period = 2, 2 % 2 = 0 (caught)
# Layer 4, range 3: period = 4, 4 % 4 = 0 (caught)
print(f"  Layer 0: caught={is_caught(0, 2)} (should be True)")
print(f"  Layer 2: caught={is_caught(2, 2)} (should be True)")
print(f"  Layer 4: caught={is_caught(4, 3)} (should be True)")

# Test 3.5: Large Depth Values
print("\nTest 3.5: Large depth values")
layers = [(1000, 10)]
result = calculate_severity(layers)
expected = 0  # 1000 % 18 = 10, not caught
print(f"Result: {result}, Expected: {expected}, Match: {result == expected}")
print(f"  is_caught(1000, 10) = {is_caught(1000, 10)} (should be False, 1000 % 18 = {1000 % 18})")

# Test 3.6: Large Range Values
print("\nTest 3.6: Large range values")
layers = [(100, 100)]
result = calculate_severity(layers)
expected = 0  # 100 % 198 = 100, not caught
print(f"Result: {result}, Expected: {expected}, Match: {result == expected}")
print(f"  is_caught(100, 100) = {is_caught(100, 100)} (should be False, 100 % 198 = {100 % 198})")

# Test 3.7: Empty Input
print("\nTest 3.7: Empty input")
layers = []
result = calculate_severity(layers)
expected = 0
print(f"Result: {result}, Expected: {expected}, Match: {result == expected}")

print("\n--- All Edge Case Tests Complete ---")
