from solution import parse_instructions, get_value


def execute_debug(instructions):
    """Execute with debug output."""
    registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    ip = 0
    step = 0

    print(f"Initial: {registers}, ip={ip}")

    while 0 <= ip < len(instructions):
        inst, arg1, arg2 = instructions[ip]
        step += 1

        if inst == 'cpy':
            registers[arg2] = get_value(arg1, registers)
            print(f"{step}. {inst} {arg1} {arg2}: {registers}, ip={ip} -> {ip+1}")
            ip += 1
        elif inst == 'inc':
            registers[arg1] += 1
            print(f"{step}. {inst} {arg1}: {registers}, ip={ip} -> {ip+1}")
            ip += 1
        elif inst == 'dec':
            registers[arg1] -= 1
            print(f"{step}. {inst} {arg1}: {registers}, ip={ip} -> {ip+1}")
            ip += 1
        elif inst == 'jnz':
            val = get_value(arg1, registers)
            offset = get_value(arg2, registers)
            if val != 0:
                print(f"{step}. {inst} {arg1} {arg2}: {val}!=0, jump {offset}, {registers}, ip={ip} -> {ip+offset}")
                ip += offset
            else:
                print(f"{step}. {inst} {arg1} {arg2}: {val}==0, no jump, {registers}, ip={ip} -> {ip+1}")
                ip += 1

    print(f"Final: {registers}")
    return registers['a']


# Test 5: Nested Loops
print("="*60)
print("Test 5: Nested Loops")
print("="*60)
test5 = """cpy 3 a
cpy 2 b
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec c
jnz c -5"""
instructions = parse_instructions(test5.strip().split('\n'))
result = execute_debug(instructions)
print(f"Result: {result}, Expected: 9")

print("\n" + "="*60)
print("Test 9: Jump with Register Offset")
print("="*60)
test9 = """cpy 2 b
cpy 1 a
jnz a b
inc a
inc a"""
instructions = parse_instructions(test9.strip().split('\n'))
result = execute_debug(instructions)
print(f"Result: {result}, Expected: 1")
