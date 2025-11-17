import re

def read_input(filename='input.md'):
    """Read and parse the input file."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    # Find first integer in the content
    match = re.search(r'\d+', content)
    if match:
        return int(match.group())
    raise ValueError("No integer found in input file")

def josephus_formula(n):
    """
    Solve using Josephus problem formula for k=2.

    For the Josephus problem where every second person is eliminated:
    - Find the highest power of 2 that is <= n, call it 2^m
    - Calculate L = n - 2^m (the remainder)
    - The winner's position is: 2 * L + 1

    This formula works because the pattern resets at each power of 2.
    """
    if n == 1:
        return 1

    # Find highest power of 2 <= n
    power_of_2 = 1
    while power_of_2 * 2 <= n:
        power_of_2 *= 2

    # Calculate L (remainder after subtracting highest power of 2)
    L = n - power_of_2

    # Apply Josephus formula
    return 2 * L + 1

def simulate_with_linked_list(n):
    """
    Simulate the elf gift exchange using a circular linked list.

    Each elf steals from the next elf in the circle (to their left).
    We use a dictionary to maintain the circular structure efficiently.
    """
    if n == 1:
        return 1

    # Create circular linked list using dict: elf -> next_elf
    next_elf = {i: i + 1 for i in range(1, n + 1)}
    next_elf[n] = 1  # Circle back to create the circle

    current = 1
    remaining = n

    while remaining > 1:
        # Current elf eliminates the next elf (to their left)
        eliminated = next_elf[current]
        # Update pointer to skip the eliminated elf
        next_elf[current] = next_elf[eliminated]
        # Move to the next active elf (now pointed to by current)
        current = next_elf[current]
        remaining -= 1

    return current

def test_example():
    """
    CRITICAL: Test the provided example: N=5 should return 3.
    This validates our understanding of the problem.
    """
    formula_result = josephus_formula(5)
    simulation_result = simulate_with_linked_list(5)

    # Both should agree
    assert formula_result == simulation_result, \
        f"Formula and simulation disagree! Formula: {formula_result}, Simulation: {simulation_result}"

    # Result should be 3 (from problem statement)
    assert formula_result == 3, \
        f"Expected 3 for N=5, got {formula_result}"

    print("✓ Example test passed: N=5 → 3")

def test_edge_cases():
    """Test edge cases with both methods."""
    # Test N=1
    assert josephus_formula(1) == 1
    assert simulate_with_linked_list(1) == 1
    assert josephus_formula(1) == simulate_with_linked_list(1)

    # Test N=2
    assert josephus_formula(2) == 1
    assert simulate_with_linked_list(2) == 1
    assert josephus_formula(2) == simulate_with_linked_list(2)

    print("✓ Edge cases passed")

def test_powers_of_two():
    """Test that powers of 2 always return 1 (mathematical property)."""
    for i in range(21):
        n = 2 ** i
        formula_result = josephus_formula(n)
        simulation_result = simulate_with_linked_list(n)

        # Both methods should agree
        assert formula_result == simulation_result, \
            f"Disagreement at N={n}: formula={formula_result}, simulation={simulation_result}"

        # Mathematical property: powers of 2 should return 1
        assert formula_result == 1, \
            f"Power of 2 (N={n}) should return 1, got {formula_result}"

    print("✓ Powers of 2 test passed")

def test_powers_of_two_plus_one():
    """Test that 2^m + 1 always returns 3 (mathematical property)."""
    for i in range(1, 20):
        n = 2 ** i + 1
        formula_result = josephus_formula(n)
        simulation_result = simulate_with_linked_list(n)

        # Both methods should agree
        assert formula_result == simulation_result, \
            f"Disagreement at N={n}: formula={formula_result}, simulation={simulation_result}"

        # Mathematical property: 2^m + 1 should return 3
        assert formula_result == 3, \
            f"2^{i} + 1 (N={n}) should return 3, got {formula_result}"

    print("✓ Powers of 2 plus 1 test passed")

def test_sequential_small():
    """
    Test values 1-20 comparing formula vs simulation.
    This is the PRIMARY validation method.
    """
    for n in range(1, 21):
        formula_result = josephus_formula(n)
        simulation_result = simulate_with_linked_list(n)

        assert formula_result == simulation_result, \
            f"Disagreement at N={n}: formula={formula_result}, simulation={simulation_result}"

    print("✓ Sequential small values (1-20) test passed")

def test_medium_values():
    """Test medium-sized values."""
    test_values = [100, 1000, 10000]
    for n in test_values:
        formula_result = josephus_formula(n)
        simulation_result = simulate_with_linked_list(n)

        assert formula_result == simulation_result, \
            f"Disagreement at N={n}: formula={formula_result}, simulation={simulation_result}"

    print("✓ Medium values test passed")

def test_actual_input():
    """
    Test the actual input value.
    We print the result for manual verification.
    """
    n = 3017957
    result = josephus_formula(n)

    # Manual calculation for verification:
    # 2^21 = 2,097,152
    # L = 3,017,957 - 2,097,152 = 920,805
    # Result = 2 * 920,805 + 1 = 1,841,611
    expected = 1841611

    print(f"✓ Actual input N={n} → {result}")
    print(f"  (Manual calculation expects: {expected})")

    # Verify against manual calculation
    assert result == expected, \
        f"Result {result} doesn't match manual calculation {expected}"

def run_all_tests():
    """Run all tests in order of importance."""
    print("\n=== Running Test Suite ===\n")

    # Most critical test first
    test_example()

    # Edge cases
    test_edge_cases()

    # Pattern validation
    test_powers_of_two()
    test_powers_of_two_plus_one()

    # Cross-validation
    test_sequential_small()
    test_medium_values()

    # Final result
    test_actual_input()

    print("\n=== All tests passed! ===")

def main():
    n = read_input()
    result = josephus_formula(n)
    print(result)

if __name__ == '__main__':
    # Run tests first
    run_all_tests()
    print("\n=== Solution for Actual Input ===")
    main()
