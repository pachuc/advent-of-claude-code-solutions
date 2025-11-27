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
    """Parse input file and extract samples and test program"""
    with open(filename) as f:
        lines = f.readlines()

    samples = []
    test_program = []
    i = 0

    # Parse samples until we hit two consecutive blank lines
    while i < len(lines):
        line = lines[i].strip()

        # Check for double blank line (end of samples section)
        if i + 1 < len(lines) and not line and not lines[i + 1].strip():
            # Skip past the double blank line
            i += 2
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

    # Parse test program (remaining lines)
    while i < len(lines):
        line = lines[i].strip()
        if line:
            instruction = parse_instruction(line)
            if instruction:
                test_program.append(instruction)
        i += 1

    return samples, test_program


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


def get_compatible_opcodes(before, instruction, after):
    """Get the set of opcode names that could produce the observed transformation"""
    # Extract A, B, C from instruction (ignore opcode number at index 0)
    _, A, B, C = instruction
    compatible = set()

    for opcode_name in ALL_OPCODES:
        result = execute_opcode(opcode_name, before, A, B, C)
        if result == after:
            compatible.add(opcode_name)

    return compatible


def build_opcode_possibilities(samples):
    """Build a mapping of opcode numbers to sets of possible opcode names"""
    # Initialize all opcodes as possible for all opcode numbers
    possibilities = {i: set(ALL_OPCODES) for i in range(16)}

    # For each sample, narrow down possibilities
    for before, instruction, after in samples:
        opcode_num = instruction[0]
        compatible = get_compatible_opcodes(before, instruction, after)
        # Intersect to narrow down possibilities
        possibilities[opcode_num] &= compatible

    return possibilities


def deduce_opcode_mapping(possibilities):
    """Deduce unique 1-to-1 mapping from opcode numbers to opcode names"""
    opcode_map = {}
    remaining = {k: v.copy() for k, v in possibilities.items()}

    # Iteratively resolve opcodes with unique possibilities
    while len(opcode_map) < 16:
        # Find an opcode number with exactly 1 possibility
        found = None
        for opcode_num, possible_names in remaining.items():
            if len(possible_names) == 1:
                found = opcode_num
                break

        if found is None:
            raise ValueError("Unable to uniquely determine opcode mapping")

        # Lock in the mapping
        locked_name = list(remaining[found])[0]
        opcode_map[found] = locked_name

        # Remove this opcode name from all other possibilities
        for opcode_num in remaining:
            remaining[opcode_num].discard(locked_name)

        # Remove the resolved opcode from remaining
        del remaining[found]

    return opcode_map


def execute_program(test_program, opcode_map):
    """Execute the test program and return the value in register 0"""
    registers = [0, 0, 0, 0]

    for instruction in test_program:
        opcode_num, A, B, C = instruction
        opcode_name = opcode_map[opcode_num]
        registers = execute_opcode(opcode_name, registers, A, B, C)

    return registers[0]


def solve(filename):
    """Solve Part 2: deduce opcode mappings and execute test program"""
    # Parse input
    samples, test_program = parse_input(filename)

    # Phase 1: Deduce opcode mappings
    possibilities = build_opcode_possibilities(samples)
    opcode_map = deduce_opcode_mapping(possibilities)

    # Phase 2: Execute test program
    result = execute_program(test_program, opcode_map)

    return result


if __name__ == "__main__":
    result = solve("input.md")
    print(result)
