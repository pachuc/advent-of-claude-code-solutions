# Implementation Plan: High-Entropy Passphrase Validation

## Problem Summary
Count valid passphrases in a list where a valid passphrase contains no duplicate words.

## Algorithm Analysis

### Time Complexity Considerations
- Input: 512 passphrases, each with varying numbers of words
- For each passphrase, we need to detect duplicates
- Best approach: O(n) per passphrase where n = number of words

### Proposed Algorithm
Use a **set-based approach** for optimal O(n) time complexity per passphrase:
1. Split each passphrase into words
2. Convert words to a set (automatically handles uniqueness)
3. Compare set length to word list length
4. If equal → no duplicates (valid), if different → duplicates exist (invalid)

**Alternative approaches considered:**
- Nested loop comparison: O(n²) - too slow, rejected
- Sorting + adjacent comparison: O(n log n) - slower than set approach, rejected
- Dictionary/Counter: O(n) - equivalent but more complex, rejected

**Selected approach:** Set comparison - O(n) time, O(n) space, simplest implementation

## Implementation Steps

### Step 1: File I/O Setup
```python
# Read input file
with open('input.md', 'r') as f:
    lines = f.read().strip().split('\n')
```
- Read entire file as string
- Strip trailing whitespace
- Split into lines (one passphrase per line)
- Handle potential empty lines at end of file

### Step 2: Core Validation Logic
```python
def is_valid_passphrase(passphrase):
    """
    Check if passphrase has no duplicate words.

    Args:
        passphrase (str): A space-separated string of words

    Returns:
        bool: True if valid (no duplicates), False otherwise
    """
    words = passphrase.split()
    return len(words) == len(set(words))
```
- Split passphrase on whitespace into word list
- Convert to set (removes duplicates)
- Compare lengths: if equal, no duplicates existed

### Step 3: Count Valid Passphrases
```python
valid_count = 0
for line in lines:
    if line.strip():  # Skip empty lines
        if is_valid_passphrase(line):
            valid_count += 1
```
- Iterate through each line
- Skip empty lines (defensive programming)
- Count valid passphrases

### Step 4: Output Result
```python
print(valid_count)
```
- Output single integer as specified
- No additional formatting required

## Complete Implementation Structure

```python
def is_valid_passphrase(passphrase):
    """Check if passphrase has no duplicate words."""
    words = passphrase.split()
    return len(words) == len(set(words))

def main():
    # Read input
    with open('input.md', 'r') as f:
        lines = f.read().strip().split('\n')

    # Count valid passphrases
    valid_count = sum(1 for line in lines if line.strip() and is_valid_passphrase(line))

    # Output result
    print(valid_count)

if __name__ == "__main__":
    main()
```

## Performance Analysis

### Time Complexity
- **Per passphrase:** O(w) where w = number of words
- **Overall:** O(n × w_avg) where n = number of passphrases, w_avg = average words per passphrase
- For the given input (~512 passphrases, ~10 words each): ~5,120 operations
- **Expected runtime:** < 1ms (highly efficient)

### Space Complexity
- **Per passphrase:** O(w) for word list and set
- **Overall:** O(w_max) where w_max = maximum words in a single passphrase
- Space is reused for each passphrase (no accumulation)
- **Expected memory:** Negligible (< 1KB)

## Edge Cases Handled

1. **Empty lines:** Skipped entirely via `if line.strip()` - not counted as valid or invalid
2. **Single word passphrase:** Valid (no duplicates possible with one word)
3. **Empty passphrase (after splitting):** Would be valid if tested directly (len([]) == len(set([])) == 0), but empty lines are skipped in main loop
4. **Multiple spaces between words:** `split()` handles automatically by splitting on any whitespace
5. **Trailing/leading whitespace:** `strip()` handles automatically before processing

## Implementation Notes

- No error handling needed for malformed input (input format guaranteed per problem spec)
- Input file (`input.md`) is assumed to exist in the working directory (standard for Advent of Code problems)
- No logging needed (simple script)
- No configuration needed (single-purpose script)
- Function can be easily unit tested independently of file I/O
- Clean separation between validation logic and I/O logic
