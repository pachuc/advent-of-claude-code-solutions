# Testing Plan: LCD Screen Pixel Display Simulation

## Updates Based on Critique

This plan has been updated to address the following issues from the critique:

1. **Rotation direction tests**: Added explicit tests (1.3b, 1.6b) to verify RIGHT and DOWN rotations
2. **Visual verification elevated**: Changed from "optional" to "RECOMMENDED" (Test 4.2)
3. **Detailed 7×3 example**: Added intermediate states for each step to make verification easier
4. **Answer validation strategy**: Added note about Advent of Code submission as final validation
5. **Debugging strategy**: Added concrete steps for troubleshooting if answer is wrong
6. **Test execution order**: Prioritized the 7×3 example as the FIRST test to run
7. **Overlap handling**: Clarified how rect operations handle already-lit pixels (Test 6.1)
8. **Manual spot check examples**: Added specific instruction tracing example

## Testing Strategy Overview

We need to verify that:
1. Screen initialization works correctly
2. Each operation type (rect, rotate row, rotate column) works correctly
3. Operations work in sequence and maintain state
4. Edge cases are handled properly
5. The final pixel count is accurate

## Test Categories

### 1. Unit Tests for Individual Operations

#### Test 1.1: Screen Initialization
**Objective**: Verify screen starts with all pixels OFF
- Create a 50×6 screen
- Verify all 300 pixels are False/0
- Expected result: 0 lit pixels

#### Test 1.2: Rectangle Operation - Basic
**Objective**: Verify rect operation turns on correct pixels
- Start with empty screen
- Execute: `rect 3x2`
- Verify:
  - Pixels at positions (0,0), (0,1), (0,2), (1,0), (1,1), (1,2) are ON
  - All other pixels are OFF
  - Total lit pixels = 6
- Test variations:
  - `rect 1x1` → 1 pixel at (0,0)
  - `rect 5x3` → 15 pixels in top-left rectangle
  - `rect 50x6` → all 300 pixels (full screen)

#### Test 1.3: Row Rotation - Basic
**Objective**: Verify row rotation shifts pixels RIGHT with wrapping
- Setup: Create screen with pattern in row 0: `[T,T,F,F,F,F,F]` (7-wide for simplicity)
- Execute: `rotate row y=0 by 2`
- Expected result: `[F,F,T,T,F,F,F]`
- Verify: Pixels shifted right, rightmost wrapped to left

#### Test 1.3b: Row Rotation - Direction Verification
**Objective**: Explicitly verify rotation direction is RIGHT not LEFT
- Setup: Row 0 = `[T,F,F,F,F]` (only first pixel on)
- Execute: `rotate row y=0 by 1`
- Expected result: `[F,T,F,F,F]` (NOT `[F,F,F,F,T]`)
- This confirms: last element wraps to first position when rotating right
- Setup: Row 0 = `[T,T,T,F,F]`
- Execute: `rotate row y=0 by 2`
- Expected result: `[F,F,T,T,T]` (last 2 elements move to front)

#### Test 1.4: Row Rotation - Full Wrap
**Objective**: Verify rotation by full width returns to original
- Setup: Row with pattern [T,F,T,F,T]
- Execute: `rotate row y=0 by 5` (full width)
- Expected result: [T,F,T,F,T] (unchanged)

#### Test 1.5: Row Rotation - Larger Than Width
**Objective**: Verify rotation handles shift > width correctly
- Setup: Row with pattern [T,T,F,F,F] (width=5)
- Execute: `rotate row y=0 by 7` (equivalent to shift by 2)
- Expected result: [F,F,T,T,F]

#### Test 1.6: Column Rotation - Basic
**Objective**: Verify column rotation shifts pixels DOWN with wrapping
- Setup: Create screen with column 0 pattern: `[T,T,F,F,F,F]` (6 rows)
- Execute: `rotate column x=0 by 2`
- Expected result: Column 0 = `[F,F,T,T,F,F]`
- Verify: Pixels shifted down, bottom wrapped to top

#### Test 1.6b: Column Rotation - Direction Verification
**Objective**: Explicitly verify rotation direction is DOWN not UP
- Setup: Column 0 = `[T,F,F,F,F,F]` (only first pixel on)
- Execute: `rotate column x=0 by 1`
- Expected result: Column 0 = `[F,T,F,F,F,F]` (NOT `[F,F,F,F,F,T]`)
- This confirms: last element wraps to first position when rotating down
- Setup: Column 1 = `[T,T,T,F,F,F]`
- Execute: `rotate column x=1 by 2`
- Expected result: Column 1 = `[F,F,T,T,T,F]` (last 2 elements move to top)

