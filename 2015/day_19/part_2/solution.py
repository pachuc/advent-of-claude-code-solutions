import re
from collections import deque


def parse_input(input_text):
    """
    Parse input to extract rules and target molecule.

    Args:
        input_text: Raw input string

    Returns:
        tuple: (rules, target) where rules is list of (source, target) tuples
               and target is the target molecule string
    """
    lines = input_text.strip().split('\n')
    rules = []
    target = None

    blank_found = False
    for line in lines:
        line = line.strip()

        if not line:
            blank_found = True
            continue

        if not blank_found and '=>' in line:
            parts = line.split(' => ')
            source = parts[0].strip()
            target_part = parts[1].strip()
            rules.append((source, target_part))
        elif blank_found and line:
            target = line
            break

    return rules, target


def count_elements(molecule):
    """
    Count individual elements in a molecule string.
    Elements are uppercase letter optionally followed by lowercase letter(s).

    Args:
        molecule: String representing the molecule

    Returns:
        int: Number of elements
    """
    # Match element symbols: Uppercase followed by optional lowercase letters
    elements = re.findall(r'[A-Z][a-z]*', molecule)
    return len(elements)


def solve_by_formula(target):
    """
    Solve using mathematical formula based on element counting.

    Formula: steps = num_elements - num_Rn - num_Ar - 2*num_Y - 1

    This works because:
    - Each step typically adds one element
    - Rn/Ar represent grouping (reduces effective steps)
    - Y represents separation (reduces effective steps)
    - Subtract 1 for starting from 'e'

    Args:
        target: Target molecule string

    Returns:
        int: Minimum number of steps
    """
    num_elements = count_elements(target)
    num_rn = target.count('Rn')
    num_ar = target.count('Ar')
    num_y = target.count('Y')

    steps = num_elements - num_rn - num_ar - 2 * num_y - 1

    return steps


def solve_by_greedy(rules, target):
    """
    Solve by greedily applying reverse replacements.

    Strategy:
    - Reverse all rules (target => source becomes source => target for backward)
    - Sort by length of pattern (longer first, then alphabetically for determinism)
    - Repeatedly find and replace until we reach 'e'

    Args:
        rules: List of (source, target) tuples
        target: Target molecule string

    Returns:
        int: Number of steps, or -1 if failed
    """
    if target == 'e':
        return 0

    # Reverse rules for backward search
    reversed_rules = [(tgt, src) for src, tgt in rules]

    # Sort by pattern length (longer first), then alphabetically for determinism
    reversed_rules.sort(key=lambda x: (-len(x[0]), x[0]))

    current = target
    steps = 0
    max_steps = len(target) * 10  # Scale with input size

    while current != 'e' and steps < max_steps:
        found = False

        for pattern, replacement in reversed_rules:
            if pattern in current:
                # Replace first occurrence
                current = current.replace(pattern, replacement, 1)
                steps += 1
                found = True
                break

        if not found:
            return -1  # No solution found

    if current == 'e':
        return steps
    else:
        return -1  # Exceeded max steps


def solve_by_bfs(rules, target):
    """
    Solve using BFS backward search from target to 'e'.
    Guaranteed to find minimum steps but potentially slower.

    Args:
        rules: List of (source, target) tuples
        target: Target molecule string

    Returns:
        int: Minimum number of steps, or -1 if not found
    """
    if target == 'e':
        return 0

    # Reverse rules
    reversed_rules = [(tgt, src) for src, tgt in rules]

    queue = deque([(target, 0)])
    visited = {target}
    max_steps = 1000

    while queue:
        current, steps = queue.popleft()

        if steps >= max_steps:
            return -1

        # Try all possible replacements
        for pattern, replacement in reversed_rules:
            # Find all occurrences
            idx = 0
            while idx < len(current):
                pos = current.find(pattern, idx)
                if pos == -1:
                    break

                # Create new molecule
                new_molecule = current[:pos] + replacement + current[pos + len(pattern):]

                if new_molecule == 'e':
                    return steps + 1

                # Only explore if shorter (pruning optimization)
                if new_molecule not in visited and len(new_molecule) < len(current):
                    visited.add(new_molecule)
                    queue.append((new_molecule, steps + 1))

                idx = pos + 1

    return -1  # No solution found


def solve(input_text, method='auto'):
    """
    Main solver function. Uses formula for complex molecules with Rn/Ar/Y structure.

    Strategy:
    1. If molecule has Rn/Ar/Y structure, use formula (fast and correct for AoC 2015 Day 19)
    2. Otherwise, use greedy (works for simple examples)
    3. Fall back to BFS if needed

    Args:
        input_text: Raw input string
        method: 'auto', 'formula', 'greedy', or 'bfs'

    Returns:
        int: Minimum number of steps
    """
    rules, target = parse_input(input_text)

    if method == 'formula':
        return solve_by_formula(target)

    if method == 'auto':
        # For molecules with Rn/Ar/Y structure, use formula (AoC 2015 Day 19 Part 2 pattern)
        if 'Rn' in target and 'Ar' in target:
            return solve_by_formula(target)
        # For simple molecules, use greedy
        else:
            greedy_result = solve_by_greedy(rules, target)
            if greedy_result != -1:
                return greedy_result

    if method == 'greedy' or method == 'auto':
        greedy_result = solve_by_greedy(rules, target)
        if greedy_result != -1:
            return greedy_result

    if method == 'bfs' or method == 'auto':
        result = solve_by_bfs(rules, target)
        return result

    return -1


def main():
    """Read input and solve the problem."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(result)


if __name__ == '__main__':
    main()
