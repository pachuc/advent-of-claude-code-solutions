# Implementation Plan: String Classification (Nice vs Naughty)

## Problem Summary
Classify 1000 strings as "nice" or "naughty" based on three criteria:
1. Contains at least 3 vowels (a, e, i, o, u)
2. Contains at least one pair of consecutive identical letters
3. Does NOT contain any forbidden substrings: ab, cd, pq, xy

## Algorithm Design

### Time Complexity Analysis
- Input size: 1000 strings
- Each string needs to be processed once: O(n) where n = number of strings
- For each string of length m: O(m) for each check
- Overall: O(n * m) which is efficient for this input size

### Space Complexity
- O(1) for checking each string (only storing counters/flags)
- O(n * m) for reading input (unavoidable)

## Implementation Steps

### Step 1: Set Up Input Handling
**Goal**: Read strings from input.md file efficiently

**Details**:
- Read file line by line to handle memory efficiently
- Strip whitespace/newlines from each line
- Handle empty lines (skip them)
- **Assumption**: Input contains only lowercase letters a-z (per problem specification)
- **Assumption**: Input may contain blank lines which should be skipped

**Implementation**:
```python
def read_input(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]
```

### Step 2: Implement Vowel Count Check
**Goal**: Check if string contains at least 3 vowels

**Details**:
- Define vowel set: {'a', 'e', 'i', 'o', 'u'}
- Iterate through string once, counting vowels
- Return True if count >= 3, False otherwise
- Time complexity: O(m) where m = string length
- **Assumption**: Input is lowercase (per problem specification)

**Implementation**:
```python
def has_three_vowels(s):
    vowels = {'a', 'e', 'i', 'o', 'u'}
    count = sum(1 for char in s if char in vowels)
    return count >= 3
```

**Why this approach**:
- Single pass through string
- Set lookup is O(1)
- Most efficient approach for this check

### Step 3: Implement Double Letter Check
**Goal**: Check if string contains at least one pair of consecutive identical letters

**Details**:
- Iterate through string comparing each character with next
- Return True immediately when found (early exit optimization)
- Time complexity: O(m) worst case, but often much faster with early exit

**Implementation**:
```python
def has_double_letter(s):
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            return True
    return False
```

**Why this approach**:
- Early exit when double found (optimization)
- Simple and efficient
- No extra space needed

### Step 4: Implement Forbidden Substring Check
**Goal**: Check that string does NOT contain ab, cd, pq, or xy

**Details**:
- Define forbidden substrings: {'ab', 'cd', 'pq', 'xy'}
- Check if any forbidden substring exists in string
- Return True if NONE found, False if ANY found
- Time complexity: O(m) for each substring check, O(4m) = O(m) total

**Implementation**:
```python
def no_forbidden_substrings(s):
    forbidden = ['ab', 'cd', 'pq', 'xy']
    for substring in forbidden:
        if substring in s:
            return False
    return True
```

**Why this approach**:
- Python's `in` operator for strings is optimized (Boyer-Moore-Horspool)
- Early exit when forbidden substring found
- Simple and readable

**Alternative considered**: Single pass checking each pair of consecutive chars
- Would be slightly faster but less maintainable
- For 1000 strings, difference is negligible

### Step 5: Combine Checks into Main Classification Function
**Goal**: Determine if a string is "nice" by checking all three criteria

**Details**:
- Call all three check functions
- String is nice if ALL three return True (AND logic)
- Use short-circuit evaluation for efficiency
- Order matters: check fastest/most likely to fail first

**Optimization note**:
- `no_forbidden_substrings` is fastest (checks only 4 substrings) and likely to fail quickly
- `has_double_letter` can exit early when found
- `has_three_vowels` always scans full string
- **Optimal order**: forbidden check → double letter → vowel count

**Implementation (optimized order)**:
```python
def is_nice(s):
    return (no_forbidden_substrings(s) and
            has_double_letter(s) and
            has_three_vowels(s))
```

### Step 6: Main Processing Function
**Goal**: Count total nice strings in input

**Details**:
- Read all strings from input file
- Apply is_nice() to each string
- Count how many pass all criteria
- Print result

**Implementation**:
```python
def count_nice_strings(filename):
    strings = read_input(filename)
    nice_count = sum(1 for s in strings if is_nice(s))
    return nice_count

if __name__ == '__main__':
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    result = count_nice_strings(filename)
    print(result)
```

**Note**: Supports command-line argument for filename or defaults to 'input.md'

## Complete Program Structure

```
solution.py
├── read_input(filename) -> List[str]
├── has_three_vowels(s) -> bool
├── has_double_letter(s) -> bool
├── no_forbidden_substrings(s) -> bool
├── is_nice(s) -> bool
├── count_nice_strings(filename) -> int
└── main execution block
```

## Performance Considerations

### For Current Input (1000 strings)
- Expected runtime: < 10ms
- All checks are O(m) per string
- Total complexity: O(n * m) where n=1000, m~20 (average string length)
- No optimization needed for this scale

### If Input Were Larger (millions of strings)
Potential optimizations:
1. **Parallel processing**: Process strings in parallel using multiprocessing
2. **Compiled regex**: Combine all checks into single regex pass
3. **Early filtering**: Check forbidden substrings first (fastest disqualification)

However, these are NOT needed for current problem scope.

## Edge Cases Handled

1. **Empty strings**: Handled by input reading (stripped and filtered)
2. **Single character strings**: All checks handle this correctly
   - Vowel check: works
   - Double letter: loop doesn't execute, returns False
   - Forbidden: no match possible, returns True
3. **All same character**: Handled correctly (e.g., "aaa" is nice)
4. **No vowels**: Returns False (fails vowel check)
5. **Multiple forbidden substrings**: Returns False on first match

## Testing Strategy Reference
See `test_plan.md` for comprehensive testing approach including:
- Unit tests for each function
- Integration tests
- Known example validation
- Edge case verification
