"""
Sporifica Virus Simulation - Advent of Code 2017 Day 22 Part 1

Simulates a virus carrier moving through an infinite 2D grid,
infecting and cleaning nodes according to specific rules.
"""

# Direction constants (screen coordinates: y increases downward)
# UP, RIGHT, DOWN, LEFT as (dx, dy) tuples
DIRECTIONS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def parse_input(filename):
    """
    Read grid from file and return set of infected positions.

    Args:
        filename: path to input file

    Returns:
        infected_nodes: set of (x, y) tuples for infected nodes
        center: (x, y) tuple for starting position
    """
    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    # Remove empty lines
    lines = [line for line in lines if line]

    height = len(lines)
    width = len(lines[0]) if lines else 0

    # Calculate center position (using integer division)
    center_x = width // 2
    center_y = height // 2

    # Find all infected nodes (marked with '#')
    infected_nodes = set()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#':
                infected_nodes.add((x, y))

    return infected_nodes, (center_x, center_y)


def simulate_virus(infected_nodes, start_pos, num_bursts=10000):
    """
    Simulate virus carrier for specified number of bursts.

    Args:
        infected_nodes: set of (x, y) infected positions
        start_pos: (x, y) starting position
        num_bursts: number of bursts to simulate

    Returns:
        count of new infections
    """
    # Create mutable copy of infected nodes
    infected = set(infected_nodes)

    # Initialize state
    pos_x, pos_y = start_pos
    direction_idx = 0  # Start facing UP
    infection_count = 0

    # Run simulation for specified number of bursts
    for _ in range(num_bursts):
        # Step 1: Turn based on current node state
        if (pos_x, pos_y) in infected:
            # Infected node: turn RIGHT
            direction_idx = (direction_idx + 1) % 4
        else:
            # Clean node: turn LEFT
            direction_idx = (direction_idx - 1) % 4

        # Step 2: Toggle infection state
        if (pos_x, pos_y) in infected:
            # Clean the infected node
            infected.remove((pos_x, pos_y))
        else:
            # Infect the clean node
            infected.add((pos_x, pos_y))
            infection_count += 1

        # Step 3: Move forward in current direction
        dx, dy = DIRECTIONS[direction_idx]
        pos_x += dx
        pos_y += dy

    return infection_count


def main():
    """Main entry point for the solution."""
    # Parse input
    infected_nodes, center = parse_input('input.md')

    # Run simulation for 10,000 bursts
    result = simulate_virus(infected_nodes, center, 10000)

    # Print result
    print(result)


if __name__ == '__main__':
    main()
