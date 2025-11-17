# Implementation Plan: Santa's Password Generator (Part 2)

## Overview
Part 2 is identical to Part 1 algorithmically - we need to find the next valid password, but now starting from the Part 1 answer (`vzbxxyzz`) instead of the original input (`vzbxkghb`). The exact same code can be reused with only the starting password changed.

## Key Insight
**We can reuse the entire Part 1 solution (`part_1_solution.py`) with minimal modification.** The algorithm, validation logic, and optimization techniques are identical.

## Why Copy-Paste Instead of Module Import?
For this puzzle solution, we use a copy-paste approach rather than importing Part 1 as a module because:
- Each puzzle part should be self-contained and independently runnable
- No shared code infrastructure is needed for simple one-off scripts
- Avoids import path complications and dependencies
- Maintains simplicity appropriate for puzzle scripts

## Implementation Steps

### Step 1: Copy Core Logic from Part 1
Reuse all functions from `part_1_solution.py`:
- `increment_password(password: str) -> str` - Increments password in base-26 with forbidden character optimization
- `has_no_forbidden_chars(password: str) -> bool` - Validates no 'i', 'o', or 'l' present
- `has_increasing_straight(password: str) -> bool` - Validates at least one sequence of 3 consecutive increasing letters
- `has_two_pairs(password: str) -> bool` - Validates at least two different non-overlapping pairs
- `is_valid_password(password: str) -> bool` - Combines all three validation checks
- `find_next_password(current: str) -> str` - Main algorithm to find next valid password

### Step 2: Modify Input Handling
**Change the starting password from Part 1 input to Part 1 answer:**
- Instead of reading from `input.md` (which contains `vzbxkghb`), use the Part 1 answer: `vzbxxyzz`
- This can be done by:
  - Option A: Reading from `part_1_answer.txt` file
  - Option B: Hardcoding `vzbxxyzz` as the starting password
  - **Recommended**: Option A for clarity and traceability

### Step 3: Main Execution Logic
```python
if __name__ == "__main__":
    # Read Part 1 answer as starting password
    with open('part_1_answer.txt', 'r') as f:
        current_password = f.read().strip()

    # Find next valid password (same algorithm as Part 1)
    next_password = find_next_password(current_password)

    # Output result
    print(next_password)
```

## Algorithm Details (Inherited from Part 1)

### Password Incrementing with Optimization
The `increment_password` function implements:
1. Base-26 increment (rightmost letter first)
2. Wrap 'z' to 'a' with carry-over to the left
3. **Critical optimization**: When incrementing produces 'i', 'o', or 'l', immediately skip to next valid character ('j', 'p', or 'm') and reset all positions to the right to 'a'
   - This prevents checking thousands of invalid passwords
   - Example: `vzbxxyzz` → `vzbxxzaa` → if 'i'/'o'/'l' appears, skip ahead

### Validation Functions
1. **has_no_forbidden_chars**: O(n) scan for 'i', 'o', 'l'
2. **has_increasing_straight**: O(n) scan for consecutive triplets (e.g., 'abc', 'xyz')
3. **has_two_pairs**: O(n) scan with non-overlapping pair detection using set to track unique pair letters

### Main Search Loop
```python
def find_next_password(current: str) -> str:
    password = increment_password(current)
    iterations = 0
    MAX_ITERATIONS = 10_000_000

    while iterations < MAX_ITERATIONS:
        if is_valid_password(password):
            return password
        password = increment_password(password)
        iterations += 1

    raise Exception("Max iterations exceeded")
```

## Time Complexity Analysis
- **Per password check**: O(n) where n = 8 (password length) → O(1)
- **Total iterations**: Typically a few hundred to a few thousand passwords need to be checked
- **With optimization**: The forbidden character skip reduces search space dramatically
- **Expected runtime**: < 1 second for typical inputs

## Space Complexity
- O(1) - only storing current password and a few temporary variables

## Expected Outcome
Starting from `vzbxxyzz`, the algorithm will:
1. Increment to get the next password (`vzbxxzaa`)
   - **Important**: While `vzbxxyzz` itself is valid (has `xyz` straight, `xx` and `zz` pairs, no forbidden chars), the algorithm correctly increments at least once before checking (see line 78 in part_1_solution.py)
2. Check validity against all three rules
3. Continue until a valid password is found
4. Return the result (expected to be an 8-character lowercase string)

## Code Reusability
**Percentage of code reuse from Part 1: ~95%**
- All validation functions: 100% reuse
- Increment function: 100% reuse
- Main search function: 100% reuse
- Only change: Input source (read from `part_1_answer.txt` instead of `input.md`)

## Complete Implementation Structure

```python
def increment_password(password: str) -> str:
    """
    Increment password by 1 in base-26, with forbidden character optimization.
    If increment produces 'i', 'o', or 'l', skip to next valid char and reset right positions.
    """
    # [Copy implementation from part_1_solution.py]

def has_no_forbidden_chars(password: str) -> bool:
    """Check if password contains no forbidden characters (i, o, l)."""
    # [Copy implementation from part_1_solution.py]

def has_increasing_straight(password: str) -> bool:
    """Check if password has at least one sequence of three consecutive increasing letters."""
    # [Copy implementation from part_1_solution.py]

def has_two_pairs(password: str) -> bool:
    """Check if password has at least two different non-overlapping pairs."""
    # [Copy implementation from part_1_solution.py]

def is_valid_password(password: str) -> bool:
    """Check if password meets all three validation requirements."""
    # [Copy implementation from part_1_solution.py]

def find_next_password(current: str) -> str:
    """Find the next valid password after the current one."""
    # [Copy implementation from part_1_solution.py]

if __name__ == "__main__":
    # Read Part 1 answer as starting password
    with open('part_1_answer.txt', 'r') as f:
        current_password = f.read().strip()

    # Find next valid password
    next_password = find_next_password(current_password)

    # Output result
    print(next_password)
```

## Implementation Checklist
- [ ] Copy all helper functions from `part_1_solution.py`
- [ ] Modify input reading to use Part 1 answer (`part_1_answer.txt`)
- [ ] Keep the same main execution flow
- [ ] Ensure output is printed to stdout
- [ ] Test with the Part 1 answer as starting point
