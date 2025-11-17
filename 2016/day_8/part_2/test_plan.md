# Testing Plan: LCD Screen Character Recognition (Part 2)

## Testing Philosophy
Since this is a script to solve a specific puzzle (not production code), we focus on:
1. Verifying the screen simulation produces the same result as Part 1 (119 lit pixels)
2. Ensuring the OCR correctly identifies letters from pixel patterns
3. Validating the final decoded message is correct
4. Basic edge case handling (blank regions, pattern matching)

We do NOT need extensive error handling, input validation, or comprehensive unit tests for every possible scenario.

## Test Strategy Overview

**UPDATED ORDER** (based on implementation workflow):

### Phase 1: Visual Inspection and Pattern Discovery
**Goal**: Run Part 1 code, display screen, and identify which letters appear

### Phase 2: Pattern Database Verification
**Goal**: Ensure all identified letters are correctly transcribed in LETTER_PATTERNS

### Phase 3: Verify Part 1 Compatibility (Regression Test)
**Goal**: Ensure reused code still works correctly (119 pixels)

### Phase 4: Integration Testing
**Goal**: Test the complete pipeline with the actual input

### Phase 5: Unit Testing OCR Components (OPTIONAL)
**Goal**: Test individual functions if integration tests fail - skip otherwise

## Detailed Test Plan

---

## Phase 1: Visual Inspection and Pattern Discovery

### Test 1.1: Display Screen and Identify Letters
**Objective**: Run Part 1 code and visually identify all letters that appear on screen

**Test steps**:
1. Run the Part 1 screen simulation code
2. Display the final 50×6 screen
3. Add column guides to show letter boundaries (every 5 pixels)
4. Manually identify each letter by examining the 5×6 blocks
5. Create a list of unique letters found

**Implementation**:
```python
def test_visual_inspection():
    screen = initialize_screen(50, 6)
    with open('input.md', 'r') as f:
        for line in f:
            if line.strip():
                parse_and_execute_instruction(screen, line.strip())

    # Display with column guides
    print("Column:  ", end="")
    for i in range(0, 50, 5):
        print(f"{i:<5}", end="")
    print("\n         " + "|    " * 10)

    for row_idx, row in enumerate(screen):
        print(f"Row {row_idx}:   ", end="")
        print(''.join('#' if pixel else '.' for pixel in row))

    print("         " + "|    " * 10)
    print("\nManually identify letters at positions 0, 5, 10, 15, 20, 25, 30, 35, 40, 45")
```

**Expected result**: A clearly visible pattern of letters (typically 8-10 letters)

**Manual task**: Write down the list of unique letters seen (e.g., "E, F, G, H, O, P, S, Z")

---

## Phase 2: Pattern Database Verification

### Test 2.1: Verify Pattern Completeness
**Objective**: Ensure all letters identified in Phase 1 are defined in LETTER_PATTERNS

**Test steps**:
1. Based on visual inspection from Test 1.1, list the required letters
2. Check that each letter exists in LETTER_PATTERNS
3. Verify each pattern is exactly 6 lines of 5 characters

**Implementation**:
```python
def test_pattern_database_complete():
    # Update this list based on Test 1.1 visual inspection
    # Example: required_letters = ['Z', 'F', 'H', 'S', 'O', 'G', 'P', 'E']
    required_letters = []  # TODO: Fill in after visual inspection

    for letter in required_letters:
        assert letter in LETTER_PATTERNS, f"Missing pattern for '{letter}'"

        pattern = LETTER_PATTERNS[letter]
        assert len(pattern) == 6, f"Pattern for '{letter}' should have 6 rows"
        for i, line in enumerate(pattern):
            assert len(line) == 5, f"Row {i} of '{letter}' should be 5 chars, got {len(line)}"

    print(f"✓ Pattern database complete: {len(required_letters)} letters defined")
```

**Expected result**: All tests pass, confirming pattern database is complete

---

## Phase 3: Verify Part 1 Compatibility (Regression Testing)

### Test 3.1: Screen Simulation Produces Correct Pixel Count
**Objective**: Verify that reused Part 1 code still generates correct screen state

**Test steps**:
1. Run the screen simulation with the actual input
2. Count the number of lit pixels
3. Compare against Part 1 answer (119 pixels)

**Expected result**: `count_lit_pixels(screen) == 119`

**Why this matters**: If we get 119 pixels, we know the screen state is correct and our OCR is working with the right data

**Implementation**:
```python
def test_part1_compatibility():
    screen = initialize_screen(50, 6)
    with open('input.md', 'r') as f:
        for line in f:
            if line.strip():
                parse_and_execute_instruction(screen, line.strip())

    pixel_count = sum(sum(row) for row in screen)
    assert pixel_count == 119, f"Expected 119 pixels, got {pixel_count}"
    print("✓ Part 1 compatibility test PASSED")
```

---

## Phase 4: Integration Testing

### Test 4.1: Full Pipeline with Actual Input
**Objective**: Run the complete solution on the actual puzzle input

