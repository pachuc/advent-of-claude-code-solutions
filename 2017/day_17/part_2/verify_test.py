#!/usr/bin/env python3
"""
Verification test comparing optimized and naive implementations.
"""

def solve_spinlock_naive(step_size, iterations):
    """Naive implementation maintaining the full buffer."""
    buffer = [0]
    current_pos = 0

    for value in range(1, iterations + 1):
        current_pos = (current_pos + step_size) % len(buffer)
        current_pos += 1
        buffer.insert(current_pos, value)

    return buffer[1]  # Return value at position 1 (after 0)


def solve_spinlock_optimized(step_size, iterations):
    """Optimized implementation tracking only position 1."""
    current_pos = 0
    buffer_len = 1
    value_after_zero = 0

    for value in range(1, iterations + 1):
        current_pos = (current_pos + step_size) % buffer_len
        insert_pos = current_pos + 1

        if insert_pos == 1:
            value_after_zero = value

        current_pos = insert_pos
        buffer_len += 1

    return value_after_zero


# Test cases from the test plan
test_cases = [
    (3, 10, "Small-scale verification"),
    (355, 2017, "Cross-validation with Part 1"),
    (1, 100, "Edge case: step_size=1"),
    (0, 100, "Edge case: step_size=0"),
    (1000, 100, "Edge case: large step_size"),
]

print("Running verification tests...\n")
all_passed = True

for step_size, iterations, description in test_cases:
    naive_result = solve_spinlock_naive(step_size, iterations)
    optimized_result = solve_spinlock_optimized(step_size, iterations)

    passed = naive_result == optimized_result
    all_passed = all_passed and passed

    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status} - {description}")
    print(f"  Step size: {step_size}, Iterations: {iterations}")
    print(f"  Naive: {naive_result}, Optimized: {optimized_result}")
    print()

if all_passed:
    print("All tests passed! ✓")
    print("\nNow testing with actual input (355, 50,000,000)...")
    result = solve_spinlock_optimized(355, 50_000_000)
    print(f"Result: {result}")
else:
    print("Some tests failed! ✗")
