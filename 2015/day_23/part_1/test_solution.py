from solution import parse_instruction, simulate


def test_parsing():
    """Test that parsing works for all instruction formats."""
    test_cases = [
        ('hlf a', ('hlf', 'a', None)),
        ('tpl b', ('tpl', 'b', None)),
        ('inc a', ('inc', 'a', None)),
        ('jmp +19', ('jmp', None, 19)),
        ('jmp -7', ('jmp', None, -7)),
        ('jie a, +4', ('jie', 'a', 4)),
        ('jio b, -3', ('jio', 'b', -3)),
    ]

    for input_str, expected in test_cases:
        result = parse_instruction(input_str)
        assert result == expected, f"Parse failed: {input_str} -> {result}, expected {expected}"
        print(f"✓ Parsed '{input_str}' correctly")

    print("All parsing tests passed!")
    return True


def test_program(program_lines, expected_a, expected_b, test_name):
    """Test a program and verify final register values."""
    registers = simulate(program_lines)
    assert registers['a'] == expected_a, f"Expected a={expected_a}, got {registers['a']}"
    assert registers['b'] == expected_b, f"Expected b={expected_b}, got {registers['b']}"
    print(f"✓ {test_name}: a={registers['a']}, b={registers['b']}")
    return True


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("PARSING TESTS")
    print("=" * 60)
    test_parsing()

    print("\n" + "=" * 60)
    print("INSTRUCTION TESTS")
    print("=" * 60)

    # Test 1.1: Increment
    test_program(['inc a', 'inc b'], 1, 1, "Test 1.1 - Increment")

    # Test 1.2: Triple
    test_program(['inc a', 'tpl a', 'tpl b'], 3, 0, "Test 1.2 - Triple")

    # Test 1.3: Half (odd number)
    test_program(['inc a', 'inc a', 'inc a', 'hlf a'], 1, 0, "Test 1.3a - Half (odd)")

    # Test 1.3: Half (even number)
    test_program(['inc a', 'inc a', 'inc a', 'inc a', 'hlf a'], 2, 0, "Test 1.3b - Half (even)")

    # Test 1.3: Half (zero)
    test_program(['hlf a'], 0, 0, "Test 1.3c - Half (zero)")

    print("\n" + "=" * 60)
    print("JUMP TESTS")
    print("=" * 60)

    # Test 2.1: Forward jump
    test_program(['jmp +2', 'inc a', 'inc a', 'inc b'], 1, 1, "Test 2.1 - Forward jump")

    # Test 2.2: Jump if even (even - taken)
    test_program(['inc a', 'inc a', 'jie a, +3', 'inc b', 'inc b'], 2, 0, "Test 2.2a - JIE (even, taken)")

    # Test 2.2: Jump if even (odd - not taken)
    test_program(['inc a', 'jie a, +2', 'inc b'], 1, 1, "Test 2.2b - JIE (odd, not taken)")

    # Test 2.2: Jump if even (zero - taken)
    test_program(['jie a, +3', 'inc b', 'inc b'], 0, 0, "Test 2.2c - JIE (zero, taken)")

    # Test 2.3: Jump if one (equals 1 - taken)
    test_program(['inc a', 'jio a, +3', 'inc b', 'inc b'], 1, 0, "Test 2.3a - JIO (1, taken)")

    # Test 2.3: Jump if one (not 1 - not taken)
    test_program(['inc a', 'inc a', 'jio a, +2', 'inc b'], 2, 1, "Test 2.3b - JIO (not 1, not taken)")

    # Test 2.3: Jump if one (zero - not taken)
    test_program(['jio a, +2', 'inc b'], 0, 1, "Test 2.3c - JIO (zero, not taken)")

    print("\n" + "=" * 60)
    print("COMPLEX FLOW TESTS")
    print("=" * 60)

    # Test 3.1: Example from problem statement
    test_program(['inc a', 'jio a, +2', 'tpl a', 'inc a'], 2, 0, "Test 3.1 - Problem example")

    print("\n" + "=" * 60)
    print("BOUNDARY TESTS")
    print("=" * 60)

    # Test 4.1: Forward termination
    test_program(['inc a', 'jmp +1'], 1, 0, "Test 4.1 - Forward termination")

    # Test 4.2: Backward termination
    test_program(['jmp -1'], 0, 0, "Test 4.2 - Backward termination")

    # Test 4.3: Immediate jump to end
    test_program(['jmp +10', 'inc a'], 0, 0, "Test 4.3 - Immediate jump to end")

    print("\n" + "=" * 60)
    print("REGISTER INDEPENDENCE TEST")
    print("=" * 60)

    # Test 5.1: Operations on different registers
    test_program(['inc a', 'inc a', 'inc b', 'tpl a', 'tpl b'], 6, 3, "Test 5.1 - Register independence")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60)


if __name__ == '__main__':
    run_all_tests()
