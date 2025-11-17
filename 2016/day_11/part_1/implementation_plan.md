# Implementation Plan: RTG and Microchip Transportation Puzzle

## Problem Analysis

This is a classic state-space search problem similar to the "Bridge and Torch" or "River Crossing" puzzles. We need to find the minimum number of steps to move all items to floor 4 while respecting safety constraints.

**Key Observations:**
- We have 5 element types: strontium, plutonium, thulium, ruthenium, curium (10 items total)
- State space can be large but is finite
- BFS guarantees finding the minimum steps
- State representation and hashing are critical for performance

## Algorithm Choice: Breadth-First Search (BFS)

**Why BFS?**
- Guarantees optimal solution (minimum steps)
- Explores states level by level
- First goal state found = shortest path

**Time Complexity:** O(b^d) where b is branching factor, d is depth
**Space Complexity:** O(b^d) for visited states

**Floor Numbering Convention:**
- Internal representation uses 0-indexed floors (0, 1, 2, 3)
- Input uses natural language: "first floor" → 0, "second floor" → 1, "third floor" → 2, "fourth floor" → 3
- Goal: All items on floor 3 (the "fourth floor")

## Implementation Steps

### Step 1: Input Parsing
**File:** `solution.py`

Create a function to parse the input text:
```python
def parse_input(input_text: str) -> dict
```

**Logic:**
1. Split input into lines (one per floor)
2. For each line, extract:
   - Element names using regex (e.g., "strontium", "plutonium")
   - Item type (generator vs microchip)
3. Build initial state representation
4. Return: Dictionary mapping floor numbers (0-3) to sets of items

**Regex patterns needed:**
- `(\w+) generator` - captures generator type
- `(\w+)-compatible microchip` - captures microchip type

**Floor mapping:**
- "first floor" → index 0
- "second floor" → index 1
- "third floor" → index 2
- "fourth floor" → index 3

**Output format:**
```python
{
    0: {('strontium', 'G'), ('strontium', 'M'), ('plutonium', 'G'), ('plutonium', 'M')},
    1: {('thulium', 'G'), ('ruthenium', 'G'), ('ruthenium', 'M'), ('curium', 'G'), ('curium', 'M')},
    2: {('thulium', 'M')},
    3: set()
}
```

### Step 2: State Representation
**Class:** `State`

Design an immutable, hashable state representation:

```python
@dataclass(frozen=True)
class State:
    elevator_floor: int  # 0-3
    floors: tuple[frozenset, frozenset, frozenset, frozenset]
```

**Why this design?**
- Immutable (frozen=True) allows hashing for visited set
- Tuple of frozensets for floor contents
- Elevator position is critical for valid moves

**Key methods:**
- `is_valid()` - checks safety constraints (called when generating new states)
- `is_goal()` - checks if all items on floor 3 (called when dequeuing from BFS)
- `__hash__()` and `__eq__()` - for set membership

**When to validate:**
- Initial state: Validate once before starting BFS
- New states: Call `is_valid()` before adding to queue
- Dequeued states: Call `is_goal()` to check if we've reached the solution

### Step 3: Safety Validation
**Function:** `is_safe_floor(floor_items: frozenset) -> bool`

Implement the microchip frying rule:

**Logic:**
1. Extract all generators on floor
2. Extract all microchips on floor
3. If no generators present → safe
4. For each microchip:
   - Check if its matching generator is present
   - If not, and other generators exist → UNSAFE
5. Return True if all microchips are safe

**Edge cases:**
- Empty floor: safe
- Only generators: safe
- Only microchips: safe
- Microchip + its own generator + other generators: safe
- Microchip without its generator + any other generator: UNSAFE

### Step 4: Move Generation
**Function:** `generate_valid_moves(state: State) -> list[State]`

Generate all valid next states from current state:

**Logic:**
1. Get current floor items where elevator is
2. **Edge case:** If current floor is empty, no moves possible (dead-end state)
3. Generate all possible item combinations to carry:
   - Single items: C(n, 1) combinations
   - Two items: C(n, 2) combinations
   - Note: Elevator MUST carry at least 1 item (per problem constraints)
4. For each direction (up/down):
   - Skip if at boundary (floor 0 can't go down, floor 3 can't go up)
   - Create new state with items moved
   - Validate both source floor (after removal) and destination floor (after addition)
   - Add to valid moves if both floors are safe
5. Return list of valid states

**Note on move ordering:** In BFS, all moves at a given depth are explored before moving to the next depth, so move ordering doesn't affect optimality. We generate both up and down moves without prioritization.

### Step 5: State Equivalence Optimization
**Function:** `canonicalize_state(state: State) -> State`

**Critical optimization:** States that differ only in element names are equivalent!

Example: `{('A','G'), ('A','M')}` is equivalent to `{('B','G'), ('B','M')}`

**Why this works:**
- The puzzle is symmetric with respect to element names
- Only the pattern of generators/microchips and their floor positions matters
- A strontium generator behaves identically to a plutonium generator
- What matters is the relationship: which microchips are paired with their generators, and where they are
- Reduces visited states by orders of magnitude

**Concrete Algorithm:**

