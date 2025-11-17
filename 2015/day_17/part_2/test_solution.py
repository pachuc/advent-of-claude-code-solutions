from solution import find_minimum_container_ways


def test_example():
    """Test 1: Example from problem statement"""
    containers = [20, 15, 10, 5, 5]
    result = find_minimum_container_ways(containers, 25)
    expected = 3
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Test 1 passed: Example case (expected {expected}, got {result})")


def test_single_container():
    """Test 3: Single container solution"""
    containers = [150, 50, 30, 20]
    result = find_minimum_container_ways(containers, 150)
    expected = 1
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Test 3 passed: Single container (expected {expected}, got {result})")


def test_multiple_singles():
    """Test 4: Multiple single-container solutions"""
    containers = [25, 25, 10, 15]
    result = find_minimum_container_ways(containers, 25)
    expected = 2
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Test 4 passed: Multiple single containers (expected {expected}, got {result})")


def test_many_containers():
    """Test 5: Requires many containers"""
    containers = [1] * 10
    result = find_minimum_container_ways(containers, 5)
    expected = 252  # C(10, 5) = 252
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Test 5 passed: Many containers (expected {expected}, got {result})")


def test_duplicates():
    """Test 6: Duplicate container values"""
    containers = [10, 10, 5, 5]
    result = find_minimum_container_ways(containers, 15)
    expected = 4
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Test 6 passed: Duplicate values (expected {expected}, got {result})")


def test_all_containers():
    """Test 7: All containers sum to target"""
    containers = [50, 30, 20, 10]
    result = find_minimum_container_ways(containers, 110)
    expected = 1
    assert result == expected, f"Expected {expected}, got {result}"
    print(f"✓ Test 7 passed: All containers needed (expected {expected}, got {result})")


if __name__ == "__main__":
    print("Running test suite...\n")
    test_example()
    test_single_container()
    test_multiple_singles()
    test_many_containers()
    test_duplicates()
    test_all_containers()
    print("\n✓ All tests passed!")
