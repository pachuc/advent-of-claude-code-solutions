"""
Test suite for Elf Present Delivery solution (Part 2)
"""

from solution import get_divisors_with_limit, calculate_presents, find_lowest_house


def test_divisors():
    """Test divisor finding with 50-house limit."""
    print("Testing divisor finding...")

    # Test 1.1: Small house number (all divisors valid)
    result = get_divisors_with_limit(12, 50)
    expected = {1, 2, 3, 4, 6, 12}
    assert result == expected, f"Test 1.1 failed: expected {expected}, got {result}"
    print("✓ Test 1.1: House 12 - all divisors valid")

    # Test 1.3: House 120 (some divisors filtered)
    # Divisor 1: 120/1 = 120 > 50, EXCLUDE
    # Divisor 2: 120/2 = 60 > 50, EXCLUDE
    # Divisor 3: 120/3 = 40 <= 50, INCLUDE
    result = get_divisors_with_limit(120, 50)
    expected = {3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120}
    assert result == expected, f"Test 1.3 failed: expected {expected}, got {result}"
    print("✓ Test 1.3: House 120 - some divisors filtered (1 and 2 excluded)")

    # Test 1.4: Perfect square (avoid duplicates)
    # Divisor 1: 100/1 = 100 > 50, EXCLUDE
    # All others: 100/d <= 50, INCLUDE
    result = get_divisors_with_limit(100, 50)
    expected = {2, 4, 5, 10, 20, 25, 50, 100}
    assert result == expected, f"Test 1.4 failed: expected {expected}, got {result}"
    assert len(result) == 8, f"Test 1.4 duplicate check failed: expected 8 divisors, got {len(result)}"
    print("✓ Test 1.4: House 100 - perfect square, no duplicates")

    # Test 1.5: Prime number
    result = get_divisors_with_limit(47, 50)
    expected = {1, 47}
    assert result == expected, f"Test 1.5 failed: expected {expected}, got {result}"
    print("✓ Test 1.5: House 47 - prime number")

    print("All divisor tests passed!\n")


def test_presents():
    """Test present calculation."""
    print("Testing present calculation...")

    # Test 2.1: House 1
    result = calculate_presents(1)
    expected = 11
    assert result == expected, f"Test 2.1 failed: expected {expected}, got {result}"
    print(f"✓ Test 2.1: House 1 = {result} presents")

    # Test 2.2: House 2
    result = calculate_presents(2)
    expected = 33  # 11*1 + 11*2 = 11 + 22 = 33
    assert result == expected, f"Test 2.2 failed: expected {expected}, got {result}"
    print(f"✓ Test 2.2: House 2 = {result} presents")

    # Test 2.3: House 100
    # Valid divisors: 2, 4, 5, 10, 20, 25, 50, 100
    # 11 × (2 + 4 + 5 + 10 + 20 + 25 + 50 + 100) = 11 × 216 = 2376
    result = calculate_presents(100)
    expected = 2376
    assert result == expected, f"Test 2.3 failed: expected {expected}, got {result}"
    print(f"✓ Test 2.3: House 100 = {result} presents (boundary case, divisor 2 at limit)")

    # Test 2.4: House 60
    # Valid divisors: 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60 (1 excluded: 60/1=60>50)
    # 11 × (2+3+4+5+6+10+12+15+20+30+60) = 11 × 167 = 1837
    result = calculate_presents(60)
    expected = 1837
    assert result == expected, f"Test 2.4 failed: expected {expected}, got {result}"
    print(f"✓ Test 2.4: House 60 = {result} presents")

    # Test 2.5: House 51 (first house excluding elf 1)
    # Valid divisors: 3, 17, 51 (1 excluded: 51/1=51>50)
    # 11 × (3 + 17 + 51) = 11 × 71 = 781
    result = calculate_presents(51)
    expected = 781
    assert result == expected, f"Test 2.5 failed: expected {expected}, got {result}"
    print(f"✓ Test 2.5: House 51 = {result} presents (elf 1 excluded)")

    print("All present calculation tests passed!\n")


def test_edge_cases():
    """Test edge cases."""
    print("Testing edge cases...")

    # Edge Case 1: House 50 (boundary - all divisors valid)
    # Divisors of 50: 1, 2, 5, 10, 25, 50
    # All satisfy constraint: 50/1=50, 50/2=25, etc.
    # 11 × (1+2+5+10+25+50) = 11 × 93 = 1023
    result = calculate_presents(50)
    expected = 1023
    assert result == expected, f"Edge case 1 failed: expected {expected}, got {result}"
    print(f"✓ Edge Case 1: House 50 = {result} presents (at boundary, all divisors valid)")

    # Edge Case 2: House 51 (first exclusion)
    # Already tested above, but worth verifying again
    result = calculate_presents(51)
    expected = 781
    assert result == expected, f"Edge case 2 failed: expected {expected}, got {result}"
    print(f"✓ Edge Case 2: House 51 = {result} presents (first house where elf 1 excluded)")

    # Edge Case 3: House 1 (minimal)
    result = calculate_presents(1)
    expected = 11
    assert result == expected, f"Edge case 3 failed: expected {expected}, got {result}"
    print(f"✓ Edge Case 3: House 1 = {result} presents (minimal case)")

    print("All edge case tests passed!\n")


def test_search():
    """Test search function."""
    print("Testing search function...")

    # Test 3.1: Very low target
    # House 6: divisors 1,2,3,6 -> 11 × (1+2+3+6) = 132
    result = find_lowest_house(100)
    expected = 6
    assert result == expected, f"Test 3.1 failed: expected {expected}, got {result}"
    print(f"✓ Test 3.1: Lowest house for target 100 = {result}")

    # Verify house 6 actually has >= 100 presents
    presents = calculate_presents(6)
    assert presents >= 100, f"Verification failed: house {result} has {presents} presents, expected >= 100"
    print(f"  Verified: House {result} has {presents} presents")

    # Verify house 5 has < 100 presents
    presents_prev = calculate_presents(5)
    assert presents_prev < 100, f"Verification failed: house {result-1} has {presents_prev} presents, expected < 100"
    print(f"  Verified: House {result-1} has {presents_prev} presents")

    print("All search tests passed!\n")


def test_integration():
    """Integration test for house 120."""
    print("Testing integration (house 120)...")

    # Manually calculate expected value
    # Divisors of 120: 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120
    # Valid (120/d <= 50): 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120
    # Sum: 3+4+5+6+8+10+12+15+20+24+30+40+60+120 = 357
    # Total: 11 × 357 = 3927

    result = calculate_presents(120)
    expected = 3927
    assert result == expected, f"Integration test failed: expected {expected}, got {result}"
    print(f"✓ Integration test: House 120 = {result} presents")
    print("Integration test passed!\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Running test suite for Elf Present Delivery (Part 2)")
    print("=" * 60)
    print()

    test_divisors()
    test_presents()
    test_edge_cases()
    test_search()
    test_integration()

    print("=" * 60)
    print("All tests passed successfully!")
    print("=" * 60)
