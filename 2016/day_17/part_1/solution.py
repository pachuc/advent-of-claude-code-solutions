import hashlib
from collections import deque


def get_open_doors(passcode, path):
    """
    Return tuple of 4 booleans for U, D, L, R door states.
    Door is open if hash character is in 'bcdef'.
    """
    hash_input = passcode + path
    hash_result = hashlib.md5(hash_input.encode()).hexdigest()[:4]
    return tuple(c in 'bcdef' for c in hash_result)


def get_valid_moves(x, y, passcode, path):
    """
    Return list of valid (new_x, new_y, direction) tuples.
    Considers both door states and grid boundaries.
    """
    doors = get_open_doors(passcode, path)
    valid_moves = []

    # Check each direction: Up, Down, Left, Right
    # Up: y-1, door[0]
    if doors[0] and y > 0:
        valid_moves.append((x, y - 1, 'U'))

    # Down: y+1, door[1]
    if doors[1] and y < 3:
        valid_moves.append((x, y + 1, 'D'))

    # Left: x-1, door[2]
    if doors[2] and x > 0:
        valid_moves.append((x - 1, y, 'L'))

    # Right: x+1, door[3]
    if doors[3] and x < 3:
        valid_moves.append((x + 1, y, 'R'))

    return valid_moves


def find_shortest_path(passcode):
    """
    BFS to find shortest path from (0,0) to (3,3).
    Returns the path string (e.g., "DDRRRD") or None if no path exists.
    """
    # Initialize BFS queue with starting position
    queue = deque([(0, 0, "")])

    while queue:
        x, y, path = queue.popleft()

        # Check if we reached the goal
        if (x, y) == (3, 3):
            return path

        # Safety check: limit maximum path length
        if len(path) >= 1000:
            continue

        # Explore all valid moves
        for new_x, new_y, direction in get_valid_moves(x, y, passcode, path):
            new_path = path + direction
            queue.append((new_x, new_y, new_path))

    # No path found
    return None


def main():
    """Main entry point"""
    try:
        # Read passcode from input file
        with open('input.md', 'r') as f:
            passcode = f.read().strip()

        if not passcode:
            print("Error: Empty passcode")
            return

        # Find shortest path
        result = find_shortest_path(passcode)

        if result:
            print(result)
        else:
            print("No path found")

    except FileNotFoundError:
        print("Error: input.md not found")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
