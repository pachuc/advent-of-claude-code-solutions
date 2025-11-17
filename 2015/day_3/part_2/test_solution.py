from solution import solve_santa_delivery

def test_example_1():
    """Test: ^v -> 3 houses"""
    result = solve_santa_delivery("^v")
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Test example 1 (^v): PASSED")

def test_example_2():
    """Test: ^>v< -> 3 houses"""
    result = solve_santa_delivery("^>v<")
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Test example 2 (^>v<): PASSED")

def test_example_3():
    """Test: ^v^v^v^v^v -> 11 houses"""
    result = solve_santa_delivery("^v^v^v^v^v")
    assert result == 11, f"Expected 11, got {result}"
    print("✓ Test example 3 (^v^v^v^v^v): PASSED")

def test_empty_string():
    """Test: empty string -> 1 house (starting position)"""
    result = solve_santa_delivery("")
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Test empty string: PASSED")

def test_single_character():
    """Test: ^ -> 2 houses"""
    result = solve_santa_delivery("^")
    assert result == 2, f"Expected 2, got {result}"
    print("✓ Test single character: PASSED")

def test_same_direction():
    """Test: >>>> -> 3 houses"""
    result = solve_santa_delivery(">>>>")
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Test same direction (>>>>): PASSED")

def test_complex_revisiting():
    """Test: >v<^>v<^ -> 3 houses"""
    result = solve_santa_delivery(">v<^>v<^")
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Test complex revisiting: PASSED")

def test_diverging_paths():
    """Test: ><>< -> 5 houses"""
    result = solve_santa_delivery("><><")
    assert result == 5, f"Expected 5, got {result}"
    print("✓ Test diverging paths: PASSED")

def test_long_straight_line():
    """Test: 1000 north movements -> 501 houses"""
    result = solve_santa_delivery("^" * 1000)
    assert result == 501, f"Expected 501, got {result}"
    print("✓ Test long straight line: PASSED")

def run_all_tests():
    """Run all tests"""
    print("\n=== Running Example Tests ===")
    test_example_1()
    test_example_2()
    test_example_3()

    print("\n=== Running Edge Case Tests ===")
    test_empty_string()
    test_single_character()
    test_same_direction()
    test_complex_revisiting()
    test_diverging_paths()
    test_long_straight_line()

    print("\n✓ All tests passed!")

if __name__ == "__main__":
    run_all_tests()