```python
def canonicalize_state(state: State) -> State:
    # Step 1: Extract all unique element names
    elements = set()
    for floor in state.floors:
        for element, item_type in floor:
            elements.add(element)

    # Step 2: For each element, create a signature (gen_floor, chip_floor)
    # where gen_floor is the floor index of the generator (or -1 if not found)
    # and chip_floor is the floor index of the microchip (or -1 if not found)
    element_signatures = []
    for elem in elements:
        gen_floor = -1
        chip_floor = -1
        for floor_idx, floor in enumerate(state.floors):
            if (elem, 'G') in floor:
                gen_floor = floor_idx
            if (elem, 'M') in floor:
                chip_floor = floor_idx
        element_signatures.append((gen_floor, chip_floor))

    # Step 3: Sort signatures to get canonical ordering
    # Elements with same signature pattern are interchangeable
    element_signatures.sort()

    # Step 4: Create mapping from old elements to new canonical names
    sorted_elements = sorted(elements)  # Need consistent ordering
    element_map = {}
    signature_to_elements = {}

    for elem in sorted_elements:
        # Find this element's signature
        gen_floor = -1
        chip_floor = -1
        for floor_idx, floor in enumerate(state.floors):
            if (elem, 'G') in floor:
                gen_floor = floor_idx
            if (elem, 'M') in floor:
                chip_floor = floor_idx
        sig = (gen_floor, chip_floor)

        if sig not in signature_to_elements:
            signature_to_elements[sig] = []
        signature_to_elements[sig].append(elem)

    # Assign canonical names based on sorted signatures
    canonical_id = 0
    for sig in sorted(signature_to_elements.keys()):
        for elem in sorted(signature_to_elements[sig]):
            element_map[elem] = f'elem{canonical_id}'
            canonical_id += 1

    # Step 5: Rebuild state with canonical names
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
```

**Key insights:**
- Elements are grouped by their signature: (generator_floor, microchip_floor)
- Elements with identical signatures are truly interchangeable
- Elevator position is preserved (it's not subject to canonicalization)
- This ensures states are equivalent only if they're truly strategically identical

### Step 6: BFS Search
**Function:** `solve(initial_state: State) -> int`

Implement BFS to find minimum steps:

**Algorithm:**
```python
def solve(initial_state):
    queue = deque([(initial_state, 0)])  # (state, steps)
    visited = {canonicalize_state(initial_state)}

    while queue:
        state, steps = queue.popleft()

        if state.is_goal():
            return steps

        for next_state in generate_valid_moves(state):
            canonical = canonicalize_state(next_state)
            if canonical not in visited:
                visited.add(canonical)
                queue.append((next_state, steps + 1))

    return -1  # No solution found
```

**Key points:**
- Use deque for O(1) popleft operations
- Track steps alongside states
- Canonicalize before checking visited
- Return steps when goal found

### Step 7: Main Function
**Function:** `main()`

Orchestrate the solution:

```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Parse input
    initial_floors = parse_input(input_text)

    # Create initial state
    initial_state = State(
        elevator_floor=0,
        floors=tuple(initial_floors[i] for i in range(4))
    )

    # Solve
    min_steps = solve(initial_state)

    # Output result
    print(min_steps)
```

## Data Structures Summary

1. **State representation:** Immutable dataclass with tuple of frozensets
2. **Queue:** `collections.deque` for BFS
3. **Visited set:** `set` of canonicalized states
4. **Floor contents:** `frozenset` of (element, type) tuples

## Expected Performance

**For the given input (10 items, 5 element pairs):**
- Without canonicalization: potentially 100,000+ states
- With canonicalization: estimated 10,000-50,000 states (rough approximation)
- Target runtime: < 5 seconds (ideally < 1 second)
- Memory usage: < 500 MB

**Important notes:**
- These are rough estimates; actual performance will be measured during testing
- State space size depends heavily on canonicalization effectiveness
- If performance is inadequate, consider A* search with heuristic (e.g., number of items not on floor 3)

## Implementation Order

1. Start with input parsing and test with given input
2. Implement State class with validation
3. Implement safety checking function
4. Implement move generation
5. Implement basic BFS without canonicalization
6. Test with simple examples
7. Add canonicalization optimization
8. Final testing with actual input

## Potential Pitfalls

1. **Off-by-one errors:** Floors are 0-indexed (0-3) but described as 1-4 in input
2. **Immutability:** Forgetting to use frozenset/tuple breaks hashing
3. **Safety checking:** Edge cases with empty floors or all same type
4. **State explosion:** Without canonicalization, may run out of memory
5. **Boundary conditions:** Elevator can't go below 0 or above 3
6. **Empty floor edge case:** If elevator ends up on empty floor, it's stuck (no moves possible)
7. **Canonicalization bugs:** Incorrectly treating non-equivalent states as equivalent would break correctness

## Error Handling

**Input parsing errors:**
- Malformed input lines → exit with error message
- Inconsistent item counts → validate total generators = total microchips

**No solution found:**
- BFS queue exhausted without finding goal → return -1 or error message
- This shouldn't happen with valid input, but good to handle

**Resource limits:**
- If visited states exceed reasonable limit (e.g., 1,000,000), exit with error
- If runtime exceeds timeout (e.g., 60 seconds), exit with error

**Note:** Since this is a script for a specific puzzle, extensive error handling is not required, but basic validation helps with debugging.
