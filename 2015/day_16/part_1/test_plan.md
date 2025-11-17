# Test Plan: Aunt Sue Identification

## Testing Strategy

The goal is to verify that our solution correctly identifies the matching Aunt Sue by comparing remembered characteristics against the MFCSAM target signature. Testing will focus on correctness of parsing, matching logic, and handling edge cases.

**Testing Approach:** We will use a combination of:
1. Manual unit tests (simple function calls with assertions)
2. Test data files for integration testing
3. Automated verification of the final answer

## Test Categories

### 1. Unit Tests - Parsing Function

**Test 1.1: Parse Valid Line**
```python
Input: "Sue 1: goldfish: 9, cars: 0, samoyeds: 9"
Expected Output: (1, {'goldfish': 9, 'cars': 0, 'samoyeds': 9})
Purpose: Verify basic parsing works correctly
```

**Test 1.2: Parse Different Sue Numbers**
```python
Input: "Sue 213: akitas: 0, perfumes: 1, vizslas: 0"
Expected Output: (213, {'akitas': 0, 'perfumes': 1, 'vizslas': 0})
Purpose: Verify parsing works for different Sue IDs
```

**Test 1.3: Parse Different Compound Names**
```python
Input: "Sue 50: children: 3, cats: 7, samoyeds: 2"
Expected Output: (50, {'children': 3, 'cats': 7, 'samoyeds': 2})
Purpose: Verify all compound types can be parsed
```

**Test 1.4: Parse With Extra Whitespace**
```python
Input: "Sue 10:   trees:  2,  children: 10,   samoyeds: 10  "
Expected Output: (10, {'trees': 2, 'children': 10, 'samoyeds': 10})
Purpose: Verify whitespace handling
```

**Test 1.5: Parse Empty or Invalid Line**
```python
Input: ""
Expected Output: None or skip
Purpose: Verify robustness against empty lines
```

### 2. Unit Tests - Matching Function

**Test 2.1: Perfect Match (All 3 Characteristics)**
```python
Aunt characteristics: {'akitas': 0, 'vizslas': 0, 'perfumes': 1}
Target signature: {'akitas': 0, 'vizslas': 0, 'perfumes': 1, ...}
Expected: True
Purpose: Verify matching when all characteristics align with target
```

**Test 2.2: Partial Match (Some Correct, Some Incorrect)**
```python
Aunt characteristics: {'goldfish': 9, 'cars': 0, 'samoyeds': 9}
Target signature: {'goldfish': 5, 'cars': 2, 'samoyeds': 2, ...}
Expected: False
Purpose: Verify mismatch detection when any characteristic differs
```

**Test 2.3: Single Mismatch**
```python
Aunt characteristics: {'akitas': 0, 'vizslas': 0, 'perfumes': 5}
Target signature: {'akitas': 0, 'vizslas': 0, 'perfumes': 1, ...}
Expected: False
Purpose: Verify that even one mismatch fails the match
```

**Test 2.4: Match With Unknown Characteristics Ignored**
```python
Aunt characteristics: {'cars': 2, 'perfumes': 1, 'goldfish': 5}
Target signature: {all 10 compounds including the above with correct values}
Expected: True
Purpose: Verify that only remembered characteristics are checked
```

**Test 2.5: All Remembered Characteristics Match Target**
```python
Aunt characteristics: {'children': 3, 'cats': 7, 'samoyeds': 2}
Target signature: {'children': 3, 'cats': 7, 'samoyeds': 2, ...}
Expected: True
Purpose: Verify correct matching logic
```

### 3. Integration Tests - Full Solution

**Test 3.1: Run on Sample Data**
Create a test file `test_input.txt` with 5 Sues where Sue 3 matches:
```
Sue 1: goldfish: 9, cars: 0, samoyeds: 9
Sue 2: perfumes: 5, trees: 8, goldfish: 8
Sue 3: children: 3, cats: 7, samoyeds: 2
Sue 4: goldfish: 10, akitas: 2, perfumes: 9
Sue 5: cars: 5, perfumes: 6, akitas: 9
```

