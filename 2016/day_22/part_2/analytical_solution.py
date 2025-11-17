import re
from collections import deque


def parse_input(input_text):
    """Parse df output."""
    nodes_dict = {}
    max_x = max_y = 0
    empty_pos = None

    lines = input_text.strip().split('\n')

    for line in lines[2:]:
        line = line.strip()
        if not line:
            continue

        parts = line.split()
        if len(parts) < 4:
            continue

        filesystem = parts[0]
        match = re.search(r'x(\d+)-y(\d+)', filesystem)
        if not match:
            continue

        x = int(match.group(1))
        y = int(match.group(2))

        size = int(parts[1][:-1])
        used = int(parts[2][:-1])
        avail = int(parts[3][:-1])

        nodes_dict[(x, y)] = {'size': size, 'used': used, 'avail': avail}

        max_x = max(max_x, x)
        max_y = max(max_y, y)

        if used == 0:
            empty_pos = (x, y)

    goal_pos = (max_x, 0)
    empty_capacity = nodes_dict[empty_pos]['size']
    wall_positions = {
        pos for pos, node in nodes_dict.items()
        if node['used'] > empty_capacity
    }

    return nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions


def bfs_to_target(grid, max_x, max_y, start, target, walls):
    """BFS to find shortest path from start to target, avoiding walls."""
    if start == target:
        return 0

    queue = deque([(start, 0)])
    visited = {start}

    while queue:
        (x, y), dist = queue.popleft()

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy

            if not (0 <= nx <= max_x and 0 <= ny <= max_y):
                continue

            if (nx, ny) in walls:
                continue

            if (nx, ny) in visited:
                continue

            if (nx, ny) == target:
                return dist + 1

            visited.add((nx, ny))
            queue.append(((nx, ny), dist + 1))

    return None


def analytical_solution(grid, max_x, max_y, empty_pos, goal_pos, wall_positions):
    """
    Analytical solution for grid sliding puzzle.

    Strategy:
    1. Move empty to position (goal_x - 1, goal_y) to get adjacent to goal
    2. Swap goal with empty (1 move) - goal moves one position left
    3. For each of the remaining goal_x - 1 positions:
       - Cycle empty around goal: takes 5 moves per position
    """
    goal_x, goal_y = goal_pos

    # Step 1: BFS to move empty from current position to (goal_x - 1, goal_y)
    target_empty_pos = (goal_x - 1, goal_y)
    steps_to_position_empty = bfs_to_target(
        grid, max_x, max_y, empty_pos, target_empty_pos, wall_positions
    )

    if steps_to_position_empty is None:
        print("Cannot reach position adjacent to goal!")
        return None

    print(f"Steps to move empty from {empty_pos} to {target_empty_pos}: {steps_to_position_empty}")

    # Step 2: One swap to move goal from (goal_x, goal_y) to (goal_x - 1, goal_y)
    swap_steps = 1
    print(f"Swap goal from {goal_pos} to ({goal_x - 1}, {goal_y}): {swap_steps} step")

    # Step 3: For each remaining position (goal_x - 1 to 1), takes 5 moves
    remaining_positions = goal_x - 1
    cycle_steps = remaining_positions * 5
    print(f"Move goal from ({goal_x - 1}, {goal_y}) to (0, {goal_y}): {remaining_positions} positions * 5 = {cycle_steps} steps")

    total = steps_to_position_empty + swap_steps + cycle_steps
    return total


def main():
    with open('input.md', 'r') as f:
        input_text = f.read()

    nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions = parse_input(input_text)

    print(f"Grid: {max_x+1} x {max_y+1}")
    print(f"Empty at: {empty_pos}")
    print(f"Goal at: {goal_pos}")
    print(f"Walls: {len(wall_positions)} nodes")
    print()

    result = analytical_solution(nodes_dict, max_x, max_y, empty_pos, goal_pos, wall_positions)
    print(f"\nTotal steps: {result}")


if __name__ == "__main__":
    main()
