"""
Evolved Sporifica Virus Simulation - Advent of Code 2017 Day 22 Part 2

Simulates a virus carrier with 4-state infection cycle moving through
an infinite 2D grid. States: CLEAN → WEAKENED → INFECTED → FLAGGED → CLEAN
"""

# Direction constants (screen coordinates: y increases downward)
# Direction indices: 0=UP, 1=RIGHT, 2=DOWN, 3=LEFT
# Each tuple is (dx, dy) for movement
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

# State constants for 4-state infection cycle
CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3


def parse_input(filename):
    """
    Read grid from file and return dict of node states.

    Args:
        filename: path to input file

    Returns:
        node_states: dict mapping (x, y) to state integer
        center: (x, y) tuple for starting position
    """
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    height = len(lines)
    width = len(lines[0]) if lines else 0

    # Calculate center position
    center_x = width // 2
    center_y = height // 2

    # Find all infected nodes and create state dictionary
    node_states = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                node_states[(x, y)] = INFECTED

    return node_states, (center_x, center_y)


def simulate_virus_evolved(node_states, start_pos, num_bursts=10000000):
    """
    Simulate evolved virus carrier with 4-state infection cycle.

    Args:
        node_states: dict mapping (x, y) to state integer
        start_pos: (x, y) starting position
        num_bursts: number of bursts to simulate (default 10 million)

    Returns:
        count of WEAKENED→INFECTED transitions
    """
    # Create mutable copy of node states
    states = dict(node_states)

    # Initialize carrier state
    pos_x, pos_y = start_pos
    direction_idx = 0  # Start facing UP (0=UP, 1=RIGHT, 2=DOWN, 3=LEFT)
    infection_count = 0

    # Run simulation
    for _ in range(num_bursts):
        # Get current node state (default to CLEAN if not in dict)
        current_state = states.get((pos_x, pos_y), CLEAN)

        # Step 1: Turn based on current state
        if current_state == CLEAN:
            direction_idx = (direction_idx - 1) % 4  # Turn LEFT
        elif current_state == WEAKENED:
            pass  # No turn
        elif current_state == INFECTED:
            direction_idx = (direction_idx + 1) % 4  # Turn RIGHT
        else:  # FLAGGED
            direction_idx = (direction_idx + 2) % 4  # REVERSE

        # Step 2: Advance state in cycle
        new_state = (current_state + 1) % 4

        # Count if transitioning WEAKENED → INFECTED
        if current_state == WEAKENED:
            infection_count += 1

        # Update state (remove if returning to CLEAN to save memory)
        if new_state == CLEAN:
            states.pop((pos_x, pos_y), None)
        else:
            states[(pos_x, pos_y)] = new_state

        # Step 3: Move forward
        dx, dy = DIRECTIONS[direction_idx]
        pos_x += dx
        pos_y += dy

    return infection_count


def main():
    """Main entry point for the solution."""
    # Parse input
    node_states, center = parse_input('input.md')

    # Run simulation for 10,000,000 bursts
    result = simulate_virus_evolved(node_states, center, 10000000)

    # Print result
    print(result)


if __name__ == '__main__':
    main()
