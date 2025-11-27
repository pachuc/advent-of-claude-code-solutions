from collections import deque

# Direction order for movement decisions: up, left, right, down
DIRECTIONS = [
    (0, -1),  # Up: same column, row above
    (-1, 0),  # Left: column to left, same row
    (1, 0),   # Right: column to right, same row
    (0, 1)    # Down: same column, row below
]


class Unit:
    """Represents a combat unit (Elf or Goblin)"""
    def __init__(self, x, y, unit_type):
        self.x = x              # Current x position (column)
        self.y = y              # Current y position (row)
        self.type = unit_type   # 'E' or 'G'
        self.hp = 200           # Hit points
        self.attack = 3         # Attack power
        self.alive = True       # Status flag


def parse_input(input_text):
    """
    Parse grid and create Unit objects.

    Returns:
        - grid: 2D list of characters (single source of truth)
        - units: list of Unit objects
    """
    lines = input_text.strip().split('\n')
    grid = [list(row) for row in lines]
    units = []

    # Scan grid for units
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in ['E', 'G']:
                units.append(Unit(x, y, grid[y][x]))

    return grid, units


def sort_units(units):
    """Sort living units in reading order (top to bottom, left to right)"""
    return sorted([u for u in units if u.alive], key=lambda u: (u.y, u.x))


def find_targets(unit, units):
    """
    Find all living enemy units.

    Args:
        unit: Current unit
        units: All units

    Returns:
        List of enemy Unit objects
    """
    enemy_type = 'E' if unit.type == 'G' else 'G'
    return [u for u in units if u.alive and u.type == enemy_type]


def bfs_distances(grid, start_x, start_y, from_unit=False):
    """
    BFS to find distances to all reachable squares.

    Args:
        grid: 2D grid (single source of truth for positions)
        start_x, start_y: Starting position
        from_unit: If True, starting position can be a unit (E or G)

    Returns:
        Dict of (x, y): distance
    """
    distances = {}

    # Check if start position is valid
    if from_unit:
        # When starting from a unit, we don't include the starting position
        # but we still BFS from there
        if grid[start_y][start_x] not in ['E', 'G', '.']:
            return distances
    else:
        # When starting from a destination, it must be passable
        if grid[start_y][start_x] != '.':
            return distances
        distances[(start_x, start_y)] = 0

    queue = deque([(start_x, start_y, 0)])

    while queue:
        x, y, dist = queue.popleft()

        # Check 4 neighbors in direction order
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy

            # Skip if out of bounds
            if ny < 0 or ny >= len(grid) or nx < 0 or nx >= len(grid[ny]):
                continue

            # Skip if not passable (wall or occupied)
            if grid[ny][nx] != '.':
                continue

            # Skip if already visited
            if (nx, ny) in distances:
                continue

            # Add to distances and queue
            distances[(nx, ny)] = dist + 1
            queue.append((nx, ny, dist + 1))

    return distances


def find_in_range_squares(targets, grid):
    """
    Find all open squares adjacent to any target.

    Args:
        targets: List of enemy units
        grid: 2D grid (single source of truth)

    Returns:
        Set of (x, y) tuples
    """
    in_range = set()

    for target in targets:
        # Check 4 adjacent squares
        for dx, dy in DIRECTIONS:
            ax, ay = target.x + dx, target.y + dy

            # Skip if out of bounds
            if ay < 0 or ay >= len(grid) or ax < 0 or ax >= len(grid[ay]):
                continue

            # Add if passable
            if grid[ay][ax] == '.':
                in_range.add((ax, ay))

    return in_range


def choose_destination(unit, targets, grid):
    """
    Choose which in-range square to move toward.

    Returns:
        (x, y) of chosen destination, or None if no valid destination
    """
    # Get in-range squares
    in_range = find_in_range_squares(targets, grid)
    if not in_range:
        return None

    # Run BFS from unit's current position
    distances = bfs_distances(grid, unit.x, unit.y, from_unit=True)

    # Filter to reachable in-range squares
    reachable = [(pos, distances[pos]) for pos in in_range if pos in distances]
    if not reachable:
        return None

    # Find minimum distance
    min_distance = min(dist for pos, dist in reachable)

    # Filter to squares with minimum distance
    nearest = [pos for pos, dist in reachable if dist == min_distance]

    # Sort by reading order and return first
    nearest.sort(key=lambda pos: (pos[1], pos[0]))  # (y, x)
    return nearest[0]


