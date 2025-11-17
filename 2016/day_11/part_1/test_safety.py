"""Test safety validation function."""
from solution import is_safe_floor

print("Testing safety validation...")

# Test 1: Empty floor - should be safe
test1 = frozenset()
result1 = is_safe_floor(test1)
print(f"Test 1 (empty floor): {result1} (expected: True)")

# Test 2: Only generators - should be safe
test2 = frozenset([('A', 'G'), ('B', 'G')])
result2 = is_safe_floor(test2)
print(f"Test 2 (only generators): {result2} (expected: True)")

# Test 3: Only microchips - should be safe
test3 = frozenset([('A', 'M'), ('B', 'M')])
result3 = is_safe_floor(test3)
print(f"Test 3 (only microchips): {result3} (expected: True)")

# Test 4: Microchip with its own generator - should be safe
test4 = frozenset([('A', 'M'), ('A', 'G')])
result4 = is_safe_floor(test4)
print(f"Test 4 (microchip with own generator): {result4} (expected: True)")

# Test 5: Multiple pairs - should be safe
test5 = frozenset([('A', 'M'), ('A', 'G'), ('B', 'M'), ('B', 'G')])
result5 = is_safe_floor(test5)
print(f"Test 5 (multiple pairs): {result5} (expected: True)")

# Test 6: Microchip with different generator - should be UNSAFE
test6 = frozenset([('A', 'M'), ('B', 'G')])
result6 = is_safe_floor(test6)
print(f"Test 6 (microchip with different generator): {result6} (expected: False)")

# Test 7: Microchip with multiple generators, missing its own - should be UNSAFE
test7 = frozenset([('A', 'M'), ('B', 'G'), ('C', 'G')])
result7 = is_safe_floor(test7)
print(f"Test 7 (unprotected microchip): {result7} (expected: False)")

# Test 8: One protected, one unprotected - should be UNSAFE
test8 = frozenset([('A', 'M'), ('A', 'G'), ('B', 'M')])
result8 = is_safe_floor(test8)
print(f"Test 8 (one protected, one unprotected): {result8} (expected: False)")

# Summary
all_tests = [
    result1 == True,
    result2 == True,
    result3 == True,
    result4 == True,
    result5 == True,
    result6 == False,
    result7 == False,
    result8 == False
]

if all(all_tests):
    print("\n✓ All safety tests PASSED!")
else:
    print("\n✗ Some safety tests FAILED!")
