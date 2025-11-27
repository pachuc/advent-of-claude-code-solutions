# Implementation Plan: Guard Sleep Pattern Analysis

## Problem Summary
Analyze historical guard shift records to find:
1. The guard with the most total minutes asleep
2. The minute (0-59) during which that guard is most frequently asleep
3. Return: Guard ID × Minute

## Algorithm Overview
This problem requires parsing timestamped records, tracking sleep patterns per guard, and finding optimal patterns. The solution involves:
- Sorting chronological records
- State tracking (current guard, sleep start time)
- Aggregating sleep minutes per guard
- Frequency analysis for specific minutes

## Time Complexity Analysis
- **Input Size**: ~900-1000 records (based on provided input)
- **Sorting**: O(n log n) where n = number of records
- **Processing**: O(n) single pass through sorted records
- **Aggregation**: O(g × m) where g = guards, m = 60 minutes (constant)
- **Overall**: O(n log n) - dominated by sorting, which is efficient for this input size

## Space Complexity
- Guard sleep tracking: O(g × m) where g = number of guards, m = 60 minutes
- Input storage: O(n)
- Overall: O(g × m + n) - reasonable for expected input size

## Implementation Steps

### Step 1: Input Parsing
**Objective**: Read and parse timestamped records from input file

**Details**:
- Read input.md file line by line
- Use regex pattern to extract timestamp: `\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\]`
- Extract event text: everything after `] ` (closing bracket and space)
  - Split on `] ` and take the second part, or use regex: `\[.+\] (.+)`
- Parse timestamp into sortable datetime object using `datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')`
- Store as list of tuples: `[(datetime_obj, event_string), ...]`

**Edge Cases**:
- Empty lines should be skipped
- Lines without proper timestamp format should be skipped with a warning
- For Advent of Code, input is assumed valid, so aggressive error handling not required

**Error Handling**:
- If timestamp parsing fails, skip the line and continue
- If regex doesn't match, skip the line
- No need for extensive validation as input is provided and guaranteed valid

### Step 2: Sort Records Chronologically
**Objective**: Order records by timestamp

**Details**:
- Sort the list of tuples by datetime object (first element)
- Python's `sorted()` or `.sort()` with datetime comparison
- This is critical as input is explicitly stated to be unordered

**Complexity**: O(n log n)

### Step 3: Parse Events and Track State
**Objective**: Identify event types and maintain current guard context

**Details**:
- Iterate through sorted records
- Use regex patterns to identify three event types:
  - `Guard #(\d+) begins shift` - Extract guard ID, set as current guard
  - `falls asleep` - Record minute when current guard falls asleep
  - `wakes up` - Record minute when current guard wakes up

**State Variables**:
- `current_guard`: ID of the guard currently on duty (None initially)
- `sleep_start`: Minute when current guard fell asleep (None if awake)

**State Validation**:
- Before processing "falls asleep": assert `current_guard is not None` (guard must be on duty)
- Before processing "wakes up": assert `sleep_start is not None` (must have fallen asleep first)
- Since Advent of Code input is valid, assertions are acceptable for error handling
- State violations indicate corrupted data or parsing errors

**Note on Shift Timing**:
- Guards may start shifts before midnight (e.g., 23:56)
- Sleep/wake events occurring after midnight belong to the guard who most recently started
- Full datetime sorting ensures this works correctly across day boundaries

### Step 4: Build Sleep Minute Tracking Data Structure
**Objective**: Track which minutes each guard is asleep

**Data Structure**:
```python
from collections import defaultdict
guard_sleep_minutes = defaultdict(lambda: [0] * 60)
# Alternative: manually initialize when first encountering a guard
# guard_sleep_minutes = {}
# if guard_id not in guard_sleep_minutes:
#     guard_sleep_minutes[guard_id] = [0] * 60
```

**Recommended Approach**: Use `defaultdict` for cleaner code and automatic initialization

**Details**:
- When guard falls asleep at minute M1
- When guard wakes up at minute M2
- Mark minutes [M1, M2) as asleep (M1 inclusive, M2 exclusive as per problem)
- Increment counter for each minute in range for that guard
- Example: Falls asleep at 23, wakes at 27 → increment guard_sleep_minutes[guard_id][23:27]
- Implementation: `for minute in range(sleep_start, wake_minute): guard_sleep_minutes[current_guard][minute] += 1`

**Edge Case**: Guards who never sleep will have all zeros in their array (if they ever appear in a shift start)

### Step 5: Calculate Total Sleep Per Guard
**Objective**: Determine which guard has most total minutes asleep

