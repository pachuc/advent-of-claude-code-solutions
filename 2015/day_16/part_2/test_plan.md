# Test Plan: Finding the Real Aunt Sue (Part 2)

## Testing Objectives
1. Verify correct parsing of input format
2. Validate matching logic for all three comparison rule types
3. Ensure unlisted compounds are properly ignored
4. Confirm correct Sue is identified from the actual input

## Test Strategy
Focus on correctness of the matching algorithm, particularly the special comparison rules that differ from Part 1.

## Testing Approach
This test plan uses a **hybrid approach**:
- **Unit Testing**: Create a separate test script (`test_solution.py`) to test the matching logic with synthetic test cases
- **Integration Testing**: Run the solution on actual input.md and verify the result
- **Manual Verification**: Cross-check the identified Sue against the MFCSAM target values

For a scripting task, this balances thoroughness with practicality.

## Differences from Part 1
**Part 1** used exact matching (==) for all compounds.

**Part 2** introduces range-based comparisons:
- **cats** and **trees**: Must use > comparison (not ==)
- **pomeranians** and **goldfish**: Must use < comparison (not ==)
- All other compounds still use ==

**Critical Testing Focus**: Boundary values where > and < matter (e.g., cats: 7 should NOT match, cats: 8 should match).

---

## Test Case 1: Parse Input Format
**Objective**: Verify input parsing extracts Sue number and compounds correctly

**Test Data**:
```
Sue 1: goldfish: 9, cars: 0, samoyeds: 9
```

**Expected Output**:
- Sue number: 1
- Compounds: {'goldfish': 9, 'cars': 0, 'samoyeds': 9}

**Validation**:
- Print parsed data structure for first few Sues
- Verify all 500 Sues are parsed
- Check that values are integers, not strings

---

## Test Case 2: Greater-Than Rule (cats)
**Objective**: Verify cats comparison uses > instead of ==

**Target**: cats: 7

**Test Scenarios**:
| Sue's cats value | Should Match? | Reason |
|-----------------|---------------|---------|
| 6 | No | 6 ≤ 7 |
| 7 | No | 7 ≤ 7 (NOT greater than) |
| 8 | Yes | 8 > 7 |
| 9 | Yes | 9 > 7 |
| 100 | Yes | 100 > 7 |

**Validation**:
- Create test cases with only cats compound
- Verify boundary case: cats: 7 should NOT match
- Verify cats: 8+ should match

---

## Test Case 3: Greater-Than Rule (trees)
**Objective**: Verify trees comparison uses > instead of ==

**Target**: trees: 3

**Test Scenarios**:
| Sue's trees value | Should Match? | Reason |
|------------------|---------------|---------|
| 2 | No | 2 ≤ 3 |
| 3 | No | 3 ≤ 3 (NOT greater than) |
| 4 | Yes | 4 > 3 |
| 5 | Yes | 5 > 3 |
| 10 | Yes | 10 > 3 |

**Validation**:
- Create test cases with only trees compound
- Verify boundary case: trees: 3 should NOT match
- Verify trees: 4+ should match

---

## Test Case 4: Less-Than Rule (pomeranians)
**Objective**: Verify pomeranians comparison uses < instead of ==

**Target**: pomeranians: 3

**Test Scenarios**:
| Sue's pomeranians value | Should Match? | Reason |
|------------------------|---------------|---------|
| 0 | Yes | 0 < 3 |
| 1 | Yes | 1 < 3 |
| 2 | Yes | 2 < 3 |
| 3 | No | 3 ≮ 3 (NOT less than) |
| 4 | No | 4 ≮ 3 |

**Validation**:
- Create test cases with only pomeranians compound
- Verify boundary case: pomeranians: 3 should NOT match
- Verify pomeranians: 0-2 should match

---

## Test Case 5: Less-Than Rule (goldfish)
**Objective**: Verify goldfish comparison uses < instead of ==

**Target**: goldfish: 5

**Test Scenarios**:
| Sue's goldfish value | Should Match? | Reason |
|---------------------|---------------|---------|
| 0 | Yes | 0 < 5 |
| 1 | Yes | 1 < 5 |
| 4 | Yes | 4 < 5 |
| 5 | No | 5 ≮ 5 (NOT less than) |
| 6 | No | 6 ≮ 5 |

**Validation**:
- Create test cases with only goldfish compound
- Verify boundary case: goldfish: 5 should NOT match
- Verify goldfish: 0-4 should match

---

## Test Case 6: Exact Match Rules
**Objective**: Verify exact match for children, samoyeds, akitas, vizslas, cars, perfumes

