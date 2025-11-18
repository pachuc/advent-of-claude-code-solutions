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

def perform_dance(programs, moves):
    """
    Execute one complete dance sequence on the programs.

    Args:
        programs: List of program names (will be modified in-place)
        moves: List of move strings

    Note: Modifies programs in-place for efficiency.
    """
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

def find_cycle_length(initial_state, moves):
    """
    Find the cycle length by repeatedly applying the dance
    until we return to the initial state.

    Args:
        initial_state: The starting configuration (list)
        moves: List of move strings

    Returns:
        The number of iterations to return to initial_state
    """
    current = initial_state.copy()
    cycle_length = 0

    while True:
        # Apply one complete dance
        perform_dance(current, moves)
        cycle_length += 1

        # Check if we've returned to initial state
        if current == initial_state:
            return cycle_length

        # Safety check to prevent infinite loops
        if cycle_length > 10_000_000:
            raise Exception(f"Cycle detection exceeded limit. Something is wrong.")

def verify_part1(moves):
    """
    Verify that one iteration produces the Part 1 answer.
    This is a critical sanity check.
    """
    initial = list('abcdefghijklmnop')
    perform_dance(initial, moves)
    result = ''.join(initial)

    expected = 'eojfmbpkldghncia'
    if result == expected:
        print(f"✓ Part 1 verification passed: {result}")
        return True
    else:
        print(f"✗ Part 1 verification FAILED!")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        return False

def solve(target_iterations=1_000_000_000):
    """
    Solve the permutation problem for a given number of iterations.

    Args:
        target_iterations: Number of times to apply the dance (default: 1 billion)

    Returns:
        String representing the final program order
    """
    # Read and parse input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()

    # Parse moves, filtering out empty strings
    moves = [m for m in input_data.split(',') if m]

    # Initial state: programs in alphabetical order
    initial = list('abcdefghijklmnop')

    # Find cycle length
    print("Finding cycle length...")
    cycle_length = find_cycle_length(initial, moves)
    print(f"Cycle detected at length: {cycle_length}")

    # Calculate effective iterations using modulo arithmetic
    effective_iterations = target_iterations % cycle_length

    # Edge case: If modulo is 0, we're at a multiple of the cycle length
    # We want the state at the end of a full cycle, not iteration 0
    if effective_iterations == 0:
        effective_iterations = cycle_length

    print(f"Effective iterations needed: {target_iterations} % {cycle_length} = {effective_iterations}")

    # Apply the dance effective_iterations times
    current = initial.copy()
    for i in range(effective_iterations):
        perform_dance(current, moves)

    result = ''.join(current)
    print(f"Final result after {target_iterations} iterations: {result}")

    return result

def main():
    """Main entry point."""
    # Read and parse input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]

    # Verify against Part 1 answer first
    print("Verifying Part 1 answer...")
    if not verify_part1(moves):
        print("ERROR: Part 1 verification failed. Aborting.")
        return

    # Solve Part 2
    print("\nSolving Part 2...")
    result = solve(1_000_000_000)

    # Output final answer
    print(f"\nFinal Answer: {result}")

if __name__ == '__main__':
    main()