**How to run:**
```python
# Modify main() to accept filename parameter
def main(filename='input.md'):
    # ... existing code ...
    with open(filename, 'r') as f:
        # ... rest of parsing ...

# Then test with:
if __name__ == "__main__":
    import sys
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'
    main(filename)
```

**Command:** `python solution.py test_input.txt`
**Expected Output:** Sue 3
**Purpose:** Verify end-to-end functionality on small dataset

**Test 3.2: Run on Actual Input**
**Command:** `python solution.py input.md`
**Expected Output:** A single Sue number (between 1-500)
**Purpose:** Find the actual answer for the problem

**Test 3.3: Automated Verification of Result**
Add this function to automatically verify the answer:
```python
def verify_uniqueness(aunts, target):
    """
    Verify exactly one Sue matches the target.
    Returns (matching_sue_id, other_matches_list)
    """
    matches = []
    for sue_id, characteristics in aunts.items():
        if matches_target(characteristics, target):
            matches.append(sue_id)

    if len(matches) == 0:
        print("# WARNING: No Sue matches!", file=sys.stderr)
        return None, []
    elif len(matches) == 1:
        print(f"# SUCCESS: Exactly one Sue matches: {matches[0]}", file=sys.stderr)
        return matches[0], []
    else:
        print(f"# WARNING: Multiple Sues match: {matches}", file=sys.stderr)
        return matches[0], matches[1:]
```

Use this in main() before verification:
```python
# 4. Find matching Sue and verify uniqueness
result, other_matches = verify_uniqueness(aunts, target)

if other_matches:
    print(f"# ERROR: Multiple matches found: {[result] + other_matches}", file=sys.stderr)
    sys.exit(1)
```
**Purpose:** Automatic verification that exactly one Sue matches

### 4. Edge Case Tests

**Test 4.1: No Matching Sue**
Create test data where no Sue matches all characteristics
```
Sue 1: goldfish: 9, cars: 0, samoyeds: 9
Sue 2: perfumes: 5, trees: 8, goldfish: 8
```
Expected Output: None or error message
Purpose: Verify handling when no match exists

**Test 4.2: Verify Uniqueness on Full Input**
After running on actual input, verify no other Sues match:
```python
# This is handled by verify_uniqueness() function in Test 3.3
# It will scan all 500 Sues and confirm only one matches
```
Expected: Exactly 1 Sue matches (no duplicates)
Purpose: Verify solution uniqueness

**Test 4.3: First Sue Matches**
```
Sue 1: children: 3, cats: 7, samoyeds: 2
Sue 2: perfumes: 5, trees: 8, goldfish: 8
```
Expected Output: 1
Purpose: Verify no off-by-one errors at boundary

**Test 4.4: Last Sue Matches**
```
Sue 499: goldfish: 9, cars: 0, samoyeds: 9
Sue 500: children: 3, cats: 7, samoyeds: 2
```
Expected Output: 500
Purpose: Verify complete iteration through all aunts

**Test 4.5: Sue With Zero Values**
```
Sue 40: vizslas: 0, cats: 7, akitas: 0
Target: {vizslas: 0, cats: 7, akitas: 0, ...}
```
Expected: True match if all align
Purpose: Verify zero values are handled correctly (not treated as missing)

### 5. Validation Tests