def choose_next_step(unit, destination, grid):
    """
    Choose which adjacent square to move to.

    Runs BFS from the DESTINATION backward to find the best first step.

    Returns:
        (x, y) of next position
    """
    # Run BFS from destination backward
    distances = bfs_distances(grid, destination[0], destination[1])

    # Check adjacent squares in direction order
    best_step = None
    best_distance = float('inf')

    for dx, dy in DIRECTIONS:
        ax, ay = unit.x + dx, unit.y + dy

        # Skip if out of bounds
        if ay < 0 or ay >= len(grid) or ax < 0 or ax >= len(grid[ay]):
            continue

        # Must be passable
        if grid[ay][ax] != '.':
            continue

        # Must be reachable from destination
        if (ax, ay) not in distances:
            continue

        # Check if this is the best (or first best) step
        if distances[(ax, ay)] < best_distance:
            best_distance = distances[(ax, ay)]
            best_step = (ax, ay)

    return best_step


def choose_attack_target(unit, targets):
    """
    Choose which adjacent enemy to attack.

    Returns:
        Unit object to attack, or None
    """
    # Filter to adjacent enemies
    adjacent = [t for t in targets
                if abs(t.x - unit.x) + abs(t.y - unit.y) == 1]

    if not adjacent:
        return None

    # Find minimum HP
    min_hp = min(t.hp for t in adjacent)

    # Filter to enemies with minimum HP
    lowest_hp = [t for t in adjacent if t.hp == min_hp]

    # Sort by reading order and return first
    lowest_hp.sort(key=lambda t: (t.y, t.x))
    return lowest_hp[0]


def execute_turn(unit, units, grid):
    """
    Execute one unit's turn: move and attack.

    Returns:
        True if combat continues, False if no targets found
    """
    # Find targets
    targets = find_targets(unit, units)
    if not targets:
        return False  # Combat ends immediately

    # MOVEMENT PHASE
    # Check if already adjacent to any target
    already_adjacent = any(abs(t.x - unit.x) + abs(t.y - unit.y) == 1
                          for t in targets)

    if not already_adjacent:
        # Choose destination
        destination = choose_destination(unit, targets, grid)

        if destination is not None:
            # Choose next step
            next_step = choose_next_step(unit, destination, grid)

            if next_step is not None:
                # Update grid: clear old position
                grid[unit.y][unit.x] = '.'

                # Update unit position
                unit.x, unit.y = next_step

                # Update grid: set new position
                grid[unit.y][unit.x] = unit.type

    # ATTACK PHASE
    # Choose attack target (targets list is still valid)
    target = choose_attack_target(unit, targets)

    if target is not None:
        # Deal damage
        target.hp -= unit.attack

        # Check if target died
        if target.hp <= 0:
            target.alive = False
            grid[target.y][target.x] = '.'

    return True  # Combat continues


def execute_round(units, grid):
    """
    Execute one full round of combat.

    Returns:
        True if round completed fully, False if ended mid-round
    """
    # Sort units in reading order
    sorted_units = sort_units(units)

    for unit in sorted_units:
        # Skip if dead (may have died earlier this round)
        if not unit.alive:
            continue

        # Execute turn
        if not execute_turn(unit, units, grid):
            return False  # Combat ended mid-round

    return True  # Round completed


def simulate_combat(grid, units):
    """
    Run full combat simulation.

    Returns:
        Number of completed rounds
    """
    rounds = 0
    max_rounds = 10000  # Safety limit

    while rounds < max_rounds:
        # Execute round
        if not execute_round(units, grid):
            break  # Combat ended mid-round, don't increment

        rounds += 1

    return rounds


def calculate_outcome(rounds, units):
    """
    Calculate final outcome value.

    Returns:
        rounds × sum_of_remaining_hp
    """
    living = [u for u in units if u.alive]
    total_hp = sum(u.hp for u in living)
    return rounds * total_hp


def main():
    """Main entry point"""
    # Read input from input.md
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input
    grid, units = parse_input(input_text)

    # Simulate combat
    rounds = simulate_combat(grid, units)

    # Calculate outcome
    result = calculate_outcome(rounds, units)

    # Print result
    print(result)


if __name__ == "__main__":
    main()
