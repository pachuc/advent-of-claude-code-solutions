# Implementation Plan: Finding Prototype Fabric Box IDs (Part 2)

## Overview
Find two box IDs that differ by exactly one character at the same position, then extract the common letters between them.

## Algorithm Analysis

### Input Characteristics
- 250 box IDs from input.md
- Each box ID is 26 characters long (all same length)
- All lowercase letters

### Complexity Analysis
- **Approach**: Brute force pairwise comparison
- **Time Complexity**: O(n² × m) where n = number of box IDs (250) and m = string length (26)
  - Number of pairs: n × (n-1) / 2 ≈ 31,125 pairs
  - Per comparison: O(26) character checks
  - Total operations: ~808,000 - extremely fast, completes in milliseconds
- **Space Complexity**: O(n × m) for storing the box IDs list
- **Why this works**: The input size is small enough that a simple O(n²) approach is optimal and clearest

### Algorithm Strategy
The problem guarantees exactly one pair of box IDs differs by one character, so we can use early termination when found.

## Implementation Steps

### Step 1: Reuse Input Parsing from Part 1
**Objective**: Read and parse the input file

**Actions**:
- Copy the `parse_input` function directly from `part_1_solution.py`
- This function already handles:
  - Reading the file
  - Splitting by newlines
  - Stripping whitespace
  - Filtering empty lines
- No modifications needed

**Expected Output**: List of 250 box ID strings

### Step 2: Implement Character Difference Counter
**Objective**: Create a helper function to count differences between two strings

**Function Signature**: `count_differences(str1: str, str2: str) -> int`

**Logic**:
- Assume both strings have the same length (guaranteed by problem)
- Compare characters at each position
- Count mismatches
- Return total count

**Recommended Implementation**:
Use the concise one-liner for clarity and simplicity:
```python
def count_differences(str1: str, str2: str) -> int:
    return sum(1 for a, b in zip(str1, str2) if a != b)
```

**Why this approach**:
- Clean and Pythonic
- Easy to understand
- Efficient enough for 26-character strings
- No need for early exit optimization given small string size

**Test case for this function**:
- `count_differences("fghij", "fguij")` → 1 (differ at position 2)
- `count_differences("abcde", "axcye")` → 2 (differ at positions 1 and 3)
- `count_differences("abcde", "abcde")` → 0 (identical)

### Step 3: Implement Function to Extract Common Letters
**Objective**: Given two strings and knowing they differ by one character, extract common letters

**Function Signature**: `get_common_letters(str1: str, str2: str) -> str`

**Logic**:
- Iterate through both strings with indices
- For each position, check if characters match
- If they match, include in result
- If they don't match, skip (this is the one differing position)
- Return concatenated common letters

**Recommended Implementation**:
Use the concise list comprehension approach:
```python
def get_common_letters(str1: str, str2: str) -> str:
    return ''.join(a for a, b in zip(str1, str2) if a == b)
```

**Why this approach**:
- Clear and readable
- Efficiently filters matching characters
- Works regardless of number of differences (though we'll only call it when exactly 1 difference exists)

**Test cases**:
- `get_common_letters("fghij", "fguij")` → "fgij"
- Should work for any pair with exactly one difference

### Step 4: Implement Main Search Function
**Objective**: Find the two box IDs that differ by exactly one character

**Function Signature**: `find_prototype_boxes(box_ids: list[str]) -> str`

**Logic**:
1. Use nested loops to compare all pairs:
   ```python
   for i in range(len(box_ids)):
       for j in range(i + 1, len(box_ids)):
   ```
   - Start `j` at `i + 1` to avoid duplicate comparisons and self-comparisons
   - This ensures we check each unique pair exactly once

2. For each pair `(box_ids[i], box_ids[j])`:
   - Count differences using `count_differences()`
   - If exactly 1 difference found:
     - Extract common letters using `get_common_letters()`
     - Return immediately (problem guarantees exactly one such pair exists)

3. If no pair found (shouldn't happen per problem statement):
   - Raise `ValueError("No matching box IDs found")` to aid debugging

**Expected behavior**:
- Early termination on first match (efficient)
- No need to check all pairs since exactly one solution exists

### Step 5: Implement Main Function
**Objective**: Orchestrate the solution and produce output

**Structure**:
```python
def main():
    # Parse input
    box_ids = parse_input('input.md')

    # Find the prototype boxes
    result = find_prototype_boxes(box_ids)

    # Output result (just the string, no extra formatting)
    print(result)
```

**Output requirements**:
- Print only the common letters string
- No additional text, newlines, or formatting
- Must match expected format exactly

### Step 6: Add Script Entry Point
**Objective**: Make the script executable

**Code**:
```python
if __name__ == '__main__':
    main()
```

## Complete Function Structure

```
parse_input(filename: str) -> list[str]
    ↓
find_prototype_boxes(box_ids: list[str]) -> str
    ↓ (for each pair)
    count_differences(str1: str, str2: str) -> int
    ↓ (if exactly 1 difference)
    get_common_letters(str1: str, str2: str) -> str
    ↓
main()
```

## Code Organization

**Recommended order in file**:
1. No import statements needed (Part 1's `Counter` import is not needed for Part 2)
2. `parse_input()` - reused from Part 1
3. `count_differences()` - helper function
4. `get_common_letters()` - helper function
5. `find_prototype_boxes()` - main algorithm
6. `main()` - orchestration
7. `if __name__ == '__main__':` - entry point

**Note**: Unlike Part 1, this solution requires no external library imports.

## Edge Cases Handled
- All box IDs have same length (guaranteed by problem)
- Exactly one pair with one difference exists (guaranteed by problem)
- No need for error handling beyond basic file I/O
- Empty strings not possible (input validation already done by problem constraints)

## Performance Expectations
- **Runtime**: < 100ms for 250 box IDs
- **Memory**: Negligible (~7KB for storing 250 strings of 26 chars each)
- **Scalability**: Could handle 10,000 box IDs in under 10 seconds if needed
