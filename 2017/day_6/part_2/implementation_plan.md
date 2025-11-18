# Implementation Plan: Memory Reallocation Loop Size Detection (Part 2)

## Problem Summary
Find the size of the infinite loop in the memory reallocation routine - specifically, count how many redistribution cycles occur between the first and second appearance of the repeated configuration.

## Key Differences from Part 1
- **Part 1**: Counted cycles until ANY configuration repeated
- **Part 2**: Count cycles BETWEEN the first and second occurrence of the repeated configuration (loop size)

## Reusable Components from Part 1
The following functions from `part_1_solution.py` can be reused without modification:
- `parse_input()` - Parses space-separated integers
- `find_max_bank()` - Finds bank with most blocks (tie-breaking by lowest index)
- `redistribute()` - Performs one redistribution cycle

## Algorithm Overview

### Data Structure Change
Instead of using a `set()` to track seen configurations, use a `dict()` that maps:
- **Key**: Configuration tuple (e.g., `(2, 4, 1, 2)`)
- **Value**: Cycle number when first seen (e.g., `1`)

### Algorithm Steps

1. **Initialize Tracking**
   - Create empty dictionary `seen_at = {}`
   - Store initial configuration: `seen_at[tuple(banks)] = 0`
   - Initialize cycle counter: `cycle_count = 0`

2. **Redistribution Loop**
   - Perform redistribution cycle
   - Increment cycle counter
   - Convert current banks to tuple (configuration)
   - Check if configuration exists in `seen_at`:
     - **If YES**: Calculate loop size = `cycle_count - seen_at[config]`, return it
     - **If NO**: Store `seen_at[config] = cycle_count`, continue

3. **Return Loop Size**
   - The difference between current cycle and first occurrence is the loop size

## Detailed Implementation Steps

### Step 1: Create Modified Tracking Function
```python
def find_loop_size(banks):
    """
    Run redistribution cycles until a repeated configuration is found.
    Returns the size of the loop (cycles between first and second occurrence).

    Note: The initial state (before any redistributions) is considered cycle 0.
    The loop size is the number of cycles between the first and second
    occurrence of the repeated configuration.
    """
    seen_at = {}  # Maps configuration tuple to cycle number when first seen
    seen_at[tuple(banks)] = 0  # Initial state is at cycle 0

    cycle_count = 0

    while True:
        redistribute(banks)
        cycle_count += 1

        config = tuple(banks)
        if config in seen_at:
            # Found a repeat - calculate loop size
            loop_size = cycle_count - seen_at[config]
            return loop_size

        seen_at[config] = cycle_count
```

### Step 2: Update Main Function
- Read input from `input.md`
- Parse input into banks list (using `parse_input()`)
- Call `find_loop_size(banks)` instead of `find_cycle_count()`
- Print the result

### Step 3: Copy Reusable Functions
Copy the following functions from Part 1 solution without modification:
- `parse_input()` - Uses `split()` which handles all whitespace (spaces, tabs, newlines)
- `find_max_bank()` - Finds bank with most blocks, tie-breaking by lowest index
- `redistribute()` - Performs one redistribution cycle

## Expected Behavior with Example

Given initial state `0 2 7 0`:

| Cycle | Configuration | Action |
|-------|--------------|--------|
| 0 | `(0, 2, 7, 0)` | Store in `seen_at` as cycle 0 |
| 1 | `(2, 4, 1, 2)` | Store in `seen_at` as cycle 1 |
| 2 | `(3, 1, 2, 3)` | Store in `seen_at` as cycle 2 |
| 3 | `(0, 2, 3, 4)` | Store in `seen_at` as cycle 3 |
| 4 | `(1, 3, 4, 1)` | Store in `seen_at` as cycle 4 |
| 5 | `(2, 4, 1, 2)` | **Found in `seen_at`!** First seen at cycle 1 |

Loop size = 5 - 1 = **4**

## Time Complexity Analysis

### Algorithm Efficiency
- **Time Complexity**: O(N × M) where:
  - N = number of cycles until repetition (bounded by number of possible configurations)
  - M = number of memory banks (for redistribution and tuple creation)

- **Space Complexity**: O(N × M) where:
  - N = number of unique configurations stored
  - M = size of each configuration tuple

### Possible Configurations Bound
With 16 banks and Part 1 answer of 4074 cycles, the actual loop occurs relatively early. The maximum number of possible configurations is theoretically very large, but in practice:
- We know from Part 1 that a repeat occurs at cycle 4074
- The loop size will be < 4074 cycles (unless the loop returns to the initial state, which is theoretically possible but unlikely)
- Dictionary lookups are O(1) average case
- Overall performance should be excellent for this input size

### Edge Case: Loop to Initial State
If the configuration at cycle 4074 happens to be the same as the initial state (cycle 0), then the loop size would equal 4074. Otherwise, the loop size will be strictly less than 4074. The algorithm handles both cases correctly.

### Optimization Considerations
- Using tuples for dictionary keys is efficient (hashable, immutable)
- Dictionary storage is more memory-intensive than a set, but necessary for tracking cycle numbers
- No optimization needed - the algorithm is already efficient for this problem size

## File Structure
```
solution.py
├── parse_input()          # Reused from Part 1
├── find_max_bank()        # Reused from Part 1
├── redistribute()         # Reused from Part 1
├── find_loop_size()       # NEW - Modified from find_cycle_count()
└── main()                 # Modified to call find_loop_size()
```

## Implementation Checklist
- [ ] Copy `parse_input()` from Part 1 (handles all whitespace including tabs)
- [ ] Copy `find_max_bank()` from Part 1
- [ ] Copy `redistribute()` from Part 1
- [ ] Implement `find_loop_size()` with dictionary tracking
- [ ] Update `main()` to call `find_loop_size()`
- [ ] Verify input file `input.md` exists and is readable
- [ ] Print the final result (should be a positive integer)
