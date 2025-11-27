def parse_input(filename):
    """
    Parse the input file to extract depth and target coordinates.

    Expected format:
    depth: <integer>
    target: <X>,<Y>

    Returns:
        tuple: (depth, target_x, target_y)
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    depth = None
    target_x = None
    target_y = None

    for line in lines:
        line = line.strip()
        if line.startswith('depth:'):
            depth = int(line.split(':')[1].strip())
        elif line.startswith('target:'):
            coords = line.split(':')[1].strip()
            target_x, target_y = map(int, coords.split(','))

    return depth, target_x, target_y


def calculate_erosion_level(geologic_index, depth):
    """
    Calculate erosion level from geologic index.

    Formula: (geologic_index + depth) % 20183

    Args:
        geologic_index: The geologic index
        depth: Cave system depth

    Returns:
        int: Erosion level
    """
    return (geologic_index + depth) % 20183


def calculate_risk_level(erosion_level):
    """
    Calculate risk level from erosion level.

    Based on erosion_level % 3:
    - 0: rocky (risk = 0)
    - 1: wet (risk = 1)
    - 2: narrow (risk = 2)

    Args:
        erosion_level: The erosion level

    Returns:
        int: Risk level (0, 1, or 2)
    """
    return erosion_level % 3


def calculate_geologic_index(x, y, target_x, target_y, erosion_levels):
    """
    Calculate geologic index for position (x, y).

    Rules (in order of precedence):
    1. Cave mouth (0,0): return 0
    2. Target position: return 0
    3. Y == 0: return X * 16807
    4. X == 0: return Y * 48271
    5. Otherwise: return erosion_level(x-1, y) * erosion_level(x, y-1)

    Args:
        x, y: Current coordinates
        target_x, target_y: Target coordinates
        erosion_levels: 2D structure storing computed erosion levels

    Returns:
        int: Geologic index for the position
    """
    # Rule 1: Cave mouth
    if x == 0 and y == 0:
        return 0

    # Rule 2: Target position
    if x == target_x and y == target_y:
        return 0

    # Rule 3: Top edge (Y = 0)
    if y == 0:
        return x * 16807

    # Rule 4: Left edge (X = 0)
    if x == 0:
        return y * 48271

    # Rule 5: Interior cells
    return erosion_levels[y][x-1] * erosion_levels[y-1][x]


def calculate_total_risk(depth, target_x, target_y):
    """
    Calculate total risk level for the rectangular region.

    Process cells row by row (y from 0 to target_y, x from 0 to target_x)
    to ensure dependencies are always satisfied.

    Args:
        depth: Cave system depth
        target_x, target_y: Target coordinates

    Returns:
        int: Total risk level
    """
    # Initialize 2D array for erosion levels
    erosion_levels = [[0] * (target_x + 1) for _ in range(target_y + 1)]

    total_risk = 0

    # Process row by row (CRITICAL: y outer, x inner for dependency satisfaction)
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            # Calculate geologic index
            geologic_index = calculate_geologic_index(x, y, target_x, target_y, erosion_levels)

            # Calculate erosion level
            erosion_level = calculate_erosion_level(geologic_index, depth)

            # Store erosion level for future dependencies
            erosion_levels[y][x] = erosion_level

            # Calculate risk level
            risk_level = calculate_risk_level(erosion_level)

            # Add to total risk
            total_risk += risk_level

    return total_risk


def main():
    """
    Main entry point for the solution.
    """
    # Parse input
    depth, target_x, target_y = parse_input("input.md")

    # Calculate total risk
    result = calculate_total_risk(depth, target_x, target_y)

    # Print result
    print(result)


if __name__ == "__main__":
    main()
