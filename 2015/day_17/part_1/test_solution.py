from solution import count_combinations


def test_example():
    """Test the example from problem statement."""
    containers = [20, 15, 10, 5, 5]
    result = count_combinations(containers, 25)
    assert result == 4, f"Expected 4, got {result}"
    print("✓ Test 1 passed: Example case")


def test_single_match():
    """Test single container exact match."""
    containers = [150]
    result = count_combinations(containers, 150)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 2 passed: Single container match")


def test_no_solution():
    """Test case with no valid combinations."""
    containers = [10, 20, 30]
    result = count_combinations(containers, 150)
    assert result == 0, f"Expected 0, got {result}"
    print("✓ Test 3 passed: No solution")


def test_multiple_containers_one_solution():
    """Test multiple containers with one solution."""
    containers = [100, 50]
    result = count_combinations(containers, 150)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 4 passed: Multiple containers, one solution")


def test_all_match_target():
    """Test where every container equals target."""
    containers = [150, 150, 150]
    result = count_combinations(containers, 150)
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Test 5 passed: All containers match target")


def test_two_identical():
    """Test with two identical containers."""
    containers = [75, 75, 50]
    result = count_combinations(containers, 150)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 6 passed: Two identical containers")


def test_multiple_paths():
    """Test multiple valid combinations."""
    containers = [50, 50, 50, 25, 25]
    result = count_combinations(containers, 100)
    assert result == 6, f"Expected 6, got {result}"
    print("✓ Test 7 passed: Multiple paths")


def test_empty_input():
    """Test empty container list."""
    containers = []
    result = count_combinations(containers, 150)
    assert result == 0, f"Expected 0, got {result}"
    print("✓ Test 8 passed: Empty input")


def test_single_too_small():
    """Test single container too small."""
    containers = [10]
    result = count_combinations(containers, 150)
    assert result == 0, f"Expected 0, got {result}"
    print("✓ Test 9 passed: Single container too small")


def test_all_containers_used():
    """Test that all containers can be used."""
    containers = [50, 50, 50]
    result = count_combinations(containers, 150)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test 10 passed: All containers used")


def test_upper_bound_property():
    """Test that result doesn't exceed 2^n."""
    containers = [20, 15, 10, 5, 5]
    result = count_combinations(containers, 25)
    max_possible = 2 ** len(containers)
    assert result <= max_possible, f"Result {result} exceeds max {max_possible}"
    print("✓ Property test passed: Upper bound")


def test_non_negative():
    """Test that result is always non-negative."""
    containers = [20, 15, 10]
    result = count_combinations(containers, 25)
    assert result >= 0, f"Result must be non-negative, got {result}"
    print("✓ Property test passed: Non-negative")


# Run all tests
if __name__ == '__main__':
    print("Running tests...\n")
    test_example()
    test_single_match()
    test_no_solution()
    test_multiple_containers_one_solution()
    test_all_match_target()
    test_two_identical()
    test_multiple_paths()
    test_empty_input()
    test_single_too_small()
    test_all_containers_used()
    test_upper_bound_property()
    test_non_negative()
    print("\n✓ All tests passed!")
