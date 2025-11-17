def parse_instructions(lines):
    """Parse input lines into instruction dictionary"""
    instructions = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Split by '->' to get operation and target wire
        parts = line.split(' -> ')
        target = parts[1].strip()
        operation = parts[0].strip()

        # Parse the operation
        if ' AND ' in operation:
            operands = operation.split(' AND ')
            instructions[target] = {'op': 'AND', 'args': [operands[0].strip(), operands[1].strip()]}
        elif ' OR ' in operation:
            operands = operation.split(' OR ')
            instructions[target] = {'op': 'OR', 'args': [operands[0].strip(), operands[1].strip()]}
        elif ' LSHIFT ' in operation:
            operands = operation.split(' LSHIFT ')
            instructions[target] = {'op': 'LSHIFT', 'args': [operands[0].strip(), operands[1].strip()]}
        elif ' RSHIFT ' in operation:
            operands = operation.split(' RSHIFT ')
            instructions[target] = {'op': 'RSHIFT', 'args': [operands[0].strip(), operands[1].strip()]}
        elif operation.startswith('NOT '):
            operand = operation[4:].strip()
            instructions[target] = {'op': 'NOT', 'args': [operand]}
        else:
            # Direct assignment (value or wire)
            instructions[target] = {'op': 'SIGNAL', 'args': [operation]}

    return instructions


def resolve_value(operand, instructions, memo):
    """Resolve operand to integer value (handle both literals and wire refs)"""
    # Check if it's a numeric literal
    if operand.isdigit():
        return int(operand)
    else:
        # It's a wire reference, evaluate it
        return evaluate_wire(operand, instructions, memo)


def evaluate_wire(wire_name, instructions, memo):
    """Recursively evaluate wire value with memoization"""
    # Check memo cache
    if wire_name in memo:
        return memo[wire_name]

    # Get instruction for this wire
    instruction = instructions[wire_name]
    op = instruction['op']
    args = instruction['args']

    result = 0

    if op == 'SIGNAL':
        # Direct assignment
        result = resolve_value(args[0], instructions, memo)
    elif op == 'AND':
        val1 = resolve_value(args[0], instructions, memo)
        val2 = resolve_value(args[1], instructions, memo)
        result = (val1 & val2) & 0xFFFF
    elif op == 'OR':
        val1 = resolve_value(args[0], instructions, memo)
        val2 = resolve_value(args[1], instructions, memo)
        result = (val1 | val2) & 0xFFFF
    elif op == 'NOT':
        val = resolve_value(args[0], instructions, memo)
        result = (~val) & 0xFFFF
    elif op == 'LSHIFT':
        val = resolve_value(args[0], instructions, memo)
        shift_amount = int(args[1])
        result = (val << shift_amount) & 0xFFFF
    elif op == 'RSHIFT':
        val = resolve_value(args[0], instructions, memo)
        shift_amount = int(args[1])
        result = (val >> shift_amount) & 0xFFFF

    # Store in memo and return
    memo[wire_name] = result
    return result


def simulate_circuit(instructions):
    """Run circuit simulation and return wire 'a' value"""
    memo = {}
    return evaluate_wire('a', instructions, memo)


def main():
    # Read input
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Parse instructions
    instructions = parse_instructions(lines)

    # First run - get original value of wire 'a'
    original_a = simulate_circuit(instructions)
    print(f"First run - wire a: {original_a}")

    # Override wire 'b' with the value from wire 'a'
    instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a)]}

    # Second run with modified wire 'b' (simulate_circuit creates fresh memo internally)
    final_a = simulate_circuit(instructions)
    print(f"Second run - wire a: {final_a}")

    # Output the final answer
    print(f"\nAnswer: {final_a}")


if __name__ == '__main__':
    main()
