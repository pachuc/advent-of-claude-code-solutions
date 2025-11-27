from collections import deque
import re


def parse_input(input_text):
    """
    Parse input like: "463 players; last marble is worth 71787 points"
    Returns: (num_players, last_marble)
    """
    match = re.search(r'(\d+) players.*?(\d+) points', input_text)
    num_players = int(match.group(1))
    last_marble = int(match.group(2))
    return num_players, last_marble


def simulate_marble_game(num_players, last_marble, debug=False):
    """
    Simulate the marble game and return highest score

    Args:
        num_players: Number of players in the game
        last_marble: Value of the last marble to place
        debug: If True, print game state for small examples (<=25 marbles)

    Returns:
        Highest score among all players
    """
    # Initialize circle with marble 0
    # Keep current marble always at index 0 (rotate as needed)
    circle = deque([0])

    # Initialize player scores (index 0 unused, players 1 to num_players)
    scores = [0] * (num_players + 1)

    # Process each marble from 1 to last_marble
    for marble in range(1, last_marble + 1):
        # Determine current player (1-indexed)
        current_player = (marble - 1) % num_players + 1

        if marble % 23 == 0:
            # Special placement
            scores[current_player] += marble
            # Move 7 positions counter-clockwise (rotate right by 7)
            circle.rotate(7)
            # Remove and score the marble at position 0
            removed = circle.popleft()
            scores[current_player] += removed
            # Marble at new position 0 is the new current

            if debug and last_marble <= 25:
                print(f"Marble {marble} (P{current_player}): SPECIAL - kept {marble}, removed {removed}, score now {scores[current_player]}")
        else:
            # Standard placement
            # Rotate to move position 2 (clockwise) to position 0
            circle.rotate(-2)
            # Insert new marble at position 0 (it becomes the new current)
            circle.appendleft(marble)

            if debug and last_marble <= 25:
                # For debug, show in canonical order (starting from 0)
                temp = list(circle)
                pos_0 = temp.index(0)
                ordered = temp[pos_0:] + temp[:pos_0]
                current_val = circle[0]
                current_idx = ordered.index(current_val)
                display = []
                for i, v in enumerate(ordered):
                    if i == current_idx:
                        display.append(f'({v})')
                    else:
                        display.append(str(v))
                print(f"Marble {marble} (P{current_player}): {' '.join(display)}")

    # Return highest score
    return max(scores)


def main():
    """
    Read input, run simulation, output result
    """
    # Read from input.md
    with open('input.md', 'r') as f:
        input_text = f.read().strip()

    # Parse input
    num_players, last_marble = parse_input(input_text)

    # Run simulation
    result = simulate_marble_game(num_players, last_marble)

    # Print result
    print(result)


if __name__ == "__main__":
    main()
