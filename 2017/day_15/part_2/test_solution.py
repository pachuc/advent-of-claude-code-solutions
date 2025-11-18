from solution import generate_values_filtered, count_matches

def test_first_5_filtered_pairs():
    """Test that the first 5 filtered pairs match the expected values from the problem."""
    print("Testing first 5 filtered pairs with example values (A=65, B=8921)...")

    FACTOR_A = 16807
    FACTOR_B = 48271
    MODULO = 2147483647

    gen_a = generate_values_filtered(65, FACTOR_A, MODULO, 4)
    gen_b = generate_values_filtered(8921, FACTOR_B, MODULO, 8)

    expected_pairs = [
        (1352636452, 1233683848),
        (1992081072, 862516352),
        (530830436, 1159784568),
        (1980017072, 1616057672),
        (740335192, 412269392),
    ]

    print("\nFirst 5 filtered pairs:")
    print("Generator A     Generator B     Expected A      Expected B")
    all_match = True
    for i in range(5):
        value_a = next(gen_a)
        value_b = next(gen_b)
        exp_a, exp_b = expected_pairs[i]

        match_a = value_a == exp_a
        match_b = value_b == exp_b

        print(f"{value_a:10d}      {value_b:10d}      {exp_a:10d}      {exp_b:10d}  {'✓' if (match_a and match_b) else '✗'}")

        if not match_a or not match_b:
            all_match = False
            print(f"  MISMATCH! A: {value_a} vs {exp_a}, B: {value_b} vs {exp_b}")

    # Verify all values are multiples of 4 for A and 8 for B
    gen_a = generate_values_filtered(65, FACTOR_A, MODULO, 4)
    gen_b = generate_values_filtered(8921, FACTOR_B, MODULO, 8)

    print("\nVerifying filter criteria:")
    for i in range(5):
        value_a = next(gen_a)
        value_b = next(gen_b)
        assert value_a % 4 == 0, f"Generator A value {value_a} is not a multiple of 4"
        assert value_b % 8 == 0, f"Generator B value {value_b} is not a multiple of 8"
    print("✓ All values meet filter criteria (A: multiples of 4, B: multiples of 8)")

    if all_match:
        print("\n✓ All pairs match expected values!")
    else:
        print("\n✗ Some pairs don't match expected values")

    return all_match


def test_example_full_count():
    """Test that 5 million pairs with example values produces 309 matches."""
    print("\n\nTesting full count with example values (A=65, B=8921)...")
    print("This may take a few seconds...")

    result = count_matches(65, 8921, 5_000_000)
    print(f"Result: {result}")
    print(f"Expected: 309")

    if result == 309:
        print("✓ Example test passed!")
        return True
    else:
        print(f"✗ Example test failed! Got {result}, expected 309")
        return False


if __name__ == "__main__":
    test1_passed = test_first_5_filtered_pairs()
    test2_passed = test_example_full_count()

    if test1_passed and test2_passed:
        print("\n\n✓✓✓ All tests passed! ✓✓✓")
    else:
        print("\n\n✗✗✗ Some tests failed ✗✗✗")
