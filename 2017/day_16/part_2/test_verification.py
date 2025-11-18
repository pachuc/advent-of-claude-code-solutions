#!/usr/bin/env python3
"""
Comprehensive verification tests for the Permutation Promenade Part 2 solution.
"""

from solution import spin, exchange, partner, perform_dance, find_cycle_length, solve

def test_unit_functions():
    """Test individual move functions."""
    print("Testing unit functions...")

    # Test spin
    programs = list('abcde')
    spin(programs, 3)
    assert programs == list('cdeab'), f"Spin failed: {programs}"

    programs = list('abcdefghijklmnop')
    spin(programs, 1)
    assert programs == list('pabcdefghijklmno'), f"Spin failed: {programs}"

    # Test exchange
    programs = list('abcde')
    exchange(programs, 0, 4)
    assert programs == list('ebcda'), f"Exchange failed: {programs}"

    # Test partner
    programs = list('abcde')
    partner(programs, 'a', 'e')
    assert programs == list('ebcda'), f"Partner failed: {programs}"

    print("  ✓ Unit functions passed")

def test_part1_answer():
    """Verify Part 1 answer is reproduced."""
    print("Testing Part 1 answer reproduction...")

    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]

    initial = list('abcdefghijklmnop')
    perform_dance(initial, moves)
    result = ''.join(initial)

    expected = 'eojfmbpkldghncia'
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"  ✓ Part 1 answer verified: {result}")

def test_cycle_closure():
    """Verify the cycle actually returns to initial state."""
    print("Testing cycle closure...")

    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]

    initial = list('abcdefghijklmnop')
    cycle_length = find_cycle_length(initial, moves)

    # Apply cycle_length iterations
    current = initial.copy()
    for _ in range(cycle_length):
        perform_dance(current, moves)

    assert current == initial, f"Cycle didn't close: {current} != {initial}"
    print(f"  ✓ Cycle closes after {cycle_length} iterations")

def test_modulo_arithmetic():
    """Verify modulo arithmetic correctness."""
    print("Testing modulo arithmetic...")

    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]

    initial = list('abcdefghijklmnop')
    cycle_length = find_cycle_length(initial, moves)

    # Test that iteration 16 == iteration (16 + 48) == iteration (16 + 2*48)
    result_16 = initial.copy()
    for _ in range(16):
        perform_dance(result_16, moves)

    result_64 = initial.copy()
    for _ in range(64):  # 16 + 48
        perform_dance(result_64, moves)

    result_112 = initial.copy()
    for _ in range(112):  # 16 + 2*48
        perform_dance(result_112, moves)

    assert result_16 == result_64, "Modulo arithmetic failed for 16 vs 64"
    assert result_16 == result_112, "Modulo arithmetic failed for 16 vs 112"

    print(f"  ✓ Modulo arithmetic verified")

def test_small_iterations():
    """Test small iteration counts."""
    print("Testing small iteration counts...")

    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]

    for n in [1, 2, 3, 10]:
        # Direct iteration
        initial = list('abcdefghijklmnop')
        for _ in range(n):
            perform_dance(initial, moves)
        result_direct = ''.join(initial)

        # Using solve function
        result_solve = solve(n)

        assert result_direct == result_solve, f"solve({n}) mismatch: {result_solve} != {result_direct}"

    print(f"  ✓ Small iteration counts verified")

def test_final_answer_validity():
    """Verify the final answer is a valid permutation."""
    print("Testing final answer validity...")

    result = solve(1_000_000_000)

    # Must be 16 characters
    assert len(result) == 16, f"Expected 16 chars, got {len(result)}"

    # Must be a valid permutation
    assert sorted(result) == sorted('abcdefghijklmnop'), f"Invalid permutation: {result}"

    # Should be different from initial (unlikely to be exactly at the start)
    assert result != 'abcdefghijklmnop', f"Result is initial state (very unlikely)"

    print(f"  ✓ Final answer is valid: {result}")

def main():
    """Run all verification tests."""
    print("=" * 60)
    print("VERIFICATION TEST SUITE")
    print("=" * 60)

    try:
        test_unit_functions()
        test_part1_answer()
        test_cycle_closure()
        test_modulo_arithmetic()
        test_small_iterations()
        test_final_answer_validity()

        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)

        # Display final answer
        result = solve(1_000_000_000)
        print(f"\nFinal Answer: {result}")

        return True

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        return False

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
