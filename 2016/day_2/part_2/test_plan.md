# Test Plan: Bathroom Keypad Code (Part 2)

## Testing Objectives
1. Verify the diamond keypad layout is correctly implemented
2. Ensure invalid moves (to empty spaces) are properly rejected
3. Validate the correct bathroom code is generated for the puzzle input
4. Confirm edge cases around boundary buttons are handled correctly

## Test Strategy Overview
Since this is a scripting problem (not production code), we focus on:
- **Correctness**: Does it produce the right answer?
- **Example validation**: Does it match the provided example?
- **Edge case handling**: Does it properly handle corner/boundary positions?

We do NOT need extensive unit tests, error handling for malformed input, or performance benchmarks beyond basic verification.

## Test Cases

### Test 1: Diamond Keypad Layout Verification
**Purpose**: Ensure the keypad dictionary is correctly defined

**Method**: Visual inspection and spot checks
- Verify the keypad dictionary contains exactly 13 entries (1-9, A-D)
- Complete expected keypad dictionary:
  ```python
  {
      (0, 2): '1',
      (1, 1): '2', (1, 2): '3', (1, 3): '4',
      (2, 0): '5', (2, 1): '6', (2, 2): '7', (2, 3): '8', (2, 4): '9',
      (3, 1): 'A', (3, 2): 'B', (3, 3): 'C',
      (4, 2): 'D'
  }
  ```
- Spot check key positions:
  - (0, 2) maps to '1' (top)
  - (2, 2) maps to '7' (center)
  - (2, 0) maps to '5' (starting position)
  - (4, 2) maps to 'D' (bottom)

**Expected Result**: All 13 positions correctly mapped as shown above

**Validation**: Print the keypad dictionary or compare against the expected dictionary

**Priority**: **MANDATORY** - This is foundational to the entire solution

---

### Test 2: Provided Example Test
**Purpose**: Verify the solution matches the example from the problem description

**Priority**: **MANDATORY** - This is the primary correctness validation

**Input**:
```
ULL
RRDDD
LURDL
UUUUD
```

**Expected Output**: `5DB3`

**Detailed Trace**:
1. Start at '5' (position 2, 0)
2. **Line 1 (ULL)**:
   - U: (2,0) -> (1,0) = invalid (no button), stay at (2,0) = '5'
   - L: (2,0) -> (2,-1) = invalid (no button), stay at (2,0) = '5'
   - L: same, stay at (2,0) = '5'
   - **Result: '5'**

3. **Line 2 (RRDDD)**: Starting at (2,0) = '5'
   - R: (2,0) -> (2,1) = '6'
   - R: (2,1) -> (2,2) = '7'
   - D: (2,2) -> (3,2) = 'B'
   - D: (3,2) -> (4,2) = 'D'
   - D: (4,2) -> (5,2) = invalid, stay at (4,2) = 'D'
   - **Result: 'D'**

4. **Line 3 (LURDL)**: Starting at (4,2) = 'D'
   - L: (4,2) -> (4,1) = invalid, stay at (4,2) = 'D'
   - U: (4,2) -> (3,2) = 'B'
   - R: (3,2) -> (3,3) = 'C'
   - D: (3,3) -> (4,3) = invalid, stay at (3,3) = 'C'
   - L: (3,3) -> (3,2) = 'B'
   - **Result: 'B'**

5. **Line 4 (UUUUD)**: Starting at (3,2) = 'B'
   - U: (3,2) -> (2,2) = '7'
   - U: (2,2) -> (1,2) = '3'
   - U: (1,2) -> (0,2) = '1'
   - U: (0,2) -> (-1,2) = invalid, stay at (0,2) = '1'
   - D: (0,2) -> (1,2) = '3'
   - **Result: '3'**

**Final Expected Code**: 5DB3

**Validation Method**:
- Create a test file with the example input
- Run the solution
- Compare output to expected "5DB3"

---

### Test 3: Actual Puzzle Input
**Purpose**: Solve the actual problem and verify we get a valid bathroom code

**Priority**: **MANDATORY** - This produces the final answer

**Input**: The 5 lines from input.md

**Expected Output**: A 5-character code consisting of digits (1-9) and/or letters (A-D)

**Validation Method**:
- Run the solution with input.md
- Verify output is exactly 5 characters long (one per line)
- Verify each character is in the valid set: 1-9, A-D
- Record the answer for submission

**Success Criteria**:
- Code is 5 characters
- All characters are valid button labels
- No runtime errors or exceptions

---

### Test 4: Corner Button Movement Constraints
**Purpose**: Verify that moves from corner buttons (1, 5, 9, D) correctly reject invalid directions

**Priority**: **OPTIONAL** - Test 2 already validates several corner cases

**Test Cases to Verify**:

**4a. Button '1' (top, position 0,2)**
- Valid moves: D (down to '3')
- Invalid moves: U, L, R (all should stay at '1')