**Target Values**:
- children: 3
- samoyeds: 2
- akitas: 0
- vizslas: 0
- cars: 2
- perfumes: 1

**Test Scenarios**:
| Compound | Sue's Value | Should Match? |
|----------|-------------|---------------|
| children | 3 | Yes |
| children | 2 or 4 | No |
| samoyeds | 2 | Yes |
| samoyeds | 1 or 3 | No |
| akitas | 0 | Yes |
| akitas | 1 | No |
| vizslas | 0 | Yes |
| vizslas | 1 | No |
| cars | 2 | Yes |
| cars | 1 or 3 | No |
| perfumes | 1 | Yes |
| perfumes | 0 or 2 | No |

**Validation**:
- Test each compound individually
- Verify exact match required (no >, <)

---

## Test Case 7: Unlisted Compounds (Ignore)
**Objective**: Verify unlisted compounds don't disqualify a match

**Test Data Type**: Synthetic (create test case)

**Scenario**:
```
Sue X: cats: 8, perfumes: 1, cars: 2
```

This Sue lists 3 compounds:
- cats: 8 (matches: 8 > 7) ✓
- perfumes: 1 (matches: 1 == 1) ✓
- cars: 2 (matches: 2 == 2) ✓

This Sue does NOT list: children, samoyeds, pomeranians, akitas, vizslas, goldfish, trees
- All unlisted compounds should be ignored (not checked)

**Expected**: This Sue should match if all listed compounds pass

**Validation**:
- Create synthetic test case with matching function
- Pass only 3 compounds to matching function
- Verify match succeeds even though 7 compounds are unlisted

---

## Test Case 8: Multiple Compounds - All Must Match
**Objective**: Verify that ALL listed compounds must match

**Test Data Type**: Synthetic

**Scenario 1 (Should FAIL)**: Two matching, one not
```
Sue X: cats: 8, goldfish: 5, perfumes: 1
```
- cats: 8 > 7 ✓
- goldfish: 5 ≮ 5 ✗ (fails less-than rule - boundary case!)
- perfumes: 1 == 1 ✓

**Expected**: No match (goldfish fails)

**Scenario 2 (Should PASS)**: All three match
```
Sue Y: cats: 8, goldfish: 4, perfumes: 1
```
- cats: 8 > 7 ✓
- goldfish: 4 < 5 ✓
- perfumes: 1 == 1 ✓

**Expected**: Match!

**Scenario 3 (Should PASS)**: All three rule types together
```
Sue Z: children: 3, trees: 5, pomeranians: 1
```
- children: 3 == 3 ✓ (exact match rule)
- trees: 5 > 3 ✓ (greater-than rule)
- pomeranians: 1 < 3 ✓ (less-than rule)

**Expected**: Match!

---

## Test Case 9: Actual Input Validation
**Objective**: Find the correct Sue from the provided input

**Test Data Type**: Actual input (input.md with 500 Sues)

**Validation Steps**:
1. Run solution on actual input.md
2. Get Sue number result (should be between 1 and 500)
3. Manually verify that Sue:
   - All listed compounds match according to rules
   - No other Sue also matches (uniqueness)

**Manual Verification Procedure**:
1. Look up the Sue number in input.md
2. For each of her 3 compounds, check against target:
   - If compound is cats or trees: verify Sue's value > target value
   - If compound is pomeranians or goldfish: verify Sue's value < target value
   - Otherwise: verify Sue's value == target value
3. Spot-check 5-10 other Sues (especially those with similar values) to ensure they don't match

**Expected Output Format**: Single integer on one line (e.g., "213")

---

## Test Case 10: Negative Test Cases (Should NOT Match)
**Objective**: Verify rejection of non-matching Sues

**Test Data Type**: Synthetic

**Critical Negative Cases**:

| Test Sue | Compounds | Why Should NOT Match |
|----------|-----------|---------------------|
| Sue A | cats: 6 | 6 ≤ 7 (need >) |
| Sue B | cats: 7 | 7 = 7 (need >, not ==) |
| Sue C | trees: 2 | 2 ≤ 3 (need >) |
| Sue D | trees: 3 | 3 = 3 (need >, not ==) |
| Sue E | pomeranians: 3 | 3 = 3 (need <, not ==) |
| Sue F | pomeranians: 4 | 4 ≥ 3 (need <) |
| Sue G | goldfish: 5 | 5 = 5 (need <, not ==) |
| Sue H | goldfish: 6 | 6 ≥ 5 (need <) |
| Sue I | children: 4 | 4 ≠ 3 (need ==) |
| Sue J | perfumes: 0 | 0 ≠ 1 (need ==) |

