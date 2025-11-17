# Implementation Summary - Part 2: Modified Repetition Code

## Problem Overview
Part 2 required decoding a message using a modified repetition code protocol. Unlike Part 1, which selected the **most frequent** character at each position, Part 2 selects the **least frequent** character at each position to decode the original message.

## Solution Approach
I adapted the Part 1 solution by making a single, strategic change to the character selection logic:

**Key Change:**
- **Part 1**: `Counter(chars_at_pos).most_common(1)[0][0]` - gets the most frequent character
- **Part 2**: `Counter(chars_at_pos).most_common()[-1][0]` - gets the least frequent character

This minimal modification leverages the fact that `Counter.most_common()` returns all items sorted by frequency in descending order. By accessing the last element with `[-1]`, we get the character with the lowest frequency.

## Implementation Details

### Files Created
1. **solution.py** - Main solution file (adapted from part_1_solution.py)
2. **test_example.txt** - Test file containing the example input from the problem description
3. **implementation_summary.md** - This summary document

### Code Structure
The solution maintains the same structure as Part 1:
- `read_input(filepath)` - Reads and parses the input file (unchanged)
- `decode_message(lines)` - Decodes the message using least frequent character selection (modified)
- `main()` - Orchestrates reading input and printing the result (unchanged)

### Modified Function
Only the `decode_message()` function was modified:

```python
def decode_message(lines):
    """Decode message by finding least frequent char at each position."""
    if not lines:
        return ""

    # Validate all lines have the same length
    message_length = len(lines[0])
    for i, line in enumerate(lines):
        if len(line) != message_length:
            raise ValueError(f"Line {i} has length {len(line)}, expected {message_length}")

    decoded = []

    for pos in range(message_length):
        # Get all characters at this position
        chars_at_pos = [line[pos] for line in lines]
        # Find least frequent character (KEY CHANGE from Part 1)
        least_frequent = Counter(chars_at_pos).most_common()[-1][0]
        decoded.append(least_frequent)

    return ''.join(decoded)
```

The only substantive change is on line 36 (solution.py:36), where `most_common(1)[0][0]` was replaced with `most_common()[-1][0]`.

## Testing Process

### Test 1: Example Validation
**Input:** The 16-line example from the problem description
**Expected Output:** `advent`
**Actual Output:** `advent`
**Result:** ✅ PASSED

This confirmed the algorithm correctly identifies the least frequent character at each position.

### Test 2: Actual Input
**Input:** 598 lines of 8-character strings from input.md
**Expected Output:** An 8-character lowercase string different from Part 1's answer
**Actual Output:** `ucmifjae`
**Result:** ✅ PASSED

### Test 3: Comparison with Part 1
**Part 1 Answer:** `qzedlxso`
**Part 2 Answer:** `ucmifjae`
**Result:** ✅ DIFFERENT (as expected)

The answers are completely different, confirming that the modified decoding strategy produces a distinct result.

### Test 4: Manual Verification
I manually verified the first two positions of the decoded message:

**Position 0:**
- Counted frequency of all first characters in the input
- Least frequent character: 'u' (appears 22 times, while most others appear 23 times)
- Solution output position 0: 'u' ✅

**Position 1:**
- Counted frequency of all second characters in the input
- Least frequent character: 'c' (appears 22 times, while most others appear 23 times)
- Solution output position 1: 'c' ✅

This manual verification confirms the solution is correctly computing the least frequent character for each position.

## Performance
The solution executed nearly instantaneously on the actual input (598 lines × 8 characters). The time complexity is O(N × M) where N is the number of lines and M is the message length, which is efficient for this problem size.

## Final Answer
**Part 2 Solution:** `ucmifjae`

## Code Quality Notes
- The solution maintains the same error handling and input validation as Part 1
- Code is clean, readable, and well-commented
- The modification from Part 1 is minimal and focused, demonstrating good code reuse
- All edge cases handled by Part 1 (empty input, file not found, mismatched line lengths) are preserved

## Conclusion
The Part 2 solution successfully decodes the message using the modified repetition code protocol. By changing just one line of code from the Part 1 solution, we efficiently adapted the algorithm to select least frequent characters instead of most frequent characters. All tests passed, and manual verification confirmed the correctness of the implementation.
