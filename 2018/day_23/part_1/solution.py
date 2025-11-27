import re


def parse_input(filename):
    """
    Parse nanobot data from input file.

    Returns:
        List of tuples: [(x, y, z, radius), ...]
    """
    nanobots = []
    pattern = r'pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)'

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            match = re.match(pattern, line)
            if match:
                x, y, z, r = map(int, match.groups())
                nanobots.append((x, y, z, r))

    return nanobots


def manhattan_distance(pos1, pos2):
    """
    Calculate Manhattan distance between two 3D points.

    Args:
        pos1: tuple (x1, y1, z1)
        pos2: tuple (x2, y2, z2)

    Returns:
        int: Manhattan distance
    """
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def find_strongest_nanobot(nanobots):
    """
    Find the nanobot with the largest signal radius.

    Args:
        nanobots: List of (x, y, z, radius) tuples

    Returns:
        tuple: (x, y, z, radius) of strongest nanobot
    """
    return max(nanobots, key=lambda bot: bot[3])


def count_in_range(nanobots, strongest):
    """
    Count nanobots within range of the strongest nanobot.

    Args:
        nanobots: List of all nanobots
        strongest: The strongest nanobot (x, y, z, radius)

    Returns:
        int: Count of nanobots in range
    """
    sx, sy, sz, sr = strongest
    count = 0
    for bot in nanobots:
        x, y, z, r = bot
        dist = manhattan_distance((sx, sy, sz), (x, y, z))
        if dist <= sr:
            count += 1
    return count


def main():
    """Main execution function."""
    nanobots = parse_input('input.md')

    # Sanity check
    if len(nanobots) == 0:
        print("Error: No nanobots found in input file")
        return 0

    strongest = find_strongest_nanobot(nanobots)
    result = count_in_range(nanobots, strongest)

    print(result)
    return result


if __name__ == "__main__":
    main()
