def parse_input(filename):
    """Parse input file and return list of component tuples."""
    components = []
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                a, b = line.split('/')
                components.append((int(a), int(b)))
            except (ValueError, AttributeError):
                # Skip malformed lines
                continue
    return components


def build_port_index(components):
    """Build a mapping from port number to list of component indices."""
    port_map = {}
    for i, (a, b) in enumerate(components):
        port_map.setdefault(a, []).append(i)
        if a != b:  # Avoid duplicates for same-port components
            port_map.setdefault(b, []).append(i)
    return port_map


def find_longest_strongest(components, port_map, current_port, used, current_length, current_strength):
    """
    Find the longest bridge, and among those, the strongest using DFS with backtracking.

    Args:
        components: List of all available components (tuples)
        port_map: Dictionary mapping port number to list of component indices
        current_port: The port type we need to match next
        used: Set of indices of components already used
        current_length: Number of components used so far
        current_strength: Accumulated strength so far

    Returns:
        Tuple of (length, strength) for the longest and strongest bridge from this state
    """
    # Current state is always valid (represents a complete bridge)
    best = (current_length, current_strength)

    # Try all unused components that have the current_port
    for component_index in port_map.get(current_port, []):
        if component_index in used:
            continue

        port_a, port_b = components[component_index]

        # Determine which end connects and which is free
        if port_a == current_port:
            next_port = port_b
        else:  # port_b == current_port
            next_port = port_a

        # Calculate strength of this component
        component_strength = port_a + port_b

        # Explore this branch
        used.add(component_index)
        result = find_longest_strongest(
            components,
            port_map,
            next_port,
            used,
            current_length + 1,  # Increment length
            current_strength + component_strength
        )
        used.remove(component_index)  # Backtrack

        # Compare: prioritize longer, then stronger
        if result[0] > best[0] or (result[0] == best[0] and result[1] > best[1]):
            best = result

    return best


def solve(components):
    """Solve the bridge building problem for Part 2."""
    port_map = build_port_index(components)
    used = set()
    length, strength = find_longest_strongest(
        components,
        port_map,
        current_port=0,
        used=used,
        current_length=0,
        current_strength=0
    )
    return strength


def main():
    components = parse_input('input.md')
    result = solve(components)
    print(result)


if __name__ == '__main__':
    main()
