#!/usr/bin/env python3
"""Manual trace of first few instructions to verify correctness"""

from solution import parse_instructions, get_value

def trace_execution():
    with open('input.md', 'r') as f:
        lines = f.readlines()

    instructions = parse_instructions(lines)

    # Print first 10 instructions
    print("First 10 instructions:")
    for i, instr in enumerate(instructions[:10]):
        print(f"{i:2d}: {instr[0]:3s} {instr[1]:2s} {instr[2]:>7s}")

    print("\n" + "="*60)
    print("Manual trace of execution:")
    print("="*60)

    # Initialize state
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
    ip = 0
    mul_count = 0
    step = 0

    # Trace first 20 steps
    while step < 20 and 0 <= ip < len(instructions):
        op, arg1, arg2 = instructions[ip]

        print(f"\nStep {step:2d}, IP={ip:2d}: {op} {arg1} {arg2}")
        print(f"  Before: a={registers['a']}, b={registers['b']}, c={registers['c']}, d={registers['d']}, e={registers['e']}, f={registers['f']}, g={registers['g']}, h={registers['h']}")

        if op == "jnz":
            x_val = get_value(arg1, registers)
            print(f"  jnz: {arg1}={x_val}, offset={arg2}")
            if x_val != 0:
                offset = get_value(arg2, registers)
                ip += offset
                print(f"  -> JUMP to IP={ip}")
            else:
                ip += 1
                print(f"  -> NO JUMP, IP={ip}")
        else:
            if op == "set":
                registers[arg1] = get_value(arg2, registers)
                print(f"  set: {arg1} = {get_value(arg2, registers)}")
            elif op == "sub":
                registers[arg1] -= get_value(arg2, registers)
                print(f"  sub: {arg1} = {arg1} - {get_value(arg2, registers)} = {registers[arg1]}")
            elif op == "mul":
                old_val = registers[arg1]
                registers[arg1] *= get_value(arg2, registers)
                mul_count += 1
                print(f"  mul: {arg1} = {old_val} * {get_value(arg2, registers)} = {registers[arg1]} [mul_count={mul_count}]")

            ip += 1

        step += 1

    print(f"\n" + "="*60)
    print(f"After {step} steps:")
    print(f"  Registers: {registers}")
    print(f"  IP: {ip}")
    print(f"  mul_count: {mul_count}")
    print("="*60)

if __name__ == "__main__":
    trace_execution()
