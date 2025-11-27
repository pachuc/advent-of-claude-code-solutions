# Implementation Plan: Inventory Management System Checksum

## Problem Summary
Calculate a checksum for a list of box IDs by:
1. Counting how many box IDs contain any letter that appears exactly 2 times
2. Counting how many box IDs contain any letter that appears exactly 3 times
3. Multiplying these two counts together

## Algorithm Overview

### Time Complexity: O(n × m)
- n = number of box IDs (~250 based on input)
- m = average length of each box ID (~26 characters)
- Total operations: ~6,500 character comparisons

### Space Complexity: O(k)
- k = size of character set (26 lowercase letters maximum)
- Using a frequency counter dictionary per box ID

## Step-by-Step Implementation

### Step 1: Input Parsing
**Function**: `parse_input(filename: str) -> list[str]`

**Logic**:
- Read the input file
- Split by newlines to get individual box IDs
- Strip whitespace from each line
- Filter out empty lines (input has trailing newline)
- Return list of box ID strings

**Edge Cases**:
- Empty lines at end of file
- Whitespace around box IDs

### Step 2: Letter Frequency Counter
**Function**: `count_letters(box_id: str) -> dict[str, int]`

**Logic**:
- Create a dictionary to store letter frequencies
- Iterate through each character in the box ID
- Increment the count for each letter
- Return the frequency dictionary

**Alternative**: Use Python's `collections.Counter` for cleaner code
- `Counter(box_id)` automatically creates frequency dictionary
- More Pythonic and efficient

**Decision**: Use `Counter` for simplicity and readability

### Step 3: Check for Exact Count Occurrences
**Function**: `has_exact_count(box_id: str, target_count: int) -> bool`

**Logic**:
- Get letter frequency dictionary using `Counter`
- Check if any letter has frequency exactly equal to `target_count`
- Return True if found, False otherwise

**Implementation**:
```python
from collections import Counter

def has_exact_count(box_id: str, target_count: int) -> bool:
    freq = Counter(box_id)
    return target_count in freq.values()
```

**Efficiency**: O(m) where m is length of box_id
- Counter creation: O(m)
- Checking values: O(k) where k ≤ 26 (alphabet size)

### Step 4: Count Box IDs with Two/Three Letter Occurrences
**Function**: `calculate_checksum(box_ids: list[str]) -> int`

**Logic**:
1. Initialize two counters: `twos_count = 0`, `threes_count = 0`
2. For each box ID in the list:
   - If `has_exact_count(box_id, 2)` is True: increment `twos_count`
   - If `has_exact_count(box_id, 3)` is True: increment `threes_count`
3. Return `twos_count * threes_count`

**Important Notes**:
- Each box ID can contribute to both counters independently
- Each box ID contributes at most once to each counter (even if multiple letters match)
- The two checks are independent (not elif)

### Step 5: Main Entry Point
**Function**: `main()`

**Logic**:
1. Parse input from `input.md`
2. Calculate checksum
3. Print the result (single integer, no extra formatting)

**File Structure**:
```python
from collections import Counter

def parse_input(filename: str) -> list[str]:
    """Read input file and return list of box IDs."""
    with open(filename, 'r') as f:
        content = f.read()

    # Split by newlines and filter out empty lines
    box_ids = [line.strip() for line in content.split('\n') if line.strip()]
    return box_ids

def has_exact_count(box_id: str, target_count: int) -> bool:
    """Check if any letter in box_id appears exactly target_count times."""
    freq = Counter(box_id)
    return target_count in freq.values()

def calculate_checksum(box_ids: list[str]) -> int:
    """Calculate checksum by counting box IDs with exact letter frequencies."""
    twos_count = 0
    threes_count = 0

    for box_id in box_ids:
        if has_exact_count(box_id, 2):
            twos_count += 1
        if has_exact_count(box_id, 3):
            threes_count += 1

    return twos_count * threes_count

def main():
    box_ids = parse_input('input.md')
    checksum = calculate_checksum(box_ids)
    print(checksum)

if __name__ == '__main__':
    main()
```

## Optimization Considerations

### Current Approach Efficiency
- For ~250 box IDs × 26 characters each: ~6,500 operations
- This is extremely fast (microseconds)
- No optimization needed for this input size

### Alternative Approaches Considered

**1. Single Pass with Combined Check**
- Check for both 2s and 3s in one iteration
- Slightly faster but less readable
- Not worth the complexity trade-off

**2. Pre-filtering**
- Skip box IDs that are too short
- Minimal benefit since all box IDs are similar length

**3. Parallel Processing**
- Overkill for this input size
- Python GIL would negate benefits

**Decision**: Stick with simple, readable approach
- Performance is already optimal for problem size
- Code clarity is more valuable

## Expected Output
For the given input, the algorithm will:
1. Count box IDs with any letter appearing exactly twice
2. Count box IDs with any letter appearing exactly three times
3. Return their product as a single integer

## Implementation Order
1. Write `parse_input()` - foundation for everything
2. Write `has_exact_count()` - core logic
3. Write `calculate_checksum()` - orchestration
4. Write `main()` - entry point
5. Test with example data
6. Run with actual input

## Summary of Plan Updates

Based on critique feedback, this plan now includes:

1. **Complete Function Implementations**: All functions now have full implementations with docstrings, not just stubs with `pass` statements
2. **Proper Input Handling**: The `parse_input()` function includes proper file reading with context manager and filtering of empty lines
3. **Independent Counting**: The `calculate_checksum()` implementation clearly shows two separate `if` statements (not `elif`) to ensure each box ID can contribute to both counters
4. **Ready to Execute**: The complete code skeleton can now be directly copied and run without modification
