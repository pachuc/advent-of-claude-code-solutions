import re

# List of all 16 opcodes
ALL_OPCODES = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani',
               'borr', 'bori', 'setr', 'seti', 'gtir', 'gtri',
               'gtrr', 'eqir', 'eqri', 'eqrr']


def parse_registers(line):
    """Parse a line like 'Before: [3, 2, 1, 1]' or 'After:  [3, 2, 2, 1]'"""
    match = re.search(r'\[(\d+), (\d+), (\d+), (\d+)\]', line)
    if match:
        return [int(match.group(i)) for i in range(1, 5)]
    return None


def parse_instruction(line):
    """Parse a line like '9 2 1 2'"""
    parts = line.strip().split()
    if len(parts) == 4:
        return [int(p) for p in parts]
    return None


def parse_input(filename):
    """Parse input file and extract all samples"""
    with open(filename) as f:
        lines = f.readlines()

    samples = []
    i = 0

    # Parse until we hit two consecutive blank lines
    while i < len(lines):
        line = lines[i].strip()

        # Check for double blank line (end of samples section)
        if i + 1 < len(lines) and not line and not lines[i + 1].strip():
            break

        # Parse a sample (3 lines + 1 blank)
        if line.startswith('Before:'):
            before = parse_registers(lines[i])
            instruction = parse_instruction(lines[i + 1])
            after = parse_registers(lines[i + 2])
            if before and instruction and after:
                samples.append((before, instruction, after))
            i += 4  # Skip to next sample (3 lines + blank)
        else:
            i += 1

    return samples


def execute_opcode(opcode_name, registers, A, B, C):
    """Execute a specific opcode and return new register state"""
    result = registers.copy()

    # Addition operations
    if opcode_name == 'addr':
        result[C] = registers[A] + registers[B]
    elif opcode_name == 'addi':
        result[C] = registers[A] + B

    # Multiplication operations
    elif opcode_name == 'mulr':
        result[C] = registers[A] * registers[B]
    elif opcode_name == 'muli':
        result[C] = registers[A] * B

    # Bitwise AND operations
    elif opcode_name == 'banr':
        result[C] = registers[A] & registers[B]
    elif opcode_name == 'bani':
        result[C] = registers[A] & B

    # Bitwise OR operations
    elif opcode_name == 'borr':
        result[C] = registers[A] | registers[B]
    elif opcode_name == 'bori':
        result[C] = registers[A] | B

    # Assignment operations
    elif opcode_name == 'setr':
        result[C] = registers[A]
    elif opcode_name == 'seti':
        result[C] = A

    # Greater-than testing
    elif opcode_name == 'gtir':
        result[C] = 1 if A > registers[B] else 0
    elif opcode_name == 'gtri':
        result[C] = 1 if registers[A] > B else 0
    elif opcode_name == 'gtrr':
        result[C] = 1 if registers[A] > registers[B] else 0

    # Equality testing
    elif opcode_name == 'eqir':
        result[C] = 1 if A == registers[B] else 0
    elif opcode_name == 'eqri':
        result[C] = 1 if registers[A] == B else 0
    elif opcode_name == 'eqrr':
        result[C] = 1 if registers[A] == registers[B] else 0

    return result


def count_matching_opcodes(before, instruction, after):
    """Count how many opcodes could produce the observed transformation"""
    _, A, B, C = instruction
    matches = 0

    for opcode_name in ALL_OPCODES:
        result = execute_opcode(opcode_name, before, A, B, C)
        if result == after:
            matches += 1

    return matches


def solve(filename):
    """Solve the problem: count samples that behave like 3+ opcodes"""
    samples = parse_input(filename)
    count = 0

    for before, instruction, after in samples:
        matching_opcodes = count_matching_opcodes(before, instruction, after)
        if matching_opcodes >= 3:
            count += 1

    return count


if __name__ == "__main__":
    result = solve("input.md")
    print(result)