Add this validation function to the solution:
```python
def validate_data(aunts, target):
    """
    Validate parsed data for integrity and correctness.
    Prints diagnostics and returns True if valid.
    """
    print(f"# Validation Results:", file=sys.stderr)

    # Test 5.1: Verify Target Signature Completeness
    expected_compounds = {'children', 'cats', 'samoyeds', 'pomeranians', 'akitas',
                         'vizslas', 'goldfish', 'trees', 'cars', 'perfumes'}
    if set(target.keys()) != expected_compounds:
        print(f"#   ERROR: Target missing compounds: {expected_compounds - set(target.keys())}",
              file=sys.stderr)
        return False
    print(f"#   ✓ Target has all 10 compounds", file=sys.stderr)

    # Test 5.2: Verify Input Parsing Completeness
    if len(aunts) != 500:
        print(f"#   WARNING: Expected 500 Sues, got {len(aunts)}", file=sys.stderr)
    else:
        print(f"#   ✓ Parsed exactly 500 Sues", file=sys.stderr)

    # Test 5.3: Verify Each Sue Has Exactly 3 Characteristics
    invalid_sues = [sid for sid, chars in aunts.items() if len(chars) != 3]
    if invalid_sues:
        print(f"#   ERROR: Sues with != 3 characteristics: {invalid_sues[:5]}...",
              file=sys.stderr)
        return False
    print(f"#   ✓ All Sues have exactly 3 characteristics", file=sys.stderr)

    # Test 5.4: Verify Compound Name Consistency
    all_compounds = set()
    for chars in aunts.values():
        all_compounds.update(chars.keys())
    invalid_compounds = all_compounds - expected_compounds
    if invalid_compounds:
        print(f"#   ERROR: Unknown compounds found: {invalid_compounds}", file=sys.stderr)
        return False
    print(f"#   ✓ All compound names are valid", file=sys.stderr)

    # Test 5.5: Verify Value Ranges
    invalid_values = []
    for sue_id, chars in aunts.items():
        for compound, count in chars.items():
            if not isinstance(count, int) or count < 0:
                invalid_values.append((sue_id, compound, count))
    if invalid_values:
        print(f"#   ERROR: Invalid values found: {invalid_values[:5]}...", file=sys.stderr)
        return False
    print(f"#   ✓ All values are non-negative integers", file=sys.stderr)

    return True
```

Call this in main() after parsing:
```python
# 3. Validate parsed data
if not validate_data(aunts, target):
    print("ERROR: Data validation failed!", file=sys.stderr)
    sys.exit(1)
```
**Purpose:** Automated data integrity checks

## Testing Execution Plan

### Phase 1: Unit Testing (Development)
Write a simple test script to verify individual functions:

```python
# test_units.py
from solution import parse_line, matches_target

def test_parsing():
    print("Testing parse_line...")

    # Test 1.1
    sue_id, chars = parse_line("Sue 1: goldfish: 9, cars: 0, samoyeds: 9")
    assert sue_id == 1
    assert chars == {'goldfish': 9, 'cars': 0, 'samoyeds': 9}
    print("  ✓ Test 1.1 passed")

    # Test 1.2
    sue_id, chars = parse_line("Sue 213: akitas: 0, perfumes: 1, vizslas: 0")
    assert sue_id == 213
    assert chars == {'akitas': 0, 'perfumes': 1, 'vizslas': 0}
    print("  ✓ Test 1.2 passed")

    # Test 1.5
    sue_id, chars = parse_line("")
    assert sue_id is None
    assert chars == {}
    print("  ✓ Test 1.5 passed")

    print("All parsing tests passed!\n")

def test_matching():
    print("Testing matches_target...")
    target = {'akitas': 0, 'vizslas': 0, 'perfumes': 1, 'other': 99}

    # Test 2.1
    assert matches_target({'akitas': 0, 'vizslas': 0, 'perfumes': 1}, target) == True
    print("  ✓ Test 2.1 passed")

    # Test 2.2
    assert matches_target({'goldfish': 9, 'cars': 0, 'samoyeds': 9},
                         {'goldfish': 5, 'cars': 2, 'samoyeds': 2}) == False
    print("  ✓ Test 2.2 passed")

    # Test 2.3
    assert matches_target({'akitas': 0, 'vizslas': 0, 'perfumes': 5}, target) == False
    print("  ✓ Test 2.3 passed")

    print("All matching tests passed!\n")

if __name__ == "__main__":
    test_parsing()
    test_matching()
    print("✓ All unit tests passed!")
```

**Run:** `python test_units.py`

### Phase 2: Integration Testing

1. **Create test data file** `test_input.txt` with sample data from Test 3.1
2. **Run on sample data:** `python solution.py test_input.txt`
   - Expected output: Sue 3
3. **If successful, run on full input:** `python solution.py input.md`
4. **Automatic verification** will run via verify_uniqueness() and verify_result()

