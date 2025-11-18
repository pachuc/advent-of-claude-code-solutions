"""Test script to verify the optimized spinlock solution."""

from solution import solve_spinlock_optimized


def solve_spinlock_naive(step_size, iterations):
    """
    Naive implementation that builds the entire buffer.
    Used for verification against the optimized solution.
    """
    buffer = [0]
    current_pos = 0

    for value in range(1, iterations + 1):
        # Step forward with circular wrapping
        current_pos = (current_pos + step_size) % len(buffer)

        # Insert after current position
        current_pos += 1
        buffer.insert(current_pos, value)

    # Return value at position 1 (after 0)
    return buffer[1]


def test_small_scale():
    """Test 1.1: Small-scale verification with step_size=3, N=10"""
    print("Test 1.1: Small-scale verification (step_size=3, N=10)")
    step_size = 3
    iterations = 10

    naive_result = solve_spinlock_naive(step_size, iterations)
    optimized_result = solve_spinlock_optimized(step_size, iterations)

    print(f"  Naive result: {naive_result}")
    print(f"  Optimized result: {optimized_result}")
    print(f"  Match: {naive_result == optimized_result}")

    # According to manual trace in test plan, value_after_zero should be 9
    assert naive_result == optimized_result, f"Results don't match: {naive_result} != {optimized_result}"
    print(f"  ✓ PASSED\n")
    return True


def test_cross_validate_part1():
    """Test 1.2: Cross-validate with Part 1 logic (step_size=355, N=2017)"""
    print("Test 1.2: Cross-validate with Part 1 (step_size=355, N=2017)")
    step_size = 355
    iterations = 2017

    naive_result = solve_spinlock_naive(step_size, iterations)
    optimized_result = solve_spinlock_optimized(step_size, iterations)

    print(f"  Naive result: {naive_result}")
    print(f"  Optimized result: {optimized_result}")
    print(f"  Match: {naive_result == optimized_result}")

    assert naive_result == optimized_result, f"Results don't match: {naive_result} != {optimized_result}"
    print(f"  ✓ PASSED\n")
    return True


def test_step_size_1():
    """Test 2.1: Edge case with step_size=1"""
    print("Test 2.1: Edge case (step_size=1, N=100)")
    step_size = 1
    iterations = 100

    naive_result = solve_spinlock_naive(step_size, iterations)
    optimized_result = solve_spinlock_optimized(step_size, iterations)

    print(f"  Naive result: {naive_result}")
    print(f"  Optimized result: {optimized_result}")
    print(f"  Match: {naive_result == optimized_result}")

    assert naive_result == optimized_result, f"Results don't match: {naive_result} != {optimized_result}"
    print(f"  ✓ PASSED\n")
    return True


def test_step_size_0():
    """Test 2.3: Edge case with step_size=0"""
    print("Test 2.3: Edge case (step_size=0, N=100)")
    step_size = 0
    iterations = 100

    naive_result = solve_spinlock_naive(step_size, iterations)
    optimized_result = solve_spinlock_optimized(step_size, iterations)

    print(f"  Naive result: {naive_result}")
    print(f"  Optimized result: {optimized_result}")
    print(f"  Match: {naive_result == optimized_result}")

    # With step_size=0, first insertion goes to position 1, then all subsequent
    # insertions go to positions 2, 3, 4, etc. So position 1 remains value 1.
    print(f"  Expected (first value): 1")

    assert naive_result == optimized_result, f"Results don't match: {naive_result} != {optimized_result}"
    assert optimized_result == 1, f"Expected 1, got {optimized_result}"
    print(f"  ✓ PASSED\n")
    return True


def test_large_step_size():
    """Test 2.2: Edge case with large step_size"""
    print("Test 2.2: Edge case (step_size=1000, N=100)")
    step_size = 1000
    iterations = 100

    naive_result = solve_spinlock_naive(step_size, iterations)
    optimized_result = solve_spinlock_optimized(step_size, iterations)

    print(f"  Naive result: {naive_result}")
    print(f"  Optimized result: {optimized_result}")
    print(f"  Match: {naive_result == optimized_result}")

    assert naive_result == optimized_result, f"Results don't match: {naive_result} != {optimized_result}"
    print(f"  ✓ PASSED\n")
    return True


def test_buffer_length_invariant():
    """Test 4.3: Verify buffer_len == iterations + 1"""
    print("Test 4.3: Buffer length invariant check")

    # Modified version to check buffer length
    step_size = 355
    iterations = 1000

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

    print(f"  Final buffer_len: {buffer_len}")
    print(f"  Expected: {iterations + 1}")
    print(f"  Match: {buffer_len == iterations + 1}")

    assert buffer_len == iterations + 1, f"Buffer length mismatch: {buffer_len} != {iterations + 1}"
    print(f"  ✓ PASSED\n")
    return True


def run_all_tests():
    """Run all test cases"""
    print("=" * 60)
    print("Running all tests for optimized spinlock solution")
    print("=" * 60 + "\n")

    all_passed = True

    try:
        all_passed &= test_small_scale()
        all_passed &= test_cross_validate_part1()
        all_passed &= test_step_size_1()
        all_passed &= test_step_size_0()
        all_passed &= test_large_step_size()
        all_passed &= test_buffer_length_invariant()
    except Exception as e:
        print(f"✗ Test failed with exception: {e}")
        all_passed = False

    print("=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    run_all_tests()
