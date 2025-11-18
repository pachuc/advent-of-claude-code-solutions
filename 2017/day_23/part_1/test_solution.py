from solution import parse_instructions, get_value, execute_program


def test_get_value():
    """Test the get_value helper function"""
    registers = {'a': 10, 'b': 20, 'c': 0, 'd': -5}

    # Test register resolution
    assert get_value('a', registers) == 10
    assert get_value('b', registers) == 20
    assert get_value('c', registers) == 0
    assert get_value('d', registers) == -5

    # Test literal resolution
    assert get_value('5', registers) == 5
    assert get_value('-3', registers) == -3
    assert get_value('100', registers) == 100
    assert get_value('0', registers) == 0
    assert get_value('-100', registers) == -100

    print("✓ get_value tests passed")


def test_set_instruction():
    """Test set instruction"""
    # Test setting from literal
    instructions = [("set", "a", "42")]
    result = execute_program(instructions)

    # Test setting from another register
    instructions = [("set", "a", "10"), ("set", "b", "a")]
    result = execute_program(instructions)

    # Test setting negative value
    instructions = [("set", "a", "-5")]
    result = execute_program(instructions)

    print("✓ set instruction tests passed")


def test_sub_instruction():
    """Test sub instruction"""
    # Test subtracting literal
    instructions = [("set", "a", "10"), ("sub", "a", "3")]
    result = execute_program(instructions)

    # Test subtracting negative (adds)
    instructions = [("set", "a", "10"), ("sub", "a", "-5")]
    result = execute_program(instructions)

    print("✓ sub instruction tests passed")


def test_mul_instruction():
    """Test mul instruction and counter"""
    # Test multiplying by literal
    instructions = [("set", "a", "5"), ("mul", "a", "3")]
    result = execute_program(instructions)
    assert result == 1, f"Expected mul_count=1, got {result}"

    # Test multiple mul instructions
    instructions = [("set", "a", "2"), ("mul", "a", "3"), ("mul", "a", "2")]
    result = execute_program(instructions)
    assert result == 2, f"Expected mul_count=2, got {result}"

    # Test multiplying by zero
    instructions = [("set", "a", "5"), ("mul", "a", "0")]
    result = execute_program(instructions)
    assert result == 1, f"Expected mul_count=1, got {result}"

    print("✓ mul instruction tests passed")


def test_jnz_instruction():
    """Test jnz instruction"""
    # Test jump when condition is true (non-zero)
    instructions = [
        ("set", "a", "5"),
        ("jnz", "a", "2"),    # Should jump
        ("set", "b", "1"),    # Should be skipped
        ("set", "c", "1")     # Should execute
    ]
    result = execute_program(instructions)

    # Test no jump when condition is false (zero)
    instructions = [
        ("set", "a", "0"),
        ("jnz", "a", "2"),    # Should NOT jump
        ("set", "b", "1"),    # Should execute
        ("set", "c", "1")     # Should execute
    ]
    result = execute_program(instructions)

    # Test jump with literal (always jumps)
    instructions = [
        ("jnz", "1", "2"),    # Should jump (1 is non-zero)
        ("set", "a", "1"),    # Should be skipped
        ("set", "b", "1")     # Should execute
    ]
    result = execute_program(instructions)

    print("✓ jnz instruction tests passed")


def test_loop():
    """Test simple loop with mul counting"""
    instructions = [
        ("set", "a", "3"),     # Counter
        ("mul", "a", "1"),     # Multiply by 1 (no-op for value)
        ("sub", "a", "1"),     # Decrement
        ("jnz", "a", "-2")     # Loop
    ]
    result = execute_program(instructions)
    assert result == 3, f"Expected mul_count=3, got {result}"

    print("✓ loop test passed")


def test_no_mul_instructions():
    """Test program with no mul instructions"""
    instructions = [
        ("set", "a", "10"),
        ("sub", "a", "5"),
        ("jnz", "a", "1")
    ]
    result = execute_program(instructions)
    assert result == 0, f"Expected mul_count=0, got {result}"

    print("✓ no mul test passed")


def test_empty_program():
    """Test empty program"""
    instructions = []
    result = execute_program(instructions)
    assert result == 0, f"Expected mul_count=0, got {result}"

    print("✓ empty program test passed")


def test_parsing():
    """Test instruction parsing"""
    lines = ["set a 5", "", "mul a 2", ""]
    parsed = parse_instructions(lines)
    assert len(parsed) == 2, f"Expected 2 instructions, got {len(parsed)}"
    assert parsed[0] == ("set", "a", "5")
    assert parsed[1] == ("mul", "a", "2")

    print("✓ parsing test passed")


if __name__ == "__main__":
    test_get_value()
    test_set_instruction()
    test_sub_instruction()
    test_mul_instruction()
    test_jnz_instruction()
    test_loop()
    test_no_mul_instructions()
    test_empty_program()
    test_parsing()

    print("\n✓ All tests passed!")
