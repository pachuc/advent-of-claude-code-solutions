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


def normalize_pattern(state):
    """
    Normalize the state to make it position-independent.
    Returns the pattern relative to the leftmost plant.

    Args:
        state: Set of pot indices with plants

    Returns:
        frozenset: Relative positions (offset from leftmost plant)
    """
    if not state:
        return frozenset()

    min_pot = min(state)
    # Create a normalized pattern by subtracting the minimum
    normalized = frozenset(pot - min_pot for pot in state)
    return normalized


def verify_pattern_consistency(state, expected_normalized, rules, num_checks=3):
    """
    Verify that the pattern continues to match over the next few generations.

    This ensures we have a true steady state (consistent shift) rather than
    a longer cycle or temporary pattern match.

    Args:
        state: Current state to verify from
        expected_normalized: The normalized pattern we expect to see
        rules: Spreading rules
        num_checks: Number of generations to verify (default 3)

    Returns:
        bool: True if pattern is consistent, False otherwise
    """
    test_state = state
    for _ in range(num_checks):
        test_state = simulate_generation(test_state, rules)
        test_normalized = normalize_pattern(test_state)
        if test_normalized != expected_normalized:
            return False
    return True


def detect_steady_state(initial_state, rules, max_generations=1000):
    """
    Simulate until pattern stabilizes or max_generations reached.

    Note on generation numbering:
        - gen=0 represents the initial state (before any simulation)
        - gen=1 represents state after 1 generation of simulation
        - When we check at loop iteration gen=N, we're checking the state
          after N generations have been simulated

    Returns:
        tuple: (generation_number, state, sum_of_indices, prev_gen, prev_state, prev_sum)
               If no pattern found: last 3 values will be None

    Algorithm:
        1. Track pattern history: {normalized_pattern: (generation, state, sum)}
        2. For each generation:
            a. Normalize the pattern (relative positions)
            b. Check if this normalized pattern was seen before
            c. If yes: verify shift is consistent over next few generations
            d. If no: continue simulating
        3. Return when stable pattern confirmed or max_generations reached
    """
    state = initial_state
    history = {}

    for gen in range(max_generations):
        normalized = normalize_pattern(state)
        current_sum = sum(state)

        if normalized in history:
            # Pattern repeats! Verify it's truly stable
            prev_gen, prev_state, prev_sum = history[normalized]

            # Verify consistency by checking next 3 generations
            if verify_pattern_consistency(state, normalized, rules, num_checks=3):
                return (gen, state, current_sum, prev_gen, prev_state, prev_sum)
            # If verification fails, continue (though this should be rare)

        history[normalized] = (gen, state, current_sum)
        state = simulate_generation(state, rules)

    # Fallback: return last state if no pattern found
    return (max_generations, state, sum(state), None, None, None)


def calculate_rate_of_change(gen, current_sum, prev_gen, prev_sum):
    """
    Calculate the rate at which the sum changes per generation.

    Args:
        gen: Current generation where pattern repeated
        current_sum: Sum of pot indices at current generation
        prev_gen: Previous generation where this pattern appeared
        prev_sum: Sum at previous generation

    Returns:
        int: Change in sum per generation
    """
    generations_elapsed = gen - prev_gen
    sum_change = current_sum - prev_sum

    # Verify the rate is an exact integer (should always be true for this problem)
    assert sum_change % generations_elapsed == 0, \
        f"Rate should be exact integer: {sum_change} / {generations_elapsed}"

    # Rate of change per generation
    rate = sum_change // generations_elapsed

    return rate


def extrapolate_to_target(target_generation, steady_gen, steady_sum, rate):
    """
    Extrapolate the sum at target generation using steady state.

    Args:
        target_generation: Target (50 billion)
        steady_gen: Generation where steady state was detected
        steady_sum: Sum at steady state generation
        rate: Change in sum per generation

    Returns:
        int: Projected sum at target generation
    """
    remaining_generations = target_generation - steady_gen
    final_sum = steady_sum + (remaining_generations * rate)

    return final_sum


def main(verbose=False):
    """
    Main function to solve Part 2.

    Args:
        verbose: If True, print debugging information

    Returns:
        int: The final sum at 50 billion generations
    """
    TARGET_GENERATION = 50_000_000_000

    # Parse input (reuse Part 1)
    initial_state, rules = parse_input('input.md')

    # Detect steady state
    result = detect_steady_state(initial_state, rules, max_generations=1000)
    gen, state, current_sum, prev_gen, prev_state, prev_sum = result

    # Check if steady state was found
    if prev_gen is None:
        # No pattern found - should not happen with valid input
        print("No steady state detected")
        return None

    # Calculate rate of change
    rate = calculate_rate_of_change(gen, current_sum, prev_gen, prev_sum)

    if verbose:
        print(f"Steady state detected at generation {gen}")
        print(f"Previous occurrence at generation {prev_gen}")
        print(f"Pattern repeats every {gen - prev_gen} generation(s)")
        print(f"Current sum: {current_sum}")
        print(f"Rate of change: {rate} per generation")
        print(f"Number of plants: {len(state)}")
        print(f"Extrapolating to generation {TARGET_GENERATION:,}...")

    # Extrapolate to 50 billion
    final_sum = extrapolate_to_target(TARGET_GENERATION, gen, current_sum, rate)

    print(final_sum)
    return final_sum


if __name__ == '__main__':
    main()
