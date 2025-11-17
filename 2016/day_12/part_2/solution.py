def get_value(operand, registers):
    """Get the value of an operand (either a register or literal)."""
    try:
        return int(operand)
    except ValueError:
        return registers[operand]


def parse_instructions(lines):
    """Parse input lines into a list of instruction tuples."""
    instructions = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) == 2:
            instructions.append((parts[0], parts[1], None))
        elif len(parts) == 3:
            instructions.append((parts[0], parts[1], parts[2]))
    return instructions


def execute(instructions):
    """Execute the assembunny instructions and return the value in register a."""
    registers = {'a': 0, 'b': 0, 'c': 1, 'd': 0}  # Part 2: c initialized to 1
    ip = 0  # instruction pointer

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

    return registers['a']


def main():
    """Read input, execute instructions, and print result."""
    with open('input.md', 'r') as f:
        instructions = parse_instructions(f.readlines())

    result = execute(instructions)
    print(result)


if __name__ == '__main__':
    main()
