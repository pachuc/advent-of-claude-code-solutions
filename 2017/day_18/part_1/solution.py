from collections import defaultdict


def get_value(operand, registers):
    """Resolve an operand to its integer value.

    Args:
        operand: Either a register name (e.g., 'a') or a literal value (e.g., '42', '-5')
        registers: Dictionary of register values

    Returns:
        The integer value of the operand
    """
    try:
        return int(operand)
    except ValueError:
        return registers[operand]


def solve(input_file='input.md'):
    """Execute the Duet assembly program and return the recovered frequency.

    Args:
        input_file: Path to the input file (default: 'input.md')

    Returns:
        The frequency of the last sound played when rcv executes with non-zero value
    """
    # Step 1: Parse input
    instructions = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                instructions.append(line.split())

    # Step 2: Initialize state
    registers = defaultdict(int)
    last_sound = None
    pc = 0  # Program counter

    # Step 3: Execute
    while 0 <= pc < len(instructions):
        instruction = instructions[pc]
        op = instruction[0]

        if op == "snd":
            last_sound = get_value(instruction[1], registers)
            pc += 1
        elif op == "set":
            registers[instruction[1]] = get_value(instruction[2], registers)
            pc += 1
        elif op == "add":
            registers[instruction[1]] += get_value(instruction[2], registers)
            pc += 1
        elif op == "mul":
            registers[instruction[1]] *= get_value(instruction[2], registers)
            pc += 1
        elif op == "mod":
            registers[instruction[1]] %= get_value(instruction[2], registers)
            pc += 1
        elif op == "rcv":
            if get_value(instruction[1], registers) != 0:
                return last_sound
            pc += 1
        elif op == "jgz":
            if get_value(instruction[1], registers) > 0:
                pc += get_value(instruction[2], registers)
            else:
                pc += 1

    # Program terminated without rcv returning a value
    return None


def solve_with_string(input_str):
    """Execute Duet program from a string (for testing).

    Args:
        input_str: The program as a multi-line string

    Returns:
        The recovered frequency value
    """
    # Parse instructions from string
    instructions = []
    for line in input_str.strip().split('\n'):
        line = line.strip()
        if line:
            instructions.append(line.split())

    # Initialize state
    registers = defaultdict(int)
    last_sound = None
    pc = 0

    # Execute
    while 0 <= pc < len(instructions):
        instruction = instructions[pc]
        op = instruction[0]

        if op == "snd":
            last_sound = get_value(instruction[1], registers)
            pc += 1
        elif op == "set":
            registers[instruction[1]] = get_value(instruction[2], registers)
            pc += 1
        elif op == "add":
            registers[instruction[1]] += get_value(instruction[2], registers)
            pc += 1
        elif op == "mul":
            registers[instruction[1]] *= get_value(instruction[2], registers)
            pc += 1
        elif op == "mod":
            registers[instruction[1]] %= get_value(instruction[2], registers)
            pc += 1
        elif op == "rcv":
            if get_value(instruction[1], registers) != 0:
                return last_sound
            pc += 1
        elif op == "jgz":
            if get_value(instruction[1], registers) > 0:
                pc += get_value(instruction[2], registers)
            else:
                pc += 1

    return None


def test_example():
    """Test the example from problem statement"""
    input_str = """set a 1
add a 2
mul a a
mod a 5
snd a
set a 0
rcv a
jgz a -1
set a 1
jgz a -2"""

    result = solve_with_string(input_str)
    assert result == 4, f"Expected 4, got {result}"
    print("✓ Example test passed")


def test_simple():
    """Test simple snd/rcv"""
    input_str = """snd 42
set a 1
rcv a"""

    result = solve_with_string(input_str)
    assert result == 42, f"Expected 42, got {result}"
    print("✓ Simple test passed")


def test_multiple_sounds():
    """Test that last sound is recovered"""
    input_str = """snd 10
snd 20
snd 30
set a 1
rcv a"""

    result = solve_with_string(input_str)
    assert result == 30, f"Expected 30, got {result}"
    print("✓ Multiple sounds test passed")


def test_negative_numbers():
    """Test negative values"""
    input_str = """set a -5
add a -3
mul a 2
snd a
set b 1
rcv b"""

    result = solve_with_string(input_str)
    assert result == -16, f"Expected -16, got {result}"
    print("✓ Negative numbers test passed")


def test_negative_literal_snd():
    """Test snd with negative literal"""
    input_str = """snd -42
set a 1
rcv a"""

    result = solve_with_string(input_str)
    assert result == -42, f"Expected -42, got {result}"
    print("✓ Negative literal snd test passed")


def test_register_jump_offset():
    """Test jgz with register offset"""
    input_str = """snd 100
set offset 4
set a 1
jgz a offset
snd 200
snd 300
snd 400
set b 1
rcv b"""

    result = solve_with_string(input_str)
    assert result == 100, f"Expected 100, got {result}"
    print("✓ Register jump offset test passed")


def test_uninitialized_register():
    """Test that uninitialized registers start at 0"""
    input_str = """add x 10
snd x
set y 1
rcv y"""

    result = solve_with_string(input_str)
    assert result == 10, f"Expected 10, got {result}"
    print("✓ Uninitialized register test passed")


def run_all_tests():
    """Run all test cases"""
    print("Running tests...\n")
    test_example()
    test_simple()
    test_multiple_sounds()
    test_negative_numbers()
    test_negative_literal_snd()
    test_register_jump_offset()
    test_uninitialized_register()
    print("\n" + "="*50)
    print("✓ All tests passed!")
    print("="*50)


if __name__ == "__main__":
    # Run test suite
    run_all_tests()

    # Run actual input
    print("\nRunning actual input:")
    result = solve()
    if result is not None:
        print(f"Result: {result}")
    else:
        print("ERROR: No result obtained")
