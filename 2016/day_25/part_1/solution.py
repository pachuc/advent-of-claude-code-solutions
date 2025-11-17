def parse_input(filename):
    """
    Read and parse the assembunny program.
    Returns list of instruction components.
    """
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                instructions.append(line.split())
    return instructions


def get_value(operand, registers):
    """
    Returns numeric value of an operand.
    If operand is a register name ('a'-'d'), return register value.
    Otherwise, convert to integer and return.
    """
    if operand in registers:
        return registers[operand]
    return int(operand)


def run_program(initial_a, instructions, max_outputs=50):
    """
    Execute assembunny program with real-time pattern validation.
    Returns True if produces alternating 0,1,0,1... pattern for max_outputs.
    Returns False immediately on first pattern violation.
    """
    # Initialize registers
    registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    pc = 0
    output_count = 0

    # Execute until we have enough outputs or program ends
    while 0 <= pc < len(instructions) and output_count < max_outputs:
        inst = instructions[pc]
        cmd = inst[0]

        # Execute instruction
        if cmd == 'cpy':
            x, y = inst[1], inst[2]
            if y in registers:  # Only copy to valid registers
                registers[y] = get_value(x, registers)
            pc += 1

        elif cmd == 'inc':
            registers[inst[1]] += 1
            pc += 1

        elif cmd == 'dec':
            registers[inst[1]] -= 1
            pc += 1

        elif cmd == 'jnz':
            x = get_value(inst[1], registers)
            if x != 0:
                offset = get_value(inst[2], registers)
                pc += offset
            else:
                pc += 1

        elif cmd == 'out':
            value = get_value(inst[1], registers)
            expected = output_count % 2  # Expected: 0, 1, 0, 1, ...

            # Early termination: fail immediately if pattern breaks
            if value != expected:
                return False

            output_count += 1
            pc += 1

    # Success: generated max_outputs with perfect alternating pattern
    return output_count >= max_outputs


def run_program_verbose(initial_a, instructions, max_outputs=100):
    """
    Modified version that returns list of outputs for inspection.
    """
    registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    pc = 0
    outputs = []

    while 0 <= pc < len(instructions) and len(outputs) < max_outputs:
        inst = instructions[pc]
        cmd = inst[0]

        if cmd == 'cpy':
            x, y = inst[1], inst[2]
            if y in registers:
                registers[y] = get_value(x, registers)
            pc += 1

        elif cmd == 'inc':
            registers[inst[1]] += 1
            pc += 1

        elif cmd == 'dec':
            registers[inst[1]] -= 1
            pc += 1

        elif cmd == 'jnz':
            x = get_value(inst[1], registers)
            if x != 0:
                offset = get_value(inst[2], registers)
                pc += offset
            else:
                pc += 1

        elif cmd == 'out':
            value = get_value(inst[1], registers)
            outputs.append(value)
            pc += 1

    return outputs


def find_clock_signal_input(instructions):
    """
    Find the lowest positive integer that produces the clock signal pattern.
    Uses early termination - invalid candidates fail fast.
    """
    verification_length = 50  # Check 50 outputs to confirm pattern

    for candidate in range(1, 10000):  # Conservative upper bound
        if run_program(candidate, instructions, verification_length):
            return candidate

    raise Exception("No solution found in range 1-10000")


def validate_solution():
    """Run validation tests to verify the solution."""
    print("=" * 50)
    print("VALIDATION TESTS")
    print("=" * 50)

    # Test 1: Parse input
    print("\n[Test 1] Parsing input...")
    instructions = parse_input('input.md')
    print(f"✓ Loaded {len(instructions)} instructions")
    print(f"  First: {instructions[0]}")
    print(f"  Last: {instructions[-1]}")

    # Test 3: Find answer
    print("\n[Test 3] Finding answer...")
    import time
    start = time.time()
    answer = find_clock_signal_input(instructions)
    elapsed = time.time() - start
    print(f"✓ Answer: {answer} (found in {elapsed:.2f}s)")

    # Test 4: Verify correctness
    print("\n[Test 4] Verifying correctness...")
    outputs = run_program_verbose(answer, instructions, 100)
    is_valid = all(outputs[i] == i % 2 for i in range(len(outputs)))
    print(f"✓ Generated {len(outputs)} outputs")
    print(f"✓ Pattern valid: {is_valid}")
    print(f"  First 20: {outputs[:20]}")

    # Test 5: Verify minimality
    print("\n[Test 5] Verifying minimality...")
    result_below = run_program(answer - 1, instructions, 50)
    print(f"✓ Answer-1 result: {result_below} (should be False)")

    # Test 6: Pattern consistency
    print("\n[Test 6] Pattern consistency...")
    for length in [20, 50, 100]:
        result = run_program(answer, instructions, length)
        print(f"✓ Length {length}: {result}")

    # Test 7: Explore first few candidates
    print("\n[Test 7] First few candidates (for debugging)...")
    for candidate in range(1, min(answer + 2, 6)):
        outputs = run_program_verbose(candidate, instructions, max_outputs=10)
        print(f"  a={candidate}: {outputs[:10]}")

    print("\n" + "=" * 50)
    print(f"FINAL ANSWER: {answer}")
    print("=" * 50)

    return answer


def main():
    """Main execution - just print the answer."""
    instructions = parse_input('input.md')
    answer = find_clock_signal_input(instructions)
    print(answer)


if __name__ == "__main__":
    # Run validation tests
    validate_solution()
