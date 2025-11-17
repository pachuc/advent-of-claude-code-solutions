import hashlib
import sys

# Set recursion limit to handle deep path exploration
sys.setrecursionlimit(5000)


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


def dfs_explore(x, y, path, passcode, max_depth=5000):
    """
    Recursively explore all paths using DFS.
    Returns the maximum length of any path that reaches the vault.
    """
    # Safety limit to prevent excessive recursion
    if len(path) > max_depth:
        return 0

    # Base case: reached the vault
    if (x, y) == (3, 3):
        return len(path)

    # Explore all valid moves from current position
    max_length = 0
    for new_x, new_y, direction in get_valid_moves(x, y, passcode, path):
        new_path = path + direction
        branch_length = dfs_explore(new_x, new_y, new_path, passcode, max_depth)
        max_length = max(max_length, branch_length)

    # If no valid moves existed, max_length remains 0 (dead end)
    return max_length


def find_longest_path(passcode):
    """
    Find the length of the longest path to the vault.
    Uses DFS to exhaustively explore all possible paths.
    Returns 0 if no path exists to the vault.
    """
    return dfs_explore(0, 0, "", passcode)


def main():
    """Main entry point"""
    try:
        # Read passcode from input file
        with open('input.md', 'r') as f:
            passcode = f.read().strip()

        if not passcode:
            print("Error: Empty passcode")
            return

        # Find longest path length
        result = find_longest_path(passcode)
        print(result)

    except FileNotFoundError:
        print("Error: input.md not found")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
