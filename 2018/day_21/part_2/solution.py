def parse_input(filename):
    """Parse the instruction file and return ip_register and instructions list"""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    # Parse IP register binding
    ip_line = lines[0]
    ip_register = int(ip_line.split()[1])

    # Parse instructions
    instructions = []
    for line in lines[1:]:
        parts = line.split()
        opcode = parts[0]
        a, b, c = int(parts[1]), int(parts[2]), int(parts[3])
        instructions.append((opcode, a, b, c))

    return ip_register, instructions


def execute_instruction(opcode, a, b, c, registers):
    """Execute a single instruction on the registers"""

    # Addition
    if opcode == 'addr':
        registers[c] = registers[a] + registers[b]
    elif opcode == 'addi':
        registers[c] = registers[a] + b

    # Multiplication
    elif opcode == 'mulr':
        registers[c] = registers[a] * registers[b]
    elif opcode == 'muli':
        registers[c] = registers[a] * b

    # Bitwise AND
    elif opcode == 'banr':
        registers[c] = registers[a] & registers[b]
    elif opcode == 'bani':
        registers[c] = registers[a] & b

    # Bitwise OR
    elif opcode == 'borr':
        registers[c] = registers[a] | registers[b]
    elif opcode == 'bori':
        registers[c] = registers[a] | b

    # Assignment
    elif opcode == 'setr':
        registers[c] = registers[a]
    elif opcode == 'seti':
        registers[c] = a

    # Greater-than
    elif opcode == 'gtir':
        registers[c] = 1 if a > registers[b] else 0
    elif opcode == 'gtri':
        registers[c] = 1 if registers[a] > b else 0
    elif opcode == 'gtrr':
        registers[c] = 1 if registers[a] > registers[b] else 0

    # Equality
    elif opcode == 'eqir':
        registers[c] = 1 if a == registers[b] else 0
    elif opcode == 'eqri':
        registers[c] = 1 if registers[a] == b else 0
    elif opcode == 'eqrr':
        registers[c] = 1 if registers[a] == registers[b] else 0


def find_last_halting_value(ip_register, instructions):
    """
    Simulate program execution and track all unique values in register 5
    when instruction 29 is reached. Detect when a value repeats (cycle)
    and return the last unique value before the cycle.

    Returns: (last_unique_value, first_value, sequence_length)
    """
    registers = [0, 0, 0, 0, 0, 0]
    ip = 0
    instruction_count = 0

    # Track unique values in register 5 at instruction 29
    seen_values = set()
    value_sequence = []

    while 0 <= ip < len(instructions):
        # Check if we're at instruction 29 (the eqrr 5 0 3)
        if ip == 29:
            current_value = registers[5]

            if current_value in seen_values:
                # We've found a cycle - this value has appeared before
                # The last unique value (before this repeat) is our answer
                if len(value_sequence) == 0:
                    # Edge case: immediate repeat (shouldn't happen)
                    return (None, None, 0)

                print(f"\nCycle detected at instruction {instruction_count}")
                print(f"Repeated value: {current_value}")
                print(f"Total unique values in sequence: {len(value_sequence)}")

                return (value_sequence[-1], value_sequence[0], len(value_sequence))
            else:
                # New unique value - add to tracking
                seen_values.add(current_value)
                value_sequence.append(current_value)

                # Progress indicator for first few values
                if len(value_sequence) <= 5:
                    print(f"Value #{len(value_sequence)}: {current_value}")

        # Standard execution steps
        registers[ip_register] = ip
        opcode, a, b, c = instructions[ip]
        execute_instruction(opcode, a, b, c, registers)
        ip = registers[ip_register]
        ip += 1
        instruction_count += 1

        # Progress indicator for long-running simulations
        if instruction_count % 10_000_000 == 0:
            print(f"Progress: {instruction_count:,} instructions executed, {len(value_sequence)} unique values found")

    # If we exit the loop without finding a cycle, return None
    return (None, None, 0)


def main():
    # Parse input
    ip_register, instructions = parse_input('input.md')
    print(f"Parsed {len(instructions)} instructions with IP bound to register {ip_register}")

    # Find the last halting value
    print("\nFinding cycle in register 5 values...")
    print("(Tracking values at instruction 29 until a repeat is detected)")

    result, first_value, sequence_length = find_last_halting_value(ip_register, instructions)

    if result is not None:
        print(f"\n{'='*60}")
        print("VALIDATION CHECKS:")
        print(f"{'='*60}")

        # Validation: First value should match Part 1 answer
        PART_1_ANSWER = 15615244
        if first_value == PART_1_ANSWER:
            print(f"✓ First value matches Part 1 answer: {PART_1_ANSWER}")
        else:
            print(f"✗ WARNING: First value {first_value} doesn't match Part 1 answer {PART_1_ANSWER}")

        # Validation: Answer should differ from Part 1
        if result != PART_1_ANSWER:
            print(f"✓ Part 2 answer differs from Part 1 answer")
        else:
            print(f"✗ WARNING: Part 2 answer is the same as Part 1 (sequence may have only 1 value)")

        # Validation: Multiple unique values
        if sequence_length > 1:
            print(f"✓ Found multiple unique values: {sequence_length}")
        else:
            print(f"✗ WARNING: Only 1 unique value found")

        print(f"\n{'='*60}")
        print(f"ANSWER: {result}")
        print(f"{'='*60}")
    else:
        print("Failed to find halting value")


if __name__ == "__main__":
    main()
