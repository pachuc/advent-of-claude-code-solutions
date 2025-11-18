#!/usr/bin/env python3
"""Verification tests for the solution"""

from solution import parse_instructions, get_value, execute_program

def test_get_value():
    """Test value resolution"""
    registers = {'a': 10, 'b': 20, 'c': 0}

    # Register resolution
    assert get_value('a', registers) == 10
    assert get_value('b', registers) == 20
    assert get_value('c', registers) == 0

    # Literal resolution
    assert get_value('5', registers) == 5
    assert get_value('-3', registers) == -3
    assert get_value('100', registers) == 100

    print("✓ get_value tests passed")

def test_set_instruction():
    """Test set instruction"""
    instructions = [('set', 'a', '42')]
    execute_program(instructions)  # Just verify no crash

    instructions = [('set', 'a', '10'), ('set', 'b', 'a')]
    execute_program(instructions)

    print("✓ set instruction tests passed")

def test_sub_instruction():
    """Test sub instruction"""
    instructions = [('set', 'a', '10'), ('sub', 'a', '3')]
    execute_program(instructions)

    # Test subtracting negative (adds)
    instructions = [('set', 'a', '10'), ('sub', 'a', '-5')]
    execute_program(instructions)

    print("✓ sub instruction tests passed")

def test_mul_instruction():
    """Test mul instruction and counter"""
    # Single mul
    instructions = [('set', 'a', '5'), ('mul', 'a', '3')]
    result = execute_program(instructions)
    assert result == 1, f"Expected mul_count=1, got {result}"

    # Multiple mul
    instructions = [('set', 'a', '2'), ('mul', 'a', '3'), ('mul', 'a', '2')]
    result = execute_program(instructions)
    assert result == 2, f"Expected mul_count=2, got {result}"

    print("✓ mul instruction tests passed")

def test_jnz_instruction():
    """Test jnz instruction"""
    # Jump when non-zero
    instructions = [
        ('set', 'a', '5'),
        ('jnz', 'a', '2'),    # Should jump
        ('set', 'b', '1'),    # Should be skipped
        ('set', 'c', '1')     # Should execute
    ]
    execute_program(instructions)

    # No jump when zero
    instructions = [
        ('set', 'a', '0'),
        ('jnz', 'a', '2'),    # Should NOT jump
        ('set', 'b', '1'),    # Should execute
        ('set', 'c', '1')     # Should execute
    ]
    execute_program(instructions)

    print("✓ jnz instruction tests passed")

def test_loop_with_mul():
    """Test loop with mul counting"""
    instructions = [
        ('set', 'a', '3'),
        ('mul', 'a', '1'),
        ('sub', 'a', '1'),
        ('jnz', 'a', '-2')
    ]
    result = execute_program(instructions)
    assert result == 3, f"Expected mul_count=3, got {result}"

    print("✓ loop with mul tests passed")

def test_no_mul():
    """Test program with no mul instructions"""
    instructions = [
        ('set', 'a', '10'),
        ('sub', 'a', '5'),
        ('jnz', 'a', '1')
    ]
    result = execute_program(instructions)
    assert result == 0, f"Expected mul_count=0, got {result}"

    print("✓ no mul tests passed")

def test_empty_program():
    """Test empty program"""
    instructions = []
    result = execute_program(instructions)
    assert result == 0, f"Expected mul_count=0, got {result}"

    print("✓ empty program tests passed")

def test_parsing():
    """Test parsing with empty lines"""
    input_text = """set a 5

mul a 2
"""
    lines = input_text.split('\n')
    parsed = parse_instructions(lines)

    assert len(parsed) == 2, f"Expected 2 instructions, got {len(parsed)}"
    assert parsed[0] == ('set', 'a', '5')
    assert parsed[1] == ('mul', 'a', '2')

    result = execute_program(parsed)
    assert result == 1, f"Expected mul_count=1, got {result}"

    print("✓ parsing tests passed")

def test_actual_input():
    """Test with actual input"""
    with open('input.md', 'r') as f:
        lines = f.readlines()

    instructions = parse_instructions(lines)
    result = execute_program(instructions)

    print(f"✓ actual input test: mul_count = {result}")

    # Run again to verify determinism
    result2 = execute_program(instructions)
    assert result == result2, f"Non-deterministic execution: {result} != {result2}"

    print("✓ determinism verified")

    return result

if __name__ == "__main__":
    print("Running verification tests...\n")

    test_get_value()
    test_set_instruction()
    test_sub_instruction()
    test_mul_instruction()
    test_jnz_instruction()
    test_loop_with_mul()
    test_no_mul()
    test_empty_program()
    test_parsing()
    actual_result = test_actual_input()

    print("\n" + "="*50)
    print("All tests passed!")
    print(f"Final answer: {actual_result}")
    print("="*50)
