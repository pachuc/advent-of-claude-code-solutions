# Test Plan - Part 2: Modified Repetition Code

## Testing Objectives
1. Verify the solution correctly selects the LEAST frequent character at each position
2. Ensure the modification from Part 1 works correctly
3. Validate the solution with the provided example
4. Test the solution with the actual puzzle input
5. Check edge cases specific to "least frequent" logic

## Test Categories

### 1. Example Validation Test
**Purpose**: Verify the algorithm works on the provided example

**Test Case**: Example from problem.md
```
Input:
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
```

**Expected Output**: `advent`

**Verification Steps**:
1. Create a test file with the example input
2. Run the solution against this test file
3. Verify output matches `advent`

**Note**: The problem statement provides the expected output as `advent`, so we trust this as the correct answer. Manual frequency counting can be error-prone for verification, so we primarily rely on the expected output provided in the problem description.

**Important Note on Ties**: When multiple characters have the same minimum frequency, `Counter.most_common()` returns them in a consistent but implementation-dependent order. For the puzzle input, this should not be an issue.

### 2. Actual Input Test
**Purpose**: Solve the actual puzzle

**Test Case**: input.md (598 lines, 8 characters each)

**Verification Steps**:
1. Run the solution: `python solution.py`
2. Verify output is an 8-character lowercase string
3. Verify output is different from Part 1 answer (`qzedlxso`)
4. Check that result makes sense (is a valid-looking string)

**Expected Characteristics**:
- Output length: exactly 8 characters
- Character set: lowercase letters a-z
- Different from Part 1 result

### 3. Comparison with Part 1
**Purpose**: Ensure the logic change from Part 1 to Part 2 is correct

**Test Case**: Run both Part 1 and Part 2 solutions on same input

**Verification Steps**:
1. Run Part 1 solution: should output `qzedlxso`
2. Run Part 2 solution: should output different result
3. For each position, verify:
   - Part 1 picks the character with highest count
   - Part 2 picks the character with lowest count
   - They should be different (unless all characters appear equally often)

### 4. Edge Case: Single Line Input
**Purpose**: Test behavior with minimal input

**Test Case**:
```
Input: hello
Expected Output: hello
```

**Rationale**: With only one line, every character appears exactly once at its position, so it should return the same string.

### 5. Edge Case: Two Lines with No Character Repetition
**Purpose**: Test when all characters at a position are unique

**Test Case**:
```
Input:
ab
cd

Expected: Should select one character from each position
Position 0: a(1), c(1) - will select one (deterministic based on Counter internals)
Position 1: b(1), d(1) - will select one
```

**Verification**: The solution should run without errors and produce a 2-character output.

### 6. Edge Case: Uniform Distribution
**Purpose**: Test when all characters appear with equal frequency

**Test Case**:
```
Input:
abc
bca
cab

Each position has each character appearing exactly once.
```

**Expected Behavior**: Solution should select some character (likely the last one encountered in Counter's ordering).

**Verification**: Ensure no crashes and output is 3 characters long.

### 7. Frequency Analysis Test
**Purpose**: Verify the counting logic is correct

**Test Case**: Create a controlled input where frequencies are known
```
Input:
aaa
aab
abc

Position 0: a(3) - most common
Position 1: a(2), b(1) - 'b' is least common
Position 2: a(1), b(1), c(1) - one of these is least (tie)
```

**Expected Output**: Character 0 should be 'a', character 1 should be 'b'

**Verification Steps**:
1. Create test file with this input
2. Manually calculate expected output
3. Run solution and compare

### 8. Input Validation Test
**Purpose**: Verify error handling works (inherited from Part 1)

**Test Cases**:

**8a. Empty file test**:
```bash
# Create empty file
touch empty_test.txt
# Run solution (modify to read from empty_test.txt)
python solution.py
# Expected: should return empty string (or handle gracefully)
```

**8b. Lines of different lengths**:
```python
# Create test file with inconsistent line lengths
cat > invalid_test.txt << EOF
abc
abcd
ab
EOF
# Expected: should raise ValueError
```

**8c. Non-existent file**:
```bash
# Run with non-existent file
# Expected: should exit with error message about file not found
```

**Verification**: These should behave the same as Part 1.

### 9. Performance Test
**Purpose**: Ensure solution runs efficiently on actual input size

**Test Case**: The actual input (598 lines × 8 chars = 4,784 characters)

**Acceptance Criteria**:
- Solution completes in under 100ms (realistically should be <10ms)
- No memory issues
- Clean output with no warnings

**Verification**:
```bash
time python solution.py
```
Should show execution time well under 100 milliseconds. Given the small input size, typical execution should be nearly instantaneous (a few milliseconds).

## Manual Verification Strategy

### Position-by-Position Analysis (Sample)
For thoroughness, manually verify at least one position from the actual input:

**Example: Verify position 0**
1. Extract all first characters from input.md
2. Count occurrences: `grep -o '^.' input.md | sort | uniq -c | sort -n`
3. Identify the character with minimum count
4. Verify this matches output[0]

### Character Distribution Check
```bash
# For each position, find least frequent character
for i in {0..7}; do
    cut -c$((i+1)) input.md | sort | uniq -c | sort -n | head -1
done
```
This bash command will show the least frequent character at each position.

### 10. Programmatic Verification Test
**Purpose**: Automatically verify each position's character selection

**Implementation**:
```python
from collections import Counter

def verify_solution(lines, expected_output):
    """Verify that the solution correctly computes least frequent chars."""
    for pos in range(len(expected_output)):
        chars = [line[pos] for line in lines if len(line) > pos]
        counts = Counter(chars)
        least_common_char = counts.most_common()[-1][0]
        assert least_common_char == expected_output[pos], \
            f"Position {pos}: expected {expected_output[pos]}, got {least_common_char}"
    print("All positions verified correctly!")

# Run after getting solution output
lines = [line.strip() for line in open('input.md') if line.strip()]
solution_output = "..." # paste actual output here
verify_solution(lines, solution_output)
```

**Verification**: Run this script after obtaining the solution to programmatically confirm each character.

## Test Execution Order
1. **Example validation** (quick confidence check)
2. **Controlled frequency test** (Test 7 - diagnostic value)
3. **Actual input test** (get the answer)
4. **Comparison with Part 1** (verify difference)
5. **Programmatic verification** (Test 10 - verify all positions)
6. **Manual position verification** (spot check correctness)
7. **Edge cases** (ensure robustness)
8. **Performance test** (verify efficiency)

## Success Criteria
- [ ] Example test produces `advent`
- [ ] Actual input produces an 8-character lowercase string
- [ ] Result differs from Part 1 answer `qzedlxso`
- [ ] Programmatic verification confirms all 8 positions are correct
- [ ] Manual verification of at least 2 positions confirms correct counting
- [ ] All edge cases handled without crashes
- [ ] Execution time under 100ms (realistically under 10ms)
- [ ] Code is a minimal, clear modification from Part 1
- [ ] Diff between Part 1 and Part 2 shows only the expected one-line change

## Debugging Strategy
If the answer is wrong:
1. Print frequency distributions for each position
2. Compare with Part 1 output position-by-position
3. Manually verify the least frequent character for position 0
4. Check for off-by-one errors or indexing issues
5. Verify `most_common()[-1]` returns least frequent, not most

## Notes on Tie-Breaking
When multiple characters have the same minimum frequency, Python's Counter.most_common() will return them in a consistent but potentially arbitrary order. This should not be an issue for the puzzle input (which likely has unique minimums), but is worth noting for edge case testing.
