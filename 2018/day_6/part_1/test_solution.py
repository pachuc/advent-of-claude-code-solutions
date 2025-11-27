from solution import solve

def test_example():
    """Test with the example from problem statement"""
    result = solve('test_inputs/example.txt')
    assert result == 17, f"Expected 17, got {result}"
    print("✓ Example test passed (result: 17)")

def test_single_coordinate():
    """Test with single coordinate - should be infinite"""
    result = solve('test_inputs/single.txt')
    assert result == 0, f"Expected 0, got {result}"
    print("✓ Single coordinate test passed (result: 0)")

def test_full_input():
    """Test with actual input"""
    result = solve('input.md')
    print(f"Result for full input: {result}")
    assert result > 0, "Should have a positive result"
    print("✓ Full input test passed")

def test_full_input_regression():
    """Regression test - verifies answer remains 4233"""
    result = solve('input.md')
    EXPECTED = 4233
    assert result == EXPECTED, f"Expected {EXPECTED}, got {result}"
    print(f"✓ Regression test passed: {result}")

def run_all_tests():
    """Run all test cases in recommended order"""
    print("Running tests...\n")

    # Critical tests first
    test_example()
    test_full_input()

    # Edge cases
    test_single_coordinate()

    # Regression
    test_full_input_regression()

    print("\n✅ All tests passed!")

if __name__ == '__main__':
    run_all_tests()
