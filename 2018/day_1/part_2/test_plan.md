# Test Plan: Chronal Calibration - Part 2

## Testing Objectives
1. Verify correct duplicate frequency detection
2. Validate proper looping through input list
3. Ensure starting frequency (0) is treated as "seen"
4. Confirm early termination when duplicate is found
5. Validate consistency with Part 1 (same input parsing)

## Test Categories

### 0. Validation Test (Part 1 Consistency)

#### Test 0.1: Verify Input Parsing Matches Part 1
**Purpose**: Confirm we're reading the same input as Part 1
**Method**: After parsing changes, verify `sum(changes) == 474`
**Expected**: Sum should match Part 1 answer
**Verification**:
```python
changes = parse_input('input.md')
assert sum(changes) == 474, "Input parsing doesn't match Part 1"
```

### 1. Example Tests (From Problem Statement)

#### Test 1.1: Basic Two-Cycle Example
**Input**: `+1, -2, +3, +1`
**Expected Output**: `2`
**Trace**:
- Start: freq=0, seen={0}
- +1: freq=1, seen={0,1}
- -2: freq=-1, seen={0,1,-1}
- +3: freq=2, seen={0,1,-1,2}
- +1: freq=3, seen={0,1,-1,2,3}
- [Cycle 2] +1: freq=4, seen={0,1,-1,2,3,4}
- [Cycle 2] -2: freq=2, **DUPLICATE FOUND** ✓

**Verification Method**: Create test file, run solver, compare output

#### Test 1.2: Early Duplicate (Second Change)
**Input**: `+1, -1`
**Expected Output**: `0`
**Trace**:
- Start: freq=0, seen={0}
- +1: freq=1, seen={0,1}
- -1: freq=0, **DUPLICATE FOUND** ✓

**Verification Method**: Returns to starting frequency

#### Test 1.3: Multi-Cycle Example 1
**Input**: `+3, +3, +4, -2, -4`
**Expected Output**: `10`
**Verification Method**: Trust problem statement (manual trace would be lengthy)

#### Test 1.4: Multi-Cycle Example 2
**Input**: `-6, +3, +8, +5, -6`
**Expected Output**: `5`
**Verification Method**: Trust problem statement

#### Test 1.5: Multi-Cycle Example 3
**Input**: `+7, +7, -2, -7, -4`
**Expected Output**: `14`
**Verification Method**: Trust problem statement

**Test Execution**: Use inline testing (no file I/O needed for small examples)
```python
def test_examples():
    # Test 1.1
    result = solve_with_list([1, -2, 3, 1])
    assert result == 2, f"Test 1.1 failed: expected 2, got {result}"

    # Test 1.2
    result = solve_with_list([1, -1])
    assert result == 0, f"Test 1.2 failed: expected 0, got {result}"

    # ... and so on
```

---

### 2. Edge Case Tests

#### Test 2.1: Return to Starting Frequency
**Input**: `+5, +3, -8`
**Expected**: Should eventually return to 0 and detect it as duplicate
**Purpose**: Confirm 0 is in `seen` set from the start
**Method**: Inline test with small list

#### Test 2.2: Duplicate in First Cycle
**Input**: `+1, -2, +3, +1, -3`
**Purpose**: Verify duplicate detection works in first pass through the list
**Method**: Inline test, verify result makes sense

---

### 3. Actual Input Test

#### Test 3.1: Run on Provided Input
**Input File**: `input.md` (983 frequency changes)
**Expected Behavior**:
- Completes within reasonable time (< 10 seconds)
- Returns a single integer
- Does not throw errors or infinite loop
- Input parsing matches Part 1: `sum(changes) == 474`

**Validation Method**:
- Run the solution with default filename
- Verify output is an integer
- **No ground truth available** - trust implementation if examples pass

**Performance Check**:
- Monitor execution time
- If takes > 30 seconds, add debug output to check cycle count

---

## Test Execution Strategy

### Phase 1: Validation (Quick Check)
1. Run Test 0.1: Verify `sum(changes) == 474`
2. **Gate**: Must pass to confirm same input as Part 1

### Phase 2: Example Tests (Must Pass)
1. Run Tests 1.1, 1.2 (with manual trace validation)
2. Run Tests 1.3, 1.4, 1.5 (trust problem statement for expected values)
3. **Gate**: All must pass before proceeding

### Phase 3: Edge Cases (Quick Validation)
1. Run Tests 2.1, 2.2
2. **Gate**: Should pass; if not, indicates algorithm bug

### Phase 4: Actual Input (Primary Goal)
1. Run Test 3.1 on actual input
2. Verify reasonable output and performance
3. **Gate**: Must complete successfully

---

## Test Implementation Approach

### Inline Testing (Recommended for Small Examples)
For script-style solution, use inline testing without file I/O:

```python
def solve_with_list(changes):
    """Helper for testing with inline lists"""
    from itertools import cycle
    seen = {0}
    frequency = 0
    for change in cycle(changes):
        frequency += change
        if frequency in seen:
            return frequency
        seen.add(frequency)

def run_tests():
    # Test examples inline
    assert solve_with_list([1, -2, 3, 1]) == 2
    assert solve_with_list([1, -1]) == 0
    assert solve_with_list([3, 3, 4, -2, -4]) == 10
    assert solve_with_list([-6, 3, 8, 5, -6]) == 5
    assert solve_with_list([7, 7, -2, -7, -4]) == 14
    print("✓ All example tests passed")
```

### File-Based Testing (For Actual Input)
Use the `filename` parameter for actual input:
```python
result = solve(filename='input.md')
print(f"Part 2 answer: {result}")
```

---

## Success Criteria
✅ Validation test passes: `sum(changes) == 474` (matches Part 1)
✅ All 5 provided examples produce correct output
✅ Edge case tests pass (Tests 2.1, 2.2)
✅ Solution completes on actual input within 10 seconds
✅ Output is a reasonable integer value
✅ No errors, exceptions, or infinite loops

## Failure Response
- If validation fails: Check input file parsing, compare with Part 1
- If examples fail: Debug algorithm logic, check `seen` set initialization
- If actual input times out: Add debug print to track cycle count
- If wrong answer: Verify `seen = {0}` at start, check duplicate detection condition
