#!/usr/bin/env python3
"""
Advent of Code 2018 - Day 19 Part 1
Instruction Pointer Simulation
"""

def create_opcode_functions():
    """Create dictionary mapping opcode names to their implementation functions"""

    def addr(regs, A, B, C):
        """Add register: regs[C] = regs[A] + regs[B]"""
        regs[C] = regs[A] + regs[B]

    def addi(regs, A, B, C):
        """Add immediate: regs[C] = regs[A] + B"""
        regs[C] = regs[A] + B

    def mulr(regs, A, B, C):
        """Multiply register: regs[C] = regs[A] * regs[B]"""
        regs[C] = regs[A] * regs[B]

    def muli(regs, A, B, C):
        """Multiply immediate: regs[C] = regs[A] * B"""
        regs[C] = regs[A] * B

    def banr(regs, A, B, C):
        """Bitwise AND register: regs[C] = regs[A] & regs[B]"""
        regs[C] = regs[A] & regs[B]

    def bani(regs, A, B, C):
        """Bitwise AND immediate: regs[C] = regs[A] & B"""
        regs[C] = regs[A] & B

    def borr(regs, A, B, C):
        """Bitwise OR register: regs[C] = regs[A] | regs[B]"""
        regs[C] = regs[A] | regs[B]

    def bori(regs, A, B, C):
        """Bitwise OR immediate: regs[C] = regs[A] | B"""
        regs[C] = regs[A] | B

    def setr(regs, A, B, C):
        """Set register: regs[C] = regs[A]"""
        regs[C] = regs[A]

    def seti(regs, A, B, C):
        """Set immediate: regs[C] = A"""
        regs[C] = A

    def gtir(regs, A, B, C):
        """Greater-than immediate/register: regs[C] = 1 if A > regs[B] else 0"""
        regs[C] = 1 if A > regs[B] else 0

    def gtri(regs, A, B, C):
        """Greater-than register/immediate: regs[C] = 1 if regs[A] > B else 0"""
        regs[C] = 1 if regs[A] > B else 0

    def gtrr(regs, A, B, C):
        """Greater-than register/register: regs[C] = 1 if regs[A] > regs[B] else 0"""
        regs[C] = 1 if regs[A] > regs[B] else 0

    def eqir(regs, A, B, C):
        """Equal immediate/register: regs[C] = 1 if A == regs[B] else 0"""
        regs[C] = 1 if A == regs[B] else 0

    def eqri(regs, A, B, C):
        """Equal register/immediate: regs[C] = 1 if regs[A] == B else 0"""
        regs[C] = 1 if regs[A] == B else 0

    def eqrr(regs, A, B, C):
        """Equal register/register: regs[C] = 1 if regs[A] == regs[B] else 0"""
        regs[C] = 1 if regs[A] == regs[B] else 0

    return {
        'addr': addr, 'addi': addi,
        'mulr': mulr, 'muli': muli,
        'banr': banr, 'bani': bani,
        'borr': borr, 'bori': bori,
        'setr': setr, 'seti': seti,
        'gtir': gtir, 'gtri': gtri, 'gtrr': gtrr,
        'eqir': eqir, 'eqri': eqri, 'eqrr': eqrr
    }


def parse_input(input_text):
    """
    Parse input and return ip_register and instructions list

    Returns:
        (ip_register, instructions)
        ip_register: int - register number bound to IP
        instructions: list of tuples (opcode_str, A, B, C)
    """
    lines = input_text.strip().split('\n')

    # Parse #ip declaration
    ip_line = lines[0]
    if not ip_line.startswith('#ip '):
        raise ValueError(f"Expected '#ip N' declaration, got: {ip_line}")

    ip_register = int(ip_line.split()[1])
    if not (0 <= ip_register <= 5):
        raise ValueError(f"IP register must be 0-5, got: {ip_register}")

    # Parse instructions
    instructions = []
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) != 4:
            raise ValueError(f"Invalid instruction format: {line}")

        opcode = parts[0]
        A, B, C = int(parts[1]), int(parts[2]), int(parts[3])
        instructions.append((opcode, A, B, C))

    return ip_register, instructions


def execute_program(ip_register, instructions, debug=False):
    """
    Execute the program and return final value in register 0

    Args:
        ip_register: Register number bound to instruction pointer
        instructions: List of instruction tuples (opcode, A, B, C)
        debug: If True, print execution trace

    Returns:
        Final value in register 0
    """
    # Initialize state
    registers = [0, 0, 0, 0, 0, 0]
    ip = 0
    opcode_functions = create_opcode_functions()

    # Safety limit to detect infinite loops
    max_iterations = 10_000_000
    iteration_count = 0

    while True:
        # Check halt condition BEFORE execution
        if ip < 0 or ip >= len(instructions):
            break

        # Safety check for infinite loops
        iteration_count += 1
        if iteration_count > max_iterations:
            raise RuntimeError(f"Exceeded {max_iterations} iterations - possible infinite loop")

        # Write IP to bound register
        registers[ip_register] = ip

        # Fetch instruction
        opcode, A, B, C = instructions[ip]

        if debug:
            print(f"IP={ip}: {opcode} {A} {B} {C} | Before: {registers}")

        # Execute instruction
        if opcode not in opcode_functions:
            raise ValueError(f"Unknown opcode: {opcode}")
        opcode_functions[opcode](registers, A, B, C)

        if debug:
            print(f"        After: {registers}")

        # Read IP from bound register
        ip = registers[ip_register]

        # Increment IP
        ip += 1

    if debug:
        print(f"Program halted at IP={ip}, iterations={iteration_count}")
        print(f"Final registers: {registers}")

    return registers[0]


def main():
    """Main entry point"""
    # Read input from input.md
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input
    ip_register, instructions = parse_input(input_text)

    # Execute program
    result = execute_program(ip_register, instructions, debug=False)

    # Print result
    print(result)


if __name__ == '__main__':
    main()