### Phase 3: Edge Case Validation

Create additional test files for edge cases:

**test_no_match.txt:**
```
Sue 1: goldfish: 9, cars: 0, samoyeds: 9
Sue 2: perfumes: 5, trees: 8, goldfish: 8
```
Run: `python solution.py test_no_match.txt`
Expected: Error message "No matching Sue found"

**test_first_match.txt:**
```
Sue 1: children: 3, cats: 7, samoyeds: 2
Sue 2: goldfish: 9, cars: 0, samoyeds: 9
```
Run: `python solution.py test_first_match.txt`
Expected: Sue 1

### Phase 4: Data Validation

Data validation runs automatically when calling `validate_data()` in main().
Check that all validation tests pass when running on actual input.

## Success Criteria

The solution is correct if:
1. ✓ All unit tests pass (`python test_units.py` succeeds)
2. ✓ Sample data test produces correct Sue number (`python solution.py test_input.txt` returns 3)
3. ✓ Full input test produces a single Sue number (`python solution.py input.md` returns a number)
4. ✓ Automatic verification confirms all 3 characteristics match (verify_result() succeeds)
5. ✓ Uniqueness check confirms no other Sue matches (verify_uniqueness() finds exactly 1)
6. ✓ Data validation passes (validate_data() returns True)
7. ✓ Edge cases are handled appropriately (error messages for no match, file not found)
8. ✓ Execution completes in reasonable time (< 1 second)

**Quick verification checklist:**
```bash
# Run all tests in sequence
python test_units.py                    # Should pass all tests
python solution.py test_input.txt       # Should output: 3
python solution.py input.md             # Should output: a number 1-500
```

## Manual Verification Process (Optional)

The solution includes automatic verification, but you can manually verify if desired:

1. **Locate the Sue in input file**
   - `grep "Sue 213:" input.md` (replace 213 with actual answer)
   - Extract the 3 characteristics

2. **Compare Against Target**
   - For each of the 3 characteristics
   - Look up the compound in target signature
   - Verify the count matches exactly

3. **Check stderr output**
   - The solution automatically prints verification details to stderr
   - Look for the "# Verification:" section showing each characteristic

Example verification output:
```
# Parsed 500 Sues
# Validation Results:
#   ✓ Target has all 10 compounds
#   ✓ Parsed exactly 500 Sues
#   ✓ All Sues have exactly 3 characteristics
#   ✓ All compound names are valid
#   ✓ All values are non-negative integers
# SUCCESS: Exactly one Sue matches: 213
# Found Sue 213
# Verification:
#   akitas: 0 (target: 0) ✓
#   perfumes: 1 (target: 1) ✓
#   vizslas: 0 (target: 0) ✓
# All characteristics match!
213
```

## Known Constraints and Assumptions

1. **Assumption:** Exactly one Sue will match (problem guarantee)
2. **Assumption:** All input lines follow the specified format
3. **Assumption:** Compound names are lowercase and consistent
4. **Assumption:** Sue numbers are sequential 1-500
5. **Constraint:** Only remembered characteristics matter (unknown are ignored)
6. **Constraint:** Must match ALL remembered characteristics (not just majority)

## Debugging Checklist

If the solution fails:
- [ ] Run unit tests: `python test_units.py` to isolate the issue
- [ ] Check parsing: Look at stderr output showing "Parsed N Sues"
- [ ] Check validation: Look at stderr "Validation Results" section
- [ ] Check target: Verify all 10 compounds defined correctly (validation checks this)
- [ ] Check matching logic: Run on test_input.txt with known answer (Sue 3)
- [ ] Check compound name spelling and case sensitivity
- [ ] Check for off-by-one errors in Sue numbering
- [ ] Verify all 500 Sues were parsed (validation checks this)
- [ ] Check for whitespace or formatting issues in comparison
- [ ] Add debug prints in parse_line() to see what's being parsed

**Debug mode:** Add verbose output by setting a flag:
```python
DEBUG = True  # Set at top of file

if DEBUG:
    print(f"# Parsed Sue {sue_id}: {characteristics}", file=sys.stderr)
```
