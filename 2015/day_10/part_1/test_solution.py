from solution import look_and_say, apply_iterations

def test_look_and_say():
    """Test the core transformation function with examples from problem"""
    test_cases = [
        ("1", "11"),
        ("11", "21"),
        ("21", "1211"),
        ("1211", "111221"),
        ("111221", "312211"),
        ("123", "111213"),
        ("1111", "41"),
        ("3331", "3311"),
    ]

    print("Testing look_and_say function:")
    all_passed = True
    for input_str, expected in test_cases:
        result = look_and_say(input_str)
        if result == expected:
            print(f"✓ {input_str} → {result}")
        else:
            print(f"✗ {input_str} → {result} (expected {expected})")
            all_passed = False

    return all_passed

def test_iterations():
    """Test multiple iterations starting from '1'"""
    print("\nTesting iterations:")
    result = "1"
    expected_sequence = ["1", "11", "21", "1211", "111221", "312211"]

    all_passed = True
    for i, expected in enumerate(expected_sequence):
        if result == expected:
            print(f"✓ Iteration {i}: {result} (length {len(result)})")
        else:
            print(f"✗ Iteration {i}: {result} (expected {expected})")
            all_passed = False

        if i < len(expected_sequence) - 1:
            result = look_and_say(result)

    return all_passed

def test_actual_input_small():
    """Test with actual input for small iterations"""
    print("\nTesting actual input with small iterations:")
    input_str = "1321131112"

    # Test first transformation manually
    first_result = look_and_say(input_str)
    print(f"Input: {input_str}")
    print(f"After 1 iteration: {first_result} (length {len(first_result)})")

    # Test 5 and 10 iterations
    for iterations in [5, 10]:
        result = apply_iterations(input_str, iterations)
        print(f"After {iterations} iterations: length = {len(result)}")

    return True

if __name__ == "__main__":
    test1 = test_look_and_say()
    test2 = test_iterations()
    test3 = test_actual_input_small()

    if test1 and test2 and test3:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed!")
