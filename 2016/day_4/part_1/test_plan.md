# Testing Plan: Room Validation and Sector ID Summation

## Updates Based on Critique
This plan has been updated to address the following items from the critique:
1. **Frequency Calculation Testing**: Clarified that this is tested indirectly through checksum generation (it's an internal step, not a separate function)
2. **Detailed Test Cases**: Added frequency breakdowns for Test 1.4 to show the step-by-step calculation for each example
3. **Edge Case Clarification**: Better documented the <5 unique letters case with detailed explanation
4. **Tie-Breaking Verification**: Added clarification for Test 3.2 confirming that y < z alphabetically
5. **Manual Validation Example**: Provided a worked example for Test 4.1 showing manual calculation
6. **Known Limitations**: Explicitly listed what is NOT tested and why this is acceptable for an AoC script

## Overview
This testing plan covers verification of the room validation algorithm, including parsing, checksum generation, and sector ID summation. The goal is to ensure correctness across various input scenarios.

## Test Strategy
Since this is a script to solve a specific problem (not production code), we focus on:
1. **Correctness**: Verify the algorithm produces the right answer
2. **Edge cases**: Test boundary conditions and special cases from the problem
3. **Example validation**: Confirm provided examples work correctly

We do NOT need to test:
- Invalid input handling (assume input is well-formed)
- File I/O errors (assume input.md exists)
- Performance under extreme load (input size is small)

## Test Levels

### Level 1: Unit Tests (Individual Functions)

#### Test 1.1: Room Entry Parsing
**Function**: `parse_room_entry(line)`

**Test Cases**:
| Input | Expected Output |
|-------|----------------|
| `"aaaaa-bbb-z-y-x-123[abxyz]"` | `("aaaaa-bbb-z-y-x", 123, "abxyz")` |
| `"a-b-c-d-e-f-g-h-987[abcde]"` | `("a-b-c-d-e-f-g-h", 987, "abcde")` |
| `"not-a-real-room-404[oarel]"` | `("not-a-real-room", 404, "oarel")` |
| `"totally-real-room-200[decoy]"` | `("totally-real-room", 200, "decoy")` |
| `"single-999[abcde]"` | `("single", 999, "abcde")` |
| `"many-dashes-in-name-1[aaaaa]"` | `("many-dashes-in-name", 1, "aaaaa")` |

**Verification**: Parse correctly extracts all three components with correct types

#### Test 1.2: Letter Frequency Calculation (Internal Step)
**Note**: This is handled internally within `generate_expected_checksum()`, not a separate function.

**Verification Approach**:
Test this indirectly through checksum generation tests (Test 1.3), which verify that:
- Dashes are excluded from counts
- Letter counts are accurate
- Only letters are considered

#### Test 1.3: Expected Checksum Generation
**Function**: `generate_expected_checksum(encrypted_name)`

**Test Cases**:

**Case 1: Different frequencies**
- Input: `"aaaaa-bbb-z-y-x"`
- Frequencies: a=5, b=3, z=1, y=1, x=1
- Expected: `"abxyz"` (sorted by frequency, then alpha for ties)

**Case 2: All tied (alphabetical order)**
- Input: `"a-b-c-d-e-f-g-h"`
- Frequencies: all 1
- Expected: `"abcde"` (first 5 alphabetically)

**Case 3: Multiple ties**
- Input: `"aaa-bb-bb-c-c-d-d-e-e"`
- Frequencies: a=3, b=4, c=2, d=2, e=2
- Expected: `"bacde"` (b=4 first, then a=3, then c,d,e tied at 2 so alphabetical)

**Case 4: Exactly 5 unique letters**
- Input: `"abcde"`
- Expected: `"abcde"`

**Case 5: Fewer than 5 unique letters**
- Input: `"aaa-bbb"`
- Frequencies: a=3, b=3 (tied)
- Sorted: a(3), b(3) — alphabetical order for tie
- Expected: `"ab"` (only 2 letters available, not 5)
- Note: Algorithm handles this via `[:5]` slice, which returns all available when < 5

**Verification**:
- Primary sort: frequency descending
- Secondary sort: alphabetical ascending
- Returns first 5 characters (or fewer if < 5 unique letters exist)

#### Test 1.4: Room Validation
**Function**: `is_real_room(encrypted_name, checksum)`

**Test Cases (from problem examples with frequency calculations)**:

**Case 1**: `"aaaaa-bbb-z-y-x"` with checksum `"abxyz"`
- Letters: a=5, b=3, x=1, y=1, z=1
- Sorted: a(5), b(3), x(1), y(1), z(1) — x,y,z tied so alphabetical order
- Expected: `"abxyz"`
- Result: `True` (matches)

**Case 2**: `"a-b-c-d-e-f-g-h"` with checksum `"abcde"`
- Letters: a=1, b=1, c=1, d=1, e=1, f=1, g=1, h=1 (all tied)
- Sorted: alphabetical order for ties
- Expected: `"abcde"` (first 5 alphabetically)
- Result: `True` (matches)

**Case 3**: `"not-a-real-room"` with checksum `"oarel"`
- Letters: n=1, o=3, t=1, a=2, r=2, e=1, l=1, m=1
- Sorted: o(3), a(2), r(2), e(1), l(1), m(1), n(1), t(1) — a,r tied at 2, then e,l,m,n,t tied at 1
- Expected: `"oarel"` (o first, then a and r alphabetically, then e and l)
- Result: `True` (matches)

**Case 4**: `"totally-real-room"` with checksum `"decoy"`
- Letters: t=2, o=2, a=2, l=2, y=1, r=1, e=1, m=1
- Sorted: t(2), o(2), a(2), l(2), e(1), m(1), r(1), y(1) — multiple ties at 2, alphabetical: a,l,o,t
- Expected: `"alort"` (NOT "decoy")
- Result: `False` (does NOT match)

**Case 5**: `"aaaaa-bbb-z-y-x"` with wrong checksum `"abxya"`
- Expected: `"abxyz"`
- Provided: `"abxya"`
- Result: `False` (wrong checksum)

**Verification**: Correctly identifies real vs decoy rooms, with detailed frequency breakdown for clarity

### Level 2: Integration Tests (End-to-End)

#### Test 2.1: Example Problem Validation
**Input**: The four example rooms from problem.md
```
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
```

**Expected Output**: `1514` (123 + 987 + 404)

**Method**:
1. Create a test input file with these 4 lines
2. Run the solve function
3. Verify output equals 1514

**Verification**: Confirms the entire pipeline works correctly

#### Test 2.2: Edge Case: All Decoys
**Input**: Room entries where no checksums match
```
fake-room-100[zzzzz]
another-fake-200[xxxxx]
```

**Expected Output**: `0`

**Verification**: Handles case with no valid rooms

#### Test 2.3: Edge Case: All Real
**Input**: Room entries where all checksums match
```
aaaaa-100[aaaaa]
bbbbb-200[bbbbb]
```

**Expected Output**: `300`

**Verification**: Correctly sums when all rooms are valid

#### Test 2.4: Large Sector IDs
**Input**: Test with large numbers
```
aaaaa-999999[aaaaa]
bbbbb-888888[bbbbb]
```

**Expected Output**: `1888887`

**Verification**: Integer overflow is not an issue (Python handles big ints)

### Level 3: Checksum Edge Cases

#### Test 3.1: Complex Tie-breaking
**Scenario**: Multiple letters with same frequency

**Test Data**:
```python
# Input: "aabbccddee-123[abcde]"
# Frequencies: a=2, b=2, c=2, d=2, e=2 (all tied)
# Expected checksum: "abcde" (alphabetical order)
# Should be REAL
```

**Verification**: Tie-breaking works correctly with alphabetical sorting

#### Test 3.2: Mixed Frequencies and Ties
**Test Data**:
```python
# Input: "zzz-yyy-abc-123[yzabc]"
# Frequencies: z=3, y=3, a=1, b=1, c=1
# Expected checksum: "yzabc"
# Reasoning: y and z both appear 3 times (tied for highest)
#            In alphabetical order: y comes before z (y is 25th letter, z is 26th)
#            Then a, b, c all tied at 1, so alphabetical order
# Should be REAL if checksum is "yzabc", DECOY if "zyabc"
```

**Verification**: Tie-breaking applies when top frequencies are tied. This test confirms alphabetical ordering works correctly (y < z alphabetically)

#### Test 3.3: Fewer Than 5 Unique Letters
**Test Data**:
```python
# Input: "aaa-bb[ab]"
# Only 2 unique letters: a=3, b=2
# Expected checksum: "ab" (only 2 characters, not 5)
# Algorithm returns: ''.join(...[:5]) which gives "ab" when only 2 letters exist
# This would validate as REAL if provided checksum is exactly "ab"
```

**Note**: This edge case is unlikely in actual input since the problem format specifies checksums are always exactly 5 characters `[xxxxx]`. However, our algorithm handles it gracefully by returning all available letters when < 5 exist. If such an entry appears, it would fail validation since the checksum format requires exactly 5 characters.

### Level 4: Actual Input Validation

#### Test 4.1: Spot Check Real Rooms
**Method**:
1. Manually validate 2-3 entries from input.md
2. Calculate expected checksum by hand
3. Verify our function produces same result

**Example Manual Validation**:
Entry: `fubrjhqlf-edvnhw-dftxlvlwlrq-803[wjvzd]`
- Remove dashes: "fubrjhqlfedvnhwdftxlvlwlrq"
- Count letters: f=3, d=3, v=3, l=3, h=2, w=2, u=1, b=1, r=1, j=1, q=2, e=1, n=1, t=1, x=1
- Sort by frequency (desc) then alpha: d(3), f(3), l(3), v(3), h(2), q(2), w(2), b(1), e(1)...
- Top 5: When multiple tied at 3, alphabetical: d, f, l, v, then h and q tied at 2, h first
- Expected: "dflvh"
- Provided: "wjvzd"
- **Manual check needed**: Run actual counter to verify

**Verification**:
- Manually calculate 1-2 entries to verify algorithm correctness
- This is a spot-check during testing, not an exhaustive validation

#### Test 4.2: Final Answer Verification
**Method**:
1. Run solve() on actual input.md
2. Verify the answer is a reasonable integer (likely in range 100,000 - 500,000)
3. Re-run to ensure deterministic result (same answer every time)

**Verification**:
- Answer is consistent across multiple runs
- Answer is within expected range based on input size

## Testing Implementation Approach

### Option 1: Inline Testing (Quick Verification)
Add a test section at the bottom of the main script:
```python
def run_tests():
    # Test parsing
    assert parse_room_entry("aaaaa-bbb-z-y-x-123[abxyz]") == ("aaaaa-bbb-z-y-x", 123, "abxyz")

    # Test checksum generation
    assert generate_expected_checksum("aaaaa-bbb-z-y-x") == "abxyz"

    # Test room validation
    assert is_real_room("aaaaa-bbb-z-y-x", "abxyz") == True
    assert is_real_room("totally-real-room", "decoy") == False

    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
    result = solve()
    print(f"Answer: {result}")
```

### Option 2: Separate Test File (More Organized)
Create `test_solution.py` with proper test functions

### Recommendation
Use **Option 1** for this problem - inline tests are sufficient for a single-file script solution. The validation function should be called before solving the actual input to ensure correctness.

## Manual Verification Steps

1. **Run Example Test**:
   - Create small test file with 4 example entries
   - Verify output is 1514

2. **Inspect Sample Outputs**:
   - Add debug prints to show each room's validation status
   - Manually verify 5-10 rooms to ensure correct classification

3. **Check Final Answer**:
   - Run on actual input.md
   - Verify answer is reasonable
   - Run multiple times to ensure consistency

4. **Verify Tie-breaking Logic**:
   - Create specific test case with known ties
   - Trace through sorting logic
   - Confirm alphabetical order is respected

## Success Criteria
- [ ] All example cases produce expected output (sum = 1514)
- [ ] Tie-breaking works correctly (alphabetical for same frequency)
- [ ] Parsing handles all input formats correctly
- [ ] Final answer on input.md is consistent across runs
- [ ] No crashes or exceptions during execution
- [ ] Solution completes in < 1 second

## Known Limitations (Acceptable for Script)
The following are NOT tested since this is a script for a specific problem:
- Input validation (assumes well-formed data per problem spec)
- Error handling for missing files (assumes input.md exists)
- Malformed entries (assumes regex will match all lines)
- Empty input file
- Single room entry
- Rooms with extremely long names
- Performance under load (input size ~947 is small)

These limitations are acceptable since we're solving a specific Advent of Code problem with known, well-formed input.