#### Test 1.7: Column Rotation - Full Wrap
**Objective**: Verify rotation by full height returns to original
- Setup: Column with pattern [T,F,T,F,T,F]
- Execute: `rotate column x=1 by 6` (full height)
- Expected result: [T,F,T,F,T,F] (unchanged)

#### Test 1.8: Column Rotation - Larger Than Height
**Objective**: Verify rotation handles shift > height correctly
- Setup: Column with pattern [T,T,F,F,F,F] (height=6)
- Execute: `rotate column x=0 by 8` (equivalent to shift by 2)
- Expected result: [F,F,T,T,F,F]

### 2. Integration Tests - Example Walkthrough

#### Test 2.1: Official Example (7×3 Screen) - CRITICAL TEST
**Objective**: Verify the exact example from problem statement works correctly
**This is the most important test - if this passes, the core logic is correct**

- Screen: 7 wide × 3 tall
- Sequence with intermediate states:

**Step 0 - Initial**:
```
.......
.......
.......
```
Lit pixels: 0

**Step 1 - `rect 3x2`**:
```
###....
###....
.......
```
Lit pixels: 6

**Step 2 - `rotate column x=1 by 1`**:
```
#.#....
###....
.#.....
```
Lit pixels: 6 (rotation doesn't change count)

**Step 3 - `rotate row y=0 by 4`**:
```
....#.#
###....
.#.....
```
Lit pixels: 6

**Step 4 - `rotate column x=1 by 1`**:
```
.#..#.#
#.#....
.#.....
```
Lit pixels: 6 (FINAL)

**Verification**:
- Check final screen state matches exactly
- Verify pixel count = 6
- If this test fails, there's a fundamental bug in the implementation

### 3. Edge Case Tests

#### Test 3.1: Empty Operations
- Execute operations on empty screen that don't turn on pixels
- `rotate row y=0 by 5` on empty screen → still empty
- `rotate column x=0 by 3` on empty screen → still empty
- Expected result: 0 lit pixels

#### Test 3.2: Rotation by Zero
- Setup: Screen with some pixels on
- Execute: `rotate row y=0 by 0`
- Expected result: No change to screen

#### Test 3.3: Sequential Rectangles
- Execute multiple rect commands:
  - `rect 2x2` → 4 pixels
  - `rect 4x3` → should add more pixels (overlapping is OK)
- Verify pixels accumulate (don't reset)

#### Test 3.4: Multiple Rotations on Same Row/Column
- Setup: Pattern in row 0
- Execute: `rotate row y=0 by 3`, then `rotate row y=0 by 2`
- Verify: Equivalent to single rotation by 5 (cumulative effect)

#### Test 3.5: Interleaved Row and Column Rotations
- Setup: Create a specific pattern
- Execute: Rotate row, then rotate column through same area
- Verify: Operations don't interfere incorrectly

### 4. Full Input Tests

#### Test 4.1: Process Complete Input File
**Objective**: Verify solution handles the actual 194-instruction input
- Load input.md
- Process all 194 instructions sequentially
- Verify:
  - No errors or crashes
  - Final pixel count is a reasonable number (> 0, < 300)
  - Result is deterministic (running twice with fresh screens gives same answer)

#### Test 4.2: Visual Verification - RECOMMENDED
**Objective**: Visually inspect the output for correctness
- After processing full input, display the screen using the display function
- **Why this is important**: Advent of Code often encodes letters in the display
- Visual patterns help verify correctness even before knowing the exact answer
- If the display looks like random noise, something is wrong
- If the display shows recognizable letters/patterns, it's likely correct
- **This test can catch catastrophic errors that numeric tests might miss**

Example of what to look for:
```
####..##..####.###..###..####.#..#.###.
#....#..#.#....#..#.#..#....#.#..#.#..#
###..#....###..###..#..#...#..####.###.
#....#....#....#..#.###...#...#..#.#..#
#....#..#.#....#..#.#....#....#..#.#..#
####..##..#....###..#....####.#..#.###.
```
Letters should be clearly readable (though may need slight squinting)

### 5. Parsing Tests

#### Test 5.1: Parse Rectangle Instructions
- Input: `"rect 5x3"`
- Expected parse: width=5, height=3
- Input: `"rect 1x1"`
- Expected parse: width=1, height=1

#### Test 5.2: Parse Row Rotation Instructions
- Input: `"rotate row y=0 by 5"`
- Expected parse: row=0, shift=5
- Input: `"rotate row y=3 by 47"`
- Expected parse: row=3, shift=47

#### Test 5.3: Parse Column Rotation Instructions
- Input: `"rotate column x=1 by 1"`
- Expected parse: column=1, shift=1
- Input: `"rotate column x=46 by 5"`
- Expected parse: column=46, shift=5

### 6. State Persistence Tests

#### Test 6.1: State Maintained Between Operations
**Objective**: Verify screen state persists correctly
- Execute: `rect 2x2` (4 pixels on at positions: (0,0), (0,1), (1,0), (1,1))
- Count: 4 pixels
- Execute: `rotate row y=0 by 1`
- Verify: Still 4 pixels on (count unchanged, positions changed to include (0,2))
- Execute: `rect 3x3` (overlapping with previous)
- **Important**: Pixels already ON stay ON (no change)
- New pixels are: (0,2), (1,2), (2,0), (2,1), (2,2) - but some may already be on
- Verify: Total count = original 4 + new unique pixels (exact count depends on overlap)
- Main check: Pixel count increases or stays same (never decreases from rect)

### 7. Correctness Validation Strategy

#### Primary Validation Method: Known Example (CRITICAL)
- Use the 7×3 example from problem statement
- This gives us a known-good test case with expected output
- **If this passes, core logic is likely correct**
- Run this test FIRST before attempting the full input

#### Secondary Validation: Visual Verification (HIGHLY RECOMMENDED)
- Display the full 50×6 screen after processing all instructions
- Look for letter patterns (this is an Advent of Code hallmark)
- If letters are readable → very likely correct
- If output is random noise → something is wrong
- **This can catch errors that numeric tests miss**

#### Tertiary Validation: Invariants
- After any rotation: pixel count stays the same
- After rect: pixel count increases (or stays same if overlapping lit pixels)
- Total pixels never exceeds 300
- Total pixels never goes negative
- These can be checked with assertions during execution

#### Manual Spot Check (if needed for debugging)
- Pick first 5-10 instructions from actual input
- Manually trace through on paper or small test
- Verify intermediate states match implementation
- Specific example to trace:
  ```
  Step 1: rect 1x1 → screen[0][0] = True, count = 1
  Step 2: rotate row y=0 by 5 → screen[0][5] = True, screen[0][0] = False, count = 1
  Step 3: rect 1x1 → screen[0][0] = True, count = 2
  Step 4: rotate row y=0 by 5 → pixels at positions 0 and 5 shift right by 5
  ...
  ```

#### Final Validation: Answer Submission
- This is an Advent of Code problem - final validation is submitting the answer
- Compare output against expected answer (once known)
- If wrong, use visual display and manual tracing to debug

## Test Execution Order (Recommended Sequence)

1. **FIRST - Official 7×3 Example**: Run Test 2.1
   - This is the most important test
   - If it fails, fix before proceeding
   - Validates core rotation and rect logic

2. **Unit tests** (if 7×3 example fails): Test each operation in isolation
   - Use rotation direction tests (1.3b, 1.6b) to find bugs
   - Test wrapping behavior
   - Test edge cases

3. **Full input processing**: Run Test 4.1
   - Process all 194 instructions
   - Check for errors and crashes

4. **Visual verification**: Run Test 4.2
   - Display the screen
   - Look for letter patterns
   - Sanity check the output

5. **Answer submission**: Submit to Advent of Code
   - If correct → done!
   - If incorrect → use manual spot checks and debug prints

## Success Criteria

✅ **Required for confidence**:
- Official 7×3 example produces exactly 6 lit pixels with correct pattern
- Full input processes without errors
- Visual display shows recognizable letter patterns (not random noise)
- Final answer is deterministic (same result on multiple runs)

✅ **Nice to have** (but not required for a script):
- All unit tests pass
- All edge cases handled
- Invariants verified

## Testing Implementation Notes

Since this is a one-off script, we don't need:
- A full testing framework (unittest/pytest)
- Extensive error handling for malformed input
- Performance benchmarks
- Test coverage metrics

We DO need:
- Ability to run the 7×3 example and verify output (CRITICAL)
- Ability to process the full input and get an answer
- Display function to visually verify the result
- Basic assertions to catch logic errors (optional but helpful)

## Debugging Strategy (if answer is wrong)

1. **Re-run the 7×3 example** with debug prints at each step
2. **Add display_screen() calls** after each operation in first 10 instructions
3. **Manually trace** the first 5-10 instructions on paper
4. **Check rotation direction**: Verify right vs left, down vs up
5. **Verify parsing**: Print parsed instruction parameters
6. **Check for off-by-one errors** in array indexing

## Test Data Summary

- **Critical test**: 7×3 screen with 4 operations (from problem) - must pass
- **Full test**: 50×6 screen with 194 operations (actual input.md)
- **Visual test**: Display output should show readable letters
- **Edge cases**: Rotation by 0, by full dimension, by > dimension (nice to have)
