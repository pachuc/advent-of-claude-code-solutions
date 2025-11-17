# Implementation Plan: Password Generation Algorithm

## Overview
Create a Python script that generates the next valid password by incrementing the current password until all validation criteria are met. The solution must be efficient enough to handle the potentially large search space.

## Updates Based on Critique
This implementation plan has been updated to address the following issues:
1. Fixed incorrect increment example (Step 1, Line 26) - clarified that increment happens first, then forbidden char optimization
2. Added additional example showing forbidden char optimization with position reset
3. Clarified iteration range in Step 3 (positions 0 to 5 for 8-char string)
4. Enhanced Step 4 explanation of pair counting with set usage
5. Added explicit pseudocode for max iterations safety check in Step 6
6. Clarified that input validation is out of scope for this script-level solution in Step 7

## Step-by-Step Implementation

### Step 1: Password Increment Function
**Objective:** Implement base-26 password incrementing with forbidden character optimization

**Details:**
- Create a function `increment_password(password: str) -> str`
- Convert string to list for mutability
- Start from rightmost character (index 7)
- For each position:
  - Increment character by 1 (e.g., 'a' → 'b')
  - If character becomes 'z' + 1, wrap to 'a' and carry to next position
  - **Optimization:** If incremented character is 'i', 'o', or 'l', immediately set it to next valid character ('j', 'p', 'm' respectively) and set all positions to the right to 'a'
- Return the modified string

**Example Logic:**
```
"abc" → "abd"
"abz" → "aca"
"azz" → "baa"
"abh" → "abi" (increment) → "abj" (forbidden char optimization skips 'i')
"azzn" → "azzo" (increment) → "azpa" (forbidden char optimization skips 'o', resets right positions)
```

### Step 2: Validation Function - Forbidden Characters
**Objective:** Check if password contains i, o, or l

**Details:**
- Create function `has_no_forbidden_chars(password: str) -> bool`
- Return `True` if none of 'i', 'o', 'l' are in password
- Implementation: `return not any(c in password for c in 'iol')`
- **Rationale:** This is the fastest check, so do it first

### Step 3: Validation Function - Increasing Straight
**Objective:** Check for three consecutive increasing letters

**Details:**
- Create function `has_increasing_straight(password: str) -> bool`
- Iterate through password positions 0 to 5 (indices where i+2 is still valid for 8-char string)
- For each position i:
  - Check if `ord(password[i+1]) == ord(password[i]) + 1`
  - AND `ord(password[i+2]) == ord(password[i]) + 2`
  - If both true, return `True`
- Return `False` if no straight found

**Example:**
- "abc" has straight at position 0
- "xabcdef" has straight at position 1
- "axcdefg" has NO straight (skips b)

### Step 4: Validation Function - Two Non-Overlapping Pairs
**Objective:** Check for at least two different non-overlapping pairs

**Details:**
- Create function `has_two_pairs(password: str) -> bool`
- Initialize: `pairs_found = []`, `i = 0`
- While `i < 7`:
  - If `password[i] == password[i+1]`:
    - Add character to `pairs_found` (store the letter that forms the pair)
    - Skip ahead by 2 positions: `i += 2` (avoid overlap)
  - Else: `i += 1`
- Return `True` if `len(set(pairs_found)) >= 2` (use set to count unique letters with pairs)

**Example:**
- "aabbcc" → pairs at positions 0,2,4 → ['a','b','c'] → set(['a','b','c']) has 3 unique → True
- "aabaa" → pairs at positions 0,3 → ['a','a'] → set(['a']) has 1 unique → False
- "aaabb" → pairs at positions 0,3 → ['a','b'] → set(['a','b']) has 2 unique → True
- "aaaaabcd" → pairs at positions 0,2 → ['a','a'] → set(['a']) has 1 unique → False

### Step 5: Combined Validation Function
**Objective:** Check all three requirements efficiently

**Details:**
- Create function `is_valid_password(password: str) -> bool`
- Check in order of efficiency (fastest to slowest):
  1. `has_no_forbidden_chars(password)` - O(8) simple check
  2. `has_increasing_straight(password)` - O(6) with early exit
  3. `has_two_pairs(password)` - O(8) with potential skips
- Return `True` only if all three pass
- Use short-circuit evaluation: `return has_no_forbidden_chars(password) and has_increasing_straight(password) and has_two_pairs(password)`

### Step 6: Main Password Generation Function
**Objective:** Find the next valid password

**Details:**
- Create function `find_next_password(current: str) -> str`
- Start with: `password = increment_password(current)` (must increment at least once)
- Initialize: `iterations = 0`, `MAX_ITERATIONS = 10_000_000`
- Loop while `iterations < MAX_ITERATIONS`:
  - If `is_valid_password(password)`: return password
  - Else: `password = increment_password(password)`
  - Increment: `iterations += 1`
- If loop exits without finding valid password, raise exception: "Max iterations exceeded"
- **Safety:** This prevents infinite loops while allowing sufficient search space

### Step 7: Input/Output Handler
**Objective:** Read input, process, and output result

**Details:**
- Read input from file or stdin
- Strip whitespace: `current_password = input_line.strip()`
- **Note:** Input validation (8 lowercase letters) is assumed for this script-level solution
- Call `find_next_password(current_password)`
- Print result to stdout

### Step 8: Main Script Structure
**Objective:** Organize code cleanly

**Details:**
```python
# Functions (in order):
# - increment_password(password)
# - has_no_forbidden_chars(password)
# - has_increasing_straight(password)
# - has_two_pairs(password)
# - is_valid_password(password)
# - find_next_password(current)

# Main execution:
if __name__ == "__main__":
    # Read input
    # Process
    # Output result
```

## Algorithm Complexity Analysis

**Time Complexity per iteration:**
- Increment: O(8) worst case with carry propagation
- Validation: O(8) for all checks combined
- Per iteration total: O(8) = O(1)

**Expected iterations:**
- Worst case is hard to determine, but optimizations significantly reduce search space
- Forbidden character skip optimization reduces search space by ~11.5% (3/26)
- Expected: tens of thousands of iterations at most for typical inputs

**Space Complexity:**
- O(1) - only storing strings of fixed length 8

## Optimization Summary

1. **Forbidden character skipping during increment:** When incrementing produces 'i', 'o', or 'l', immediately jump to next valid character and reset rightward positions
2. **Validation order:** Check fastest conditions first to fail fast
3. **Non-overlapping pair detection:** Skip by 2 when pair found to avoid checking overlaps
4. **Early exits:** Use boolean short-circuit evaluation

## Expected Output Format
Plain text string, 8 lowercase letters, no additional formatting or newlines beyond the answer itself.
