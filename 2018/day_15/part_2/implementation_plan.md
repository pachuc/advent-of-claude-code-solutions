# Implementation Plan: Part 2 - Elven Victory Without Casualties

## Problem Summary
Find the minimum Elf attack power (≥4) that allows Elves to win without a single Elf dying. Calculate the outcome (rounds × remaining HP) for that battle.

## Key Differences from Part 1
1. **Variable Elf attack power** instead of fixed 3
2. **Track Elf casualties** during simulation
3. **Search for minimum attack power** that satisfies constraints
4. **Resetable game state** for multiple simulation attempts
5. **Success condition**: All Elves survive AND all Goblins die

## Algorithm Approach

### High-Level Strategy
We'll use a **binary search** approach to find the minimum Elf attack power efficiently:
- Lower bound: 4 (minimum required)
- Upper bound: Start with a reasonable estimate (e.g., 200, since that's max HP)
- For each attack power: run full simulation and check if all Elves survive
- Binary search converges to minimum successful power

**Rationale**: Binary search is O(log n) instead of linear O(n). Given that each simulation could be expensive (many rounds, many units), this optimization is valuable.

### Alternative Approach Considered
Linear search from 4 upward until success. This is simpler but potentially slower if the answer is high (e.g., 34). However, for small answer values, performance difference is negligible.

**Decision**: Start with binary search, but linear search from 4 is also acceptable since we're not optimizing for production.

## Step-by-Step Implementation Plan

### Step 1: Reuse Part 1 Code Structure
- **Copy** the entire `part_1_solution.py` as the foundation
- The core combat simulation logic is identical
- We'll modify only the specific parts needed for Part 2

### Step 2: Modify Unit Class
**Location**: `Unit.__init__()` method

**Changes**:
- Remove the hardcoded `self.attack = 3`
- Add `attack_power` parameter to constructor
- Store attack power from parameter

**Code change**:
```python
def __init__(self, x, y, unit_type, attack_power=3):
    self.x = x
    self.y = y
    self.type = unit_type
    self.hp = 200
    self.attack = attack_power  # Now parameterized
    self.alive = True
```

### Step 3: Modify parse_input() Function
**Location**: `parse_input()` function

**Changes**:
- Add parameters for `elf_attack_power` and `goblin_attack_power`
- When creating units, pass appropriate attack power based on unit type

**Code change**:
```python
def parse_input(input_text, elf_attack_power=3, goblin_attack_power=3):
    lines = input_text.strip().split('\n')
    grid = [list(row) for row in lines]
    units = []

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in ['E', 'G']:
                attack = elf_attack_power if grid[y][x] == 'E' else goblin_attack_power
                units.append(Unit(x, y, grid[y][x], attack))

    return grid, units
```

### Step 4: Create Simulation Wrapper with Elf Tracking
**New function**: `simulate_with_elf_check()`

**Purpose**: Run simulation and track whether any Elf dies

**Implementation**:
```python
def simulate_with_elf_check(input_text, elf_attack_power):
    """
    Simulate combat with given Elf attack power.

    Note: Each call to parse_input() creates fresh, independent grid and units objects,
    so no deep copy is needed. The simulation mutates these objects but they are
    discarded after each call.

    Returns:
        tuple: (success: bool, rounds: int, outcome: int)
        - success: True if all Elves survived and won
        - rounds: completed rounds
        - outcome: final outcome value
    """
    # Parse with custom attack powers (creates fresh game state)
    grid, units = parse_input(input_text, elf_attack_power, 3)

    # Count initial Elves
    initial_elf_count = sum(1 for u in units if u.type == 'E')

    # Simulate combat (mutates grid and units)
    rounds = simulate_combat(grid, units)

    # Check end conditions
    living_elves = sum(1 for u in units if u.alive and u.type == 'E')
    living_goblins = sum(1 for u in units if u.alive and u.type == 'G')

    # Success: all Elves alive and all Goblins dead
    success = (living_elves == initial_elf_count) and (living_goblins == 0)

    # Calculate outcome
    outcome = calculate_outcome(rounds, units)

    return success, rounds, outcome
```

### Step 5: Implement Binary Search for Minimum Attack Power
**New function**: `find_minimum_elf_attack_power()`

**Implementation**:
```python
def find_minimum_elf_attack_power(input_text):
    """
    Binary search to find minimum Elf attack power for zero casualties.

    Returns:
        tuple: (min_power: int, rounds: int, outcome: int)

    Raises:
        RuntimeError: If no valid attack power found within reasonable bounds
    """
    low = 4  # Minimum required
    high = 200  # Conservative upper bound (with attack 200, Elves one-shot Goblins)

    best_power = None
    best_rounds = None
    best_outcome = None

    while low <= high:
        mid = (low + high) // 2
        success, rounds, outcome = simulate_with_elf_check(input_text, mid)

        if success:
            # This power works, try lower
            best_power = mid
            best_rounds = rounds
            best_outcome = outcome
            high = mid - 1
        else:
            # This power failed, need higher
            low = mid + 1

    # Validate that a solution was found
    if best_power is None:
        raise RuntimeError("No valid attack power found in range 4-200")

    return best_power, best_rounds, best_outcome
```

**Key points**:
- Start with reasonable bounds (4 to 200)
- Upper bound 200 is sufficient because at that power, Elves deal massive damage
- When success found, try lower powers
- When failure, try higher powers
- Track best successful result
- Validate solution was found before returning

### Step 6: Add Optional Debug Output
**Enhancement**: Add verbose parameter for debugging binary search

**Optional modification to `find_minimum_elf_attack_power()`**:
```python
def find_minimum_elf_attack_power(input_text, verbose=False):
    """
    Binary search to find minimum Elf attack power for zero casualties.

    Args:
        input_text: The puzzle input
        verbose: If True, print debug information during search

    Returns:
        tuple: (min_power: int, rounds: int, outcome: int)
    """
    low = 4
    high = 200
    best_power = None
    best_rounds = None
    best_outcome = None

    while low <= high:
        mid = (low + high) // 2
        success, rounds, outcome = simulate_with_elf_check(input_text, mid)

        if verbose:
            status = "SUCCESS" if success else "FAILURE"
            print(f"Testing attack power {mid}: {status}")

        if success:
            best_power = mid
            best_rounds = rounds
            best_outcome = outcome
            high = mid - 1
        else:
            low = mid + 1

    if best_power is None:
        raise RuntimeError("No valid attack power found in range 4-200")

    if verbose:
        print(f"Minimum attack power found: {best_power}")

    return best_power, best_rounds, best_outcome
```

**Note**: This is optional but helpful for debugging and verification.

### Step 7: Update Main Function
**Location**: `main()` function

**Changes**:
```python
def main():
    # Read input
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Find minimum attack power (using binary search)
    try:
        min_power, rounds, outcome = find_minimum_elf_attack_power(input_text)
    except RuntimeError as e:
        print(f"Error: {e}")
        return

    # Print result
    print(f"Minimum Elf attack power: {min_power}")
    print(f"Completed rounds: {rounds}")
    print(f"Outcome: {outcome}")
    print(outcome)  # Final answer on last line
```

**Note**:
- Error handling added for cases where no solution is found
- The last `print(outcome)` ensures the answer is easily parseable

## Code Reuse Summary

### Functions to Keep Unchanged (from Part 1)
- `sort_units()` - Still sorts by reading order
- `find_targets()` - Still finds enemies
- `bfs_distances()` - Pathfinding logic unchanged
- `find_in_range_squares()` - Target adjacency unchanged
- `choose_destination()` - Movement logic unchanged
- `choose_next_step()` - Step selection unchanged
- `choose_attack_target()` - Target selection unchanged
- `execute_turn()` - Turn execution unchanged
- `execute_round()` - Round execution unchanged
- `simulate_combat()` - Combat loop unchanged
- `calculate_outcome()` - Outcome calculation unchanged
- `DIRECTIONS` constant - Still same 4 directions

### Functions to Modify
1. `Unit.__init__()` - Add attack_power parameter
2. `parse_input()` - Add attack power parameters

### New Functions to Add
1. `simulate_with_elf_check()` - Wrapper for tracking Elf survival
2. `find_minimum_elf_attack_power()` - Binary search implementation with error handling

## Runtime Complexity Analysis

### Per-Simulation Complexity
- Grid size: ~32×32 = 1024 cells
- Units: ~20 units initially
- Rounds: Typically 20-50 rounds
- Per turn: BFS is O(grid_size) = O(1024)
- Per round: O(units × grid_size) = O(20 × 1024) = O(20k)
- Full simulation: O(rounds × units × grid_size) = O(50 × 20 × 1024) ≈ O(1M)

### Binary Search Complexity
- Search space: 4 to 200 = ~196 values
- Binary search iterations: log₂(196) ≈ 8 iterations
- Total: 8 × O(1M) ≈ O(8M) operations
- **Expected runtime**: < 1 second on modern hardware

### Linear Search Complexity
- Worst case: 196 simulations
- If answer is 34 (like Example 5): 31 simulations
- Total: up to 196 × O(1M) ≈ O(196M) operations
- **Expected runtime**: Still < 5 seconds on modern hardware

**Conclusion**: Both approaches are fast enough for this problem. Binary search is more elegant but linear search is simpler.

## Edge Cases to Handle

1. **No Elves in input**: Should not happen with valid input
2. **No Goblins in input**: Combat ends immediately, all Elves survive
3. **Attack power 4 already works**: Binary search will find it correctly
4. **Very high attack power needed**: Binary search handles this efficiently
5. **Elf dies on last Goblin kill**: Must still count as failure (Elf died)

## Implementation Order

1. Copy `part_1_solution.py` to working file
2. Modify `Unit.__init__()` to accept attack_power parameter (default=3 for backward compatibility)
3. Modify `parse_input()` to use attack powers
4. Add `simulate_with_elf_check()` function with clear documentation about state management
5. Add `find_minimum_elf_attack_power()` function with error handling and validation
6. Update `main()` function with try-except block
7. (Optional) Add verbose parameter for debugging
8. Test with examples from problem statement
9. Run on actual input

## Expected Output Format

```
Minimum Elf attack power: 15
Completed rounds: 29
Outcome: 4988
4988
```

The final line contains just the numeric answer for easy parsing.
