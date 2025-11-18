# Implementation Plan: Circular Digit Sum (Inverse Captcha)

## Problem Analysis

We need to solve a circular captcha where we sum digits that match their next neighbor in a circular sequence. The input is 2000 digits long, which is small enough that algorithmic efficiency is not a major concern - even O(n) will execute instantly.

## Algorithm Design

**Approach**: Single-pass linear scan with modulo arithmetic for circular wrapping

**Time Complexity**: O(n) where n is the length of the digit sequence
**Space Complexity**: O(1) - only storing the running sum

## Implementation Steps

### Step 1: Input Reading and Parsing
- Read the input from `input.md`
- Strip any whitespace/newlines to get clean digit string
- No error handling needed - problem guarantees valid non-empty digit string
- Note: See `test_plan.md` for verification strategy

### Step 2: Core Algorithm Implementation
Create a function `solve_captcha(digits: str) -> int`:

1. **Initialize variables**:
   - `total_sum = 0` - accumulator for matching digits
   - `n = len(digits)` - cache the length

2. **Iterate through each position**:
   - Use a for loop with index `i` from 0 to n-1
   - For each position, compare `digits[i]` with `digits[(i + 1) % n]`
   - The modulo operation handles the circular wrap (last digit compares with first)

3. **Check for matches and accumulate**:
   - If `digits[i] == digits[(i + 1) % n]`:
     - Add `int(digits[i])` to `total_sum`
   - Note: We convert the character to integer only when needed

4. **Return the result**:
   - Return `total_sum`

### Step 3: Main Execution Flow
1. Read input file content
2. Clean the input (strip whitespace)
3. Call `solve_captcha()` with the cleaned input
4. Print the result as a single integer (just the number, no additional formatting)

## Code Structure

```
solution.py
├── solve_captcha(digits: str) -> int
│   └── Main algorithm logic
└── main execution block
    ├── Read input.md
    ├── Parse/clean input
    ├── Call solve_captcha()
    └── Print result
```

## Key Implementation Details

### Circular Index Calculation
- Use `(i + 1) % n` to get next index
- When `i = n-1` (last position), `(n-1 + 1) % n = 0` (wraps to first)
- This elegantly handles the circular nature without special cases

### Character to Integer Conversion
- Only convert when we find a match: `int(digits[i])`
- Characters '0'-'9' convert directly to integers 0-9

### Edge Cases Handled by Design
- **Single digit**: When n=1, `(0 + 1) % 1 = 0`, compares with itself
- **Two digits**: Works naturally with modulo
- **Zero digits**: Character '0' works the same as any other digit
- **Empty string**: Not handled - problem guarantees non-empty input

## Algorithm Efficiency Considerations

**Why O(n) is optimal**:
- We must examine every digit at least once to determine matches
- Cannot do better than O(n) for this problem
- With n=2000, this runs in microseconds

**No optimization needed**:
- Input size is small (2000 characters)
- Simple operations (character comparison, integer addition)
- No complex data structures required
- Memory usage is minimal (single integer accumulator)

## Implementation Pseudocode

```
function solve_captcha(digits):
    total_sum = 0
    n = length(digits)

    for i from 0 to n-1:
        next_i = (i + 1) % n
        if digits[i] == digits[next_i]:
            total_sum += int(digits[i])

    return total_sum

main:
    content = read_file("input.md")
    digits = content.strip()
    result = solve_captcha(digits)
    print(result)
```

## Expected Output

For the given input, we should get a single integer representing the sum of all digits that match their circular successor.
