def test_calculate_fuel():
    """Test base fuel calculation (from Part 1)."""
    from solution import calculate_fuel

    assert calculate_fuel(12) == 2
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 654
    assert calculate_fuel(100756) == 33583
    print("  calculate_fuel tests passed")


def test_provided_examples():
    """Test recursive fuel calculation with provided examples."""
    from solution import calculate_recursive_fuel

    # Example 1: Mass of 14
    assert calculate_recursive_fuel(14) == 2, f"Expected 2, got {calculate_recursive_fuel(14)}"

    # Example 2: Mass of 1969
    assert calculate_recursive_fuel(1969) == 966, f"Expected 966, got {calculate_recursive_fuel(1969)}"

    # Example 3: Mass of 100756
    assert calculate_recursive_fuel(100756) == 50346, f"Expected 50346, got {calculate_recursive_fuel(100756)}"

    print("  Provided example tests passed")


def test_edge_cases():
    """Test edge cases for small masses."""
    from solution import calculate_recursive_fuel

    # Mass 0 (extreme edge case)
    assert calculate_recursive_fuel(0) == 0, "Mass 0 should produce 0 fuel"

    # Very small masses (negative initial fuel)
    assert calculate_recursive_fuel(1) == 0, "Mass 1 should produce 0 fuel"
    assert calculate_recursive_fuel(2) == 0, "Mass 2 should produce 0 fuel"
    assert calculate_recursive_fuel(5) == 0, "Mass 5 should produce 0 fuel"

    # Boundary: zero initial fuel
    assert calculate_recursive_fuel(6) == 0, "Mass 6 should produce 0 fuel"
    assert calculate_recursive_fuel(7) == 0, "Mass 7 should produce 0 fuel"
    assert calculate_recursive_fuel(8) == 0, "Mass 8 should produce 0 fuel"

    # Boundary: just positive
    assert calculate_recursive_fuel(9) == 1, "Mass 9 should produce 1 fuel"
    assert calculate_recursive_fuel(10) == 1, "Mass 10 should produce 1 fuel"
    assert calculate_recursive_fuel(11) == 1, "Mass 11 should produce 1 fuel"

    # Mass 12 (Part 1 example)
    assert calculate_recursive_fuel(12) == 2, "Mass 12 should produce 2 fuel"

    print("  Edge case tests passed")


def test_part2_geq_part1():
    """Verify Part 2 answer is always >= Part 1 for same mass."""
    from solution import calculate_fuel, calculate_recursive_fuel

    test_masses = [0, 1, 5, 9, 12, 14, 33, 50, 100, 500, 1000, 1969, 100756]

    for mass in test_masses:
        part1 = calculate_fuel(mass)
        part2 = calculate_recursive_fuel(mass)

        # Part 2 is always >= 0
        assert part2 >= 0, f"Part 2 ({part2}) should be >= 0 for mass {mass}"

        # Part 2 is always >= Part 1 when Part 1 > 0
        if part1 > 0:
            assert part2 >= part1, f"Part 2 ({part2}) should be >= Part 1 ({part1}) for mass {mass}"

        # If Part 1 fuel >= 9, Part 2 must be strictly greater (because fuel-for-fuel is positive)
        if part1 >= 9:
            assert part2 > part1, f"Part 2 ({part2}) should be > Part 1 ({part1}) for mass {mass} (fuel >= 9)"

    print("  Part 2 >= Part 1 tests passed")


def test_spot_check_first_input():
    """Manually verify calculation for first input mass."""
    from solution import calculate_recursive_fuel

    # First mass in input.md is 80891
    result = calculate_recursive_fuel(80891)
    expected = 40413
    assert result == expected, f"Expected {expected} for mass 80891, got {result}"

    print("  Spot check for mass 80891 passed")


def test_full_solution():
    """Test the complete solution against actual input."""
    from solution import read_masses, calculate_total_fuel

    masses = read_masses('input.md')

    # Verify we read 100 masses
    assert len(masses) == 100, f"Expected 100 masses, got {len(masses)}"

    total_fuel = calculate_total_fuel(masses)

    # Must be greater than Part 1 answer
    part1_answer = 3267638
    assert total_fuel > part1_answer, f"Part 2 ({total_fuel}) should be > Part 1 ({part1_answer})"

    # Sanity check: shouldn't be unreasonably large
    assert total_fuel < 2 * part1_answer, f"Part 2 answer seems too large: {total_fuel}"

    print(f"  Full solution test passed")
    print(f"    Part 1 answer: {part1_answer}")
    print(f"    Part 2 answer: {total_fuel}")
    print(f"    Additional fuel: {total_fuel - part1_answer}")
    print(f"    Ratio (Part2/Part1): {total_fuel / part1_answer:.4f}")


def run_all_tests():
    """Run all tests."""
    print("Running tests...\n")
    test_calculate_fuel()
    test_provided_examples()
    test_edge_cases()
    test_part2_geq_part1()
    test_spot_check_first_input()
    test_full_solution()
    print("\n" + "=" * 40)
    print("ALL TESTS PASSED!")
    print("=" * 40)


if __name__ == '__main__':
    run_all_tests()
