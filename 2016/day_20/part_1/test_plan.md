# Test Plan: Firewall IP Whitelist Identification

## Testing Strategy

We need to verify that our solution correctly:
1. Parses input ranges
2. Merges overlapping and adjacent ranges
3. Finds the lowest unblocked IP address
4. Handles edge cases

## Test Categories

### 1. Example Test (Provided in Problem Statement)

**Purpose**: Verify basic correctness with the given example

**Input**:
```
5-8
0-2
4-7
```

**Expected Process**:
- Parsed ranges: [(5, 8), (0, 2), (4, 7)]
- Sorted ranges: [(0, 2), (4, 7), (5, 8)]
- Merged ranges: [(0, 2), (4, 8)]
- Blocked IPs: 0, 1, 2, 4, 5, 6, 7, 8
- Unblocked IPs: 3, 9, 10, ...
- **Expected Output**: `3`

**Verification**: Run solution and compare output

### 2. Edge Case: First IP is Unblocked

**Purpose**: Test when 0 is not in any range

**Input**:
```
5-10
15-20
```

**Expected Process**:
- Merged ranges: [(5, 10), (15, 20)]
- IP 0 is not blocked
- **Expected Output**: `0`

**Verification**: Confirms we start checking from 0

### 3. Edge Case: First Range Starts at 0

**Purpose**: Test when blocked ranges start from 0 with a gap

**Input**:
```
0-5
10-15
```

**Expected Process**:
- Merged ranges: [(0, 5), (10, 15)]
- IPs 0-5 blocked, 6-9 unblocked
- **Expected Output**: `6`

**Verification**: Confirms we skip past ranges correctly

### 4. Edge Case: Adjacent Ranges (Should Merge)

**Purpose**: Verify that adjacent ranges are merged correctly

**Input**:
```
0-5
6-10
11-15
```

**Expected Process**:
- Ranges are adjacent (no gaps)
- Merged ranges: [(0, 15)]
- **Expected Output**: `16`

**Verification**: Tests the `range.start <= current.end + 1` logic

### 5. Edge Case: Overlapping Ranges

**Purpose**: Verify overlapping ranges merge correctly

**Input**:
```
0-10
5-15
12-20
```

**Expected Process**:
- All ranges overlap
- Merged ranges: [(0, 20)]
- **Expected Output**: `21`

**Verification**: Tests max() logic when extending ranges

### 6. Edge Case: Ranges in Random Order

**Purpose**: Verify sorting works correctly

**Input**:
```
50-60
10-20
30-40
0-5
```

**Expected Process**:
- Sorted: [(0, 5), (10, 20), (30, 40), (50, 60)]
- No merging needed (all disjoint)
- **Expected Output**: `6`

**Verification**: Tests that sorting precedes merging

### 7. Edge Case: Single Range

**Purpose**: Test minimal input

**Input**:
```
10-20
```

**Expected Process**:
- Merged ranges: [(10, 20)]
- **Expected Output**: `0`

**Verification**: Handles simple case

### 8. Edge Case: Empty Input File

**Purpose**: Test handling of empty input

**Input**:
```
(empty file)
```

**Expected Process**:
- No ranges to parse
- No ranges to merge
- No IPs blocked
- **Expected Output**: `0`

**Verification**: Confirms proper handling of empty/minimal input

### 9. Edge Case: Duplicate Ranges

**Purpose**: Test that duplicates are handled

**Input**:
```
5-10
5-10
5-10
```

**Expected Process**:
- All merge into single range
- Merged ranges: [(5, 10)]
- **Expected Output**: `0`

**Verification**: Merging handles duplicates naturally

### 10. Edge Case: Nested Ranges

**Purpose**: Test when one range completely contains another

**Input**:
```
0-100
20-30
50-60
```

**Expected Process**:
- Input ranges (unsorted): [(0, 100), (20, 30), (50, 60)]
- After sorting by start value: [(0, 100), (20, 30), (50, 60)]
- During merging:
  - Start with (0, 100)
  - (20, 30): 20 <= 100+1, so merge: end = max(100, 30) = 100
  - (50, 60): 50 <= 100+1, so merge: end = max(100, 60) = 100
- Merged ranges: [(0, 100)]
- **Expected Output**: `101`

**Verification**: Tests max() logic when contained range has smaller end

### 11. Actual Input Test

**Purpose**: Solve the actual problem

