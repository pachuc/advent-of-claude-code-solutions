# Test Plan: Wrapping Paper Calculator

## Testing Objectives
1. Verify correct calculation logic for individual presents
2. Ensure accurate parsing of input format
3. Validate total calculation across all presents
4. Test edge cases specific to the problem domain

## Test Strategy

### 1. Unit Tests: Individual Present Calculations

#### Test 1.1: Example 1 from Problem Statement
**Input:** `2x3x4`
**Expected Calculation:**
- Sides: 2*3=6, 3*4=12, 2*4=8
- Surface area: 2*(6+12+8) = 52
- Slack (min side): 6
- Total: 52 + 6 = 58

**Verification:** Call `calculate_wrapping_paper(2, 3, 4)` → should return 58

#### Test 1.2: Example 2 from Problem Statement
**Input:** `1x1x10`
**Expected Calculation:**
- Sides: 1*1=1, 1*10=10, 1*10=10
- Surface area: 2*(1+10+10) = 42
- Slack (min side): 1
- Total: 42 + 1 = 43

**Verification:** Call `calculate_wrapping_paper(1, 1, 10)` → should return 43

#### Test 1.3: Cube (All Dimensions Equal)
**Input:** `5x5x5`
**Expected Calculation:**
- Sides: 5*5=25, 5*5=25, 5*5=25
- Surface area: 2*(25+25+25) = 150
- Slack (min side): 25 (all equal)
- Total: 150 + 25 = 175

**Verification:** Call `calculate_wrapping_paper(5, 5, 5)` → should return 175

#### Test 1.4: Very Flat Box (One Dimension is 1)
**Input:** `1x20x30`
**Expected Calculation:**
- Sides: 1*20=20, 20*30=600, 1*30=30
- Surface area: 2*(20+600+30) = 1300
- Slack (min side): 20
- Total: 1300 + 20 = 1320

**Verification:** Call `calculate_wrapping_paper(1, 20, 30)` → should return 1320

#### Test 1.5: Two Equal Dimensions
**Input:** `10x10x15`
**Expected Calculation:**
- Sides: 10*10=100, 10*15=150, 10*15=150
- Surface area: 2*(100+150+150) = 800
- Slack (min side): 100
- Total: 800 + 100 = 900

**Verification:** Call `calculate_wrapping_paper(10, 10, 15)` → should return 900

### 2. Integration Tests: Input Parsing

#### Test 2.1: Parse Single Line
**Input string:** `"29x13x26"`
**Expected output:** l=29, w=13, h=26
**Verification:**
```python
line = "29x13x26"
l, w, h = map(int, line.split('x'))
assert l == 29 and w == 13 and h == 26
```

#### Test 2.2: Parse Multiple Lines
**Input:**
```
2x3x4
1x1x10
```
**Expected:** Should correctly parse both lines and sum their wrapping paper
**Manual calculation:** 58 + 43 = 101

### 3. End-to-End Tests: Full Input File

#### Test 3.1: Verify First Few Entries
Manually calculate wrapping paper for first 3 presents from input.md:
- Line 1: `29x13x26` → sides: 377, 338, 754 → surface: 2938 → slack: 338 → total: 3276
- Line 2: `11x11x14` → sides: 121, 154, 154 → surface: 858 → slack: 121 → total: 979
- Line 3: `27x2x5` → sides: 54, 10, 135 → surface: 398 → slack: 10 → total: 408

**Partial sum:** 3276 + 979 + 408 = 4663

**Verification Method:**
```python
# Run script with only first 3 lines of input
# Verify output matches 4663
```

#### Test 3.2: Count Lines
**Verify:** Input file has 1000 presents (1000 non-empty lines)
```python
with open('input.md', 'r') as f:
    line_count = len([l for l in f.read().strip().split('\n') if l])
assert line_count == 1000
```

#### Test 3.3: All Values Are Positive Integers
**Verify:** All dimensions are positive integers
```python
with open('input.md', 'r') as f:
    for line in f.read().strip().split('\n'):
        if line:
            l, w, h = map(int, line.split('x'))
            assert l > 0 and w > 0 and h > 0
```

