import re
import sys


def parse_input(filename):
    """Parse the input file to extract position and velocity data."""
    points = []
    pattern = r'position=<\s*(-?\d+),\s*(-?\d+)>\s+velocity=<\s*(-?\d+),\s*(-?\d+)>'

    try:
        with open(filename, 'r') as f:
            for line in f:
                match = re.match(pattern, line.strip())
                if match:
                    px, py, vx, vy = map(int, match.groups())
                    points.append((px, py, vx, vy))
                elif line.strip():  # Non-empty line that didn't match
                    print(f"Warning: Could not parse line: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        return []

    return points


def calculate_positions(points, t):
    """Calculate positions of all points at time t."""
    positions = []
    for px, py, vx, vy in points:
        x = px + t * vx
        y = py + t * vy
        positions.append((x, y))
    return positions


def get_bounding_box(positions):
    """Get bounding box coordinates (min_x, min_y, max_x, max_y)."""
    if not positions:
        return (0, 0, 0, 0)

    xs = [x for x, y in positions]
    ys = [y for x, y in positions]

    return (min(xs), min(ys), max(xs), max(ys))


def get_bounding_box_area(positions):
    """Calculate the area of the bounding box."""
    min_x, min_y, max_x, max_y = get_bounding_box(positions)
    width = max_x - min_x
    height = max_y - min_y
    return width * height


def find_alignment_time(points):
    """Find the time when points are most aligned (minimum bounding box area)."""
    t = 0
    prev_area = float('inf')
    MAX_ITERATIONS = 100000

    while t < MAX_ITERATIONS:
        positions = calculate_positions(points, t)
        current_area = get_bounding_box_area(positions)

        if current_area > prev_area:
            # Area is increasing, previous t was the minimum
            return max(0, t - 1)

        prev_area = current_area
        t += 1

    raise RuntimeError("Failed to find alignment within iteration limit")


def visualize_points(positions):
    """Visualize points as a grid of characters."""
    min_x, min_y, max_x, max_y = get_bounding_box(positions)

    # Normalize coordinates to start at (0, 0)
    point_set = {(x - min_x, y - min_y) for (x, y) in positions}

    # Create visualization
    lines = []
    for y in range(max_y - min_y + 1):
        row = ""
        for x in range(max_x - min_x + 1):
            row += '#' if (x, y) in point_set else ' '
        lines.append(row)

    return '\n'.join(lines)


def extract_letters(message_visual):
    """Extract individual letters from the visual message."""
    lines = message_visual.split('\n')
    if not lines:
        return []

    width = max(len(line) for line in lines)
    height = len(lines)

    # Pad all lines to same width
    lines = [line.ljust(width) for line in lines]

    # Find columns with content
    columns_with_content = []
    for col in range(width):
        has_content = any(lines[row][col] == '#' for row in range(height))
        if has_content:
            columns_with_content.append(col)

    if not columns_with_content:
        return []

    # Find gaps (2+ consecutive spaces) to determine letter boundaries
    gaps = []
    for i in range(len(columns_with_content) - 1):
        gap_size = columns_with_content[i+1] - columns_with_content[i] - 1
        if gap_size >= 2:
            gaps.append((columns_with_content[i] + 1, columns_with_content[i+1] - 1))

    # Determine letter boundaries
    letter_boundaries = []
    start = 0
    for gap_start, gap_end in gaps:
        letter_boundaries.append((start, gap_start - 1))
        start = gap_end + 1
    letter_boundaries.append((start, width - 1))

    # Extract each letter
    letters = []
    for start, end in letter_boundaries:
        letter_lines = []
        for row in range(height):
            segment = lines[row][start:end+1]
            letter_lines.append(segment)
        letters.append(letter_lines)

    return letters


def recognize_letter(letter_lines):
    """Recognize a single letter from its visual pattern."""
    # Standard 10-row letter patterns (6 chars wide)
    patterns = {
        'A': ['  ##  ', ' #  # ', '#    #', '#    #', '######', '#    #', '#    #', '#    #', '#    #', '#    #'],
        'B': ['##### ', '#    #', '#    #', '#    #', '##### ', '#    #', '#    #', '#    #', '#    #', '##### '],
        'C': [' #### ', '#    #', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#    #', ' #### '],
        'E': ['######', '#     ', '#     ', '#     ', '##### ', '#     ', '#     ', '#     ', '#     ', '######'],
        'F': ['######', '#     ', '#     ', '#     ', '##### ', '#     ', '#     ', '#     ', '#     ', '#     '],
        'G': [' #### ', '#    #', '#     ', '#     ', '#     ', '#  ###', '#    #', '#    #', '#   ##', ' ### #'],
        'H': ['#    #', '#    #', '#    #', '#    #', '######', '#    #', '#    #', '#    #', '#    #', '#    #'],
        'J': ['    ##', '     #', '     #', '     #', '     #', '     #', '     #', '#    #', '#    #', ' #### '],
        'K': ['#    #', '#   # ', '#  #  ', '# #   ', '##    ', '# #   ', '#  #  ', '#   # ', '#    #', '#    #'],
        'L': ['#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '#     ', '######'],
        'N': ['#    #', '##   #', '##   #', '# #  #', '# #  #', '#  # #', '#  # #', '#   ##', '#   ##', '#    #'],
        'P': ['##### ', '#    #', '#    #', '#    #', '##### ', '#     ', '#     ', '#     ', '#     ', '#     '],
        'R': ['##### ', '#    #', '#    #', '#    #', '##### ', '#  #  ', '#   # ', '#   # ', '#    #', '#    #'],
        'X': ['#    #', '#    #', ' #  # ', ' #  # ', '  ##  ', '  ##  ', ' #  # ', ' #  # ', '#    #', '#    #'],
        'Z': ['######', '     #', '     #', '    # ', '   #  ', '  #   ', ' #    ', '#     ', '#     ', '######'],
    }

    # Try to match the letter
    for char, pattern in patterns.items():
        if len(letter_lines) != len(pattern):
            continue
        # Check if lines match (with flexible width)
        matches = True
        for i in range(len(letter_lines)):
            # Normalize both to 6 chars and compare
            l1 = letter_lines[i].ljust(6)[:6]
            l2 = pattern[i]
            if l1 != l2:
                matches = False
                break
        if matches:
            return char

    return '?'


def read_message(message_visual):
    """Read the message from the visual representation."""
    letters = extract_letters(message_visual)
    message = ''
    for letter_lines in letters:
        char = recognize_letter(letter_lines)
        message += char
    return message


def main(input_file='input.md'):
    """Main function to orchestrate the solution."""
    # Parse input
    points = parse_input(input_file)
    if not points:
        print("Error: No valid points parsed from input")
        return

    print(f"Parsed {len(points)} points")

    # Find alignment time
    print("Finding alignment time...")
    alignment_time = find_alignment_time(points)

    # Get positions at alignment time
    aligned_positions = calculate_positions(points, alignment_time)

    # Visualize
    message_visual = visualize_points(aligned_positions)

    # Read the message
    message = read_message(message_visual)

    # Output
    print(f"\nMessage appears at t={alignment_time}")
    print("\nMessage (visual):")
    print(message_visual)
    print(f"\nMessage (text): {message}")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    main(input_file)
