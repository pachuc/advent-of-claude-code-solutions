# Implementation Plan - Part 2: Modified Repetition Code

## Overview
Part 2 uses the same input and almost identical logic to Part 1, but instead of selecting the **most frequent** character at each position, we select the **least frequent** character. This is a minimal modification to the existing Part 1 solution.

## Key Differences from Part 1
- **Part 1**: `Counter.most_common(1)[0][0]` - gets the most frequent character
- **Part 2**: `Counter.most_common()[-1][0]` - gets the least frequent character (last item in the sorted list)

## Implementation Steps

### Step 1: Reuse Part 1 Structure
- Copy the structure from `part_1_solution.py` as the foundation
- Keep the same functions: `read_input()`, `decode_message()`, and `main()`
- Maintain the same input reading and validation logic

### Step 2: Modify the decode_message() Function
The only substantive change needed:
- **Current (Part 1)**: The line in `decode_message()` that finds the most frequent character uses `Counter(chars_at_pos).most_common(1)[0][0]`
- **Modified (Part 2)**: Change to `Counter(chars_at_pos).most_common()[-1][0]`
  - `most_common()` without argument returns ALL items sorted by frequency (descending)
  - Index `[-1]` gets the last element, which is the least frequent
  - `[0]` gets the character from the (char, count) tuple

**Alternative approach** (equally valid):
- Use `Counter(chars_at_pos).most_common()[:-1]` and reverse, or
- Manually find minimum: `min(Counter(chars_at_pos).items(), key=lambda x: x[1])[0]`
- The `most_common()[-1][0]` approach is cleanest and most readable

**Note on Tie-Breaking**: If multiple characters tie for least frequent, `Counter.most_common()` will return one of them in a consistent but implementation-dependent order. This should not affect the puzzle solution, as the actual input likely has unique minimum frequencies at each position.

### Step 3: Preserve Input Handling
- Keep the same `read_input()` function unchanged
- Continue reading from 'input.md'
- Maintain validation for non-empty lines and equal line lengths

### Step 4: Keep Validation Logic
- Retain the check that all lines have the same length
- This prevents errors from malformed input
- No additional validation needed for Part 2

### Step 5: Main Function
- Keep the same structure: read input, decode, print result
- No changes needed to main() function

## Algorithm Complexity Analysis

### Time Complexity
- **Reading input**: O(N × M) where N = number of lines, M = message length
- **Decoding**: For each of M positions:
  - Collect characters: O(N)
  - Count frequencies: O(N)
  - Get least common (via most_common()): O(K log K) where K = unique chars per position (typically K ≤ 26)
  - Total for all positions: O(M × (N + K log K))
- **Overall**: O(N × M) since K is bounded by alphabet size (26)

### Space Complexity
- **Input storage**: O(N × M) for storing all lines
- **Counter per position**: O(K) where K ≤ 26
- **Overall**: O(N × M)

### Efficiency for Given Input
- Input: 598 lines × 8 characters = 4,784 characters
- This is very small; any reasonable algorithm will run instantly
- No optimization needed beyond the straightforward approach

## Complete Code Structure

```python
from collections import Counter
import sys

def read_input(filepath):
    """Read and parse input file."""
    # [Same as Part 1 - no changes]

def decode_message(lines):
    """Decode message by finding LEAST frequent char at each position."""
    if not lines:
        return ""

    message_length = len(lines[0])
    # Validate equal lengths
    for i, line in enumerate(lines):
        if len(line) != message_length:
            raise ValueError(f"Line {i} has length {len(line)}, expected {message_length}")

    decoded = []
    for pos in range(message_length):
        chars_at_pos = [line[pos] for line in lines]
        # KEY CHANGE: Get LEAST frequent instead of most frequent
        least_frequent = Counter(chars_at_pos).most_common()[-1][0]
        decoded.append(least_frequent)

    return ''.join(decoded)

def main():
    lines = read_input('input.md')
    result = decode_message(lines)
    print(result)

if __name__ == '__main__':
    main()
```

## Implementation Checklist
- [ ] Copy imports from Part 1 (Counter, sys)
- [ ] Copy read_input() function unchanged
- [ ] Copy decode_message() structure with modification to line 36
- [ ] Change `most_common(1)[0][0]` to `most_common()[-1][0]`
- [ ] Copy main() function unchanged
- [ ] Verify script can be run as standalone module

## Expected Behavior
- Read 598 lines of 8-character strings from input.md
- For each of 8 positions, count character frequencies
- Select the least frequent character at each position
- Combine into final 8-character lowercase string
- Print result to stdout

## Expected Output Characteristics
- **Length**: Exactly 8 characters
- **Character set**: Lowercase letters (a-z)
- **Different from Part 1**: Should NOT be `qzedlxso` (the Part 1 answer)
- **Format**: Single line output with no extra formatting

## Verification Strategy
After implementation, verify only the expected line changed:
```bash
# Compare Part 1 and Part 2 solutions to ensure minimal diff
diff part_1_solution.py solution.py
# Should show only the one-line change in decode_message()
```