### 4. Edge Case Tests

#### Test 4.1: Minimum Dimensions (1x1x1) [OPTIONAL]
**Input:** `1x1x1`
**Expected Calculation:**
- Sides: 1, 1, 1
- Surface area: 2*3 = 6
- Slack: 1
- Total: 7

**Note:** This test is optional as minimum dimensions are unlikely in real input.

#### Test 4.2: Large Dimensions [OPTIONAL]
**Input:** `30x30x30` (close to max in our input)
**Expected Calculation:**
- Sides: 900, 900, 900
- Surface area: 2*2700 = 5400
- Slack: 900
- Total: 6300

**Note:** This test is optional as it's mainly for boundary validation.

#### Test 4.3: Empty Line Handling [RECOMMENDED]
**Verify:** Script handles potential empty lines without crashing
```python
# Test with input containing empty lines
test_input = "2x3x4\n\n1x1x10\n"
# Should process only the two valid lines
```

**Priority:** This is more important as the input file may have trailing newlines.

### 5. Regression Test: Full Solution

#### Test 5.1: Run Against Full Input
**Method:**
1. Run the script against the complete input.md file
2. Record the output value
3. Verify the output is a positive integer
4. Verify the output is reasonable (should be > 1000 since we have 1000 boxes with minimum paper ~7 each)

**Sanity checks:**
- Output should be > 7000 (minimum if all boxes were 1x1x1)
- Output should be < 10,000,000 (maximum if all were 30x30x30)

#### Test 5.2: Deterministic Output
**Verify:** Running the script multiple times produces the same result
```bash
python solution.py > output1.txt
python solution.py > output2.txt
diff output1.txt output2.txt  # Should be identical
```

### 6. Manual Verification Sampling

#### Test 6.1: Random Sample Verification
Manually select 5 random lines from input and verify calculations:
- Pick lines: 100, 250, 500, 750, 999
- Calculate expected wrapping paper by hand
- Add debug output to script to print individual calculations (use `--debug` flag)
- Verify those specific lines match hand calculations

**Example debug usage:**
```bash
python solution.py --debug | head -n 5  # See first 5 calculations
python solution.py --debug | grep "10x20x30"  # Find specific box calculation
```

### 7. Final Answer Verification

#### Test 7.1: Submit to Advent of Code
**Final verification step:**
1. Run the script to get the final answer
2. Submit the answer to the Advent of Code website
3. Confirm the answer is accepted
4. This is the ultimate validation that the solution is correct

**Note:** This is the definitive test - if Advent of Code accepts the answer, the solution is correct.

## Test Execution Order

1. **Unit tests first** (Tests 1.1-1.5): Verify core calculation logic
2. **Parsing tests** (Tests 2.1-2.2): Ensure input handling works
3. **Edge cases** (Tests 4.1-4.3): Verify boundary conditions
4. **Sample verification** (Test 3.1): Manually verify a few entries
5. **Full run** (Tests 5.1-5.2): Execute against complete input
6. **Manual sampling** (Test 6.1): Spot-check random entries with debug mode
7. **Final validation** (Test 7.1): Submit answer to Advent of Code

## Success Criteria

✅ All example cases from problem statement produce correct output
✅ Unit tests for individual calculations pass
✅ Input parsing handles all 1000 lines correctly
✅ Edge cases (cube, flat box, minimum dimensions) handled properly
✅ Full script produces a consistent, reasonable output
✅ Random sampling matches hand calculations
✅ Final answer is accepted by Advent of Code when submitted

## Known Limitations (Acceptable for This Script)

- No input validation for malformed lines (assumes valid input format)
- No error handling for file not found (assumes input.md exists)
- No handling for negative dimensions (assumes valid positive integers)
- No handling for non-integer dimensions (assumes all dimensions are integers)

These limitations are acceptable because:
1. The problem guarantees valid input format
2. We're solving a specific puzzle, not building production software
3. Adding extensive validation would not improve correctness for valid inputs
