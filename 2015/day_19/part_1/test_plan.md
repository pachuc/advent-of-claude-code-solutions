# Test Plan: Molecular Replacement Calibration

## Testing Objective
Verify that the solution correctly counts distinct molecules generated from single replacements, handling all edge cases and matching expected behavior.

## Test Strategy
1. **Unit Tests**: Test individual functions in isolation
2. **Integration Tests**: Test the complete workflow with known examples
3. **Edge Case Tests**: Verify handling of special scenarios
4. **Full Input Test**: Validate against actual problem input

## Unit Tests

### Test 1: Pattern Finding - Basic Case
**Function**: `find_all_occurrences(text, pattern)`

**Test Case 1.1**: Single occurrence
- Input: `text="ABCDEF"`, `pattern="CD"`
- Expected: `[2]`
- Validates: Basic pattern matching works

**Test Case 1.2**: Multiple non-overlapping occurrences
- Input: `text="ABABAB"`, `pattern="AB"`
- Expected: `[0, 2, 4]`
- Validates: Multiple occurrences are found

**Test Case 1.3**: Overlapping occurrences
- Input: `text="HHH"`, `pattern="HH"`
- Expected: `[0, 1]`
- Validates: Overlapping patterns are all detected (critical edge case)

**Test Case 1.4**: No occurrences
- Input: `text="ABCDEF"`, `pattern="XY"`
- Expected: `[]`
- Validates: Returns empty list when pattern not found

**Test Case 1.5**: Single character pattern
- Input: `text="HOHOHO"`, `pattern="H"`
- Expected: `[0, 2, 4]`
- Validates: Single character patterns work correctly

**Test Case 1.6**: Pattern at boundaries
- Input: `text="ABCDEF"`, `pattern="AB"`
- Expected: `[0]`
- Validates: Pattern at start works
- Input: `text="ABCDEF"`, `pattern="EF"`
- Expected: `[4]`
- Validates: Pattern at end works

### Test 2: Input Parsing
**Function**: `parse_input(filename)`

**Test Case 2.1**: Parse sample input
- Create a small test input file with 3 rules and 1 molecule
- Expected: Correctly separated rules list and medicine string
- Validates: Parsing logic correctly splits input sections using dynamic blank line detection

**Test Case 2.2**: Handle whitespace
- Input with trailing/leading whitespace on molecule line
- Expected: Whitespace stripped from molecule
- Validates: Input cleaning works

**Test Case 2.3**: Variable number of rules
- Test with different numbers of rules (e.g., 5 rules, 50 rules)
- Expected: Correctly parses regardless of rule count
- Validates: Dynamic blank line detection works (not hard-coded line numbers)

### Test 3: Molecule Generation
**Function**: `generate_molecules(rules, medicine)`

**Test Case 3.1**: Single rule, single occurrence
- Rules: `[("H", "HO")]`
- Medicine: `"H"`
- Expected: Set with 1 molecule: `{"HO"}`
- Validates: Basic replacement works

**Test Case 3.2**: Single rule, multiple occurrences
- Rules: `[("H", "HO")]`
- Medicine: `"HH"`
- Expected: Set with 2 molecules: `{"HOH", "HHO"}`
- Validates: Each occurrence generates a separate molecule

**Test Case 3.3**: Multiple rules for same source
- Rules: `[("H", "HO"), ("H", "OH")]`
- Medicine: `"H"`
- Expected: Set with 2 molecules: `{"HO", "OH"}`
- Validates: All rules are applied

**Test Case 3.4**: Rule where pattern equals replacement
- Rules: `[("H", "H")]`
- Medicine: `"HOH"`
- Expected: Set with 2 molecules: `{"HOH", "HOH"}` → Actually just 1: `{"HOH"}`
- Validates: Edge case where replacement doesn't change the molecule (generates same string)

## Integration Tests

### Test 4: Example from Problem Statement
**Complete workflow test**

**Input**:
```
H => HO
H => OH
O => HH

HOH
```

**Expected Output**: `4`

**Expected Molecules** (detailed trace):
- Rule "H => HO", H at position 0: `HO` + `OH` = `HOOH`
- Rule "H => OH", H at position 0: `OH` + `OH` = `OHOH`
- Rule "H => HO", H at position 2: `HO` + `HO` = `HOHO`
- Rule "H => OH", H at position 2: `HO` + `OH` = `HOOH` (duplicate)
- Rule "O => HH", O at position 1: `H` + `HH` + `H` = `HHHH`

**Distinct**: `{HOOH, OHOH, HOHO, HHHH}` = 4 molecules

**Note**: The fourth replacement creates `HOOH` which was already created by the first replacement, so it's correctly counted only once.

**Validation**:
- Run complete solve function with this input
- Verify output is exactly 4
- This is the most critical test as it matches the problem example

### Test 5: Duplicate Detection
**Objective**: Verify that duplicate molecules are counted only once

**Input**:
```
H => AB
O => AB

HOH
```

**Expected**:
- H at 0 → `ABOAH`
- H at 2 → `HOAB`
- O at 1 → `HABH`

All distinct, so output = 3

**Alternate test for actual duplicates**:
```
H => O
O => H

HOH
```

