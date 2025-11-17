# Implementation Plan - Part 2: Count Total Allowed IPs

## Problem Analysis

Part 2 builds directly on Part 1's solution. Instead of finding the **lowest unblocked IP**, we need to count **all unblocked IPs** across the entire 32-bit IP address space (0 to 4,294,967,295).

### Key Insight
The Part 1 solution already does most of the heavy lifting:
1. Parses blocked IP ranges
2. Merges overlapping/adjacent ranges to create a simplified blacklist

We can reuse this logic and add a counting step.

## Algorithm Approach

### Total IP Space
- 32-bit IP addresses: 0 to 4,294,967,295 inclusive
- **Total possible IPs: 2^32 = 4,294,967,296**

### Strategy
1. Parse blocked IP ranges (reuse Part 1)
2. Merge overlapping/adjacent ranges (reuse Part 1)
3. Calculate total blocked IPs from merged ranges
4. Subtract blocked IPs from total IP space (4,294,967,296)

### Counting Blocked IPs
For each merged range `(start, end)`:
- Number of IPs in range = `end - start + 1`

Total blocked = sum of all IP counts in merged ranges

**Total allowed = 4,294,967,296 - Total blocked**

## Implementation Steps

### Step 1: Reuse Part 1 Functions
- **`parse_input(filename)`**: Already complete, no changes needed
- **`merge_ranges(ranges)`**: Already complete, no changes needed

### Step 2: Implement IP Counting Function
Create a new function `count_allowed_ips(merged_ranges)`:

```python
def count_allowed_ips(merged_ranges):
    """Count total allowed IPs in the 32-bit address space"""
    TOTAL_IP_SPACE = 2**32  # 4,294,967,296

    # Calculate total blocked IPs
    blocked_count = 0
    for start, end in merged_ranges:
        blocked_count += (end - start + 1)

    # Allowed IPs = Total - Blocked
    allowed_count = TOTAL_IP_SPACE - blocked_count

    # Verification assertion to catch arithmetic errors
    assert blocked_count + allowed_count == TOTAL_IP_SPACE, "Count mismatch!"

    return allowed_count
```

**Logic Explanation:**
- Each range blocks `(end - start + 1)` IPs (inclusive counting)
- Sum all blocked IPs across all merged ranges
- Subtract from total 32-bit space
- Assertion verifies arithmetic correctness

### Step 3: Update Main Function
Modify the `main()` function to:
1. Parse input
2. Merge ranges
3. Count allowed IPs (instead of finding lowest)
4. Print the count
5. Optionally print debug information

```python
def main():
    """Main execution"""
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    debug = '--debug' in sys.argv

    ranges = parse_input(filename)
    merged = merge_ranges(ranges)

    # Optional debug output
    if debug:
        print(f"Parsed {len(ranges)} ranges")
        print(f"Merged to {len(merged)} ranges")
        print(f"First merged range: {merged[0] if merged else 'N/A'}")

    result = count_allowed_ips(merged)
    print(result)
```

## Time Complexity Analysis

### Input Size
- ~946 IP ranges in the input file
- After merging, likely significantly fewer (maybe 100-200 merged ranges)

### Complexity Breakdown
1. **Parsing**: O(n) where n = number of input lines (~946)
2. **Sorting**: O(n log n) for sorting ranges (~946 log 946 ≈ 9,500 operations)
3. **Merging**: O(n) single pass through sorted ranges
4. **Counting**: O(m) where m = number of merged ranges (likely < 200)

**Overall: O(n log n)** - dominated by sorting step

### Efficiency
- For ~1,000 input ranges, this is extremely fast (microseconds to milliseconds)
- No iteration through the 4 billion IP space required
- Memory efficient: stores only ranges, not individual IPs

## Code Structure

The solution will have this structure:

```
part_1_solution.py (reuse):
├── parse_input(filename)       [NO CHANGES]
├── merge_ranges(ranges)        [NO CHANGES]

solution.py (new):
├── parse_input(filename)       [COPIED]
├── merge_ranges(ranges)        [COPIED]
├── count_allowed_ips(merged)   [NEW]
└── main()                      [MODIFIED]
```

## Edge Cases Handled

1. **Empty input**: No ranges blocked → all 4,294,967,296 IPs allowed
2. **Overlapping ranges**: Handled by merge_ranges() to avoid double-counting
3. **Adjacent ranges**: Merged into single range (e.g., 0-5 and 6-10 → 0-10)
4. **All IPs blocked**: Edge case where blocked_count = 4,294,967,296 → result = 0
5. **Large ranges**: Each range counted as single arithmetic operation, not iteration

## Why This Approach Works

1. **Merging prevents double-counting**: Overlapping ranges like [5-8] and [4-7] are merged to [4-8], counted once
2. **Mathematical counting**: We count range sizes arithmetically, not by iteration
3. **Efficient for large space**: Works regardless of IP space size (no 4-billion loop)
4. **Reuses proven code**: Part 1's merge logic is already correct and tested

## Expected Output

For the given input, we expect:
- Total IPs: 4,294,967,296
- Blocked IPs: (calculated from merged ranges)
- Allowed IPs: 4,294,967,296 - blocked IPs

The result will be a single integer printed to stdout.
