# Test Plan: Bathroom Keypad Code

## Testing Strategy
Verify the implementation handles all aspects of the problem correctly through a combination of example validation, edge case testing, and manual verification.

**Testing Approach**: All tests will be run manually by creating test input files and comparing outputs through visual inspection. No automated test framework is required for this script.

## Test Cases

### Test 1: Example from Problem Statement
**Purpose**: Validate against known correct output

**Input**:
```
ULL
RRDDD
LURDL
UUUUD
```

**Expected Output**: `1985`

**Verification Steps**:
1. Run the solution with this input
2. Compare output to expected value
3. If mismatch, trace through execution step-by-step to identify error

**Manual Trace**:
- Start: 5 (1,1)
- ULL: 5→2→1→1 = **1**
- RRDDD: 1→2→3→6→9→9 = **9**
- LURDL: 9→8→5→6→9→8 = **8**
- UUUUD: 8→5→2→2→2→5 = **5**

### Test 2: Boundary Testing - All Edges
**Purpose**: Ensure boundary detection works for all edges of the keypad

**Input**:
```
UL
U
UR
R
DR
D
DL
L
```

**Starting Position**: 5 (center)

**Expected Behavior**:
- UL: 5→2→1 = **1** (top-left corner)
- U: 1→1 = **1** (already at top edge, can't go up)
- UR: 1→1→2 = **2** (move right from top edge)
- R: 2→3 = **3** (top-right corner)
- DR: 3→6→6 = **6** (move down, try to move right from edge)
- D: 6→9 = **9** (bottom-right corner)
- DL: 9→9→8 = **8** (try down from bottom edge, move left)
- L: 8→7 = **7** (bottom-left corner)

**Expected Output**: `11236987`

### Test 3: No Movement and Empty Line Handling
**Purpose**: Verify handling of empty lines and positions that don't change

**Input**:
```
UDLR

RLDU
```

**Expected Behavior**:
- Starting at 5
- UDLR: 5→2→5→4→5 = **5** (return to center)
- Empty line is skipped entirely and does not produce a digit
- RLDU: 5→6→5→2→5 = **5** (return to center)

**Expected Output**: `55` (two digits, empty line produces no output)

### Test 4: All Invalid Moves
**Purpose**: Ensure position doesn't change when all moves are invalid

**Input**:
```
UUUUUUUUU
LLLLLLLLL
```

**Expected Behavior**:
- Start: 5 (1,1)
- UUUUUUUUU: 5→2→2→2... = **2** (hit top edge immediately)
- LLLLLLLLL: 2→1→1→1... = **1** (hit left edge)

**Expected Output**: `21`

### Test 5: Single Direction Sequences
**Purpose**: Test each direction individually

**Input**:
```
UUU
DDD
LLL
RRR
```

**Expected Behavior**:
- Start: 5
- UUU: 5→2→2→2 = **2**
- DDD: 2→5→8→8 = **8**
- LLL: 8→7→7→7 = **7**
- RRR: 7→8→9→9 = **9**

**Expected Output**: `2879`

**Note**: The third D in line 2 (DDD) attempts to move from 8 to an invalid position (row 3), so it stays at 8.

### Test 6: Actual Input Validation
**Purpose**: Verify solution works with the actual provided input

**Input Analysis**:
- The input.md file contains 5 non-empty instruction lines plus 1 empty line at the end
- Expected output should be a 5-digit code

**Steps**:
1. Run solution with the actual input.md content
2. Record the output code
3. Verify output is exactly 5 digits (one per non-empty input line)
4. Verify all output characters are digits from 1-9
5. Manually verify the first line of instructions to ensure logic is correct

**Manual Verification for Line 1** (LURLLLLLDUULRDDDRLRDD...):
- Start at 5 (1,1)
- L: 5→4 (1,0)
- U: 4→1 (0,0)
- R: 1→2 (0,1)
- L: 2→1 (0,0)
- L: 1→1 (already at left edge, stays at 1)
- Continue processing full line...
- Record final position and button value
- Compare to first digit of actual output

## Logic Verification Exercises

### Exercise: Corner Starting Positions
**Purpose**: Mentally verify the algorithm works from different starting positions

**Scenario**:
If we started at button 1 (0,0) instead of 5, and received input `DDRR`:
- Start: 1 (0,0)
- D: 1→4 (1,0)
- D: 4→7 (2,0)
- R: 7→8 (2,1)
- R: 8→9 (2,2)
- Result: **9**

**Note**: This is a thought experiment to validate the movement logic, not an executable test case.

## Verification Procedure

### Step 1: Run Example Test
1. Create a test file with the example input
2. Run the solution
3. Verify output is exactly "1985"

### Step 2: Trace First Actual Input Line
1. Manually trace through the first line of actual input
2. Verify the code produces the correct first digit
3. This validates the core logic

### Step 3: Run Full Actual Input
1. Run solution with actual input.md
2. Verify output is a 5-character string (corresponding to 5 non-empty instruction lines)
3. Verify all characters are digits from 1-9
4. Verify no errors or exceptions occur during execution

### Step 4: Boundary Validation
1. Run Test 2 (boundary testing)
2. Verify all edge cases produce expected results
3. Pay special attention to corners

### Step 5: Edge Case Verification
1. Run Tests 3, 4, and 5
2. Verify handling of:
   - Returning to same position
   - All invalid moves
   - Single direction sequences

## Success Criteria
- ✓ Example test produces "1985"
- ✓ Actual input produces a 5-digit code
- ✓ All boundary tests pass
- ✓ Manual trace of first actual input line matches code output
- ✓ No crashes or errors on any test case

## Debugging Strategy (if tests fail)
1. Add debug print statements to show position after each move
2. Compare debug output to manual trace
3. Check boundary validation logic (0 <= row <= 2, 0 <= col <= 2)
4. Verify keypad mapping (row/col to button value)
5. Ensure position persists between instruction lines
6. Check input parsing (stripping whitespace, handling empty lines)
