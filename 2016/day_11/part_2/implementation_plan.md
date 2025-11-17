# Implementation Plan - RTG Transportation Part 2

## Overview
Part 2 is an extension of Part 1 with 4 additional items on the first floor. The core algorithm from Part 1 can be reused with a modification to add the new items to the initial state.

## Core Strategy
- **Reuse Part 1 solution**: The BFS algorithm, state representation, safety validation, and canonicalization from `part_1_solution.py` are all applicable
- **Single modification needed**: Add 4 new items to the first floor during initialization
- **Algorithm**: BFS guarantees minimum steps; state canonicalization prevents redundant exploration of equivalent states

## Step-by-Step Implementation Plan

### Step 1: Copy and Adapt Part 1 Solution
- Start with `part_1_solution.py` as the foundation
- The following components require NO changes:
  - `is_safe_floor()` - safety validation logic
  - `State` class - state representation
  - `generate_valid_moves()` - move generation
  - `canonicalize_state()` - critical for performance with more items
  - `solve()` - BFS algorithm
  - Data structures and imports

### Step 2: Modify Initial State Setup
The ONLY code change needed is in the `main()` function:

**Current approach (Part 1):**
```python
# Parse input
initial_floors = parse_input(input_text)
```

**New approach (Part 2):**
```python
# Parse input
initial_floors = parse_input(input_text)

# Add the 4 new items to first floor
initial_floors[0].add(('elerium', 'G'))
initial_floors[0].add(('elerium', 'M'))
initial_floors[0].add(('dilithium', 'G'))
initial_floors[0].add(('dilithium', 'M'))
```

This adds:
- Elerium generator and microchip (matching pair)
- Dilithium generator and microchip (matching pair)

All items start on floor 0 (first floor) where the elevator begins.

### Step 3: Verify Input Parsing
- The `parse_input()` function from Part 1 works unchanged
- It extracts initial state from `input.md`
- After parsing, we manually add the 4 new items (they're not in input.md)

### Step 4: Ensure State Creation Remains Correct
```python
initial_state = State(
    elevator_floor=0,
    floors=tuple(frozenset(initial_floors[i]) for i in range(4))
)
```
This code is unchanged and correctly handles the expanded first floor.

### Step 5: Output the Result
```python
min_steps = solve(initial_state)
print(min_steps)
```
Unchanged from Part 1.

## Algorithm Efficiency Considerations

### Time Complexity
- **State space size**: With 7 element pairs (14 items total), the theoretical state space is enormous (potentially millions of states)
- **Canonicalization**: Critical optimization that treats equivalent states as identical
  - Example: (plutonium on floor 1, strontium on floor 2) is equivalent to (strontium on floor 1, plutonium on floor 2) if their respective chips are in the same relative positions
  - This dramatically reduces the effective state space from millions to thousands/tens of thousands
  - Without canonicalization, the solution would be intractable
- **BFS pruning**: Visited states are tracked to avoid revisiting

### Space Complexity
- **Visited set**: Stores canonical states - could grow to hundreds of thousands of entries with 14 items
  - Each canonical state is a lightweight tuple of frozensets
  - Modern systems with adequate RAM should handle this easily
- **Queue**: At most contains one level of BFS frontier, typically smaller than visited set

### Performance Expectations
- Part 1 with 5 element pairs (10 items) took 37 steps
- Part 2 with 7 element pairs (14 items) will require more steps (likely in the 55-65 range)
- Runtime should still be reasonable (likely 10-120 seconds depending on hardware, maximum ~5 minutes)
- The additional 4 items are all on floor 0 (first floor), so they increase the complexity of early moves but follow the same patterns
- Canonicalization is what makes the solution tractable - expect visited set size in the thousands to tens of thousands

## Implementation Details

### Data Structures
- **Items**: Tuples of `(element_name, type)` where type is 'G' or 'M'
- **Floors**: Sets of items (converted to frozensets for immutability)
- **State**: Dataclass with `elevator_floor` (int) and `floors` (tuple of frozensets)

### Safety Rule Implementation
The existing `is_safe_floor()` correctly handles:
1. Empty floors (safe)
2. Floors with only microchips (safe)
3. Floors with generators - each microchip must have its matching generator
4. The new elerium and dilithium items follow the same rules

### Canonicalization Strategy
The existing canonicalization works by:
1. Creating a signature for each element: `(generator_floor, microchip_floor)`
2. Grouping elements with identical signatures
3. Assigning canonical names based on sorted signatures
4. This ensures states that differ only in element names are treated as identical

This is especially valuable with 7 pairs - many states will be equivalent.

## Complete Code Structure

```
part_2_solution.py
├── Imports (from collections, dataclasses, itertools, re)
├── parse_input(input_text) [unchanged]
├── is_safe_floor(floor_items) [unchanged]
├── State class [unchanged]
│   ├── is_valid()
│   └── is_goal()
├── generate_valid_moves(state) [unchanged]
├── canonicalize_state(state) [unchanged]
├── solve(initial_state) [unchanged]
└── main() [MODIFIED]
    ├── Read input.md
    ├── Parse input
    ├── ADD 4 NEW ITEMS TO FLOOR 0  <-- ONLY CHANGE
    ├── Create initial state
    ├── Solve
    └── Print result
```

## Summary
This implementation requires minimal changes from Part 1. The robust BFS algorithm with canonicalization will handle the increased state space efficiently. The only modification is adding 4 items to the initial state on floor 0.