**Test steps**:
1. Run `solve('input.md')`
2. Capture the decoded message
3. Display the screen visually for human inspection

**Expected result**:
- A string of 8-10 uppercase letters
- No '?' characters (indicating all patterns were recognized)
- The message looks like a reasonable code

**Implementation**:
```python
def test_full_pipeline():
    result = solve('input.md')

    # Sanity checks
    assert isinstance(result, str), "Result should be a string"
    assert len(result) >= 8, f"Expected at least 8 letters, got {len(result)}"
    assert len(result) <= 10, f"Expected at most 10 letters, got {len(result)}"
    assert result.isupper(), f"Result should be uppercase, got {result}"
    assert result.isalpha(), f"Result should be alphabetic only, got {result}"
    assert '?' not in result, f"Found unrecognized pattern: {result}"

    print(f"✓ Full pipeline test PASSED")
    print(f"  Decoded message: {result}")
    print(f"  Message length: {len(result)}")
```

**Manual verification**:
- Visually inspect the displayed screen
- Confirm that the decoded letters match what you see in each 5×6 block
- Compare the OCR output character-by-character with your manual reading

---

## Phase 5: Unit Test OCR Components (OPTIONAL)

**NOTE**: These unit tests are OPTIONAL for a puzzle-solving script. Only implement them if:
- Integration tests fail and you need to debug specific functions
- You want extra confidence in individual components

For most puzzle solutions, **Phase 1-4 are sufficient**. Skip Phase 5 unless debugging.

### Test 5.1: Extract Letter Function (OPTIONAL)
**Objective**: Verify that `extract_letter()` correctly extracts 5×6 regions

**Test approach**: Create a mock screen with known patterns

**Test case**:
```python
def test_extract_letter():
    # Create a simple screen with a known pattern
    screen = [
        [True, True, False, False, False, False, True, True, True, True, True],  # Row 0
        [True, False, True, False, False, False, True, False, False, False, True],  # Row 1
        [True, True, False, False, False, False, True, True, True, True, True],  # Row 2
        [True, False, True, False, False, False, True, False, False, False, False],  # Row 3
        [True, False, True, False, False, False, True, False, False, False, False],  # Row 4
        [True, False, True, False, False, False, True, True, True, True, True],  # Row 5
    ]

    # Extract first letter (columns 0-4)
    pattern = extract_letter(screen, 0)

    expected = [
        '##...',
        '#.#..',
        '##...',
        '#.#..',
        '#.#..',
        '#.#..'
    ]

    assert pattern == expected, f"Expected {expected}, got {pattern}"
    print("✓ Extract letter test PASSED")
```

**Edge cases to test**:
- Extract from column 0 (leftmost)
- Extract from column 45 (rightmost)
- Extract from a completely blank region

### Test 5.2: Recognize Letter Function (OPTIONAL)
**Objective**: Verify that `recognize_letter()` correctly matches patterns

**Test approach**: Test with known patterns from the database

**Test case**:
```python
def test_recognize_letter():
    # Test a known pattern (once we've defined LETTER_PATTERNS)
    pattern_A = [
        '.##..',
        '#..#.',
        '#..#.',
        '####.',
        '#..#.',
        '#..#.'
    ]

    result = recognize_letter(pattern_A)
    assert result == 'A', f"Expected 'A', got '{result}'"

    # Test blank pattern
    pattern_blank = [
        '.....',
        '.....',
        '.....',
        '.....',
        '.....',
        '.....'
    ]

    result = recognize_letter(pattern_blank)
    # Should return None, '', or skip this position
    assert result is None or result == '', f"Expected blank, got '{result}'"

    print("✓ Recognize letter test PASSED")
```

**Edge cases to test**:
- All-blank pattern (5×6 dots)
- Known letter pattern
- Unknown pattern (should return '?' or raise informative error)

---

## Phase 6: Final Visual Verification

### Test 6.1: Manual Visual Inspection
**Objective**: Human verification that the decoded message matches the pixel display

**Process**:
1. Run the code and display the 50×6 screen
2. Print column guides (every 5 columns) to show letter boundaries
3. Manually read each 5×6 block as a letter
4. Compare manual reading with the OCR output
5. If they match, the solution is correct

**Example display format**:
```
Column:  0    5    10   15   20   25   30   35   40   45
        |    |    |    |    |    |    |    |    |    |
Row 0:  ####..##..####.####.####.####..##..###...##.####.
Row 1:  ...#.#..#....#.#....#....#....#..#.#..#.#..#....#
Row 2:  ..#..#......#..###..###..###..#....###..#..#...#..
Row 3:  .#...#.##..#...#....#....#....#.##.#..#.#..#..#...
Row 4:  #....#..#.#....#....#....#....#..#.#..#.#..#.#....
Row 5:  ####..###.####.#....#....####..###.###...##..####.
        |    |    |    |    |    |    |    |    |    |
        A    B    C    D    E    F    G    H    I    J  (placeholder example)
```

