from solution import parse_instructions, evaluate_wire, simulate_circuit

def test_basic_circuit():
    """Test basic circuit evaluation (from test plan)"""
    test_input = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

    lines = test_input.strip().split('\n')
    instructions = parse_instructions(lines)
    memo = {}

    print("Test 2: Simple Circuit Evaluation")
    tests = [
        ('x', 123),
        ('y', 456),
        ('d', 72),   # 123 AND 456
        ('e', 507),  # 123 OR 456
        ('f', 492),  # 123 << 2
        ('g', 114),  # 456 >> 2
        ('h', 65412), # NOT 123
        ('i', 65079)  # NOT 456
    ]

    all_passed = True
    for wire, expected in tests:
        result = evaluate_wire(wire, instructions, memo)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} Wire {wire}: {result} (expected {expected})")
        if not passed:
            all_passed = False

    return all_passed


def test_not_operation():
    """Test NOT operation edge cases"""
    test_input = """0 -> x
65535 -> y
1 -> z
NOT x -> a
NOT y -> b
NOT z -> c"""

    lines = test_input.strip().split('\n')
    instructions = parse_instructions(lines)
    memo = {}

    print("\nTest 4: NOT Operation")
    tests = [
        ('a', 65535),  # NOT 0
        ('b', 0),      # NOT 65535
        ('c', 65534)   # NOT 1
    ]

    all_passed = True
    for wire, expected in tests:
        result = evaluate_wire(wire, instructions, memo)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} Wire {wire}: {result} (expected {expected})")
        if not passed:
            all_passed = False

    return all_passed


def test_part2_logic():
    """Test Part 2 two-stage simulation"""
    test_input = """NOT b -> a
100 -> b"""

    lines = test_input.strip().split('\n')
    instructions = parse_instructions(lines)

    print("\nTest 7: Part 2 Two-Stage Simulation")

    # First run
    memo1 = {}
    original_a = evaluate_wire('a', instructions, memo1)
    expected_first = 65435  # NOT 100
    print(f"  First run - wire a: {original_a} (expected {expected_first})")

    # Override b
    instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a)]}

    # Second run with fresh memo
    memo2 = {}
    final_a = evaluate_wire('a', instructions, memo2)
    expected_second = 100  # NOT 65435
    print(f"  Second run - wire a: {final_a} (expected {expected_second})")

    passed = original_a == expected_first and final_a == expected_second
    status = "✓" if passed else "✗"
    print(f"  {status} Two-stage simulation test")

    return passed


def test_overflow():
    """Test 16-bit overflow handling"""
    test_input = """65535 -> x
x LSHIFT 1 -> y
x LSHIFT 8 -> z"""

    lines = test_input.strip().split('\n')
    instructions = parse_instructions(lines)
    memo = {}

    print("\nTest 3: 16-bit Overflow Handling")
    tests = [
        ('x', 65535),
        ('y', 65534),  # (65535 << 1) & 0xFFFF
        ('z', 65280)   # (65535 << 8) & 0xFFFF
    ]

    all_passed = True
    for wire, expected in tests:
        result = evaluate_wire(wire, instructions, memo)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} Wire {wire}: {result} (expected {expected})")
        if not passed:
            all_passed = False

    return all_passed


def test_mixed_operands():
    """Test mixed literal and wire operands"""
    test_input = """123 -> x
1 AND x -> y
x AND 456 -> z"""

    lines = test_input.strip().split('\n')
    instructions = parse_instructions(lines)
    memo = {}

    print("\nTest 5: Mixed Literal and Wire Operands")
    tests = [
        ('y', 1),   # 1 AND 123
        ('z', 72)   # 123 AND 456
    ]

    all_passed = True
    for wire, expected in tests:
        result = evaluate_wire(wire, instructions, memo)
        passed = result == expected
        status = "✓" if passed else "✗"
        print(f"  {status} Wire {wire}: {result} (expected {expected})")
        if not passed:
            all_passed = False

    return all_passed


if __name__ == '__main__':
    print("Running unit tests...\n")
    print("=" * 50)

    results = []
    results.append(test_basic_circuit())
    results.append(test_not_operation())
    results.append(test_overflow())
    results.append(test_mixed_operands())
    results.append(test_part2_logic())

    print("\n" + "=" * 50)
    print(f"\nSummary: {sum(results)}/{len(results)} tests passed")

    if all(results):
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed")
