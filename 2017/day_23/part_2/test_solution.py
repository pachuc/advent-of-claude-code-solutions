"""
Test suite for Part 2 solution
"""
from solution import is_composite, count_composites


def test_primality():
    """Test the is_composite function with known values"""
    print("Testing primality function...")

    # Test known primes (should return False)
    primes = [2, 3, 5, 7, 11, 97, 997]
    for p in primes:
        result = is_composite(p)
        status = "✓" if not result else "✗"
        print(f"  {status} is_composite({p}) = {result} (expected False)")
        assert not result, f"{p} is prime but marked as composite"

    # Test known composites (should return True)
    composites = [4, 6, 8, 9, 15, 100, 1000]
    for c in composites:
        result = is_composite(c)
        status = "✓" if result else "✗"
        print(f"  {status} is_composite({c}) = {result} (expected True)")
        assert result, f"{c} is composite but marked as prime"

    # Test edge cases
    edge_cases = [(0, True), (1, True)]
    for n, expected in edge_cases:
        result = is_composite(n)
        status = "✓" if result == expected else "✗"
        print(f"  {status} is_composite({n}) = {result} (expected {expected})")
        assert result == expected, f"{n} should be {expected}"

    # Test large numbers in target range
    # 106700 = 2^2 × 5^2 × 1067, definitely composite
    result = is_composite(106700)
    status = "✓" if result else "✗"
    print(f"  {status} is_composite(106700) = {result} (expected True)")
    assert result, f"106700 should be composite"

    # Test some large primes in the range (verified)
    large_primes = [106699, 106721]
    for p in large_primes:
        result = is_composite(p)
        status = "✓" if not result else "✗"
        print(f"  {status} is_composite({p}) = {result} (expected False - it's prime)")
        assert not result, f"{p} is prime"

    print("✓ All primality tests passed!\n")


def test_range_logic():
    """Test the range and counting logic"""
    print("Testing range logic...")

    # Test that range has exactly 1001 values
    b = 106700
    c = 123700
    step = 17

    count = 0
    current = b
    values = []
    while current <= c:
        count += 1
        values.append(current)
        current += step

    print(f"  ✓ Range has {count} values (expected 1001)")
    assert count == 1001, f"Expected 1001 values, got {count}"

    # Test boundaries
    print(f"  ✓ First value: {values[0]} (expected 106700)")
    assert values[0] == 106700, f"First value should be 106700"

    print(f"  ✓ Last value: {values[-1]} (expected 123700)")
    assert values[-1] == 123700, f"Last value should be 123700"

    print(f"  ✓ 123717 not in range: {123717 not in values}")
    assert 123717 not in values, f"123717 should not be in range"

    print("✓ All range tests passed!\n")


def test_small_scale():
    """Test counting on small, manually verifiable ranges"""
    print("Testing small-scale counting...")

    # Test: [10, 30] step 5
    # Values: 10, 15, 20, 25, 30 (all composite)
    result = count_composites(10, 30, 5)
    print(f"  ✓ count_composites(10, 30, 5) = {result} (expected 5)")
    assert result == 5, f"Expected 5, got {result}"

    # Test: [2, 7] step 1
    # Values: 2, 3, 4, 5, 6, 7
    # Primes: 2, 3, 5, 7
    # Composites: 4, 6
    result = count_composites(2, 7, 1)
    print(f"  ✓ count_composites(2, 7, 1) = {result} (expected 2)")
    assert result == 2, f"Expected 2, got {result}"

    # Test: [4, 10] step 2
    # Values: 4, 6, 8, 10 (all composite)
    result = count_composites(4, 10, 2)
    print(f"  ✓ count_composites(4, 10, 2) = {result} (expected 4)")
    assert result == 4, f"Expected 4, got {result}"

    print("✓ All small-scale tests passed!\n")


def test_answer_sanity():
    """Verify the final answer is reasonable"""
    print("Testing final answer sanity...")

    result = count_composites(106700, 123700, 17)
    print(f"  Final answer: {result}")
    print(f"  ✓ Answer in valid range [0, 1001]: {0 <= result <= 1001}")
    assert 0 <= result <= 1001, f"Answer must be between 0 and 1001"

    # By Prime Number Theorem, ~91% should be composite
    print(f"  ✓ Answer > 900 (expect ~90%+ composite): {result > 900}")
    assert result > 900, f"Expected >900 composites based on prime density"

    print(f"  ✓ Answer < 1001 (expect some primes): {result < 1001}")
    assert result < 1001, f"Expected <1001 (should have some primes)"

    print("✓ Answer sanity check passed!\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Running test suite for Part 2")
    print("=" * 60 + "\n")

    test_primality()
    test_range_logic()
    test_small_scale()
    test_answer_sanity()

    print("=" * 60)
    print("All tests passed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
