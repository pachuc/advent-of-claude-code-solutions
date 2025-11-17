import re
import sys
from collections import deque


def parse_input(input_text):
    """Parse df output to extract complete grid structure."""
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

    # Pre-compute wall positions
    empty_capacity = nodes_dict[empty_pos]['size']
    wall_positions = {
        pos for pos, node in nodes_dict.items()
        if node['used'] > empty_capacity
    }

    return nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions


def find_minimum_steps_debug(grid, max_x, max_y, initial_goal_pos, initial_empty_pos, target_pos):
    """BFS with path tracking for debugging."""
    initial_state = (initial_goal_pos[0], initial_goal_pos[1],
                     initial_empty_pos[0], initial_empty_pos[1])

    if initial_goal_pos == target_pos:
        return 0, []

    queue = deque([(initial_state, 0, [])])  # (state, steps, path)
    visited = {initial_state}

    while queue:
        state, steps, path = queue.popleft()
        goal_x, goal_y, empty_x, empty_y = state

        if (goal_x, goal_y) == target_pos:
            return steps, path

        # Get current empty capacity
        empty_capacity = grid[(empty_x, empty_y)]['size']

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            adj_x = empty_x + dx
            adj_y = empty_y + dy

            if not (0 <= adj_x <= max_x and 0 <= adj_y <= max_y):
                continue

            if (adj_x, adj_y) not in grid:
                continue

            adj_used = grid[(adj_x, adj_y)]['used']
            if adj_used > empty_capacity:
                continue

            new_empty_x, new_empty_y = adj_x, adj_y

            if (adj_x, adj_y) == (goal_x, goal_y):
                new_goal_x, new_goal_y = empty_x, empty_y
                move_desc = f"Move goal from ({goal_x},{goal_y}) to ({new_goal_x},{new_goal_y})"
            else:
                new_goal_x, new_goal_y = goal_x, goal_y
                move_desc = f"Move empty from ({empty_x},{empty_y}) to ({new_empty_x},{new_empty_y})"

            new_state = (new_goal_x, new_goal_y, new_empty_x, new_empty_y)

            if new_state not in visited:
                visited.add(new_state)
                new_path = path + [move_desc]
                queue.append((new_state, steps + 1, new_path))

    return None, []


def main():
    with open('input.md', 'r') as f:
        input_text = f.read()

    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    print(f"Grid: {max_x+1} x {max_y+1}")
    print(f"Empty at: {empty_pos}, capacity: {nodes_dict[empty_pos]['size']}T")
    print(f"Goal at: {goal_pos}, used: {nodes_dict[goal_pos]['used']}T")
    print(f"Walls: {len(wall_positions)} nodes")
    print()

    target_pos = (0, 0)
    steps, path = find_minimum_steps_debug(nodes_dict, max_x, max_y, goal_pos, empty_pos, target_pos)

    print(f"Steps: {steps}")
    print(f"\nFirst 10 moves:")
    for i, move in enumerate(path[:10], 1):
        print(f"{i}. {move}")

    print(f"\nLast 10 moves:")
    for i, move in enumerate(path[-10:], len(path)-9):
        print(f"{i}. {move}")


if __name__ == "__main__":
    main()