**Expected**:
- H at 0 → `OOH`
- H at 2 → `HOO`
- O at 1 → `HHH`

All distinct, so output = 3

## Edge Cases Tests

### Test 6: Pattern at Multiple Positions
**Scenario**: Same pattern appears multiple times

**Input**:
```
Ca => CaCa

CaCaCa
```

**Expected**:
- Ca at 0 → `CaCaCaCa`
- Ca at 2 → `CaCaCaCa` (duplicate!)
- Ca at 4 → `CaCaCaCa` (duplicate!)

Output = 1 (all replacements create the same molecule)

**Validates**: Duplicates from different positions are handled

### Test 7: Long Replacements
**Scenario**: Replacement string is much longer than source

**Input**:
```
H => CRnFYFYFAr

H
```

**Expected**: 1 distinct molecule (`CRnFYFYFAr`)

**Validates**: Long replacement strings don't cause issues

### Test 8: Source Not in Medicine
**Scenario**: A rule's source pattern doesn't appear in the medicine

**Input**:
```
X => YZ
H => HO

HOH
```

**Expected**: Only H replacements work, X rule generates nothing

**Validates**: Rules with no matches are safely ignored

### Test 9: Very Short Medicine
**Scenario**: Medicine is a single character

**Input**:
```
H => HO

H
```

**Expected**: 1 molecule

**Validates**: Minimal input case works

### Test 10: No Applicable Rules
**Scenario**: No rules match the medicine molecule

**Input**:
```
X => Y
Z => W

HOH
```

**Expected**: 0 molecules (empty set, so count is 0)

**Validates**: Case where no replacements are possible

### Test 11: Pattern Longer Than Medicine
**Scenario**: A rule's source pattern is longer than the entire medicine molecule

**Input**:
```
ABCDEFGH => XYZ

AB
```

**Expected**: 0 molecules (pattern won't be found)

**Validates**: `find_all_occurrences` handles this correctly without errors

## Full Input Validation

### Test 12: Actual Problem Input
**Objective**: Verify solution works with the real input

**Steps**:
1. Run the solve function with `input.md`
2. Record the output number
3. Verify the number is reasonable (rough estimate: 200-800, but could be outside this range)
4. Check runtime is acceptable (< 5 seconds)

**Validation Checks**:
- Output is a positive integer
- Output is greater than the number of rules (43) - sanity check
- Output is less than (rules × molecule_length) ≈ 43 × 600 = ~25,800 - upper bound
- No errors or exceptions during execution

**Note**: The 200-800 range is a very rough estimate. The actual answer depends on:
- How many times each pattern appears in the molecule
- How many duplicate molecules are generated from different replacements
- Don't treat this range as a strict requirement, just a sanity check

**Manual Verification** (if needed):
- Spot check a few molecules by manually tracing a couple replacements
- Verify different positions of the same source create different molecules

## Performance Tests

### Test 13: Runtime Verification
**Objective**: Ensure solution completes in reasonable time

**Method**:
- Time the execution with full input
- Expected: < 1 second for the algorithm described
- Acceptable: < 5 seconds

**If too slow**: Algorithm may need optimization (unlikely with this approach)

## Test Execution Order

1. **First**: Run all unit tests (Tests 1-3) to verify components work
2. **Second**: Run the example test (Test 4) - **this is the most critical validation**
3. **Third**: Run edge case tests (Tests 6-11) to ensure robustness
4. **Finally**: Run full input test (Test 12) to get the actual answer

## Success Criteria

The solution is considered correct if:
1. ✓ All unit tests pass
2. ✓ Example test produces output of 4
3. ✓ Edge cases are handled without errors
4. ✓ Full input produces a reasonable integer output
5. ✓ Execution time is acceptable (< 5 seconds)

## Debugging Strategy

If tests fail:

1. **For unit test failures**:
   - Check the specific function implementation
   - Verify loop conditions and boundary cases
   - Add print statements to trace execution

2. **For example test failure**:
   - Print all generated molecules to see what's being created
   - Manually trace through each rule application
   - Check if duplicates are being counted multiple times

3. **For unexpected output on full input**:
   - Verify parsing is correct (print first few rules and medicine)
   - Check if molecule count seems reasonable
   - Spot-check a few random replacements manually

## Test Implementation Notes

- For a script-based solution, manual testing with print statements is acceptable
- Can optionally use `assert` statements for quick verification
- Could create a formal test suite with `unittest` or `pytest`, but not required for this problem
- **Priority**: Test 4 (example case) is the most critical - if this passes, high confidence in correctness

**Testing Approach**:
```python
# Simple test harness example
def test_find_all_occurrences():
    assert find_all_occurrences("HHH", "HH") == [0, 1]
    assert find_all_occurrences("ABABAB", "AB") == [0, 2, 4]
    print("✓ Pattern finding tests passed")

def test_example():
    # Create test input file or use test data
    result = solve("test_input.txt")  # With HOH example
    assert result == 4, f"Expected 4, got {result}"
    print("✓ Example test passed")

# Run tests
test_find_all_occurrences()
test_example()
print("\nRunning full input:")
answer = solve("input.md")
print(f"Answer: {answer}")
```

The actual input test will give us the answer to submit
