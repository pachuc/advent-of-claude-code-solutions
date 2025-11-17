# Implementation Plan: String Classification (Nice vs Naughty)

## Problem Summary
Count how many strings in the input satisfy BOTH conditions:
1. Contains a non-overlapping pair of two letters appearing at least twice
2. Contains at least one letter that repeats with exactly one letter between them

## Algorithm Analysis

### Time Complexity Considerations
- **Input size**: 1000 strings
- **String length**: Typical length appears to be 15-20 characters
- **Required efficiency**: O(n*m) where n is number of strings and m is average string length

Since we have only 1000 strings with relatively short lengths, a straightforward O(n*m²) solution would be acceptable, but we can optimize to O(n*m) for each condition check.

### Space Complexity
- O(m) for storing pairs and checking conditions for each string
- Overall: O(1) additional space per string

## Implementation Strategy

### Step 1: File Structure Setup
- Create a single Python script `solution.py`
- Read input from `input.md`
- Output a single integer count

### Step 2: Implement Condition 1 Check (Non-overlapping Pairs)
**Function**: `has_non_overlapping_pair(s: str) -> bool`

**Algorithm**:
1. Iterate through string to find all pairs (i, i+1)
2. For each pair, search for another occurrence starting from i+2 onwards
3. Use string slicing to check if the same pair exists later
4. Return True immediately upon finding the first non-overlapping match
5. Return False if no non-overlapping pairs found

**Implementation approach**:
```python
def has_non_overlapping_pair(s: str) -> bool:
    # For each position i, check if pair s[i:i+2] appears again after position i+1
    for i in range(len(s) - 1):
        pair = s[i:i+2]
        # Search for the same pair starting from i+2 to avoid overlap
        # s[i+2:] begins at index i+2, so earliest match would be at positions [i+2, i+3]
        # This ensures the two pairs don't share any characters (no overlap)
        if pair in s[i+2:]:
            return True
    return False
```

**Time complexity**: O(m²) worst case, but Python's `in` operator is highly optimized
**Space complexity**: O(1)

**Edge cases handled**:
- Strings shorter than 4 characters: Will correctly return False (minimum length for non-overlapping pair is 4: "xyxy")
- Overlapping pairs like "aaa": Will correctly return False since we start searching from i+2

### Step 3: Implement Condition 2 Check (Letter Repeat with One Between)
**Function**: `has_repeat_with_one_between(s: str) -> bool`

**Algorithm**:
1. Iterate through string from index 0 to len(s)-3
2. Check if character at position i equals character at position i+2
3. Return True immediately upon finding the first match
4. Return False if no such pattern exists

**Implementation approach**:
```python
def has_repeat_with_one_between(s: str) -> bool:
    # Check if s[i] == s[i+2] for any valid i
    for i in range(len(s) - 2):
        if s[i] == s[i+2]:
            return True
    return False
```

**Time complexity**: O(m)
**Space complexity**: O(1)

**Edge cases handled**:
- Strings shorter than 3 characters: Will correctly return False (minimum length is 3: "aba")
- Multiple matches: Returns True on first match (efficient short-circuit)

### Step 4: Implement Main Classification Logic
**Function**: `is_nice(s: str) -> bool`

**Algorithm**:
1. Return True only if BOTH conditions are satisfied
2. Use short-circuit evaluation for efficiency

**Implementation approach**:
```python
def is_nice(s: str) -> bool:
    return has_non_overlapping_pair(s) and has_repeat_with_one_between(s)
```

### Step 5: Implement Input Processing and Counting
**Function**: `main()`

**Algorithm**:
1. Read the input file `input.md`
2. Split into lines and strip whitespace
3. Filter out empty lines
4. Count strings that satisfy `is_nice()`
5. Print the result

**Implementation approach**:
```python
def main():
    with open('input.md', 'r') as f:
        lines = f.read().strip().split('\n')

    nice_count = 0
    for line in lines:
        line = line.strip()
        if line and is_nice(line):
            nice_count += 1

    print(nice_count)
```

### Step 6: Add Entry Point
```python
if __name__ == "__main__":
    main()
```

## Overall Algorithm Complexity
- **Time Complexity**: O(n * m²) where n = 1000 strings, m = average string length (~16 chars)
  - For 1000 strings × 16² = ~256,000 operations
  - Highly acceptable for this problem size
- **Space Complexity**: O(1) additional space (not counting input storage)

## Optimization Considerations
Given the input size, no further optimization is necessary. The algorithm will run in milliseconds. If we had millions of strings or very long strings, we could consider:
- Using a hash map to track pair positions for condition 1
- Early termination strategies
- Parallel processing

However, these optimizations would add code complexity without meaningful performance gains for this problem.

## Code Organization
```
solution.py
├── has_non_overlapping_pair(s: str) -> bool
├── has_repeat_with_one_between(s: str) -> bool
├── is_nice(s: str) -> bool
└── main()
```

## Implementation Order
1. Write helper function `has_non_overlapping_pair`
2. Write helper function `has_repeat_with_one_between`
3. Write classification function `is_nice`
4. Write main function with file I/O and counting logic
5. Add entry point guard
6. Test with provided examples before running on full input