**4b. Button '5' (left edge, position 2,0)**
- Valid moves: R (to '6')
- Invalid moves: U, L, D (all should stay at '5')
- **Note**: Test 2 already validates button '5' behavior with "ULL" line

**4c. Button '9' (right edge, position 2,4)**
- Valid moves: L (to '8')
- Invalid moves: U, R, D (all should stay at '9')

**4d. Button 'D' (bottom, position 4,2)**
- Valid moves: U (to 'B')
- Invalid moves: D, L, R (all should stay at 'D')
- **Note**: Test 2 already validates button 'D' behavior

**Validation Method**: Manual trace through the detailed walkthrough in Test 2 to verify these corner cases are already covered. The example test exercises buttons '5', 'D', and several edge positions, providing sufficient validation of corner button behavior.

**When to Run**: Only if Test 2 fails or if additional validation is desired

---

### Test 5: Edge Button Invalid Moves
**Purpose**: Test buttons on the diamond edges that have empty spaces adjacent

**Priority**: **OPTIONAL** - Test 2 already covers many edge cases

**Key positions to validate**:
- Button '2' (position 1,1): U, L should be invalid
- Button '4' (position 1,3): U, R should be invalid
- Button 'A' (position 3,1): D, L should be invalid
- Button 'C' (position 3,3): D, R should be invalid
- **Note**: Test 2 validates button 'C' behavior in the "LURDL" line

**Validation Method**: Manual inspection of Test 2's detailed trace, which already covers several edge buttons

**When to Run**: Only if Test 2 fails or if comprehensive edge case validation is needed

---

### Test 6: Center Button '7' - All Valid Moves
**Purpose**: Verify a button in the center has all four valid moves

**Priority**: **OPTIONAL** - Test 2 already validates center button behavior

**Position**: (2, 2)

**Expected Valid Moves**:
- U: (2,2) -> (1,2) = '3' ✓
- D: (2,2) -> (3,2) = 'B' ✓
- L: (2,2) -> (2,1) = '6' ✓
- R: (2,2) -> (2,3) = '8' ✓

**Validation Method**: The example test (Test 2) already validates button '7' behavior:
- Line "RRDDD" navigates to '7' and moves down to 'B'
- Line "UUUUD" navigates through '7' going up to '3'

**When to Run**: Not needed - already covered by Test 2

---

### Test 7: Long Movement Sequences
**Purpose**: Verify the solution handles long instruction lines without errors

**Priority**: **AUTOMATIC** - Covered by Test 3

**Observation**: The actual input has lines of ~200-300 characters

**Validation**: The actual puzzle input test (Test 3) automatically covers this - verify no performance issues or errors. No separate test needed.

**Note**: Starting position verification (previously Test 7) is **redundant** - Test 2 already validates starting position with the "ULL" line that produces '5' as output

---

## Regression Test: Part 1 Comparison
**Purpose**: Ensure we understand why Part 2 differs from Part 1

**Method**:
- Run Part 1 solution with same input: Expected output is "19636"
- Run Part 2 solution with same input: Expected different output (diamond layout)
- Document the difference to confirm we're solving the right problem

---

## Testing Execution Order

### Mandatory Tests (Must Run)
1. **First**: Test 1 (keypad layout verification) - foundational, ensures correct setup
2. **Second**: Test 2 (provided example) - confirms basic correctness, validates algorithm
3. **Third**: Test 3 (actual puzzle input) - produces the final answer

### Optional Tests (Run Only If Needed)
4. **Test 4** (corner buttons) - only if Test 2 fails or additional validation desired
5. **Test 5** (edge buttons) - only if Test 2 fails with edge-related issues
6. **Test 6** (center button) - redundant, covered by Test 2
7. **Test 7** (long sequences) - automatically covered by Test 3

**Recommended Approach**: Run Tests 1, 2, and 3 in order. If all pass, testing is complete. If Test 2 or 3 fails, then run relevant optional tests to diagnose the issue.

---

## Success Criteria Summary

The solution is considered correct if:
1. ✓ **Test 1 passes**: Keypad dictionary has all 13 entries correctly mapped
2. ✓ **Test 2 passes**: Produces "5DB3" for the example input
3. ✓ **Test 3 passes**: Produces a valid 5-character code for the actual input
4. ✓ **No runtime errors or exceptions**
5. ✓ **All characters in output are valid button labels** (1-9, A-D)

**Minimum Required**: Tests 1, 2, and 3 must all pass for the solution to be considered complete and correct.

## Debugging Strategy (If Tests Fail)

If the example test fails:
1. Add debug print statements to show current position after each move
2. Compare trace output to the detailed trace in Test 2
3. Check keypad dictionary for typos
4. Verify starting position is (2, 0)

If the actual input produces invalid characters:
1. Print the keypad lookup for each position
2. Verify keypad dictionary has all 13 entries
3. Check for off-by-one errors in coordinate calculations

If movement seems wrong:
1. Verify direction mappings: U = row-1, D = row+1, L = col-1, R = col+1
2. Check that invalid moves return original position, not new position
3. Ensure keypad is passed correctly to all functions
