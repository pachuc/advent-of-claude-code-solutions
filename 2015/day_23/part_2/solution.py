def parse_instructions(filename):
    """Parse input file into list of instruction dictionaries"""
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                parts = line.replace(',', '').split()
                op = parts[0]

                if op in ['hlf', 'tpl', 'inc']:
                    instructions.append({"op": op, "reg": parts[1]})
                elif op == 'jmp':
                    instructions.append({"op": op, "offset": int(parts[1])})
                elif op in ['jie', 'jio']:
                    instructions.append({"op": op, "reg": parts[1], "offset": int(parts[2])})

    return instructions


def execute_instruction(inst, registers, pc):
    """Execute a single instruction and return new PC value"""
    op = inst["op"]

    if op == "hlf":
        registers[inst["reg"]] //= 2
        return pc + 1
    elif op == "tpl":
        registers[inst["reg"]] *= 3
        return pc + 1
    elif op == "inc":
        registers[inst["reg"]] += 1
        return pc + 1
    elif op == "jmp":
        return pc + inst["offset"]
    elif op == "jie":
        if registers[inst["reg"]] % 2 == 0:
            return pc + inst["offset"]
        return pc + 1
    elif op == "jio":
        if registers[inst["reg"]] == 1:
            return pc + inst["offset"]
        return pc + 1

    # Should never reach here with valid input
    raise ValueError(f"Unknown instruction: {op}")


def simulate(instructions, initial_a=1, initial_b=0, verbose=False, max_iterations=1_000_000):
    """Run the simulation and return final register values"""
    registers = {"a": initial_a, "b": initial_b}
    pc = 0
    iterations = 0

    while 0 <= pc < len(instructions):
        if verbose:
            print(f"[{iterations}] PC={pc} | a={registers['a']}, b={registers['b']} | {instructions[pc]}")

        pc = execute_instruction(instructions[pc], registers, pc)
        iterations += 1

        if iterations > max_iterations:
            raise RuntimeError(f"Exceeded max iterations ({max_iterations}). Possible infinite loop.")

    if verbose:
        print(f"Program terminated at PC={pc} after {iterations} iterations")
        print(f"Final: a={registers['a']}, b={registers['b']}")

    return registers


def main():
    """Main entry point"""
    instructions = parse_instructions("input.md")
    registers = simulate(instructions, initial_a=1, initial_b=0)
    print(registers["b"])


if __name__ == "__main__":
    main()