**Input**: Use the provided `input.md` file with ~946 ranges

**Expected Process**:
- Parse all 946 ranges
- Sort and merge
- Find lowest unblocked IP

**Verification**:
- Solution should run quickly (< 1 second)
- Output should be a reasonable integer (likely small, possibly 0 or close to it)
- Manually verify first few merged ranges if needed

**How to Verify**:
1. Examine first few sorted ranges from input.md
2. Check if 0 is covered in any range
3. If covered, find where that range ends and check next range

## Testing Methodology

### Unit Testing Approach

**Test Each Function Separately**:

1. **Test `parse_input()`**:
   - Create small test file with content like "5-10\n15-20"
   - Verify it returns correct list of tuples: [(5, 10), (15, 20)]
   - Check integer conversion works
   - Test empty file returns empty list

2. **Test `merge_ranges()`**:
   - Provide pre-parsed ranges like [(0, 5), (3, 8), (10, 15)]
   - Verify merging logic: should return [(0, 8), (10, 15)]
   - Test with empty list: should return empty list
   - Test with single range: should return that range unchanged
   - Test adjacent ranges: [(0, 5), (6, 10)] should merge to [(0, 10)]

3. **Test `find_lowest_unblocked()`**:
   - Provide pre-merged ranges like [(5, 10), (15, 20)]
   - Verify returns 0 (since 0 not blocked)
   - Test with [(0, 5), (10, 15)]: should return 6
   - Test with empty list: should return 0

### Integration Testing Approach

**Test Complete Pipeline**:
- Create small test input files for each edge case
- Run complete solution
- Verify output matches expected

### Manual Verification for Actual Input

**Step-by-step manual check**:
1. Run solution on actual input
2. Print intermediate results:
   - Number of original ranges: 946
   - Number of merged ranges: (should be much less)
   - First few merged ranges
   - Final answer
3. Manually verify first merged range contains 0 or not
4. If contains 0, check where it ends and if there's a gap

## Test Execution Plan

### Step 1: Create Test Files
Create separate test input files for each edge case:
- `test_example.txt`
- `test_first_unblocked.txt`
- `test_starts_at_zero.txt`
- etc.

### Step 2: Run Unit Tests
Test each function with various inputs using assertions or manual verification

### Step 3: Run Integration Tests
For each test file:
```bash
python solution.py test_example.txt
# Verify output is 3

python solution.py test_first_unblocked.txt
# Verify output is 0

# ... etc
```

Or using default input file:
```bash
python solution.py
# Uses input.md by default
```

### Step 4: Run Actual Input
```bash
python solution.py input.md
# or simply
python solution.py
# (uses input.md by default)
# Record output
# Verify it's reasonable
```

### Step 5: Debug Output (if needed)
Add debug prints to verify:
- Number of parsed ranges
- Sample of sorted ranges
- Number of merged ranges
- Sample of merged ranges
- Candidate IP as we scan through ranges

## Expected Outcomes

### Correctness Criteria
- All test cases produce expected output
- Solution handles edge cases correctly
- Actual input produces a valid IP address (0 to 4,294,967,295)

### Performance Criteria
- Solution completes in < 1 second for actual input
- No memory issues with ~946 ranges
- Algorithm scales efficiently

## Debugging Strategy

If tests fail:

1. **Wrong answer on example**: Check merging logic
2. **Wrong answer when 0 is unblocked**: Check initialization of candidate
3. **Wrong answer for adjacent ranges**: Check the `<= end + 1` condition
4. **Performance issues**: Verify O(n log n) complexity, check for nested loops

## Validation Checklist

- [ ] Example test passes
- [ ] First IP unblocked test passes
- [ ] First range starts at 0 test passes
- [ ] Adjacent ranges merge correctly
- [ ] Overlapping ranges merge correctly
- [ ] Random order handled correctly
- [ ] Single range works
- [ ] Empty input file handled
- [ ] Duplicates handled
- [ ] Nested ranges handled
- [ ] Actual input produces valid result
- [ ] Performance is acceptable (< 1 second)
- [ ] Output format is correct (single integer, no extra text)
- [ ] Command-line argument works correctly
- [ ] Default filename works when no argument provided

## Notes

- We don't need exhaustive testing of all possible inputs since this is a scripting task
- Focus on edge cases that could break the merging or gap-finding logic
- The actual input test is the ultimate validation
- Manual inspection of intermediate results helps verify correctness
