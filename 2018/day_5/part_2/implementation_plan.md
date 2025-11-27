# Implementation Plan: Optimized Polymer Reaction (Part 2)

## Overview
Part 2 builds directly on Part 1 by finding the optimal unit type to remove before reacting the polymer. We can reuse the efficient stack-based reaction algorithm from `part_1_solution.py` and extend it with optimization logic.

## Algorithm Analysis

### Part 1 Review
- **Algorithm**: Stack-based single-pass polymer reaction
- **Time Complexity**: O(n) where n is polymer length
- **Space Complexity**: O(n) for the stack
- **Input Size**: ~50,000 characters
- **Part 1 Result**: 11,546 units after full reaction

### Part 2 Requirements
- Try removing each of 26 unit types (A-Z, case-insensitive)
- React the polymer after each removal
- Find the minimum resulting length
- **Worst-case complexity**: O(26 × n) = O(n) since 26 is constant
- **Expected runtime**: Very reasonable even for 50k input

### Optimization Opportunities
1. **Skip non-existent units**: Only test unit types that actually appear in the polymer
2. **Reuse reaction algorithm**: The stack-based approach from Part 1 is already optimal
3. **No need for preprocessing**: We can filter and react in a single pass

## Step-by-Step Implementation Plan

### Step 1: Import and Reuse Part 1 Code
**File**: `solution.py`

- Import or copy the `reacts()` function from `part_1_solution.py` (lines 1-12)
  - This function checks if two units react (same letter, opposite polarity)
  - Already optimal, no changes needed

- Import or copy the `react_polymer()` function from `part_1_solution.py` (lines 15-37)
  - Stack-based algorithm that processes polymer in O(n) time
  - Already optimal, no changes needed

- Import or copy the `read_input()` function from `part_1_solution.py` (lines 40-58)
  - Handles markdown files and extracts alphabetic characters
  - Already works correctly, no changes needed

**Rationale**: The Part 1 solution is already well-structured and efficient. We should reuse it entirely.

### Step 2: Determine Units to Test
**Approach**: Test all 26 letters of the alphabet

**Purpose**: Determine which unit types to test for removal

**Implementation**: Simply use the string `'abcdefghijklmnopqrstuvwxyz'`

**Rationale**:
- While we could optimize by only testing unit types present in the polymer, this adds an extra O(n) pass
- Testing all 26 letters is simpler and the performance difference is negligible
- Non-existent unit types will simply have no effect when removed
- For a one-off script solving this problem, simplicity is preferred over micro-optimization

**Alternative Approach** (slightly more optimal but adds complexity):
```python
def get_unit_types(polymer):
    """Get all unique unit types in the polymer (case-insensitive)."""
    return set(polymer.lower())
```
This saves at most 26 - k iterations where k is the number of unique types, but adds code complexity.

### Step 3: Implement Unit Type Removal and Reaction
**Function**: `remove_unit_and_react(polymer, unit_to_remove)`

**Purpose**: Remove all instances of a specific unit type (both cases) and react the result

**Implementation**:
```python
def remove_unit_and_react(polymer, unit_to_remove):
    """
    Remove all instances of a unit type and react the polymer.

    Args:
        polymer: String representing the polymer
        unit_to_remove: Lowercase letter representing the unit type to remove

    Returns:
        Integer representing the length of the reacted polymer
    """
    # Filter out the unit type (both uppercase and lowercase)
    filtered_polymer = ''.join(
        c for c in polymer
        if c.lower() != unit_to_remove
    )

    # React the filtered polymer
    return react_polymer(filtered_polymer)
```

**Time Complexity**: O(n) for filtering + O(n) for reacting = O(n)
**Space Complexity**: O(n) for the filtered polymer string

**Alternative Approach (More Memory Efficient)**:
Instead of creating an intermediate filtered string, we could modify `react_polymer()` to accept a skip parameter. However, given the problem constraints (~50k characters), the simpler approach is preferable for clarity.

**Rationale**: This approach is clean and reuses the proven Part 1 reaction algorithm. The two-pass approach (filter then react) is simple and efficient enough for the input size.

