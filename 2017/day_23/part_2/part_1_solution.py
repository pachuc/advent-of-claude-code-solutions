def parse_instructions(lines):
    """Parse input lines into instruction tuples"""
    instructions = []
    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue
        parts = line.split()
        # All instructions have format: op arg1 arg2
        instructions.append((parts[0], parts[1], parts[2]))
    return instructions


def get_value(operand, registers):
    """Resolve operand to actual value"""
    if operand.lstrip('-').isdigit():
        return int(operand)
    else:
        return registers[operand]


def execute_program(instructions):
    """Main interpreter loop"""
    # Initialize state
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
    ip = 0
    mul_count = 0

    # Loop until ip out of bounds
    while 0 <= ip < len(instructions):
        op, arg1, arg2 = instructions[ip]

        # jnz is special - it handles ip itself
        if op == "jnz":
            x_val = get_value(arg1, registers)
            if x_val != 0:
                offset = get_value(arg2, registers)
                ip += offset  # Jump by offset
            else:
                ip += 1  # No jump, proceed normally
        else:
            # All other instructions: execute then increment ip
            if op == "set":
                registers[arg1] = get_value(arg2, registers)
            elif op == "sub":
                registers[arg1] -= get_value(arg2, registers)
            elif op == "mul":
                registers[arg1] *= get_value(arg2, registers)
                mul_count += 1  # Track mul invocations

            ip += 1  # Common increment for non-jump instructions

    return mul_count


def main():
    """Entry point"""
    # Read input file
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse instructions
    instructions = parse_instructions(lines)

    # Execute program
    result = execute_program(instructions)

    # Print result (just the number)
    print(result)


if __name__ == "__main__":
    main()
