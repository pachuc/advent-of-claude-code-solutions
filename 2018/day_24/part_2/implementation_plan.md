# Implementation Plan: Immune System Simulator - Part 2 (Boosted Combat)

## Overview
Part 2 requires finding the minimum boost value that allows the Immune System to win, then returning the number of Immune System units remaining. We will heavily reuse the Part 1 solution code and add boost functionality with an efficient search algorithm.

## Core Algorithm Strategy

### Search Algorithm: Binary Search
- **Rationale**: Testing every boost value sequentially would be inefficient. Binary search will find the minimum winning boost in O(log n) simulations.
- **Search Space**: Start with a reasonable range (e.g., 1 to 10000). The upper bound can be adjusted if needed.
- **Invariant**: If boost B wins, any boost > B also wins (monotonic property).

### Key Modifications from Part 1
1. Add boost parameter to combat simulation
2. Apply boost to Immune System groups' attack damage
3. Implement binary search to find minimum winning boost
4. Handle stalemate detection (neither side making progress)

## Step-by-Step Implementation

### Step 1: Copy and Modify Part 1 Solution
**File**: `solution.py`

1. Copy all code from `part_1_solution.py` as the foundation
2. Keep all existing classes and functions:
   - `Group` class with all methods
   - `parse_modifiers()` function
   - `parse_input()` function
   - `target_selection()` function
   - `attack_phase()` function
   - `simulate_combat()` function

### Step 2: Add Boost Application Function
**Location**: After `parse_input()` function

```python
def apply_boost(immune_groups: List[Group], boost: int) -> List[Group]:
    """
    Apply boost to immune groups' attack damage in-place.
    Since we parse fresh groups for each simulation, no copying needed.
    """
```

**Implementation details**:
- Modify each immune group's `attack_damage` in-place by adding `boost`
- Return the modified list (same objects, now boosted)
- No deep copying needed since we parse fresh groups for each simulation
- This is simple, efficient, and sufficient for our use case

### Step 3: Keep simulate_combat() Unchanged
**No changes needed to Part 1's simulate_combat() function**

**Rationale**:
- Part 1 already returns `(winner, units_remaining)` as a 2-tuple
- Part 1 already handles stalemates by returning "Stalemate" as the winner string (lines 256, 269, 278)
- For binary search, we only need to check: `winner == "Immune System"` for wins
- All other cases ("Infection" or "Stalemate") are treated as non-wins
- The existing stalemate detection (no units killed in a round) is sufficient
- No need to add a third return value or max_rounds parameter

### Step 4: Implement Binary Search Function
**Function**: `find_minimum_boost()`

**Algorithm**:
```
left = 1
right = 10000  # Conservative upper bound (see note below)

while left < right:
    mid = (left + right) // 2

    # Parse fresh groups for simulation (combat mutates groups)
    immune_groups, infection_groups = parse_input("input.md")

    # Apply boost to immune system (modifies in-place)
    apply_boost(immune_groups, mid)

    # Simulate combat (returns 2-tuple from Part 1)
    winner, units = simulate_combat(immune_groups, infection_groups)

    if winner == "Immune System":
        # This boost works, try smaller
        right = mid
    else:
        # This boost doesn't work (Infection wins or stalemate), try larger
        left = mid + 1

# Validate that we found a winning boost
immune_groups, infection_groups = parse_input("input.md")
apply_boost(immune_groups, left)
winner, units = simulate_combat(immune_groups, infection_groups)

if winner != "Immune System":
    raise ValueError(f"No winning boost found in range [1, {right}]. Try increasing upper bound.")

# left is now the minimum boost
return left
```

**Key considerations**:
- Parse input fresh for each simulation (groups are mutated during combat)
- Stalemates (winner == "Stalemate") count as "not winning" so we search higher
- Binary search converges to minimum working boost
- Final validation ensures the found boost actually wins
- Upper bound of 10000 is based on typical Advent of Code puzzle ranges
- If validation fails, the error message indicates the range should be increased

