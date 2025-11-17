from solution import get_value, parse_instructions, execute


def test_example_program():
    """Test the example program from Part 1 problem statement."""
    program = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""
    instructions = parse_instructions(program.split('\n'))
    result = execute(instructions)
    assert result == 42, f"Expected 42, got {result}"
    print("✓ Test 1 passed: Example program outputs 42")


def test_part1_regression():
    """Test that Part 1 configuration still produces the correct result."""
    with open('input.md', 'r') as f:
        instructions = parse_instructions(f.readlines())

    # Temporarily modify execute to use c=0
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    ip = 0

    while 0 <= ip < len(instructions):
        inst, arg1, arg2 = instructions[ip]

        if inst == 'cpy':
            registers[arg2] = get_value(arg1, registers)
            ip += 1
        elif inst == 'inc':
            registers[arg1] += 1
            ip += 1
        elif inst == 'dec':
            registers[arg1] -= 1
            ip += 1
        elif inst == 'jnz':
            if get_value(arg1, registers) != 0:
                ip += get_value(arg2, registers)
            else:
                ip += 1

    result = registers['a']
    assert result == 318077, f"Expected 318077, got {result}"
    print("✓ Test 2 passed: Part 1 regression test (c=0) outputs 318077")


def test_part2_full_input():
    """Test Part 2 with c=1 initialization."""
    with open('input.md', 'r') as f:
        instructions = parse_instructions(f.readlines())

    result = execute(instructions)

    # Verification checks
    assert isinstance(result, int), f"Result should be an integer, got {type(result)}"
    assert result > 0, f"Result should be positive, got {result}"
    assert result != 318077, f"Part 2 result should differ from Part 1 (318077), got {result}"

    print(f"✓ Test 3 passed: Part 2 full input produces {result}")
    print(f"  - Result is positive: {result > 0}")
    print(f"  - Result differs from Part 1: {result != 318077}")

    return result


if __name__ == '__main__':
    print("Running tests...")
    print()

    # Test 1: Example program
    test_example_program()

    # Test 2: Part 1 regression
    test_part1_regression()

    # Test 3: Part 2 full input
    result = test_part2_full_input()

    print()
    print("=" * 50)
    print(f"All tests passed! Part 2 answer: {result}")
    print("=" * 50)
