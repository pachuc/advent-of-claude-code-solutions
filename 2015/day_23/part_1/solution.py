def read_input(filename):
    """Read instruction lines from file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]


def parse_instruction(line):
    """Parse a single instruction line into structured format.

    Returns:
        tuple: (operation, register_or_None, offset_or_None)
    """
    parts = line.replace(',', '').split()
    op = parts[0]

    if op in ['hlf', 'tpl', 'inc']:
        return (op, parts[1], None)
    elif op == 'jmp':
        return (op, None, int(parts[1]))
    elif op in ['jie', 'jio']:
        return (op, parts[1], int(parts[2]))


def execute_instruction(instruction, ip, registers):
    """Execute one instruction and return new instruction pointer.

    Args:
        instruction: Parsed instruction tuple (op, reg, offset)
        ip: Current instruction pointer
        registers: Dictionary of register values

    Returns:
        int: New instruction pointer value
    """
    op, reg, offset = instruction

    if op == 'hlf':
        registers[reg] //= 2
        return ip + 1
    elif op == 'tpl':
        registers[reg] *= 3
        return ip + 1
    elif op == 'inc':
        registers[reg] += 1
        return ip + 1
    elif op == 'jmp':
        return ip + offset
    elif op == 'jie':
        if registers[reg] % 2 == 0:
            return ip + offset
        return ip + 1
    elif op == 'jio':
        if registers[reg] == 1:
            return ip + offset
        return ip + 1


def simulate(instruction_strings):
    """Run the simulation and return final register values.

    Args:
        instruction_strings: List of instruction strings

    Returns:
        dict: Final register values {'a': value, 'b': value}
    """
    # Pre-parse all instructions once
    instructions = [parse_instruction(line) for line in instruction_strings]
    registers = {'a': 0, 'b': 0}
    ip = 0

    # Safety check for infinite loops
    MAX_ITERATIONS = 1_000_000
    iteration_count = 0

    while 0 <= ip < len(instructions):
        if iteration_count > MAX_ITERATIONS:
            raise RuntimeError(f"Possible infinite loop detected: exceeded {MAX_ITERATIONS} iterations")
        iteration_count += 1

        ip = execute_instruction(instructions[ip], ip, registers)

    return registers


def main():
    """Main entry point."""
    instructions = read_input('input.md')
    registers = simulate(instructions)
    print(registers['b'])


if __name__ == '__main__':
    main()