**Validation**:
- Create test cases for each Sue above
- Verify matching function returns False for each
- These test the boundaries and exact-match failures

---

## Test Case 11: Boundary Value Summary
**Objective**: Test critical boundary values

| Compound | Boundary Value | Should Match? |
|----------|---------------|---------------|
| cats: 7 | Exactly at target | No (need >) |
| cats: 8 | Just above target | Yes |
| trees: 3 | Exactly at target | No (need >) |
| trees: 4 | Just above target | Yes |
| pomeranians: 3 | Exactly at target | No (need <) |
| pomeranians: 2 | Just below target | Yes |
| goldfish: 5 | Exactly at target | No (need <) |
| goldfish: 4 | Just below target | Yes |

**Validation**:
- These are the most likely error cases
- Ensure <= and >= are not used where < and > are required

---

## Edge Cases to Consider

### Edge Case 1: Sue with all exact-match compounds
```
Sue X: children: 3, samoyeds: 2, akitas: 0
```
All three use exact-match rules. Should match only if all three are exactly right.

### Edge Case 2: Sue with all range-based compounds
```
Sue Y: cats: 9, trees: 5, pomeranians: 1, goldfish: 2
```
Mix of > and < rules. Should match only if all ranges satisfied.

### Edge Case 3: First Sue (Sue 1)
Ensure iteration starts correctly at Sue 1.

### Edge Case 4: Last Sue (Sue 500)
Ensure all 500 Sues are checked.

---

## Testing Execution Plan

### Phase 1: Unit Testing (Matching Logic)
**Tool**: Create `test_solution.py` with test functions

1. **Test parsing** (Test Case 1):
   - Parse a few sample lines
   - Verify Sue numbers and compound dictionaries
   - Verify values are integers, not strings

2. **Test greater-than rules** (Test Cases 2-3):
   - cats: 6, 7, 8 (only 8 should match)
   - trees: 2, 3, 4 (only 4 should match)

3. **Test less-than rules** (Test Cases 4-5):
   - pomeranians: 2, 3, 4 (only 2 should match)
   - goldfish: 4, 5, 6 (only 4 should match)

4. **Test exact-match rules** (Test Case 6):
   - children: 2, 3, 4 (only 3 should match)
   - perfumes: 0, 1, 2 (only 1 should match)

5. **Test unlisted compounds** (Test Case 7):
   - Sue with only 3 matching compounds
   - Verify 7 unlisted compounds don't disqualify

6. **Test multiple compounds** (Test Case 8):
   - All three rule types together
   - One failing compound disqualifies

7. **Test negative cases** (Test Case 10):
   - Boundary failures (cats: 7, goldfish: 5, etc.)
   - Verify all return False

### Phase 2: Integration Testing
**Tool**: Run `python solution.py` on actual input

1. Parse full input.md file (500 Sues)
2. Run matching algorithm
3. Verify output is a single integer between 1 and 500
4. Time execution (should be near-instantaneous)

### Phase 3: Manual Verification
**Tool**: Manual inspection

1. Look up the result Sue in input.md
2. Manually verify her 3 compounds match according to rules
3. Spot-check 5-10 other Sues to ensure they don't match:
   - Sues with similar values
   - Sues just before and after the result
   - Random sampling

### Phase 4: Cross-Reference with Problem Requirements
**Tool**: Checklist

- [ ] Verify all Part 2 rules are implemented (not Part 1 rules)
- [ ] Confirm > is used for cats and trees
- [ ] Confirm < is used for pomeranians and goldfish
- [ ] Confirm == is used for all others
- [ ] Confirm unlisted compounds are ignored
- [ ] Verify output format matches expected (single integer)

---

## Expected Output Format
```
<Sue_Number>
```
A single integer between 1 and 500.

**Example**: If Sue 213 is the match, output should be:
```
213
```

(Note: The actual expected answer is unknown until the solution runs, but the format should match the above.)

---

## Success Criteria
✓ Solution parses all 500 Sues correctly (verified by spot-checking parsed data)
✓ Matching logic correctly implements all three rule types (verified by unit tests)
✓ Boundary values handled correctly (cats: 7 fails, cats: 8 passes, etc.)
✓ Unlisted compounds are properly ignored (verified by test case)
✓ Exactly one Sue is identified as matching
✓ Manual verification confirms the Sue's compounds match target values
✓ Output is a single integer between 1 and 500
✓ Execution completes in reasonable time (< 1 second)