### Step 4: Implement Main Optimization Logic
**Function**: `find_shortest_polymer(polymer)`

**Purpose**: Try removing each unit type and find the minimum resulting length

**Implementation**:
```python
def find_shortest_polymer(polymer):
    """
    Find the shortest polymer by removing one unit type optimally.

    Args:
        polymer: String representing the polymer

    Returns:
        Integer representing the minimum achievable polymer length
    """
    # Handle edge case of empty polymer
    if not polymer:
        return 0

    # Test all 26 possible unit types
    min_length = float('inf')

    for unit in 'abcdefghijklmnopqrstuvwxyz':
        length = remove_unit_and_react(polymer, unit)
        min_length = min(min_length, length)

    return min_length
```

**Alternative (more Pythonic but same logic)**:
```python
def find_shortest_polymer(polymer):
    """Find the shortest polymer by removing one unit type optimally."""
    if not polymer:
        return 0

    return min(
        remove_unit_and_react(polymer, unit)
        for unit in 'abcdefghijklmnopqrstuvwxyz'
    )
```

**Time Complexity**: O(26 × n) = O(n) since 26 is a constant
**Space Complexity**: O(n) for the filtered polymer in each iteration

**Edge Case Handling**:
- Empty polymer returns 0 (not `float('inf')`)
- Single character will be removed and return 0
- All same type will collapse to 0

**Rationale**: Simple brute-force approach that tests all possibilities. With 26 unit types and n = 50,000, we're looking at worst-case 2.6 million operations, which is very fast.

### Step 5: Implement Main Function
**Function**: `main()`

**Purpose**: Orchestrate the solution

**Implementation**:
```python
def main():
    """Main execution function."""
    # Read the polymer from input
    polymer = read_input('input.md')

    # Find the shortest polymer achievable
    result = find_shortest_polymer(polymer)

    # Print the result
    print(result)
```

**Rationale**: Clean separation of concerns. Main function should be simple and readable.

### Step 6: Add Script Entry Point
**Implementation**:
```python
if __name__ == '__main__':
    main()
```

**Rationale**: Standard Python practice for executable scripts.

## Complete File Structure

**File**: `solution.py`

```
1. Helper function: reacts(a, b) [from Part 1]
2. Core function: react_polymer(polymer) [from Part 1]
3. Input function: read_input(filename) [from Part 1]
4. New function: remove_unit_and_react(polymer, unit_to_remove)
5. New function: find_shortest_polymer(polymer)
6. Main function: main()
7. Entry point: if __name__ == '__main__'
```

**Note**: Copy the Part 1 functions directly into `solution.py` rather than importing, for a self-contained script.

## Performance Considerations

### Time Complexity Analysis
- **Reading input**: O(n)
- **For each of 26 unit types**:
  - Filtering: O(n)
  - Reacting: O(n)
- **Total**: O(n + 26×2n) = O(52n) = O(n) since constants are dropped

### Space Complexity Analysis
- **Input polymer**: O(n)
- **Filtered polymer**: O(n)
- **Reaction stack**: O(n)
- **Unit types set**: O(1) (max 26)
- **Total**: O(n)

### Expected Runtime
- Input size: ~50,000 characters
- Unique unit types: ~26 (worst case)
- Operations: ~26 × 50,000 × 2 = ~2.6 million
- **Expected runtime**: < 1 second on modern hardware

## Edge Cases to Handle

1. **Empty polymer**: Should return 0
2. **Single character**: Should return 1
3. **All same type**: Removing that type leaves empty string (length 0)
4. **No reactions possible**: Some removals might not create any new reactions
5. **Complete collapse**: Some removals might cause complete polymer collapse

## Testing Strategy Reference
See `test_plan.md` for detailed testing approach.

## Implementation Order

1. Copy Part 1 functions into solution.py (reacts, react_polymer, read_input)
2. Implement remove_unit_and_react()
3. Implement find_shortest_polymer() with empty polymer edge case handling
4. Implement main()
5. Test with example from problem statement (dabAcCaCBAcCcaDA → 4)
6. Run on actual input and verify result < 11546
