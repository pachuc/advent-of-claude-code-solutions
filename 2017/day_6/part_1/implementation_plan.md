# Implementation Plan: Memory Reallocation Cycle Detection

## Problem Analysis

We need to simulate a memory reallocation process that redistributes blocks across memory banks until we encounter a configuration that we've seen before. The challenge is to:
1. Efficiently track seen configurations
2. Correctly implement the redistribution algorithm
3. Handle tie-breaking (lowest index wins)
4. Count cycles until repetition occurs

### Input Characteristics
- Input: 16 space-separated integers (based on provided input)
- Values range from 0 to 15 in the example
- Small number of banks (16), but potentially many cycles before repetition

### Algorithm Complexity Considerations
- **Time Complexity**: O(C × N) where C is the number of cycles and N is the number of banks
  - Each cycle requires O(N) to find max bank and O(B) to redistribute B blocks
  - In worst case, B ≤ total blocks, so redistribution is O(N) amortized
  - Number of cycles C could be large but is bounded by possible unique configurations
- **Space Complexity**: O(C × N) for storing all seen configurations
  - Each configuration is N integers
  - We store C configurations before finding a repeat
- **Expected Performance**: Given only 16 banks, this should run very quickly even for thousands of cycles

### Data Structure Choice
- Use a **set of tuples** to track seen configurations
  - Tuples are hashable and immutable (required for set membership)
  - Set lookup is O(1) average case
  - Alternative: dict mapping configuration to cycle number (useful for debugging)

## Step-by-Step Implementation Plan

### Step 1: Input Parsing
**File**: `solution.py`
```python
def parse_input(input_string):
    """Parse space-separated integers into a list of bank values."""
    # Read the input line
    # Split by whitespace (handles tabs and spaces)
    # Convert to integers
    # Return as a list (mutable, needed for redistribution)
```

**Details**:
- Use `strip()` to remove leading/trailing whitespace
- Use `split()` to handle any whitespace delimiter
- Convert each element to integer using list comprehension or map
- Return a list (not tuple) since we'll modify banks during redistribution

### Step 2: Find Maximum Bank
**Function**: `find_max_bank(banks)`
```python
def find_max_bank(banks):
    """
    Find the index of the bank with the most blocks.
    If there's a tie, return the lowest index.
    """
    # Initialize max_value and max_index
    # Iterate through banks with enumerate
    # Update max only if current value is STRICTLY greater (not >=)
    # This ensures tie-breaking favors lowest index
    # Return the index
```

**Details**:
- Use a simple loop with enumerate to track both value and index
- Key insight: Use `>` not `>=` in comparison to favor lower indices
- Time complexity: O(N) where N is number of banks
- Alternative: Use `max()` with key function, but loop is clearer

### Step 3: Redistribute Blocks
**Function**: `redistribute(banks)`
```python
def redistribute(banks):
    """
    Perform one redistribution cycle.
    Modifies banks in-place and returns the new configuration.
    """
    # Find the bank with most blocks
    # Store the number of blocks to redistribute
    # Set that bank to 0
    # Start from the next bank (with wrapping)
    # Distribute blocks one at a time in circular fashion
    # Return the banks (for convenience)
```

**Details**:
- Modify banks in-place for efficiency
- Use modulo operator `%` for circular indexing: `(start_index + i) % len(banks)`
- Distribute blocks sequentially: for i in range(blocks_to_distribute)
- Example: If bank 2 has 7 blocks, start at bank 3, distribute to banks 3,4,5,6,7,8,9 (wrapping)

### Step 4: Main Simulation Loop
**Function**: `find_cycle_count(banks)`
```python
def find_cycle_count(banks):
    """
    Run redistribution cycles until a repeated configuration is found.
    Returns the number of cycles completed.
    """
    # Create a set to track seen configurations
    # Convert initial banks to tuple and add to set
    # Initialize cycle counter to 0

    # Loop indefinitely:
    #   - Perform redistribution
    #   - Increment cycle counter
    #   - Convert banks to tuple
    #   - Check if configuration is in seen set
    #   - If yes: return cycle count
    #   - If no: add to set and continue
```

**Details**:
- **Important**: Add the initial configuration to the seen set before starting
  - This handles cases where the initial state repeats immediately (e.g., `[0,0,0,0]`)
  - After cycle 1 with `[0,0,0,0]`, we get `[0,0,0,0]` again, which is correctly detected as a repeat
- Convert list to tuple for hashing: `tuple(banks)`
- Use `in` operator for set membership (O(1) average)
- Exit loop when duplicate found and return cycle count
- Alternative: Use while True with break, or condition-based while loop
- **Optional during debugging**: Add a max iterations check (e.g., 100,000) to prevent infinite loops if there's a bug in duplicate detection

### Step 5: Main Program Structure
```python
def main():
    """Main entry point for the solution."""
    # Read input from file or stdin
    # Parse the input
    # Run the simulation
    # Print the result
```

**Details**:
- Read from `input.md` file
- Handle file I/O gracefully
- Print only the final answer (integer)
- Keep it simple - no extensive error handling needed for this context

### Step 6: Integration and Testing Hooks
```python
if __name__ == "__main__":
    main()
```

**Details**:
- Allow script to be run directly
- Also allow functions to be imported for testing
- No command-line argument parsing needed

## Implementation Order

1. **First**: Implement `parse_input()` - establishes data structure
2. **Second**: Implement `find_max_bank()` - core logic, easy to test
3. **Third**: Implement `redistribute()` - most complex, uses find_max_bank
4. **Fourth**: Implement `find_cycle_count()` - orchestrates everything
5. **Fifth**: Implement `main()` - I/O wrapper
6. **Finally**: Add if __name__ == "__main__" guard

## Edge Cases to Handle in Implementation

1. **Tie-breaking**: Multiple banks with same max value
   - Solution: Use `>` not `>=` in comparison

2. **Wraparound**: Distributing blocks that wrap around the bank array
   - Solution: Use modulo arithmetic `(index + offset) % len(banks)`

3. **Zero blocks**: Bank with 0 blocks selected (if all are 0)
   - Not possible given input, but algorithm handles it naturally

4. **Single bank**: Only one memory bank
   - Would loop immediately (same config after redistribution)

5. **Large block count**: One bank has many blocks
   - Blocks distributed may lap around multiple times
   - Modulo handles this correctly

## Optimization Considerations

Given the problem constraints:
- **Not needed**: Cycle detection algorithms (Floyd's, Brent's) - overkill for this
- **Not needed**: Hash map for faster duplicate detection - set is already O(1)
- **Not needed**: Lazy evaluation or generators - simple loop is fine
- **Sufficient**: Basic simulation with set-based duplicate detection

The straightforward simulation approach is optimal for this problem size.

## Code Structure Summary

```
solution.py
├── parse_input(input_string) → list[int]
├── find_max_bank(banks) → int
├── redistribute(banks) → list[int]
├── find_cycle_count(banks) → int
└── main() → None
```

Total estimated lines of code: ~60-80 lines including comments and whitespace
