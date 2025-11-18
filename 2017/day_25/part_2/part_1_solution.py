from collections import defaultdict
import re


def parse_input(input_text):
    """
    Parses the input blueprint into structured data.

    Returns:
        initial_state: str - The starting state (e.g., 'A')
        num_steps: int - Number of steps to execute
        states: dict - Nested dictionary of state machine rules
    """
    # Extract initial state
    initial_match = re.search(r"Begin in state ([A-Z])\.", input_text)
    initial_state = initial_match.group(1)

    # Extract number of steps
    steps_match = re.search(r"after (\d+) steps", input_text)
    num_steps = int(steps_match.group(1))

    # Parse state definitions
    states = {}

    # Split by "In state X:" to get state blocks
    state_blocks = re.split(r'In state ([A-Z]):', input_text)[1:]  # Skip first empty element

    for i in range(0, len(state_blocks), 2):
        state_name = state_blocks[i]
        state_content = state_blocks[i + 1]

        states[state_name] = {}

        # Extract rules for value 0 and value 1
        value_blocks = re.split(r'If the current value is ([01]):', state_content)[1:]

        for j in range(0, len(value_blocks), 2):
            current_value = int(value_blocks[j])
            rule_content = value_blocks[j + 1]

            # Extract write value
            write_match = re.search(r"Write the value ([01])", rule_content)
            write_value = int(write_match.group(1))

            # Extract move direction
            move_match = re.search(r"Move one slot to the (left|right)", rule_content)
            move_direction = 1 if move_match.group(1) == "right" else -1

            # Extract next state
            next_match = re.search(r"Continue with state ([A-Z])", rule_content)
            next_state = next_match.group(1)

            states[state_name][current_value] = {
                'write': write_value,
                'move': move_direction,
                'next_state': next_state
            }

    return initial_state, num_steps, states


def simulate_turing_machine(states, initial_state, num_steps):
    """
    Simulates the Turing machine for the specified number of steps.

    Args:
        states: dict - State machine rules
        initial_state: str - Starting state
        num_steps: int - Number of steps to execute

    Returns:
        tape: defaultdict - The tape after simulation (only non-zero values stored)
    """
    tape = defaultdict(int)
    cursor = 0
    current_state = initial_state

    for step in range(num_steps):
        # Read current value at cursor position
        current_value = tape[cursor]

        # Get rule for current state and value
        rule = states[current_state][current_value]

        # Write new value
        tape[cursor] = rule['write']

        # Move cursor
        cursor += rule['move']

        # Transition to next state
        current_state = rule['next_state']

    return tape


def calculate_checksum(tape):
    """
    Calculates the diagnostic checksum by counting 1s on the tape.

    Args:
        tape: dict - The tape containing binary values

    Returns:
        int - The count of 1s on the tape
    """
    return sum(tape.values())


def main(input_file='input.md'):
    """
    Main function that orchestrates the Turing machine simulation.

    Args:
        input_file: str - Path to input file

    Returns:
        int - The diagnostic checksum
    """
    # Read input file
    try:
        with open(input_file, 'r') as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"Error: {input_file} not found")
        return None

    # Parse input
    initial_state, num_steps, states = parse_input(input_text)

    # Simulate Turing machine
    tape = simulate_turing_machine(states, initial_state, num_steps)

    # Calculate checksum
    checksum = calculate_checksum(tape)

    # Output result
    print(checksum)
    return checksum


if __name__ == "__main__":
    main()
