# Implementation Plan - Part 2: Guard Sleep Pattern Analysis

## Overview
Part 2 uses a different strategy than Part 1. Instead of finding the sleepiest guard overall and then their most frequent minute, we need to find the (guard, minute) pair with the highest frequency across ALL guards simultaneously.

**Important Context:**
- Part 1 answer was **48680** using Strategy 1 (sleepiest guard overall)
- Part 2 should produce a **different answer** using Strategy 2 (most frequent guard-minute pair)
- This difference validates that we've implemented the correct strategy change

## Code Reuse from Part 1
The Part 1 solution can be largely reused! The following components remain identical:
- **Input parsing**: `parse_input()` function - unchanged
- **Record sorting**: `sort_records()` function - unchanged
- **Sleep pattern tracking**: `track_sleep_patterns()` function - unchanged
- Data structure: `guard_sleep_minutes` dictionary mapping guard_id → array of 60 frequencies

## What Changes
Only the final analysis step changes:
- **Part 1**: Find guard with max total sleep → then find that guard's max minute
- **Part 2**: Find (guard, minute) pair with max frequency across all guards

## Implementation Steps

### Step 1: Copy Core Functions from Part 1
Copy the following functions from `part_1_solution.py` as they work perfectly for Part 2:
- `parse_input(filename)` - Parses timestamp and event from each line
- `sort_records(records)` - Sorts by datetime chronologically
- `track_sleep_patterns(sorted_records)` - Builds the frequency tracking structure

**Rationale**: These functions handle the data processing identically for both strategies.

### Step 2: Remove Part 1 Specific Functions
Delete or skip these Part 1 functions as they implement Strategy 1:
- `find_sleepiest_guard()` - Not needed, we're not looking for sleepiest guard
- `find_best_minute()` - Not needed, we need to check all guards simultaneously

### Step 3: Implement New Analysis Function
Create a new function: `find_most_frequent_guard_minute(guard_sleep_minutes)`

**Logic**:
```python
def find_most_frequent_guard_minute(guard_sleep_minutes):
    """Find the (guard, minute) pair with highest frequency across all guards"""
    max_frequency = 0
    best_guard = None
    best_minute = None

    # Iterate through all guards
    for guard_id, sleep_array in guard_sleep_minutes.items():
        # For this guard, check all 60 minutes
        for minute in range(60):
            frequency = sleep_array[minute]
            # Track the maximum frequency across all combinations
            if frequency > max_frequency:
                max_frequency = frequency
                best_guard = guard_id
                best_minute = minute

    return best_guard, best_minute, max_frequency
```

**Time Complexity**: O(G × 60) where G is the number of guards. Since there are typically 10-20 guards, this is very efficient (O(1200) operations max).

**Space Complexity**: O(1) - only tracking a few variables.

**Tie-Breaking Behavior**: If multiple (guard, minute) pairs have the same maximum frequency, the algorithm will return whichever pair is encountered first during iteration (determined by dictionary iteration order and the minute loop). The problem doesn't specify tie-breaking rules, so this natural behavior is acceptable.

### Step 4: Update Main solve() Function
Modify the `solve()` function to:
1. Parse and sort records (same as Part 1)
2. Track sleep patterns (same as Part 1)
3. Call `find_most_frequent_guard_minute()` instead of the Part 1 approach
4. Calculate answer: `guard_id × minute`
5. Print results with appropriate descriptions

**Implementation**:
```python
def solve(filename='input.md'):
    # Parse and sort records
    records = parse_input(filename)
    sorted_records = sort_records(records)

    # Track sleep patterns (builds guard_sleep_minutes)
    guard_sleep_minutes = track_sleep_patterns(sorted_records)

    # Find the guard-minute pair with highest frequency
    best_guard, best_minute, max_frequency = find_most_frequent_guard_minute(guard_sleep_minutes)

    # Calculate answer
    answer = best_guard * best_minute

    # Print results
    print(f"Guard #{best_guard} was asleep most frequently at minute {best_minute}")
    print(f"Frequency: asleep {max_frequency} times at this minute")
    print(f"Answer: {best_guard} × {best_minute} = {answer}")

    return answer
```

### Step 5: Add Main Entry Point
Include the standard Python entry point:
```python
if __name__ == '__main__':
    solve()
```

## Algorithm Efficiency

### Time Complexity Analysis
- **Parsing**: O(N) where N is number of input lines (~935 lines)
- **Sorting**: O(N log N) - ~935 log 935 ≈ 9,300 operations
- **Sleep tracking**: O(N) - iterate through sorted records once
- **Finding max frequency**: O(G × 60) where G is number of guards (~15 guards × 60 = 900 operations)
- **Overall**: O(N log N) dominated by sorting - very efficient

### Space Complexity Analysis
- **Records storage**: O(N) for storing parsed records
- **Guard sleep tracking**: O(G × 60) - typically 15 guards × 60 minutes = 900 integers
- **Overall**: O(N + G) - very memory efficient

### Performance Expectations
With ~935 input lines and ~15 guards, the solution should execute in milliseconds. No optimization needed.

## Summary of Changes from Part 1
1. **Removed**: `find_sleepiest_guard()` and `find_best_minute()` functions
2. **Added**: `find_most_frequent_guard_minute()` function
3. **Modified**: `solve()` function to use new analysis approach
4. **Unchanged**: All parsing, sorting, and sleep tracking logic (80% of code reused!)

## Expected Output Format
```
Guard #<ID> was asleep most frequently at minute <MINUTE>
Frequency: asleep <COUNT> times at this minute
Answer: <ID> × <MINUTE> = <RESULT>
```

## Testing and Validation
After implementation, refer to `test_plan.md` for comprehensive testing strategy. Key validation steps:
1. Verify answer differs from Part 1 (48680)
2. Manually verify the identified guard-minute pair frequency
3. Test with the problem statement example (Guard #99, minute 45 = 4455)
4. Ensure execution completes in under 1 second
