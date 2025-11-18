def parse_instruction_line(line):
    """Parse a single instruction line and return instruction dict

    This helper function is separated for testability.
    """
    parts = line.strip().split()
    # Input is assumed to be well-formed (7 space-separated parts)
    return {
        'target_reg': parts[0],
        'operation': parts[1],
        'amount': int(parts[2]),
        'cond_reg': parts[4],
        'comparator': parts[5],
        'cond_val': int(parts[6])
    }

def parse_input(filename):
    """Parse input file and return list of instruction tuples"""
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            instructions.append(parse_instruction_line(line))
    return instructions

def get_comparator(operator):
    """Return comparison function for given operator string"""
    comparators = {
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b,
        '==': lambda a, b: a == b,
        '!=': lambda a, b: a != b
    }
    return comparators[operator]

def process_instructions(instructions, verbose=False):
    """Execute all instructions and track maximum value during execution

    Args:
        instructions: List of instruction dictionaries
        verbose: If True, print register state after each modification

    Returns:
        tuple: (dict, int) where dict is {register_name: value} and int is max_value_ever
    """
    registers = {}  # defaultdict could work but explicit is clearer
    # NEW: Track maximum value across all states
    # Start at 0 since all registers implicitly begin at 0
    max_value_ever = 0

    for i, instr in enumerate(instructions):
        # Get current value of condition register (0 if not exists)
        cond_reg_value = registers.get(instr['cond_reg'], 0)

        # Evaluate condition
        comparator = get_comparator(instr['comparator'])
        if comparator(cond_reg_value, instr['cond_val']):
            # Condition is true, apply operation
            current_value = registers.get(instr['target_reg'], 0)

            if instr['operation'] == 'inc':
                registers[instr['target_reg']] = current_value + instr['amount']
            elif instr['operation'] == 'dec':
                registers[instr['target_reg']] = current_value - instr['amount']

            # NEW: Update maximum after each modification
            max_value_ever = max(max_value_ever, registers[instr['target_reg']])

            if verbose:
                print(f"After instruction {i+1}: {instr['target_reg']} = {registers[instr['target_reg']]}, max_ever = {max_value_ever}")

    return registers, max_value_ever

def find_max_register_value(registers):
    """Return the maximum value in any register"""
    if not registers:
        return 0  # Edge case: no registers modified
    return max(registers.values())

def main():
    """Main execution function"""
    try:
        # Parse input
        instructions = parse_input('input.md')
    except FileNotFoundError:
        print("Error: input.md not found")
        return
    except Exception as e:
        print(f"Error reading input: {e}")
        return

    # Process all instructions - now returns tuple
    registers, max_during_execution = process_instructions(instructions, verbose=False)

    # Print the maximum value during execution (Part 2 answer)
    print(max_during_execution)

if __name__ == '__main__':
    main()
