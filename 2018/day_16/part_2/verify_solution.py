#!/usr/bin/env python3
"""Verification script for Part 2 solution"""

from solution import *

def test_parsing():
    """Test that parsing works correctly"""
    print("Test 1: Parsing validation")
    samples, test_program = parse_input("input.md")

    # Check samples
    assert len(samples) > 0, "No samples parsed"
    print(f"  ✓ Parsed {len(samples)} samples")

    # Check test program
    assert len(test_program) > 0, "No test program parsed"
    print(f"  ✓ Parsed {len(test_program)} test program instructions")

    # Verify sample structure
    for i, (before, instruction, after) in enumerate(samples[:5]):
        assert len(before) == 4, f"Sample {i}: before should have 4 registers"
        assert len(instruction) == 4, f"Sample {i}: instruction should have 4 values"
        assert len(after) == 4, f"Sample {i}: after should have 4 registers"
    print(f"  ✓ Sample structure validated")

    # Verify test program structure
    for i, instruction in enumerate(test_program[:5]):
        assert len(instruction) == 4, f"Instruction {i}: should have 4 values"
    print(f"  ✓ Test program structure validated")

    return samples, test_program


def test_opcode_compatibility():
    """Test opcode compatibility checking"""
    print("\nTest 2: Opcode compatibility")
    # Example from problem statement
    before = [3, 2, 1, 1]
    instruction = [9, 2, 1, 2]
    after = [3, 2, 2, 1]

    compatible = get_compatible_opcodes(before, instruction, after)
    print(f"  Compatible opcodes: {compatible}")

    # The example should match mulr, addi, seti
    expected = {'mulr', 'addi', 'seti'}
    assert compatible == expected, f"Expected {expected}, got {compatible}"
    print(f"  ✓ Correctly identified {len(compatible)} compatible opcodes")


def test_opcode_mapping():
    """Test opcode mapping deduction"""
    print("\nTest 3: Opcode mapping deduction")
    samples, _ = parse_input("input.md")

    # Build possibilities
    possibilities = build_opcode_possibilities(samples)
    print(f"  Built possibilities for {len(possibilities)} opcode numbers")

    # Check all opcodes have possibilities
    for opcode_num, possible_names in possibilities.items():
        assert len(possible_names) > 0, f"Opcode {opcode_num} has no possibilities"
    print(f"  ✓ All opcode numbers have at least 1 possibility")

    # Deduce mapping
    opcode_map = deduce_opcode_mapping(possibilities)
    print(f"  Deduced mapping for {len(opcode_map)} opcodes")

    # Validate mapping
    assert len(opcode_map) == 16, f"Should have 16 mappings, got {len(opcode_map)}"
    assert set(opcode_map.keys()) == set(range(16)), "Should map all opcode numbers 0-15"
    assert len(set(opcode_map.values())) == 16, "Should have 16 unique opcode names"
    assert set(opcode_map.values()) == set(ALL_OPCODES), "Should use all opcodes"
    print(f"  ✓ Mapping is valid: 16 unique 1-to-1 mappings")

    # Print the mapping
    print("\n  Deduced opcode mapping:")
    for opcode_num in sorted(opcode_map.keys()):
        print(f"    Opcode {opcode_num:2d} -> {opcode_map[opcode_num]}")

    return opcode_map


def test_program_execution():
    """Test program execution"""
    print("\nTest 4: Program execution")
    samples, test_program = parse_input("input.md")

    # Get opcode mapping
    possibilities = build_opcode_possibilities(samples)
    opcode_map = deduce_opcode_mapping(possibilities)

    # Execute program
    result = execute_program(test_program, opcode_map)
    print(f"  ✓ Program executed successfully")
    print(f"  Register 0 value: {result}")

    # Validate result
    assert isinstance(result, int), f"Result should be an integer, got {type(result)}"
    assert result >= 0, f"Result should be non-negative, got {result}"
    print(f"  ✓ Result is a valid non-negative integer")

    return result


def test_consistency():
    """Test that solution is deterministic"""
    print("\nTest 5: Consistency check")
    result1 = solve("input.md")
    result2 = solve("input.md")

    assert result1 == result2, f"Solution is non-deterministic: {result1} != {result2}"
    print(f"  ✓ Solution is deterministic (both runs: {result1})")

    return result1


def main():
    print("=" * 60)
    print("VERIFICATION TESTS FOR PART 2 SOLUTION")
    print("=" * 60)

    try:
        # Run all tests
        test_parsing()
        test_opcode_compatibility()
        test_opcode_mapping()
        test_program_execution()
        final_answer = test_consistency()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print(f"FINAL ANSWER: {final_answer}")
        print("=" * 60)

        return final_answer

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    answer = main()
    if answer is None:
        exit(1)
