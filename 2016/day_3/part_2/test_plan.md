# Test Plan - Triangle Validation (Part 2)

## Testing Strategy
Verify that the column-based triangle reading and validation works correctly for various input scenarios.

## Test Cases

### 1. Example from Problem Statement
**Purpose**: Verify basic functionality with known example

**Input**:
```
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
```

**Expected Processing**:
- Group 1: Triangles (101,102,103), (301,302,303), (501,502,503)
- Group 2: Triangles (201,202,203), (401,402,403), (601,602,603)

**Manual Validation**:
- Triangle (101, 102, 103):
  - 101 + 102 = 203 > 103 ✓
  - 101 + 103 = 204 > 102 ✓
  - 102 + 103 = 205 > 101 ✓
  - **Valid**

- Triangle (301, 302, 303):
  - 301 + 302 = 603 > 303 ✓
  - 301 + 303 = 604 > 302 ✓
  - 302 + 303 = 605 > 301 ✓
  - **Valid**

- Triangle (501, 502, 503):
  - 501 + 502 = 1003 > 503 ✓
  - 501 + 503 = 1004 > 502 ✓
  - 502 + 503 = 1005 > 501 ✓
  - **Valid**

All 6 triangles follow the same pattern and should be valid.

**Expected Output**: 6 valid triangles

**Test Method**: Create small test file, run solution, verify output

---

### 2. Mixed Valid and Invalid Triangles
**Purpose**: Ensure triangle inequality is properly checked

**Input**:
```
5 10 25
6 11 26
7 12 27
3 4 5
4 5 6
5 6 7
```

**Expected Processing**:
- Group 1:
  - Triangle (5, 6, 7): 5+6=11>7 ✓, 5+7=12>6 ✓, 6+7=13>5 ✓ → **Valid**
  - Triangle (10, 11, 12): All checks pass → **Valid**
  - Triangle (25, 26, 27): All checks pass → **Valid**

- Group 2:
  - Triangle (3, 4, 5): 3+4=7>5 ✓, 3+5=8>4 ✓, 4+5=9>3 ✓ → **Valid**
  - Triangle (4, 5, 6): All checks pass → **Valid**
  - Triangle (5, 6, 7): All checks pass → **Valid**

**Expected Output**: 6 valid triangles

**Note**: This demonstrates the key difference from Part 1. In Part 1, the first row `5 10 25` would be INVALID (5+10=15 not > 25), but in Part 2, we extract column values which form different triangles.

---

### 3. Mix of Invalid and Valid Triangles
**Purpose**: Verify invalid triangles are correctly rejected while valid ones are counted

**Input**:
```
1 2 100
2 3 101
3 4 102
```

**Expected Processing**:
- Triangle (1, 2, 3): 1+2=3 NOT > 3 → **Invalid**
- Triangle (2, 3, 4): 2+3=5>4 ✓, 2+4=6>3 ✓, 3+4=7>2 ✓ → **Valid**
- Triangle (100, 101, 102): All checks pass → **Valid**

**Expected Output**: 2 valid triangles

---

### 4. Incomplete Group (Edge Case)
**Purpose**: Handle input not divisible by 3

**Input**:
```
10 20 30
11 21 31
12 22 32
40 50 60
41 51 61
```

**Expected Processing**:
- Group 1 (rows 0-2): Process 3 triangles normally
  - Triangle (10, 11, 12): 10+11=21>12 ✓, 10+12=22>11 ✓, 11+12=23>10 ✓ → **Valid**
  - Triangle (20, 21, 22): 20+21=41>22 ✓, 20+22=42>21 ✓, 21+22=43>20 ✓ → **Valid**
  - Triangle (30, 31, 32): 30+31=61>32 ✓, 30+32=62>31 ✓, 31+32=63>30 ✓ → **Valid**
- Rows 3-4: Incomplete group (only 2 rows), should be **skipped**

**Expected Output**: 3 valid triangles

---

### 5. Single Group
**Purpose**: Minimum valid input

**Input**:
```
100 200 300
101 201 301
102 202 302
```

**Expected Output**: Should process exactly 3 triangles

---

### 6. Full Input File (input.md)
**Purpose**: Final validation with actual puzzle input

**Input**: The provided input.md file (1993 lines)

**Expected Processing**:
- Total lines: 1993
- Complete groups: 664 groups (1992 lines, last line incomplete)
- Total triangles checked: 664 × 3 = 1992 triangles

**Validation Method**:
- Run the solution on input.md
- Verify the output is a reasonable integer (between 0 and 1992)
- **Compare with Part 1 answer (1050)**: Should be different since we're reading differently
- The answer should make sense given the validation logic

**Success Criteria**:
- Program completes without errors
- Returns single integer
- Answer is different from Part 1 (1050)

---

## Testing Procedure

### Phase 1: Manual Small Tests
1. Create test file with the example from problem statement
2. Run solution manually: `python part_2_solution.py` (with modified input path)
3. Verify output matches expected (6)

### Phase 2: Edge Case Testing
1. Test incomplete group handling (4-5 lines of input)
2. Test single group (3 lines)
3. Test mixed valid/invalid triangles

### Phase 3: Full Input Validation
1. Run on actual input.md
2. Verify:
   - No runtime errors
   - Output is an integer
   - Output is in valid range [0, 1992]
   - Output differs from Part 1 answer

### Phase 4: Logic Verification
Manually verify first few groups from input.md:
```
Row 0: 566  477  376
Row 1: 575  488  365
Row 2:  50   18  156
```

Triangles:
- (566, 575, 50): 566+575=1141>50 ✓, 566+50=616>575 ✓, 575+50=625>566 ✓ → **Valid**
- (477, 488, 18): 477+488=965>18 ✓, 477+18=495>488 ✓, 488+18=506>477 ✓ → **Valid**
- (376, 365, 156): 376+365=741>156 ✓, 376+156=532>365 ✓, 365+156=521>376 ✓ → **Valid**

First group should contribute 3 valid triangles.

---

### 7. Empty Input (Edge Case)
**Purpose**: Handle completely empty input file

**Input**: Empty file (0 lines)

**Expected Processing**:
- `range(0, -2, 3)` produces empty range
- No iterations occur

**Expected Output**: 0 valid triangles

---

### 8. One Line Only (Edge Case)
**Purpose**: Handle input with only 1 line

**Input**:
```
100 200 300
```

**Expected Processing**:
- `range(0, -1, 3)` produces empty range
- No complete groups available

**Expected Output**: 0 valid triangles

---

### 9. Two Lines Only (Edge Case)
**Purpose**: Handle input with only 2 lines

**Input**:
```
100 200 300
101 201 301
```

**Expected Processing**:
- `range(0, 0, 3)` produces empty range
- No complete groups available

**Expected Output**: 0 valid triangles

---

## Success Criteria

- ✓ All manual tests pass with expected outputs
- ✓ Edge cases handled without errors (including 0, 1, 2 line inputs)
- ✓ Full input produces a valid result
- ✓ Result differs from Part 1 (validates we changed the algorithm)
- ✓ Manual verification of first group confirms logic is correct

## Debugging Strategy (if tests fail)

1. **Wrong count**: Add debug prints showing each triangle being processed
2. **Off-by-one errors**: Verify range boundaries and group indexing
3. **Parse errors**: Print raw rows before extracting columns
4. **Logic errors**: Manually trace through first group with pen and paper
