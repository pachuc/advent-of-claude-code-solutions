#!/usr/bin/env python3
"""
Advent of Code 2018 - Day 19 Part 2
Instruction Pointer Simulation with Optimization

Key insight: The program computes the sum of all divisors of a target number N
stored in register 4. Part 2 initializes register 0 to 1, which causes the
initialization to build a much larger target number, making direct simulation
impractical (would require O(N^2) operations).

Strategy:
1. Run initialization to extract target number N from register 4
2. Compute sum of divisors efficiently using O(sqrt(N)) algorithm
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


def sum_of_divisors(n):
    """
    Compute sum of all divisors of n (including 1 and n)
    Time complexity: O(sqrt(n))

    Algorithm:
    - Iterate from 1 to sqrt(n)
    - For each i that divides n, add both i and n/i to the sum
    - Handle perfect squares carefully to avoid double-counting
    """
    if n <= 0:
        return 0

    divisor_sum = 0
    i = 1

    # Iterate up to sqrt(n)
    while i * i <= n:
        if n % i == 0:
            divisor_sum += i  # Add the smaller divisor
            # Add the paired divisor if it's different (avoid double-count for perfect squares)
            if i != n // i:
                divisor_sum += n // i
        i += 1

    return divisor_sum


def extract_target_number(ip_register, instructions, initial_r0):
    """
    Run initialization until register 4 stabilizes, then return its value.

    Args:
        ip_register: Register bound to instruction pointer
        instructions: List of instruction tuples
        initial_r0: Initial value for register 0

    Returns:
        (target_number, iterations_used)
    """
    registers = [initial_r0, 0, 0, 0, 0, 0]
    ip = 0
    opcode_functions = create_opcode_functions()

    # Track r4 stability
    r4_stable_count = 0
    last_r4 = 0
    max_iterations = 1000  # Generous limit

    for iteration in range(max_iterations):
        # Check halt condition
        if ip < 0 or ip >= len(instructions):
            raise RuntimeError(f"Program halted during initialization at IP={ip}")

        # Execute one instruction
        registers[ip_register] = ip
        opcode, A, B, C = instructions[ip]
        opcode_functions[opcode](registers, A, B, C)
        ip = registers[ip_register] + 1

        # Check if r4 changed
        if registers[4] != last_r4:
            last_r4 = registers[4]
            r4_stable_count = 0
        else:
            r4_stable_count += 1

        # If r4 stable for 10 iterations and positive, we're done
        if r4_stable_count >= 10 and registers[4] > 0:
            return registers[4], iteration

    raise RuntimeError(f"Register 4 did not stabilize within {max_iterations} iterations")


def verify_algorithm_with_part1(ip_register, instructions):
    """
    Verify our algorithm interpretation using Part 1's known answer.
    Returns True if verification passes, False otherwise.
    """
    # Extract target for Part 1 (r0=0)
    target_part1, iterations = extract_target_number(ip_register, instructions, initial_r0=0)

    print(f"Part 1 verification: target={target_part1} (after {iterations} iterations)")

    # Compute sum of divisors
    result = sum_of_divisors(target_part1)

    # Should equal 1056 (Part 1's known answer)
    if result == 1056:
        print(f"Algorithm verified: sum_of_divisors({target_part1}) = {result}")
        return True
    else:
        print(f"Algorithm verification FAILED: sum_of_divisors({target_part1}) = {result}, expected 1056")
        return False


def main():
    """Main entry point"""
    # Read input from input.md
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input
    ip_register, instructions = parse_input(input_text)

    # CRITICAL: Verify algorithm using Part 1 first
    print("="*60)
    print("Verifying algorithm with Part 1...")
    print("="*60)
    if not verify_algorithm_with_part1(ip_register, instructions):
        raise RuntimeError("Algorithm verification failed - aborting")

    print()
    print("="*60)
    print("Solving Part 2...")
    print("="*60)

    # Extract target number for Part 2 (r0=1)
    target_number, iterations = extract_target_number(
        ip_register, instructions, initial_r0=1
    )

    print(f"Extracted target: {target_number} (after {iterations} iterations)")

    # Compute answer efficiently
    result = sum_of_divisors(target_number)

    print(f"Sum of divisors of {target_number} = {result}")
    print()
    print("="*60)
    print(f"Final Answer: {result}")
    print("="*60)


if __name__ == '__main__':
    main()
