def spin(programs, x):
    """Rotate last x programs to the front (modifies in-place)"""
    if x == 0:
        return
    programs[:] = programs[-x:] + programs[:-x]

def exchange(programs, a, b):
    """Swap programs at positions a and b (modifies in-place)"""
    programs[a], programs[b] = programs[b], programs[a]

def partner(programs, name_a, name_b):
    """Swap programs named name_a and name_b (modifies in-place)"""
    idx_a = programs.index(name_a)
    idx_b = programs.index(name_b)
    programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]

def main():
    # Read input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()

    # Parse moves
    moves = input_data.split(',')

    # Initialize programs
    programs = list('abcdefghijklmnop')

    # Execute each move
    for move in moves:
        if not move:  # Skip empty strings
            continue

        if move[0] == 's':
            x = int(move[1:])
            spin(programs, x)

        elif move[0] == 'x':
            parts = move[1:].split('/')
            a, b = int(parts[0]), int(parts[1])
            exchange(programs, a, b)

        elif move[0] == 'p':
            parts = move[1:].split('/')
            name_a, name_b = parts[0], parts[1]
            partner(programs, name_a, name_b)

    # Output result
    result = ''.join(programs)
    print(result)

if __name__ == '__main__':
    main()
