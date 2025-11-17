def parse_circuit(lines):
    """
    Parse circuit instructions into a dictionary mapping wire names to their operations.

    Returns:
        dict: {wire_name: (operation_type, operands)}
    """
    circuit = {}

    for line in lines:
        line = line.strip()
        if not line:  # Skip empty lines
            continue

        # Split by " -> " to get operation and output wire
        left_side, output_wire = line.split(' -> ')
        parts = left_side.split()

        if len(parts) == 1:
            # Direct assignment: could be "123 -> x" or "lx -> a"
            if parts[0].isdigit():
                circuit[output_wire] = ('VALUE', int(parts[0]))
            else:
                circuit[output_wire] = ('WIRE', parts[0])

        elif len(parts) == 2:
            # NOT operation: "NOT x -> h"
            circuit[output_wire] = ('NOT', parts[1])

        elif len(parts) == 3:
            # Binary operations: AND, OR, LSHIFT, RSHIFT
            operation = parts[1]  # AND, OR, LSHIFT, RSHIFT
            # Note: parts[0] and parts[2] stay as strings
            # They will be resolved later (could be wire names or numeric literals)
            circuit[output_wire] = (operation, parts[0], parts[2])

    return circuit


def get_value(operand, circuit, cache):
    """
    Resolve an operand to its numeric value.
    If it's a number, return it directly.
    If it's a wire, evaluate that wire recursively.
    """
    if operand.isdigit():
        return int(operand)
    else:
        # It's a wire name - recursively evaluate it
        return evaluate_wire(operand, circuit, cache)


def evaluate_wire(wire, circuit, cache):
    """
    Recursively evaluate a wire's signal value.
    Uses memoization to cache results.

    Returns:
        int: The 16-bit signal value (0-65535)
    """
    # Check if wire value already in cache
    if wire in cache:
        return cache[wire]

    # Get operation for this wire from circuit dictionary
    operation = circuit[wire]
    op_type = operation[0]

    # Compute result based on operation type
    if op_type == 'VALUE':
        result = operation[1]

    elif op_type == 'WIRE':
        result = get_value(operation[1], circuit, cache)

    elif op_type == 'AND':
        input1, input2 = operation[1], operation[2]
        result = get_value(input1, circuit, cache) & get_value(input2, circuit, cache)

    elif op_type == 'OR':
        input1, input2 = operation[1], operation[2]
        result = get_value(input1, circuit, cache) | get_value(input2, circuit, cache)

    elif op_type == 'LSHIFT':
        input_wire, shift_amount = operation[1], operation[2]
        result = get_value(input_wire, circuit, cache) << int(shift_amount)

    elif op_type == 'RSHIFT':
        input_wire, shift_amount = operation[1], operation[2]
        result = get_value(input_wire, circuit, cache) >> int(shift_amount)

    elif op_type == 'NOT':
        result = ~get_value(operation[1], circuit, cache)

    # Apply 16-bit mask to ensure result stays within valid range
    result = result & 0xFFFF

    # Cache the result
    cache[wire] = result

    return result


def solve(input_text, target_wire='a'):
    """
    Main solution function.

    Args:
        input_text: String containing all circuit instructions
        target_wire: The wire to evaluate (default: 'a')

    Returns:
        int: Signal value on the target wire
    """
    lines = input_text.strip().split('\n')
    circuit = parse_circuit(lines)
    cache = {}
    return evaluate_wire(target_wire, circuit, cache)


if __name__ == "__main__":
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(result)
