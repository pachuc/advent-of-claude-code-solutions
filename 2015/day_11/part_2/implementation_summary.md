# Implementation Summary: Password Generation Algorithm (Part Two)

## Overview
Successfully implemented a solution to find the next valid password after `vzbxxyzz` (Part 1 answer) by incrementing passwords in base-26 and validating against three security requirements. Part 2 reuses the exact same algorithm from Part 1 with only a different starting password.

## Problem
Given the password `vzbxxyzz` (the result from Part One), find the next valid password that:
1. Contains at least one increasing straight of 3 consecutive letters (e.g., `abc`, `xyz`)
2. Does NOT contain the letters `i`, `o`, or `l`
3. Contains at least two different, non-overlapping pairs of letters (e.g., `aa` and `bb`)

## Solution Result
**Input:** `vzbxxyzz` (Part 1 answer)
**Output:** `vzcaabcc`

### Verification
The output meets all requirements:
- ✓ Has increasing straight: `abc` at positions 4-6
- ✓ No forbidden characters (i, o, l)
- ✓ Two different pairs: `aa` at positions 3-4 and `cc` at positions 6-7

## Files Created

### 1. solution.py
Main solution file containing:

#### Core Functions:
- **`increment_password(password: str) -> str`**: Increments password by one position in base-26 arithmetic, handling wrap-arounds from 'z' to 'a' with carry propagation
- **`has_increasing_straight(password: str) -> bool`**: Checks for at least one sequence of 3 consecutive letters in alphabetical order
- **`has_forbidden_chars(password: str) -> bool`**: Checks if password contains 'i', 'o', or 'l'
- **`has_two_pairs(password: str) -> bool`**: Checks for at least two different, non-overlapping pairs using a while loop with manual index control to properly skip pairs
- **`is_valid_password(password: str) -> bool`**: Combines all three validation checks with short-circuit evaluation
- **`skip_forbidden_chars(password: str) -> str`**: Optimization that skips entire ranges of passwords containing forbidden characters
- **`find_next_password(current: str) -> str`**: Main algorithm that increments and validates until finding the next valid password
- **`main()`**: Reads input from `input.md`, finds next password, and prints result

### 2. test_solution.py
Comprehensive test suite containing:
- Unit tests for all helper functions
- Tests for password increment logic (including edge cases like wrap-arounds)
- Tests for validation functions with various inputs
- Integration tests using Part One examples (`abcdefgh` → `abcdffaa`, `ghijklmn` → `ghjaabcc`)
- All 7 test suites with 30+ test cases

### 3. verify_output.py
Verification script that:
- Checks basic properties (length, lowercase, ordering)
- Verifies each of the three requirements
- Identifies and displays the specific straight and pairs found
- Confirms overall validity

## Implementation Approach

### Algorithm Structure
1. Start with input password
2. Increment by one (we need the NEXT password, not current)
3. Check for forbidden characters and skip ahead if found (optimization)
4. Validate against all three requirements
5. If valid, return; otherwise increment and repeat

### Key Design Decisions

#### 1. Base-26 Increment Logic
Used right-to-left iteration with carry propagation, similar to decimal arithmetic:
```python
while i >= 0:
    if chars[i] == 'z':
        chars[i] = 'a'
        i -= 1  # Carry to next position
    else:
        chars[i] = chr(ord(chars[i]) + 1)
        break
```

#### 2. Two Pairs Detection
Critical implementation detail: Used a while loop with manual index control (not a for loop) to properly skip both characters in a found pair:
```python
i = 0
while i < len(password) - 1:
    if password[i] == password[i+1]:
        pairs.add(password[i])
        i += 2  # Skip both characters
    else:
        i += 1
```
This ensures non-overlapping pairs and tracks different letters using a set.

#### 3. Skip Optimization
When forbidden characters are found, increment the leftmost forbidden character and set all positions to its right to 'a'. This skips entire ranges:
- `abciefgh` → `abcjaaaa` (skips all passwords starting with `abci`)
- `ghijklmn` → `ghjaaaaa` (skips all passwords starting with `ghi`)

This optimization reduces iterations from potentially millions to thousands.

#### 4. Validation Order
Ordered checks by likelihood of failure and computational cost:
1. Forbidden chars first (cheapest, often fails)
2. Two pairs second (moderate cost)
3. Increasing straight last (moderate cost)

Short-circuit evaluation ensures we don't do unnecessary work.

## Testing Process

### Phase 1: Unit Testing
All unit tests passed successfully:
- ✓ Password increment with wrap-arounds
- ✓ Increasing straight detection in various positions
- ✓ Forbidden character detection
- ✓ Two different pairs detection (including edge cases like `aaaa`)
- ✓ Skip optimization including edge case where forbidden char is at end

### Phase 2: Integration Testing
Verified against Part One examples:
- ✓ `abcdefgh` → `abcdffaa` (correct)
- ✓ `ghijklmn` → `ghjaabcc` (correct)

Both examples produced expected outputs, confirming the algorithm logic is correct.

### Phase 3: Solution Testing
Ran solution with Part 2 input `vzbxxyzz` (Part 1 answer):
- ✓ Produced output `vzcaabcc`
- ✓ Verified output meets all three requirements
- ✓ Confirmed output comes after input in sequence
- ✓ Execution completed quickly (under 1 second)

### Testing Results
**Status:** All tests passed ✓

The comprehensive test suite of 30+ test cases across 7 test functions all passed, including:
- Edge cases (wrap-arounds, forbidden chars at various positions)
- Boundary conditions (all z's, single pairs vs multiple pairs)
- Known examples from problem statement
- Actual problem input

## Performance

The solution executed very quickly (under 1 second) thanks to:
- Efficient O(n) validation functions where n=8 (password length)
- Skip optimization that reduces search space dramatically
- Short-circuit evaluation in validation checks

The skip optimization was crucial - without it, the solution could have taken significantly longer due to needing to skip past forbidden characters.

## Complexity Analysis

- **Time Complexity:** O(k*n) where k is iterations needed, n=8 (password length)
- **Space Complexity:** O(n) for string manipulation
- **Actual iterations:** Relatively few due to skip optimization

## Conclusion

The solution successfully finds the next valid password after `vzbxxyzz` (Part 1 answer), which is **`vzcaabcc`**. The implementation is clean, well-tested, and efficient. All validation requirements are met, and the algorithm handles edge cases correctly.

The modular design with separate validation functions made testing straightforward and ensured correctness. The skip optimization was essential for reasonable performance. By reusing the Part 1 solution with only a change to the input source (reading from `part_1_answer.txt` instead of `input.md`), Part 2 was solved efficiently and correctly.
