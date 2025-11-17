from solution import is_valid_triangle, parse_line, count_valid_triangles
import os


def run_tests():
    """Run all unit tests for the triangle validation solution."""

    print("Running Triangle Validation Tests...")
    print("=" * 60)

    # Test 1: Algorithm Correctness Tests
    print("\n1. Algorithm Correctness Tests:")

    # Test 1.1: Invalid Triangle (Example from Problem)
    assert is_valid_triangle(5, 10, 25) == False, "Test 1.1 failed: 5 10 25 should be invalid"
    print("  ✓ Test 1.1: Invalid triangle (5, 10, 25)")

    # Test 1.2: Valid Equilateral Triangle
    assert is_valid_triangle(5, 5, 5) == True, "Test 1.2 failed: 5 5 5 should be valid"
    print("  ✓ Test 1.2: Valid equilateral (5, 5, 5)")

    # Test 1.3: Valid Scalene Triangle
    assert is_valid_triangle(3, 4, 5) == True, "Test 1.3 failed: 3 4 5 should be valid"
    print("  ✓ Test 1.3: Valid scalene (3, 4, 5)")

    # Test 1.4: Valid Isosceles Triangle
    assert is_valid_triangle(5, 5, 8) == True, "Test 1.4 failed: 5 5 8 should be valid"
    print("  ✓ Test 1.4: Valid isosceles (5, 5, 8)")

    # Test 1.5: Invalid - Sum Equals Third Side
    assert is_valid_triangle(1, 2, 3) == False, "Test 1.5 failed: 1 2 3 should be invalid"
    print("  ✓ Test 1.5: Invalid - sum equals third side (1, 2, 3)")

    # Test 1.6: Invalid - One Side Too Long
    assert is_valid_triangle(1, 1, 100) == False, "Test 1.6 failed: 1 1 100 should be invalid"
    print("  ✓ Test 1.6: Invalid - one side too long (1, 1, 100)")

    # Test 1.7: Large Valid Triangle
    assert is_valid_triangle(999, 999, 999) == True, "Test 1.7 failed: 999 999 999 should be valid"
    print("  ✓ Test 1.7: Large valid triangle (999, 999, 999)")

    # Test 2: Input Parsing Tests
    print("\n2. Input Parsing Tests:")

    # Test 2.1: Standard Format
    assert parse_line("566  477  376\n") == (566, 477, 376), "Test 2.1 failed"
    print("  ✓ Test 2.1: Standard format parsing")

    # Test 2.2: Extra Whitespace
    assert parse_line("  575   488   365  \n") == (575, 488, 365), "Test 2.2 failed"
    print("  ✓ Test 2.2: Extra whitespace handling")

    # Test 2.3: Mixed Spacing
    assert parse_line(" 50   18  156\n") == (50, 18, 156), "Test 2.3 failed"
    print("  ✓ Test 2.3: Mixed spacing parsing")

    # Test 3: Edge Cases
    print("\n3. Edge Cases:")

    # Test 3.1: All Zero
    assert is_valid_triangle(0, 0, 0) == False, "Test 3.1 failed: 0 0 0 should be invalid"
    print("  ✓ Test 3.1: All zero sides (0, 0, 0)")

    # Test 3.2: One Zero
    assert is_valid_triangle(0, 5, 5) == False, "Test 3.2 failed: 0 5 5 should be invalid"
    print("  ✓ Test 3.2: One zero side (0, 5, 5)")

    # Test 3.3: Order Independence
    assert is_valid_triangle(3, 4, 5) == True, "Test 3.3a failed"
    assert is_valid_triangle(4, 5, 3) == True, "Test 3.3b failed"
    assert is_valid_triangle(5, 3, 4) == True, "Test 3.3c failed"
    print("  ✓ Test 3.3: Order independence")

    # Test 3.4: Boundary Case - Just Valid
    assert is_valid_triangle(5, 5, 9) == True, "Test 3.4 failed: 5 5 9 should be valid"
    print("  ✓ Test 3.4: Boundary case - just valid (5, 5, 9)")

    # Test 3.5: Boundary Case - Just Invalid
    assert is_valid_triangle(5, 5, 10) == False, "Test 3.5 failed: 5 5 10 should be invalid"
    print("  ✓ Test 3.5: Boundary case - just invalid (5, 5, 10)")

    # Test 3.6: Large Side with Two Medium Sides
    assert is_valid_triangle(100, 40, 50) == False, "Test 3.6 failed: 100 40 50 should be invalid"
    print("  ✓ Test 3.6: Large side with two medium sides (100, 40, 50)")

    # Test 3.7: Negative Numbers
    assert is_valid_triangle(-5, 10, 10) == False, "Test 3.7 failed: -5 10 10 should be invalid"
    print("  ✓ Test 3.7: Negative numbers (-5, 10, 10)")

    # Test 4: Integration Test - Small Sample
    print("\n4. Integration Tests:")

    # Create a small test file
    test_filename = 'test_sample.txt'
    with open(test_filename, 'w') as f:
        f.write("5 10 25\n")
        f.write("3 4 5\n")
        f.write("1 2 3\n")
        f.write("5 5 8\n")

    result = count_valid_triangles(test_filename)
    assert result == 2, f"Test 4.1 failed: Expected 2, got {result}"
    print(f"  ✓ Test 4.1: Small sample file (expected 2, got {result})")

    # Clean up test file
    os.remove(test_filename)

    # Test 5: Manual Verification of First Few Lines
    print("\n5. Manual Verification of Actual Input:")

    # Manually verify specific triangles from input
    test_cases = [
        ((566, 477, 376), True, "Line 1"),
        ((575, 488, 365), True, "Line 2"),
        ((50, 18, 156), False, "Line 3"),
        ((558, 673, 498), True, "Line 4"),
        ((133, 112, 510), False, "Line 5"),
        ((910, 265, 611), False, "Line 8"),
        ((894, 252, 545), False, "Line 9"),
    ]

    for (a, b, c), expected, label in test_cases:
        result = is_valid_triangle(a, b, c)
        assert result == expected, f"  {label} failed: {a} {b} {c} should be {'valid' if expected else 'invalid'}"
        status = "valid" if result else "invalid"
        print(f"  ✓ {label}: ({a}, {b}, {c}) correctly identified as {status}")

    print("\n" + "=" * 60)
    print("All tests passed! ✓")
    print("=" * 60)


if __name__ == '__main__':
    run_tests()
