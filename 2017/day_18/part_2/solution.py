from collections import defaultdict, deque


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


class Program:
    """Encapsulates the state of a single program instance."""

    def __init__(self, program_id):
        """Initialize a program with the given ID.

        Args:
            program_id: 0 or 1
        """
        self.program_id = program_id
        self.registers = defaultdict(int)
        self.registers['p'] = program_id  # p register is initialized to program ID
        self.pc = 0  # Program counter
        self.message_queue = deque()  # FIFO queue for incoming messages
        self.state = "running"  # "running", "blocked", or "terminated"
        self.send_count = 0  # Track number of sends (for program 1)

    def is_blocked(self):
        """Check if the program is blocked waiting for a message."""
        return self.state == "blocked"

    def is_terminated(self):
        """Check if the program has terminated."""
        return self.state == "terminated"

    def can_execute(self):
        """Check if the program can currently execute."""
        return self.state == "running"


def execute_until_blocked(current_program, other_program, instructions):
    """Execute one program until it blocks or terminates.

    Args:
        current_program: The Program instance to execute
        other_program: The other Program instance (for message passing)
        instructions: List of parsed instructions

    Returns:
        True if at least one instruction was executed, False otherwise
    """
    executed_count = 0
    max_iterations = 10000000  # Safety limit to prevent infinite loops

    while current_program.can_execute() and executed_count < max_iterations:
        # Check if pc is out of bounds
        if not (0 <= current_program.pc < len(instructions)):
            current_program.state = "terminated"
            break

        # Get current instruction
        instruction = instructions[current_program.pc]
        op = instruction[0]

        # Execute instruction
        if op == "snd":
            value = get_value(instruction[1], current_program.registers)
            other_program.message_queue.append(value)
            if current_program.program_id == 1:
                current_program.send_count += 1
            current_program.pc += 1

        elif op == "rcv":
            if len(current_program.message_queue) == 0:
                # Block and wait for a message
                current_program.state = "blocked"
                break  # Stop execution, don't increment pc
            else:
                # Receive message from queue
                value = current_program.message_queue.popleft()
                current_program.registers[instruction[1]] = value
                current_program.state = "running"
                current_program.pc += 1

        elif op == "set":
            current_program.registers[instruction[1]] = get_value(instruction[2], current_program.registers)
            current_program.pc += 1

        elif op == "add":
            current_program.registers[instruction[1]] += get_value(instruction[2], current_program.registers)
            current_program.pc += 1

        elif op == "mul":
            current_program.registers[instruction[1]] *= get_value(instruction[2], current_program.registers)
            current_program.pc += 1

        elif op == "mod":
            current_program.registers[instruction[1]] %= get_value(instruction[2], current_program.registers)
            current_program.pc += 1

        elif op == "jgz":
            if get_value(instruction[1], current_program.registers) > 0:
                current_program.pc += get_value(instruction[2], current_program.registers)
            else:
                current_program.pc += 1

        executed_count += 1

    return executed_count > 0


def is_deadlock(program0, program1):
    """Check if both programs are in deadlock.

    Deadlock occurs when:
    - Both programs are blocked on receive
    - Both queues are empty

    Args:
        program0: First Program instance
        program1: Second Program instance

    Returns:
        True if deadlocked, False otherwise
    """
    both_blocked = (program0.state == "blocked" and program1.state == "blocked")
    both_empty = (len(program0.message_queue) == 0 and len(program1.message_queue) == 0)
    return both_blocked and both_empty


def both_terminated(program0, program1):
    """Check if both programs have terminated naturally.

    Args:
        program0: First Program instance
        program1: Second Program instance

    Returns:
        True if both terminated, False otherwise
    """
    return program0.state == "terminated" and program1.state == "terminated"


def solve(input_file='input.md'):
    """Execute the dual-program Duet system and count program 1's sends.

    Args:
        input_file: Path to the input file (default: 'input.md')

    Returns:
        The number of times program 1 sent a value before deadlock/termination
    """
    # Parse instructions
    instructions = []
    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                instructions.append(line.split())

    # Create two programs
    program0 = Program(0)
    program1 = Program(1)

    # Execute until deadlock or both terminate
    while True:
        # Unblock programs that now have messages waiting
        if program0.state == "blocked" and len(program0.message_queue) > 0:
            program0.state = "running"
        if program1.state == "blocked" and len(program1.message_queue) > 0:
            program1.state = "running"

        # Execute program 0 until it blocks or terminates
        execute_until_blocked(program0, program1, instructions)

        # Execute program 1 until it blocks or terminates
        execute_until_blocked(program1, program0, instructions)

        # Check termination conditions
        if is_deadlock(program0, program1):
            break

        if both_terminated(program0, program1):
            break

    return program1.send_count


def solve_with_string(input_str):
    """Execute dual-program Duet from a string (for testing).

    Args:
        input_str: The program as a multi-line string

    Returns:
        The number of times program 1 sent a value
    """
    # Parse instructions from string
    instructions = []
    for line in input_str.strip().split('\n'):
        line = line.strip()
        if line:
            instructions.append(line.split())

    # Create two programs
    program0 = Program(0)
    program1 = Program(1)

    # Execute until deadlock or both terminate
    while True:
        # Unblock programs that now have messages waiting
        if program0.state == "blocked" and len(program0.message_queue) > 0:
            program0.state = "running"
        if program1.state == "blocked" and len(program1.message_queue) > 0:
            program1.state = "running"

        # Execute program 0 until it blocks or terminates
        execute_until_blocked(program0, program1, instructions)

        # Execute program 1 until it blocks or terminates
        execute_until_blocked(program1, program0, instructions)

        # Check termination conditions
        if is_deadlock(program0, program1):
            break

        if both_terminated(program0, program1):
            break

    return program1.send_count


def test_example():
    """Test the example from problem statement"""
    input_str = """snd 1
snd 2
snd p
rcv a
rcv b
rcv c
rcv d"""

    result = solve_with_string(input_str)
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Example test passed (result: 3)")


def test_simple_send_receive():
    """Test simple send and receive"""
    input_str = """snd 42
rcv a"""

    result = solve_with_string(input_str)
    assert result == 1, f"Expected 1, got {result}"
    print("✓ Simple send/receive test passed (result: 1)")


def test_p_register_initialization():
    """Test that p register is initialized correctly"""
    input_str = """snd p
snd p
rcv a
rcv b"""

    result = solve_with_string(input_str)
    assert result == 2, f"Expected 2, got {result}"
    print("✓ Register p initialization test passed (result: 2)")


def test_immediate_deadlock():
    """Test immediate deadlock with no sends"""
    input_str = """rcv a"""

    result = solve_with_string(input_str)
    assert result == 0, f"Expected 0, got {result}"
    print("✓ Immediate deadlock test passed (result: 0)")


def test_loop_with_sends():
    """Test loop that sends multiple values"""
    input_str = """set counter 3
snd counter
add counter -1
jgz counter -2
rcv x"""

    result = solve_with_string(input_str)
    assert result == 3, f"Expected 3, got {result}"
    print("✓ Loop with sends test passed (result: 3)")


def run_all_tests():
    """Run all test cases"""
    print("Running tests...\n")
    test_example()
    test_simple_send_receive()
    test_p_register_initialization()
    test_immediate_deadlock()
    test_loop_with_sends()
    print("\n" + "="*50)
    print("✓ All tests passed!")
    print("="*50)


if __name__ == "__main__":
    # Run test suite
    run_all_tests()

    # Run actual input
    print("\nRunning actual input:")
    result = solve()
    print(f"Result: {result}")