**Details**:
- For each guard, sum all values in their 60-minute array
- Track: `guard_total_sleep = {guard_id: total_minutes}`
- Find guard with maximum total sleep minutes
- Store: `sleepiest_guard_id = max(guard_total_sleep, key=guard_total_sleep.get)`

**Tie-Breaking**: If multiple guards have the same total sleep minutes, `max()` will return the first guard encountered in dictionary iteration order. This is acceptable and consistent behavior.

**Complexity**: O(g × m) = O(g × 60) ≈ O(g)

### Step 6: Find Most Frequent Sleep Minute for Sleepiest Guard
**Objective**: Identify which minute the sleepiest guard is asleep most often

**Details**:
- Access sleep array for sleepiest guard: `guard_sleep_minutes[sleepiest_guard_id]`
- Find index (minute) with maximum value
- Implementation: `best_minute = max(range(60), key=lambda m: guard_sleep_minutes[sleepiest_guard_id][m])`

**Tie-Breaking**: If multiple minutes have the same maximum frequency, `max()` with `range(60)` returns the first occurrence (lowest minute number). This is explicit and consistent behavior.

**Edge Case**: If guard never sleeps, all values are 0, minute 0 would be returned (though this guard wouldn't be selected as sleepiest unless all guards never sleep)

### Step 7: Calculate and Return Answer
**Objective**: Compute final result

**Details**:
- Calculate: `answer = sleepiest_guard_id × best_minute`
- Print result
- Return value for testing

## Code Structure

```python
def parse_input(filename):
    """Parse input file and return list of (datetime, event) tuples"""
    pass

def sort_records(records):
    """Sort records chronologically"""
    pass

def track_sleep_patterns(sorted_records):
    """Process records and build guard sleep tracking"""
    # Returns: guard_sleep_minutes dict
    pass

def find_sleepiest_guard(guard_sleep_minutes):
    """Find guard with most total sleep minutes"""
    # Returns: (guard_id, total_minutes) - total returned for debugging/logging
    pass

def find_best_minute(guard_sleep_minutes, guard_id):
    """Find minute when guard is asleep most frequently"""
    # Returns: minute (0-59)
    pass

def solve():
    """Main solution function"""
    records = parse_input('input.md')
    sorted_records = sort_records(records)
    guard_sleep_minutes = track_sleep_patterns(sorted_records)
    sleepiest_guard, _ = find_sleepiest_guard(guard_sleep_minutes)
    best_minute = find_best_minute(guard_sleep_minutes, sleepiest_guard)
    answer = sleepiest_guard * best_minute
    return answer
```

## Key Implementation Details

### Regex Patterns
```python
import re
# For parsing each line:
line_pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\] (.+)'
# Alternatively, split on '] ' after extracting timestamp

# For identifying event types:
guard_pattern = r'Guard #(\d+) begins shift'
sleep_pattern = r'falls asleep'
wake_pattern = r'wakes up'
```

### Timestamp Parsing
- Use `datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M')`
- Extract minute component: `datetime_obj.minute`
- Full datetime used for sorting to handle shifts spanning midnight

### Sleep Range Marking
- When processing "wakes up" event:
  - Assert `sleep_start is not None` (data validation)
  - Extract wake minute: `wake_minute = current_datetime.minute`
  - Range: `for minute in range(sleep_start, wake_minute)`
  - Increment: `guard_sleep_minutes[current_guard][minute] += 1`
  - Reset state: `sleep_start = None`

## Expected Behavior Per Example
Given example data:
- Guard #10: 50 total minutes asleep
- Guard #99: 30 total minutes asleep
- Guard #10 is sleepiest
- Guard #10 most asleep at minute 24
- Answer: 10 × 24 = 240

## Optimization Considerations
- The algorithm is already efficient: O(n log n) for ~1000 records is negligible
- No need for advanced optimizations (hash maps already used)
- Code clarity is more important than micro-optimizations
- All operations are single-pass after sorting

## Potential Issues to Avoid
1. **Off-by-one errors**: Remember wake minute is NOT counted as asleep (use range with exclusive end)
2. **State management**: Assert current_guard is set before processing sleep events
3. **Integer parsing**: Guard IDs should be integers for calculations and final answer
4. **Sorting stability**: Must sort by full timestamp, not just minute, to handle shifts across midnight
5. **Edge case**: Using defaultdict ensures all guards have entries automatically
6. **Input file format**: Note that input.md is a markdown file, but just read it as plain text
7. **Wake without sleep**: Assert sleep_start is not None before processing wake events
