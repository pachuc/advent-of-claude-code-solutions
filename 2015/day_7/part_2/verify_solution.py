"""Verification tests for the circuit simulation solution"""

from solution import parse_instructions, evaluate_wire, simulate_circuit

def test_simple_circuit():
    """Test basic circuit evaluation with all operation types"""
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

    # Expected values
    assert evaluate_wire('x', instructions, memo) == 123, "x should be 123"
    assert evaluate_wire('y', instructions, memo) == 456, "y should be 456"
    assert evaluate_wire('d', instructions, memo) == 72, "x AND y should be 72"
    assert evaluate_wire('e', instructions, memo) == 507, "x OR y should be 507"
    assert evaluate_wire('f', instructions, memo) == 492, "x LSHIFT 2 should be 492"
    assert evaluate_wire('g', instructions, memo) == 114, "y RSHIFT 2 should be 114"
    assert evaluate_wire('h', instructions, memo) == 65412, "NOT x should be 65412"
    assert evaluate_wire('i', instructions, memo) == 65079, "NOT y should be 65079"

    print("✓ Simple circuit test passed")


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

    assert evaluate_wire('a', instructions, memo) == 65535, "NOT 0 should be 65535"
    assert evaluate_wire('b', instructions, memo) == 0, "NOT 65535 should be 0"
    assert evaluate_wire('c', instructions, memo) == 65534, "NOT 1 should be 65534"

    print("✓ NOT operation test passed")


def test_16bit_overflow():
    """Test 16-bit overflow handling for left shift"""
    test_input = """65535 -> x
x LSHIFT 1 -> y
x LSHIFT 8 -> z"""

    lines = test_input.strip().split('\n')
    instructions = parse_instructions(lines)
    memo = {}

    assert evaluate_wire('x', instructions, memo) == 65535, "x should be 65535"
    assert evaluate_wire('y', instructions, memo) == 65534, "(65535 << 1) & 0xFFFF should be 65534"
    assert evaluate_wire('z', instructions, memo) == 65280, "(65535 << 8) & 0xFFFF should be 65280"

    print("✓ 16-bit overflow test passed")


def test_part2_logic():
    """Test the two-stage simulation process"""
    test_input = """NOT b -> a
100 -> b"""

    lines = test_input.strip().split('\n')
    instructions = parse_instructions(lines)

    # First run
    memo1 = {}
    original_a = evaluate_wire('a', instructions, memo1)
    assert original_a == 65435, "First run: a should be NOT 100 = 65435"

    # Override b
    instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a)]}

    # Second run with fresh memo
    memo2 = {}
    final_a = evaluate_wire('a', instructions, memo2)
    assert final_a == 100, "Second run: a should be NOT 65435 = 100"

    # Verify values changed
    assert original_a != final_a, "Values should be different between runs"

    print("✓ Part 2 logic test passed")


def test_full_input():
    """Test with the actual puzzle input"""
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse instructions
    instructions = parse_instructions(lines)

    # Check we parsed all instructions
    assert len(instructions) > 0, "Should have parsed instructions"

    # First run
    original_a = simulate_circuit(instructions)
    assert 0 <= original_a <= 65535, "First run wire a should be in valid 16-bit range"
    assert original_a == 3176, f"First run wire a should be 3176, got {original_a}"

    # Override b
    instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a)]}

    # Second run
    final_a = simulate_circuit(instructions)
    assert 0 <= final_a <= 65535, "Second run wire a should be in valid 16-bit range"
    assert final_a == 14710, f"Second run wire a should be 14710, got {final_a}"

    # Values should be different
    assert original_a != final_a, "Wire a values should differ between runs"

    print("✓ Full input test passed")
    print(f"  First run: a = {original_a}")
    print(f"  Second run: a = {final_a}")


def test_mixed_operands():
    """Test operations with both literals and wire references"""
    test_input = """123 -> x
1 AND x -> y
x AND 456 -> z"""

    lines = test_input.strip().split('\n')
    instructions = parse_instructions(lines)
    memo = {}

    assert evaluate_wire('y', instructions, memo) == 1, "1 AND 123 should be 1"
    assert evaluate_wire('z', instructions, memo) == 72, "123 AND 456 should be 72"

    print("✓ Mixed operands test passed")


if __name__ == '__main__':
    print("Running verification tests...\n")

    try:
        test_simple_circuit()
        test_not_operation()
        test_16bit_overflow()
        test_mixed_operands()
        test_part2_logic()
        test_full_input()

        print("\n" + "="*50)
        print("ALL TESTS PASSED ✓")
        print("="*50)
        print("\nThe solution correctly:")
        print("  • Parses all instruction types")
        print("  • Handles bitwise operations correctly")
        print("  • Manages 16-bit overflow properly")
        print("  • Implements Part 2 two-stage simulation")
        print("  • Produces the correct final answer: 14710")

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        exit(1)