### Step 5: Implement Main Function
**Function**: `main()`

**Logic**:
```python
def main():
    # Find minimum boost using binary search
    min_boost = find_minimum_boost()

    # Simulate with minimum boost to get final answer
    immune_groups, infection_groups = parse_input("input.md")
    apply_boost(immune_groups, min_boost)
    winner, units_remaining = simulate_combat(immune_groups, infection_groups)

    # Verify Immune System won (should be guaranteed by find_minimum_boost validation)
    assert winner == "Immune System", f"Expected Immune System win, got {winner}"

    # Output the answer
    print(units_remaining)
```

### Step 6: Group Management Strategy
**Decision**: Parse input fresh for each simulation

**Rationale**:
- Groups are mutated during combat (units change, groups die)
- Parsing fresh ensures clean state for each simulation
- No need for deep copying or manual state reset
- Overhead is negligible: parsing takes ~1ms, binary search runs ~13-15 times
- Simpler and less error-prone than copying

**Implementation**: Call `parse_input("input.md")` at the start of each binary search iteration and in the final simulation.

## Code Structure

```
solution.py
├── Imports (re, typing)
├── DEBUG flag and log function
├── Group class (from Part 1, unchanged)
├── parse_modifiers() (from Part 1, unchanged)
├── parse_input() (from Part 1, unchanged)
├── apply_boost() [NEW] - modifies groups in-place
├── target_selection() (from Part 1, unchanged)
├── attack_phase() (from Part 1, unchanged)
├── simulate_combat() (from Part 1, UNCHANGED - already handles stalemates)
├── find_minimum_boost() [NEW] - binary search with validation
└── main() [MODIFIED] - calls find_minimum_boost()
```

## Time Complexity Analysis

### Per Simulation
- Parsing: O(G) where G = number of groups
- Per round:
  - Target selection: O(G²) for finding best targets
  - Attack phase: O(G log G) for sorting by initiative
- Total rounds: Typically < 100 rounds per simulation
- **Per simulation**: O(R × G²) where R = rounds, G = groups

### Overall Algorithm
- Binary search iterations: O(log B) where B = boost range (log₂ 10000 ≈ 13-14)
- Total simulations: ~13-14
- **Total complexity**: O(log B × R × G²) ≈ O(14 × 100 × 400) = very manageable

### Input Size Considerations
- Current input: 10 Immune groups + 10 Infection groups = 20 total groups
- Binary search: ~13-14 simulations needed
- Expected runtime: < 1 second

## Edge Cases to Handle

1. **Boost = 0**: Don't test, start at boost = 1
2. **Very high boost needed**: If 10000 isn't enough, double the upper bound
3. **Stalemate scenarios**: Return "Stalemate" as non-winning result
4. **No damage dealt**: Already handled in simulate_combat()
5. **All groups immune**: Handled by stalemate detection

## Implementation Checklist

- [ ] Copy Part 1 solution code as foundation
- [ ] Implement `apply_boost()` function (in-place modification)
- [ ] Implement `find_minimum_boost()` with binary search and validation
- [ ] Update `main()` function to use boost search
- [ ] Test with example input (should find boost of 1570, answer 51 units)
- [ ] Run on actual input
- [ ] Verify answer is correct

**Note on simulate_combat()**: No changes needed - Part 1 version already handles stalemates correctly.

## Expected Behavior

**Example from problem**:
- Minimum boost: 1570
- Units remaining: 51

**Actual input**:
- Minimum boost: TBD (will be found by binary search)
- Units remaining: TBD (answer to output)

## Optimization Notes

1. **No need for caching**: Each simulation is independent
2. **Fresh parsing**: Simpler than deep copying, negligible overhead
3. **Binary search bounds**: Start conservatively, can adjust if needed
4. **Early termination**: Stalemate detection prevents infinite loops
