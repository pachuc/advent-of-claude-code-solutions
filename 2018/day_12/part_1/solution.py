def parse_input(filename):
    """Parse the input file to extract initial state and rules."""
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Parse initial state from first line
    initial_state = set()
    first_line = lines[0].strip()
    state_string = first_line.split(': ')[1]

    for i, char in enumerate(state_string):
        if char == '#':
            initial_state.add(i)

    # Parse rules from remaining lines
    rules = {}
    for line in lines[1:]:
        line = line.strip()
        if line and '=>' in line:
            pattern, result = line.split(' => ')
            rules[pattern] = result

    return initial_state, rules


def get_pattern(pot, state):
    """Get the 5-character pattern for a given pot position."""
    pattern = ""
    for i in range(pot - 2, pot + 3):
        pattern += '#' if i in state else '.'
    return pattern


def simulate_generation(state, rules):
    """Simulate one generation of plant growth."""
    # Handle empty state edge case
    if not state:
        return set()

    next_state = set()
    # Expand range by 2 in each direction since rules check 2 pots away
    min_pot = min(state) - 2
    max_pot = max(state) + 2

    for pot in range(min_pot, max_pot + 1):
        pattern = get_pattern(pot, state)
        # Use .get() to default to '.' for patterns not in rules
        if rules.get(pattern, '.') == '#':
            next_state.add(pot)

    return next_state


def main():
    # Parse input
    initial_state, rules = parse_input('input.md')

    # Run simulation for 20 generations
    state = initial_state
    for generation in range(20):
        state = simulate_generation(state, rules)

    # Calculate and print the sum of pot indices with plants
    result = sum(state)
    print(result)


if __name__ == '__main__':
    main()
