#!/usr/bin/env python3
"""
Test suite for the Dueling Generators solution.
"""

import time
from solution import generate_values, count_matches, parse_input


def test_generator_a():
    """Test Generator A produces correct sequence."""
    print("Test 1: Generator A sequence...")
    gen = generate_values(65, 16807, 2147483647)
    expected = [1092455, 1181022009, 245556042, 1744312007, 1352636452]
    for i, exp_val in enumerate(expected):
        val = next(gen)
        assert val == exp_val, f"Value {i+1} mismatch: expected {exp_val}, got {val}"
    print("✓ Generator A produces correct sequence")


def test_generator_b():
    """Test Generator B produces correct sequence."""
    print("Test 2: Generator B sequence...")
    gen = generate_values(8921, 48271, 2147483647)
    expected = [430625591, 1233683848, 1431495498, 137874439, 285222916]
    for i, exp_val in enumerate(expected):
        val = next(gen)
        assert val == exp_val, f"Value {i+1} mismatch: expected {exp_val}, got {val}"
    print("✓ Generator B produces correct sequence")


def test_lowest_16_bits():
    """Test lowest 16 bits extraction."""
    print("Test 3: Lowest 16 bits extraction...")
    assert (1092455 & 0xFFFF) == 43879
    assert (430625591 & 0xFFFF) == 54071
    assert (245556042 & 0xFFFF) == 58186
    assert (1431495498 & 0xFFFF) == 58186
    # Verify the third pair matches
    assert (245556042 & 0xFFFF) == (1431495498 & 0xFFFF)
    print("✓ Lowest 16 bits extraction works correctly")


def test_first_five_pairs():
    """Test first 5 pairs have exactly 1 match (the 3rd pair)."""
    print("Test 4: First five pairs...")
    result = count_matches(65, 8921, 5)
    assert result == 1, f"Expected 1 match in first 5 pairs, got {result}"
    print("✓ First 5 pairs: 1 match (correct)")


def test_example_case():
    """Test with full example (40M pairs, expected 588)."""
    print("Test 5: Example case (40M pairs, A=65, B=8921)...")
    start_time = time.time()
    result = count_matches(65, 8921, 40_000_000)
    end_time = time.time()
    duration = end_time - start_time

    print(f"  Result: {result}")
    print(f"  Runtime: {duration:.2f} seconds")

    assert result == 588, f"Expected 588, got {result}"
    print("✓ Example case produces correct result (588)")


def test_actual_input():
    """Test with actual input."""
    print("Test 6: Actual input (A=277, B=349)...")
    start_time = time.time()
    result = count_matches(277, 349, 40_000_000)
    end_time = time.time()
    duration = end_time - start_time

    print(f"  Result: {result}")
    print(f"  Runtime: {duration:.2f} seconds")

    # Verify result is in reasonable range
    assert 0 <= result <= 40_000_000, "Result out of reasonable range"
    print("✓ Actual input processed successfully")

    return result


def run_all_tests():
    """Run all tests in order."""
    print("=" * 60)
    print("Running Dueling Generators Test Suite")
    print("=" * 60)

    # Unit tests (fast)
    test_lowest_16_bits()
    test_generator_a()
    test_generator_b()
    test_first_five_pairs()

    print()

    # Integration test with example
    test_example_case()

    print()

    # Actual solution
    actual_result = test_actual_input()

    print()
    print("=" * 60)
    print("All tests passed!")
    print(f"Final answer: {actual_result}")
    print("=" * 60)

    return actual_result


if __name__ == "__main__":
    run_all_tests()
