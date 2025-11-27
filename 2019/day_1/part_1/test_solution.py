from solution import calculate_fuel, calculate_total_fuel, read_masses

# ============ Unit Tests (No File Dependencies) ============

def test_provided_examples():
    """Test against the 4 examples from problem statement."""
    assert calculate_fuel(12) == 2
    assert calculate_fuel(14) == 2
    assert calculate_fuel(1969) == 654
    assert calculate_fuel(100756) == 33583


def test_edge_cases():
    """Test boundary values for the formula."""
    assert calculate_fuel(9) == 1   # smallest positive fuel
    assert calculate_fuel(8) == 0   # zero fuel
    assert calculate_fuel(6) == 0   # exactly divisible by 3
    assert calculate_fuel(3) == -1  # negative fuel (theoretical)


def test_floor_division():
    """Ensure floor division behavior is correct."""
    assert calculate_fuel(10) == 1
    assert calculate_fuel(11) == 1
    assert calculate_fuel(13) == 2


def test_sum_of_examples():
    """Test summing functionality."""
    total = calculate_total_fuel([12, 14, 1969, 100756])
    assert total == 34241


def test_empty_input():
    """Empty list should return 0."""
    assert calculate_total_fuel([]) == 0


def test_single_module():
    """Single module should return its fuel value."""
    assert calculate_total_fuel([12]) == 2


def test_spot_check_input_values():
    """Verify calculations for specific input file values."""
    assert calculate_fuel(80891) == 26961
    assert calculate_fuel(109412) == 36468
    assert calculate_fuel(149508) == 49834


# ============ Integration Tests (With File Dependencies) ============

def test_input_count():
    """Verify we read the correct number of masses."""
    masses = read_masses('input.md')
    assert len(masses) == 100


def test_input_boundaries():
    """Verify first and last values are read correctly."""
    masses = read_masses('input.md')
    assert masses[0] == 80891
    assert masses[-1] == 125521


def test_answer_sanity():
    """Verify answer is in reasonable range."""
    masses = read_masses('input.md')
    total = calculate_total_fuel(masses)
    assert 1_600_000 < total < 5_000_000


def test_mathematical_consistency():
    """Verify sum is calculated correctly."""
    masses = read_masses('input.md')
    total_fuel = calculate_total_fuel(masses)
    alternative_sum = sum(mass // 3 - 2 for mass in masses)
    assert total_fuel == alternative_sum


# ============ Test Runner ============

if __name__ == '__main__':
    # Unit tests (no file dependencies)
    print("Running unit tests...")
    test_provided_examples()
    test_edge_cases()
    test_floor_division()
    test_sum_of_examples()
    test_empty_input()
    test_single_module()
    test_spot_check_input_values()
    print("All unit tests passed!")

    # Integration tests (with input file)
    print("\nRunning integration tests...")
    test_input_count()
    test_input_boundaries()
    test_answer_sanity()
    test_mathematical_consistency()
    print("All integration tests passed!")

    print("\nAll tests passed!")
