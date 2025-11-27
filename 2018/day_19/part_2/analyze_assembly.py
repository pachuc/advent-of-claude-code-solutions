#!/usr/bin/env python3
"""
Analyze the assembly code to understand what it computes
"""

import sys
sys.path.append('.')
from part_1_solution import parse_input, create_opcode_functions

def trace_execution(ip_register, instructions, initial_r0=0, max_iterations=100):
    """
    Trace execution and show register states
    """
    registers = [initial_r0, 0, 0, 0, 0, 0]
    ip = 0
    opcode_functions = create_opcode_functions()

    iteration = 0

    print(f"Starting with r0={initial_r0}")
    print(f"IP bound to register {ip_register}")
    print("-" * 80)

    while iteration < max_iterations:
        if ip < 0 or ip >= len(instructions):
            print(f"\nProgram halted at IP={ip}")
            print(f"Final registers: {registers}")
            return registers, iteration, True

        # Write IP to bound register
        registers[ip_register] = ip

        # Fetch instruction
        opcode, A, B, C = instructions[ip]

        print(f"IP={ip:2d}: {opcode} {A} {B} {C} | Before: {registers} | ", end='')

        # Execute instruction
        opcode_functions[opcode](registers, A, B, C)

        print(f"After: {registers}")

        # Read IP from bound register
        ip = registers[ip_register]

        # Increment IP
        ip += 1

        iteration += 1

    print(f"\nReached iteration limit ({max_iterations})")
    print(f"Current IP: {ip}, Registers: {registers}")
    return registers, iteration, False

def analyze_register4_initialization(ip_register, instructions, initial_r0=0):
    """
    Run until register 4 stabilizes, then return its value
    """
    registers = [initial_r0, 0, 0, 0, 0, 0]
    ip = 0
    opcode_functions = create_opcode_functions()

    # Track when r4 last changed
    r4_stable_count = 0
    last_r4 = 0

    for iteration in range(10000):
        if ip < 0 or ip >= len(instructions):
            print(f"Halted at IP={ip} after {iteration} iterations")
            return registers[4], registers, iteration

        # Write IP to bound register
        registers[ip_register] = ip

        # Fetch and execute instruction
        opcode, A, B, C = instructions[ip]
        opcode_functions[opcode](registers, A, B, C)

        # Check if r4 changed
        if registers[4] != last_r4:
            last_r4 = registers[4]
            r4_stable_count = 0
            print(f"Iteration {iteration:4d}, IP={ip:2d}: r4 changed to {registers[4]}, regs={registers}")
        else:
            r4_stable_count += 1
            # If r4 hasn't changed for 10 iterations and we're in a loop, it's probably stable
            if r4_stable_count == 10 and registers[4] > 0:
                print(f"\nRegister 4 appears stable at: {registers[4]}")
                print(f"Current IP: {ip}, Iteration: {iteration}")
                print(f"Registers: {registers}")
                return registers[4], registers, iteration

        # Read IP from bound register
        ip = registers[ip_register]

        # Increment IP
        ip += 1

    print(f"Reached max iterations with r4={registers[4]}")
    return registers[4], registers, 10000

def main():
    with open('input.md', 'r') as f:
        input_text = f.read()

    ip_register, instructions = parse_input(input_text)

    print("=" * 80)
    print("PART 1 ANALYSIS (r0=0)")
    print("=" * 80)
    target_r4_part1, regs1, iter1 = analyze_register4_initialization(ip_register, instructions, initial_r0=0)

    print("\n" + "=" * 80)
    print("PART 2 ANALYSIS (r0=1)")
    print("=" * 80)
    target_r4_part2, regs2, iter2 = analyze_register4_initialization(ip_register, instructions, initial_r0=1)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Part 1: r4 = {target_r4_part1}")
    print(f"Part 2: r4 = {target_r4_part2}")

    # Now compute sum of divisors for Part 1's target and see if it equals 1056
    def sum_of_divisors(n):
        if n <= 0:
            return 0
        total = 0
        i = 1
        while i * i <= n:
            if n % i == 0:
                total += i
                if i != n // i:
                    total += n // i
            i += 1
        return total

    sum_part1 = sum_of_divisors(target_r4_part1)
    print(f"\nSum of divisors of {target_r4_part1} = {sum_part1}")
    print(f"Expected Part 1 answer: 1056")
    print(f"Algorithm verification: {'PASSED' if sum_part1 == 1056 else 'FAILED'}")

    if sum_part1 == 1056:
        print(f"\n*** Algorithm confirmed: The program computes sum of divisors! ***")
        sum_part2 = sum_of_divisors(target_r4_part2)
        print(f"\nPart 2 answer (predicted): {sum_part2}")

if __name__ == '__main__':
    main()