**Manual verification checklist**:
- [ ] Each letter is visually distinct
- [ ] Letters match the OCR output character-by-character
- [ ] No letters are missing or misidentified
- [ ] Blank regions are correctly ignored

---

## Edge Cases to Consider

### Edge Case 1: All-Blank 5×6 Region
**Scenario**: A 5×6 block with all OFF pixels (could be trailing space)

**Expected behavior**: Should be skipped or represented as empty, not treated as a letter

**Test**:
```python
blank_pattern = ['.....' for _ in range(6)]
result = recognize_letter(blank_pattern)
assert result is None or result == ''
```

### Edge Case 2: Unrecognized Pattern
**Scenario**: A 5×6 block that doesn't match any pattern in the database

**Expected behavior**:
- Option 1: Return '?' to indicate unknown
- Option 2: Raise an informative error with the pattern
- Option 3: Print the pattern and ask user to add it

**Test approach**: Intentionally pass an unknown pattern

**Implementation**:
```python
unknown_pattern = [
    '#####',
    '#####',
    '#####',
    '#####',
    '#####',
    '#####'
]
result = recognize_letter(unknown_pattern)
# Should either return '?' or raise an error
```

### Edge Case 3: Pattern Variation
**Scenario**: A letter might have slight variations in the pattern

**Expected behavior**: Our pattern database should exactly match the font used by Advent of Code

**Mitigation**: The problem states a specific font is used (consistent across AoC 2016), so exact matching should work.

**Status**: Low priority - only relevant if exact matching fails.

---

## Testing Execution Order (UPDATED)

**Follow this order to efficiently test the solution:**

1. **Phase 1 - Visual Inspection (Test 1.1)**: Run Part 1 code, display screen with column guides, manually identify letters
2. **Phase 2 - Pattern Database (Test 2.1)**: Verify all identified letters are in LETTER_PATTERNS with correct format
3. **Phase 3 - Regression Test (Test 3.1)**: Verify pixel count is still 119 (Part 1 compatibility)
4. **Phase 4 - Integration Test (Test 4.1)**: Run full pipeline and check output validity
5. **Phase 6 - Final Verification (Test 6.1)**: Manually confirm decoded message matches visual inspection
6. **Phase 5 - Unit Tests (Optional)**: Only if integration tests fail and you need to debug specific functions

**NOTE**: Most puzzle solutions only need Phases 1-4 and 6. Phase 5 is optional debugging.

---

## Acceptance Criteria

The solution is considered correct if:

1. ✓ Part 1 pixel count is still 119 (regression test passes - Test 3.1)
2. ✓ Pattern database contains all required letters (Test 2.1)
3. ✓ All 10 letter positions are processed (range 0 to 45)
4. ✓ No '?' characters in the output (all patterns recognized - Test 4.1)
5. ✓ Output is uppercase alphabetic string only (Test 4.1)
6. ✓ Output length is reasonable: 8-10 characters (Test 4.1)
7. ✓ Manual visual inspection confirms the decoded message matches screen (Test 6.1)

---

## Debugging Strategy

If tests fail, follow this debugging process:

### Issue: Pixel count is not 119
**Cause**: Part 1 code was broken during refactoring
**Fix**: Review changes to Part 1 functions, ensure exact behavior is preserved

### Issue: Extracted patterns don't match expected
**Cause**: Off-by-one error in column indexing
**Fix**: Check that extract_letter() uses correct slice [col:col+5]

### Issue: Letters not recognized (getting '?')
**Cause**: Pattern database is incomplete or incorrect
**Fix**: Display the unrecognized pattern, visually compare to known letters, add to database

### Issue: Decoded message looks wrong
**Cause**: Either extraction or recognition is failing
**Fix**:
1. Display the screen with column guides
2. Manually decode the first few letters
3. Compare with OCR output
4. Identify where they diverge
5. Debug that specific extraction/recognition

---

## Test Data Summary

**Primary test input**: `input.md` (the actual puzzle input)

**Mock test data**:
- Small custom screens for unit testing extract_letter()
- Known letter patterns for testing recognize_letter()

**Expected outputs**:
- Part 1 compatibility: 119 pixels
- Part 2 solution: An uppercase string (exact value unknown until solved)

---

## Final Verification Checklist

Before submitting the answer:

- [ ] **Phase 1 complete**: Screen displayed with column guides, letters manually identified
- [ ] **Phase 2 complete**: All identified letters are in LETTER_PATTERNS with correct format
- [ ] **Phase 3 complete**: Part 1 regression test passes (119 pixels)
- [ ] **Phase 4 complete**: Integration test passes (full pipeline)
- [ ] **Phase 6 complete**: Manual visual verification confirms decoded message
- [ ] **No '?' in output**: All patterns were successfully recognized
- [ ] **Output valid**: Uppercase alphabetic string, 8-10 characters
- [ ] **Consistent results**: Running solve() multiple times produces same output

If all items are checked, the solution is ready to submit!
