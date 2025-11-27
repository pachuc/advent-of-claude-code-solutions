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


def find_halting_value(ip_register, instructions):
    """
    Simulate program execution and find the value in register 5
    when instruction 29 is first reached
    """
    registers = [0, 0, 0, 0, 0, 0]
    ip = 0
    instruction_count = 0

    while 0 <= ip < len(instructions):
        # Check if we're at instruction 29 (the eqrr 5 0 3)
        if ip == 29:
            print(f"First reached instruction 29 after {instruction_count} instructions")
            print(f"Register 5 value: {registers[5]}")
            return registers[5]

        # Write IP to bound register
        registers[ip_register] = ip

        # Execute instruction at IP
        opcode, a, b, c = instructions[ip]
        execute_instruction(opcode, a, b, c, registers)

        # Read IP from bound register
        ip = registers[ip_register]

        # Increment IP
        ip += 1
        instruction_count += 1

    return None


def verify_halting(ip_register, instructions, r0_value):
    """
    Verify that setting register 0 to r0_value causes the program to halt quickly
    """
    registers = [r0_value, 0, 0, 0, 0, 0]
    ip = 0
    instruction_count = 0

    while 0 <= ip < len(instructions):
        # Write IP to bound register
        registers[ip_register] = ip

        # Execute instruction at IP
        opcode, a, b, c = instructions[ip]
        execute_instruction(opcode, a, b, c, registers)

        # Read IP from bound register
        ip = registers[ip_register]

        # Increment IP
        ip += 1
        instruction_count += 1

        # Safety check - if we exceed reasonable count, something's wrong
        if instruction_count > 1000000:
            print("Warning: Exceeded 1 million instructions in verification")
            return False

    print(f"Verification: Program halted after {instruction_count} instructions")
    return True


def main():
    # Parse input
    ip_register, instructions = parse_input('input.md')
    print(f"Parsed {len(instructions)} instructions with IP bound to register {ip_register}")

    # Find the halting value
    result = find_halting_value(ip_register, instructions)

    if result is not None:
        print(f"\nAnswer: {result}")

        # Verify the solution
        print("\nVerifying solution...")
        if verify_halting(ip_register, instructions, result):
            print("Verification successful!")
    else:
        print("Failed to find halting value")


if __name__ == "__main__":
    main()
