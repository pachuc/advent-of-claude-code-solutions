import re
from collections import deque
from dataclasses import dataclass
from itertools import combinations

def parse_input(input_text):
    """Parse input text to extract initial floor states."""
    lines = input_text.strip().split('\n')
    floors = {0: set(), 1: set(), 2: set(), 3: set()}

    floor_mapping = {
        'first': 0,
        'second': 1,
        'third': 2,
        'fourth': 3
    }

    for line in lines:
        # Extract floor number
        floor_match = re.search(r'The (\w+) floor', line)
        if not floor_match:
            continue
        floor_num = floor_mapping[floor_match.group(1)]

        # Extract generators
        generators = re.findall(r'(\w+) generator', line)
        for gen in generators:
            floors[floor_num].add((gen, 'G'))

        # Extract microchips
        microchips = re.findall(r'(\w+)-compatible microchip', line)
        for chip in microchips:
            floors[floor_num].add((chip, 'M'))

    return floors


def is_safe_floor(floor_items):
    """Check if a floor configuration is safe (microchips won't fry)."""
    if not floor_items:
        return True

    generators = {elem for elem, item_type in floor_items if item_type == 'G'}
    microchips = {elem for elem, item_type in floor_items if item_type == 'M'}

    # If no generators, always safe
    if not generators:
        return True

    # Check each microchip
    for chip in microchips:
        # If microchip's generator is present, it's protected
        if chip not in generators:
            # Unprotected microchip with generators present - UNSAFE
            return False

    return True


@dataclass(frozen=True)
class State:
    """Immutable state representation."""
    elevator_floor: int
    floors: tuple  # tuple of frozensets

    def is_valid(self):
        """Check if state is valid (all floors are safe)."""
        return all(is_safe_floor(floor) for floor in self.floors)

    def is_goal(self):
        """Check if all items are on floor 3 (fourth floor)."""
        return all(len(self.floors[i]) == 0 for i in range(3)) and len(self.floors[3]) > 0


def generate_valid_moves(state):
    """Generate all valid next states from current state."""
    current_floor = state.elevator_floor
    current_items = state.floors[current_floor]

    # If current floor is empty, no moves possible
    if not current_items:
        return []

    valid_moves = []

    # Generate all possible item combinations to carry (1 or 2 items)
    items_list = list(current_items)
    item_combinations = []

    # Single items
    for item in items_list:
        item_combinations.append([item])

    # Two items
    for combo in combinations(items_list, 2):
        item_combinations.append(list(combo))

    # Try moving up and down
    directions = []
    if current_floor < 3:  # Can move up
        directions.append(current_floor + 1)
    if current_floor > 0:  # Can move down
        directions.append(current_floor - 1)

    for next_floor in directions:
        for items_to_move in item_combinations:
            # Create new floor configurations
            new_floors = list(state.floors)

            # Remove items from current floor
            new_current_floor = set(current_items)
            for item in items_to_move:
                new_current_floor.remove(item)

            # Add items to destination floor
            new_dest_floor = set(new_floors[next_floor])
            for item in items_to_move:
                new_dest_floor.add(item)

            # Check if both floors are safe
            if is_safe_floor(new_current_floor) and is_safe_floor(new_dest_floor):
                # Create new state
                new_floors[current_floor] = frozenset(new_current_floor)
                new_floors[next_floor] = frozenset(new_dest_floor)

                new_state = State(
                    elevator_floor=next_floor,
                    floors=tuple(new_floors)
                )

                valid_moves.append(new_state)

    return valid_moves


def canonicalize_state(state):
    """Convert state to canonical form for equivalence checking."""
    # Extract all unique element names
    elements = set()
    for floor in state.floors:
        for element, item_type in floor:
            elements.add(element)

    # For each element, create a signature (gen_floor, chip_floor)
    element_signatures = {}
    for elem in elements:
        gen_floor = -1
        chip_floor = -1
        for floor_idx, floor in enumerate(state.floors):
            if (elem, 'G') in floor:
                gen_floor = floor_idx
            if (elem, 'M') in floor:
                chip_floor = floor_idx
        element_signatures[elem] = (gen_floor, chip_floor)

    # Group elements by signature
    signature_to_elements = {}
    for elem, sig in element_signatures.items():
        if sig not in signature_to_elements:
            signature_to_elements[sig] = []
        signature_to_elements[sig].append(elem)

    # Assign canonical names based on sorted signatures
    element_map = {}
    canonical_id = 0
    for sig in sorted(signature_to_elements.keys()):
        for elem in sorted(signature_to_elements[sig]):
            element_map[elem] = f'elem{canonical_id}'
            canonical_id += 1

    # Rebuild state with canonical names
    new_floors = []
    for floor in state.floors:
        new_floor = frozenset(
            (element_map[elem], item_type)
            for elem, item_type in floor
        )
        new_floors.append(new_floor)

    return State(
        elevator_floor=state.elevator_floor,
        floors=tuple(new_floors)
    )


def solve(initial_state):
    """Use BFS to find minimum steps to goal state."""
    if not initial_state.is_valid():
        return -1

    if initial_state.is_goal():
        return 0

    queue = deque([(initial_state, 0)])
    visited = {canonicalize_state(initial_state)}

    while queue:
        state, steps = queue.popleft()

        for next_state in generate_valid_moves(state):
            if next_state.is_goal():
                return steps + 1

            canonical = canonicalize_state(next_state)
            if canonical not in visited:
                visited.add(canonical)
                queue.append((next_state, steps + 1))

    return -1  # No solution found


def main():
    # Read input
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input
    initial_floors = parse_input(input_text)

    # Create initial state (elevator starts on floor 0)
    initial_state = State(
        elevator_floor=0,
        floors=tuple(frozenset(initial_floors[i]) for i in range(4))
    )

    # Solve
    min_steps = solve(initial_state)

    # Output result
    print(min_steps)


if __name__ == '__main__':
    main()
