import re
import sys
from collections import deque


def parse_input(input_text):
    """
    Parse df output to extract complete grid structure.

    Returns:
        tuple: (nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions)
        - nodes_dict: {(x, y): {'size': int, 'used': int, 'avail': int}}
        - max_x, max_y: Grid dimensions (maximum coordinates)
        - empty_pos: (x, y) tuple of empty node
        - goal_pos: (x, y) tuple of goal node (max_x, 0)
        - wall_positions: set of (x, y) positions that cannot be moved
    """
    nodes_dict = {}
    max_x = max_y = 0
    empty_pos = None

    lines = input_text.strip().split('\n')

    # Skip first 2 header lines
    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 4:
            continue

        # Extract coordinates from filesystem path
        filesystem = parts[0]
        match = re.search(r'x(\d+)-y(\d+)', filesystem)
        if not match:
            continue

        x = int(match.group(1))
        y = int(match.group(2))

        # Extract data values
        size = int(parts[1][:-1])   # Remove 'T' suffix
        used = int(parts[2][:-1])   # Remove 'T' suffix
        avail = int(parts[3][:-1])  # Remove 'T' suffix

        # Build dictionary
        nodes_dict[(x, y)] = {
            'size': size,
            'used': used,
            'avail': avail
        }

        # Track max coordinates
        max_x = max(max_x, x)
        max_y = max(max_y, y)

        # Find empty node
        if used == 0:
            empty_pos = (x, y)

    # Goal position is (max_x, 0)
    goal_pos = (max_x, 0)

    # Validate parsing results
    empty_count = sum(1 for node in nodes_dict.values() if node['used'] == 0)
    assert empty_count == 1, f"Expected 1 empty node, found {empty_count}"
    assert len(nodes_dict) > 0, "Grid is empty"
    assert empty_pos is not None, "No empty node found"
    assert empty_pos in nodes_dict, "Empty position not in grid"
    assert goal_pos in nodes_dict, "Goal position not in grid"

    # Pre-compute wall positions
    # A wall is any node whose data is too large to fit in the empty space
    empty_capacity = nodes_dict[empty_pos]['size']
    wall_positions = {
        pos for pos, node in nodes_dict.items()
        if node['used'] > empty_capacity
    }

    # Verify goal can actually be moved
    goal_used = nodes_dict[goal_pos]['used']
    assert goal_used <= empty_capacity, \
        f"Goal node cannot be moved! Goal has {goal_used}T but empty capacity is {empty_capacity}T"

    return nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions


def find_minimum_steps(grid, max_x, max_y, wall_positions, initial_goal_pos, initial_empty_pos, target_pos):
    """
    Use BFS to find minimum steps to move goal to target.

    Args:
        grid: Dictionary {(x, y): {'size': int, 'used': int, 'avail': int}}
        max_x, max_y: Grid boundaries (maximum coordinates)
        wall_positions: Set of (x, y) positions that cannot be moved (INITIALLY)
        initial_goal_pos: Starting position of goal data (x, y)
        initial_empty_pos: Starting position of empty node (x, y)
        target_pos: Target position for goal data (x, y)

    Returns:
        int: Minimum number of steps, or None if no solution exists
    """
    # State: (goal_x, goal_y, empty_x, empty_y)
    initial_state = (initial_goal_pos[0], initial_goal_pos[1],
                     initial_empty_pos[0], initial_empty_pos[1])

    # Check if already at target
    if initial_goal_pos == target_pos:
        return 0

    # BFS initialization
    queue = deque([(initial_state, 0)])  # (state, steps)
    visited = {initial_state}

    while queue:
        state, steps = queue.popleft()
        goal_x, goal_y, empty_x, empty_y = state

        # Check if goal reached target
        if (goal_x, goal_y) == target_pos:
            return steps

        # Get the current empty node's capacity (this changes as empty moves!)
        empty_capacity = grid[(empty_x, empty_y)]['size']

        # Try moving data from each adjacent node into empty position
        # Directions: up, down, left, right
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            # Calculate adjacent position
            adj_x = empty_x + dx
            adj_y = empty_y + dy

            # Check grid boundaries
            if not (0 <= adj_x <= max_x and 0 <= adj_y <= max_y):
                continue

            # Check if position exists in grid
            if (adj_x, adj_y) not in grid:
                continue

            # Check if adjacent node's data can fit in current empty node's capacity
            # This is the KEY check - it uses the CURRENT empty position's capacity!
            adj_used = grid[(adj_x, adj_y)]['used']
            if adj_used > empty_capacity:
                continue  # Cannot fit this data in current empty node

            # Create new state after moving data from adjacent into empty
            new_empty_x, new_empty_y = adj_x, adj_y

            # If we moved the goal, update goal position
            if (adj_x, adj_y) == (goal_x, goal_y):
                new_goal_x, new_goal_y = empty_x, empty_y
            else:
                new_goal_x, new_goal_y = goal_x, goal_y

            new_state = (new_goal_x, new_goal_y, new_empty_x, new_empty_y)

            # Add to queue if not visited
            if new_state not in visited:
                visited.add(new_state)
                queue.append((new_state, steps + 1))

    # No solution found
    return None


def analytical_min_steps(grid, max_x, max_y, empty_pos, goal_pos, wall_positions):
    """
    Analytical solution using pattern-based calculation.
    This is more efficient than BFS for this specific type of puzzle.
    """
    from collections import deque

    # BFS to find shortest path from empty to (goal_x - 1, goal_y)
    target_empty = (goal_pos[0] - 1, goal_pos[1])

    queue = deque([(empty_pos, 0)])
    visited = {empty_pos}

    while queue:
        pos, dist = queue.popleft()

        if pos == target_empty:
            # Found the distance to position empty next to goal
            # Formula: dist + 1 (initial swap) + 5 * (goal_x - 1) (remaining moves)
            # After the initial swap, the goal is at position goal_x - 1
            # We need to move it goal_x - 1 more times to reach position 0
            # Each of these moves takes 5 steps (cycle empty around + swap)
            return dist + 1 + 5 * (goal_pos[0] - 1)

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = pos[0] + dx, pos[1] + dy

            if not (0 <= nx <= max_x and 0 <= ny <= max_y):
                continue

            if (nx, ny) in wall_positions:
                continue

            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            queue.append(((nx, ny), dist + 1))

    return None


def main():
    """Main entry point."""
    # Read input file
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input (now includes wall positions)
    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    # Use full BFS for guaranteed correctness
    result = find_minimum_steps(
        nodes_dict, max_x, max_y, wall_positions, goal_pos, empty_pos, (0, 0)
    )

    # Handle result
    if result is None:
        print("Error: No solution found!", file=sys.stderr)
        sys.exit(1)

    # Print result
    print(result)


if __name__ == "__main__":
    main()
