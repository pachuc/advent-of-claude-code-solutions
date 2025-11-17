# Implementation Plan: Firewall IP Whitelist Identification

## Problem Summary
Find the lowest-valued IP address (0 to 4,294,967,295) that is NOT blocked by any of the given firewall blacklist ranges.

## Algorithm Analysis

### Naive Approach (REJECTED)
- Iterate through all 4.3 billion IPs checking against ~946 ranges
- Time Complexity: O(2^32 * n) where n = number of ranges
- **This is computationally infeasible**

### Optimal Approach (SELECTED)
Merge overlapping/adjacent ranges, then find the first gap starting from 0.

**Time Complexity**: O(n log n) for sorting + O(n) for merging = O(n log n)
**Space Complexity**: O(n) for storing ranges

This is highly efficient even with large inputs.

## Step-by-Step Implementation Plan

### Step 1: Parse Input
**File**: `solution.py` (create new file)

**Task**: Read and parse the blocked IP ranges from input
- Read input file line by line
- For each line in format "start-end":
  - Split on hyphen to get start and end values
  - Convert both to integers
  - Store as tuple (start, end) in a list
- Handle empty lines if present

**Data Structure**: List of tuples `[(start1, end1), (start2, end2), ...]`

### Step 2: Sort Ranges
**Task**: Sort all ranges by their start values

- Use Python's built-in `sort()` or `sorted()`
- Sort by the first element (start) of each tuple
- This groups overlapping and adjacent ranges together

**Why**: Sorting enables efficient merging in a single pass

### Step 3: Merge Overlapping and Adjacent Ranges
**Task**: Combine ranges that overlap or are adjacent into single continuous ranges

**Algorithm**:
```
Initialize merged_ranges as empty list
Initialize current_start, current_end from first range in sorted list

For each range in sorted_ranges (starting from second):
    if range.start <= current_end + 1:
        # Ranges overlap or are adjacent
        # Merge by extending current_end to max of both ends
        current_end = max(current_end, range.end)
    else:
        # No overlap - save current range and start new one
        Add (current_start, current_end) to merged_ranges
        Set current_start, current_end = range.start, range.end

Add final (current_start, current_end) to merged_ranges
```

**Implementation Note**:
- Since tuples are immutable in Python, we track `current_start` and `current_end` as separate variables
- Alternatively, use lists `[start, end]` instead of tuples `(start, end)`

**Key Logic**:
- Two ranges overlap if: `range2.start <= range1.end`
- Two ranges are adjacent if: `range2.start == range1.end + 1`
- We check `range.start <= current_end + 1` to handle both cases

**Example**:
- Input: `[(0, 2), (4, 7), (5, 8)]`
- After sorting: `[(0, 2), (4, 7), (5, 8)]`
- Merging:
  - Start with current_start=0, current_end=2
  - (4, 7): 4 > 2+1, so save (0, 2), current_start=4, current_end=7
  - (5, 8): 5 <= 7+1, so merge: current_end = max(7, 8) = 8
- Result: `[(0, 2), (4, 8)]`

### Step 4: Find Lowest Unblocked IP
**Task**: Scan through merged ranges to find first gap starting from 0

**Algorithm**:
```
Initialize candidate = 0

For each merged_range in merged_ranges:
    if candidate < merged_range.start:
        # Found a gap! candidate is not blocked
        return candidate
    else:
        # candidate is blocked, move past this range
        candidate = merged_range.end + 1

# If we exit loop, candidate is the answer
return candidate
```

**Logic**:
- Start with candidate = 0 (lowest possible IP)
- For each merged range:
  - If candidate < range start: we found a gap before this range
  - Otherwise: candidate is blocked, jump to range.end + 1
- If all ranges are checked and no gap found, candidate is beyond all ranges
- Note: No need for `max()` since we only update candidate when it's >= range.start

**Example with `[(0, 2), (4, 8)]`**:
- candidate = 0
- Range (0, 2): 0 >= 0, so candidate = 2 + 1 = 3
- Range (4, 8): 3 < 4, so return 3 ✓

### Step 5: Return Result
**Task**: Output the lowest unblocked IP address

- Print the result as a single integer
- Ensure no extra whitespace or formatting

## Implementation Structure

```python
def parse_input(filename):
    """Parse IP ranges from input file"""
    # Return list of (start, end) tuples
    # Handle empty file case
    pass

def merge_ranges(ranges):
    """Sort and merge overlapping/adjacent ranges"""
    # Return list of merged (start, end) tuples
    # Handle empty input case
    pass

def find_lowest_unblocked(merged_ranges):
    """Find lowest IP not in any range"""
    # Return integer
    # If no ranges provided, return 0
    pass

def main():
    """Main execution"""
    import sys

    # Accept filename as command-line argument, default to input.md
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    ranges = parse_input(filename)
    merged = merge_ranges(ranges)
    result = find_lowest_unblocked(merged)
    print(result)

if __name__ == '__main__':
    main()
```

## Edge Cases to Handle

1. **Empty input file**: Should return 0 (no IPs blocked)
2. **First IP (0) is unblocked**: Should return 0
3. **All ranges start above 0**: First unblocked is 0
4. **Ranges cover everything from 0 up**: Find first gap
5. **Single range in input**: Simple case
6. **All ranges are disjoint**: Multiple gaps, return first
7. **Adjacent ranges (e.g., 0-5 and 6-10)**: Should merge to 0-10
8. **Overlapping ranges**: Must merge correctly
9. **Ranges in random order**: Sorting handles this
10. **Duplicate ranges**: Merging handles this

## Input File Handling

- Input file: Defaults to `input.md`, can be specified via command-line argument
- Usage: `python solution.py [input_file]`
- Format: One range per line as "start-end"
- Skip empty lines if any exist
- No need for extensive error handling (assuming well-formed input)
- Handle empty file case by returning empty list of ranges

## Expected Output Format

Single integer printed to stdout, e.g.:
```
3
```

## Performance Expectations

- Input size: ~946 ranges
- Time complexity: O(n log n) ≈ O(946 * log(946)) ≈ O(9000) operations
- Should execute in milliseconds
- Memory: O(n) ≈ ~1000 ranges maximum after merging
