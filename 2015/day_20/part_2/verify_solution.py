"""
Verification script to test the solution implementation
"""

from solution import get_divisors_with_limit, calculate_presents, find_lowest_house

def test_divisors():
    """Test divisor finding with 50-house limit"""
    print("Testing divisor finding...")

    # Test Case 1.1: Small house number (all divisors valid)
    result = get_divisors_with_limit(12, 50)
    expected = {1, 2, 3, 4, 6, 12}
    assert result == expected, f"House 12 divisors: expected {expected}, got {result}"
    print("✓ House 12: All divisors valid")

    # Test Case 1.4: Perfect square (avoid duplicates)
    result = get_divisors_with_limit(100, 50)
    expected = {2, 4, 5, 10, 20, 25, 50, 100}
    assert result == expected, f"House 100 divisors: expected {expected}, got {result}"
    assert len(result) == 8, f"House 100: expected 8 divisors, got {len(result)}"
    print("✓ House 100: Perfect square handling, no duplicates")

    # Test Case 1.3: Large house number (some divisors filtered)
    result = get_divisors_with_limit(120, 50)
    expected = {3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120}
    assert result == expected, f"House 120 divisors: expected {expected}, got {result}"
    print("✓ House 120: Some divisors filtered (elves 1 and 2 excluded)")

    # Test Case 1.5: Prime number within limit
    result = get_divisors_with_limit(47, 50)
    expected = {1, 47}
    assert result == expected, f"House 47 divisors: expected {expected}, got {result}"
    print("✓ House 47: Prime number handling")

    print()

def test_presents():
    """Test present calculation"""
    print("Testing present calculation...")

    # Test Case 2.1: House 1
    result = calculate_presents(1)
    expected = 11
    assert result == expected, f"House 1: expected {expected}, got {result}"
    print(f"✓ House 1: {result} presents")

    # Test Case 2.2: House 2
    result = calculate_presents(2)
    expected = 33
    assert result == expected, f"House 2: expected {expected}, got {result}"
    print(f"✓ House 2: {result} presents")

    # Test Case 2.3: House 100
    result = calculate_presents(100)
    expected = 2376
    assert result == expected, f"House 100: expected {expected}, got {result}"
    print(f"✓ House 100: {result} presents (boundary case)")

    # Test Case 2.4: House 60
    result = calculate_presents(60)
    expected = 1837
    assert result == expected, f"House 60: expected {expected}, got {result}"
    print(f"✓ House 60: {result} presents")

    # Test Case 2.5: House 51 (critical edge case - first house excluding elf 1)
    result = calculate_presents(51)
    expected = 781
    assert result == expected, f"House 51: expected {expected}, got {result}"
    print(f"✓ House 51: {result} presents (first house where elf 1 is excluded)")

    print()

def test_edge_cases():
    """Test edge cases"""
    print("Testing edge cases...")

    # Edge Case 3: House 1 (minimal case)
    result = calculate_presents(1)
    expected = 11
    assert result == expected, f"House 1 (minimal): expected {expected}, got {result}"
    print(f"✓ House 1 (minimal): {result} presents")

    # Edge Case 1: House 50 (boundary case)
    result = calculate_presents(50)
    expected = 1023
    assert result == expected, f"House 50 (boundary): expected {expected}, got {result}"
    print(f"✓ House 50 (boundary): {result} presents")

    # Edge Case 2: House 51 (first exclusion)
    result = calculate_presents(51)
    expected = 781
    assert result == expected, f"House 51 (first exclusion): expected {expected}, got {result}"
    print(f"✓ House 51 (first exclusion): {result} presents")

    print()

def test_search():
    """Test search function"""
    print("Testing search function...")

    # Test Case 3.1: Very low target
    result = find_lowest_house(100)
    expected = 6
    assert result == expected, f"Target 100: expected house {expected}, got {result}"

    # Verify house 6 has sufficient presents
    house_6_presents = calculate_presents(6)
    assert house_6_presents >= 100, f"House 6 should have >= 100 presents, got {house_6_presents}"

    # Verify house 5 has insufficient presents
    house_5_presents = calculate_presents(5)
    assert house_5_presents < 100, f"House 5 should have < 100 presents, got {house_5_presents}"

    print(f"✓ Target 100: Correctly found house {result}")
    print(f"  - House 6: {house_6_presents} presents (>= 100)")
    print(f"  - House 5: {house_5_presents} presents (< 100)")

    print()

def test_integration():
    """Integration test"""
    print("Testing integration (house 120)...")

    result = calculate_presents(120)
    expected = 3927
    assert result == expected, f"House 120: expected {expected}, got {result}"
    print(f"✓ House 120: {result} presents")

    print()

def verify_final_answer():
    """Verify the final answer for the actual input"""
    print("Verifying final answer for input 34,000,000...")

    target = 34000000
    answer = 831600

    # Check that the answer house has enough presents
    presents_at_answer = calculate_presents(answer)
    print(f"House {answer}: {presents_at_answer:,} presents")
    assert presents_at_answer >= target, f"House {answer} should have >= {target:,} presents, got {presents_at_answer:,}"

    # Check that the previous house doesn't have enough
    presents_before = calculate_presents(answer - 1)
    print(f"House {answer - 1}: {presents_before:,} presents")
    assert presents_before < target, f"House {answer - 1} should have < {target:,} presents, got {presents_before:,}"

    print(f"✓ Answer {answer} is correct!")
    print(f"  - House {answer}: {presents_at_answer:,} presents (>= {target:,})")
    print(f"  - House {answer - 1}: {presents_before:,} presents (< {target:,})")

    return True

if __name__ == "__main__":
    print("=" * 60)
    print("SOLUTION VERIFICATION")
    print("=" * 60)
    print()

    try:
        test_divisors()
        test_presents()
        test_edge_cases()
        test_search()
        test_integration()
        verify_final_answer()

        print()
        print("=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)

    except AssertionError as e:
        print()
        print("=" * 60)
        print(f"TEST FAILED: {e}")
        print("=" * 60)
        raise
