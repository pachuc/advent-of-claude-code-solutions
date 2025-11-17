from solution import count_combinations

def test_example():
    """Test the example from problem statement."""
    containers = [20, 15, 10, 5, 5]
    result = count_combinations(containers, 25)
    print(f"Test 1 (Example): Expected 4, Got {result} - {'PASS' if result == 4 else 'FAIL'}")
    return result == 4

def test_single_match():
    """Test single container exact match."""
    containers = [150]
    result = count_combinations(containers, 150)
    print(f"Test 2 (Single match): Expected 1, Got {result} - {'PASS' if result == 1 else 'FAIL'}")
    return result == 1

def test_no_solution():
    """Test case with no valid combinations."""
    containers = [10, 20, 30]
    result = count_combinations(containers, 150)
    print(f"Test 3 (No solution): Expected 0, Got {result} - {'PASS' if result == 0 else 'FAIL'}")
    return result == 0

def test_two_identical():
    """Test with two identical containers."""
    containers = [75, 75, 50]
    result = count_combinations(containers, 150)
    print(f"Test 4 (Two identical): Expected 1, Got {result} - {'PASS' if result == 1 else 'FAIL'}")
    return result == 1

def test_multiple_paths():
    """Test multiple valid combinations."""
    containers = [50, 50, 50, 25, 25]
    result = count_combinations(containers, 100)
    print(f"Test 5 (Multiple paths): Expected 6, Got {result} - {'PASS' if result == 6 else 'FAIL'}")
    return result == 6

def test_all_containers_used():
    """Test that all containers can be used."""
    containers = [50, 50, 50]
    result = count_combinations(containers, 150)
    print(f"Test 6 (All used): Expected 1, Got {result} - {'PASS' if result == 1 else 'FAIL'}")
    return result == 1

# Run all tests
if __name__ == '__main__':
    tests = [
        test_example(),
        test_single_match(),
        test_no_solution(),
        test_two_identical(),
        test_multiple_paths(),
        test_all_containers_used()
    ]

    print(f"\n{'='*50}")
    print(f"Tests passed: {sum(tests)}/{len(tests)}")
    if all(tests):
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed!")
