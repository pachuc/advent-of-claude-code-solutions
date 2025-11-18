# Implementation Summary: Memory Reallocation Loop Size Detection (Part 2)

## Overview
Successfully implemented a solution to detect the loop size in a memory reallocation routine. This builds on Part 1, which found when a configuration first repeated. Part 2 determines how many cycles occur between the first and second appearance of the repeated configuration.

## Problem Summary
Given a set of memory banks with block counts, repeatedly redistribute blocks following specific rules until a configuration repeats. The goal is to find the **loop size** - the number of cycles between the first and second occurrence of the repeated configuration.

## Solution Approach

### Key Modification from Part 1
The main difference from Part 1 is in the tracking mechanism:
- **Part 1**: Used a `set()` to track seen configurations, counted until any repeat
- **Part 2**: Used a `dict()` to map configurations to their first occurrence cycle, calculated the difference when a repeat was detected

### Implementation Strategy
1. **Reused Components from Part 1**:
   - `parse_input()`: Parses space or tab-separated integers
   - `find_max_bank()`: Finds the bank with most blocks (lowest index wins ties)
   - `redistribute()`: Performs one redistribution cycle

2. **New Function - `find_loop_size()`**:
   - Maintains a dictionary `seen_at` mapping configuration tuples to cycle numbers
   - Stores initial state at cycle 0
   - Performs redistribution cycles and tracks each configuration
   - When a repeat is detected, calculates: `loop_size = current_cycle - first_occurrence_cycle`
   - Returns the loop size

## Algorithm Details

### Data Structure
```python
seen_at = {
    (0, 2, 7, 0): 0,      # Initial configuration at cycle 0
    (2, 4, 1, 2): 1,      # Configuration after cycle 1
    (3, 1, 2, 3): 2,      # Configuration after cycle 2
    # ... and so on
}
```

### Redistribution Process
1. Find the bank with the most blocks (ties won by lowest index)
2. Empty that bank and redistribute blocks one at a time
3. Start with the next bank (wrapping around to index 0 after the last bank)
4. Continue until all blocks are distributed

### Loop Detection
- Track each configuration with its first occurrence cycle number
- When a configuration appears that's already in `seen_at`, calculate the loop size
- Loop size = current cycle number - cycle number when first seen

## Files Created
- **solution.py**: Main solution file containing all functions and logic

## Testing Process

### Test 1: Example Input
**Input**: `[0, 2, 7, 0]`
**Expected**: Loop size of 4
**Result**: ✓ PASSED

Manual trace:
- Cycle 0: `(0, 2, 7, 0)` - stored
- Cycle 1: `(2, 4, 1, 2)` - stored
- Cycle 2: `(3, 1, 2, 3)` - stored
- Cycle 3: `(0, 2, 3, 4)` - stored
- Cycle 4: `(1, 3, 4, 1)` - stored
- Cycle 5: `(2, 4, 1, 2)` - **REPEAT!** First seen at cycle 1
- Loop size = 5 - 1 = 4 ✓

### Test 2: Actual Input
**Input**: `[11, 11, 13, 7, 0, 15, 5, 5, 4, 4, 1, 1, 7, 1, 15, 11]`
**Result**: Loop size of **2793**
**Validation**:
- Loop size is positive ✓
- Loop size ≤ 4074 (Part 1 answer) ✓
- Result is consistent with problem constraints ✓

### Test 3: Edge Cases
All edge case tests passed:
- **Tie-breaking**: Correctly selects lowest index when multiple banks have the same maximum
- **Wrap-around**: Correctly wraps around to index 0 after the last bank
- **Single bank**: Returns loop size of 1 (configuration repeats immediately)
- **All zeros**: Returns loop size of 1 (stays in same state)

### Test 4: Unit Tests
All unit tests for individual functions passed:
- `parse_input()`: Correctly handles spaces and tabs
- `find_max_bank()`: Correctly finds max with tie-breaking
- `redistribute()`: Correctly redistributes blocks with wrap-around

## Final Answer
**Loop size: 2793**

This means that after the first occurrence of the repeated configuration, it takes exactly 2793 redistribution cycles before that same configuration appears again.

## Performance
- **Runtime**: < 1 second
- **Memory**: Minimal (stores ~4000-5000 configurations)
- **Correctness**: 100% test pass rate

## Relationship to Part 1
- Part 1 answer: 4074 cycles until first repeat
- Part 2 answer: 2793 cycles in the loop
- This means the repeated configuration first appeared at cycle 4074 - 2793 = 1281, and then appeared again at cycle 4074

## Code Quality
The solution is:
- **Simple**: Minimal code, easy to understand
- **Correct**: All tests pass, edge cases handled
- **Efficient**: O(N×M) time complexity where N is cycles and M is bank count
- **Reusable**: Leveraged Part 1 code effectively
