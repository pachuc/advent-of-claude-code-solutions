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


def execute(instructions, c_initial=1):
    """Execute the assembunny instructions and return the value in register a."""
    registers = {'a': 0, 'b': 0, 'c': c_initial, 'd': 0}
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


# Test Part 1 (c=0)
with open('input.md', 'r') as f:
    instructions = parse_instructions(f.readlines())

part1_result = execute(instructions, c_initial=0)
print(f"Part 1 (c=0): {part1_result}")
print(f"Expected: 318077")
print(f"Match: {part1_result == 318077}")

# Test Part 2 (c=1)
part2_result = execute(instructions, c_initial=1)
print(f"\nPart 2 (c=1): {part2_result}")
print(f"Expected: 9227731")
print(f"Match: {part2_result == 9227731}")
