# Test Plan: Electromagnetic Moat Bridge Builder - Part 2

## Testing Strategy

Since this is a scripting problem (not production code), focus testing on:
1. Correctness of the algorithm with known examples
2. Edge cases specific to the problem constraints
3. Verification that we're optimizing for length-then-strength correctly
4. Validation against actual input

## Test Cases

### Test 1: Example from Problem Statement (Primary Validation)

**Input:**
```
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10
```

**Expected Behavior:**
- Multiple bridges can be built
- Two longest bridges both have length 4:
  - `0/2--2/2--2/3--3/4`: strength = 18
  - `0/2--2/2--2/3--3/5`: strength = 19
- Should return **19** (strongest among longest)

**Verification:**
- Run solution with this input
- Assert output == 19
- This validates both length prioritization and strength tiebreaking

### Test 2: Simple Linear Chain

**Input:**
```
0/1
1/2
2/3
3/4
```

**Expected Behavior:**
- Only one possible bridge: `0/1--1/2--2/3--3/4`
- Length = 4
- Strength = (0+1) + (1+2) + (2+3) + (3+4) = 18

**Verification:**
- Output should be 18
- Tests basic chain building

### Test 3: Multiple Paths, Different Lengths

**Input:**
```
0/5
0/10
10/20
```

**Expected Behavior:**
- Bridge 1: `0/5` (length=1, strength=5)
- Bridge 2: `0/10--10/20` (length=2, strength=40)
- Should return **40** (longer bridge wins even though per-component it's not "strongest")

**Verification:**
- Output should be 40
- Tests that length is prioritized over raw strength

### Test 4: Same Length, Different Strengths

**Input:**
```
0/1
1/2
0/5
5/10
```

**Expected Behavior:**
- Bridge 1: `0/1--1/2` (length=2, strength=6)
- Bridge 2: `0/5--5/10` (length=2, strength=20)
- Should return **20** (same length, stronger wins)

**Verification:**
- Output should be 20
- Tests strength-based tiebreaking

### Test 5: Single Component Bridge

**Input:**
```
0/7
```

**Expected Behavior:**
- Only bridge: `0/7`
- Length = 1
- Strength = 7

**Verification:**
- Output should be 7
- Tests minimal valid bridge

### Test 6: Multiple Starting Components

**Input:**
```
0/3
0/5
3/7
5/9
```

**Expected Behavior:**
- Bridge 1: `0/3--3/7` (length=2, strength=20)
- Bridge 2: `0/5--5/9` (length=2, strength=24)
- Should return **24**

**Verification:**
- Output should be 24
- Tests multiple valid starting points with same length

### Test 7: Component with Same Ports on Both Ends

**Input:**
```
0/5
5/5
5/10
```

**Expected Behavior:**
- Can build: `0/5--5/5--5/10`
- Length = 3
- Strength = (0+5) + (5+5) + (5+10) = 30

**Verification:**
- Output should be 30
- Tests components where both ports have same value (already handled correctly by Part 1's build_port_index)

### Test 8: No Path Beyond Starting Component

**Input:**
```
0/7
1/2
2/3
```

**Expected Behavior:**
- Can only use `0/7` (nothing connects to 7)
- Length = 1
- Strength = 7

**Verification:**
- Output should be 7
- Tests dead-end detection

### Test 10: No Valid Starting Component (Optional Edge Case)

**Input:**
```
1/2
3/4
5/6
```

**Expected Behavior:**
- No component has port 0, so no bridge can be built
- Should return 0 (representing empty bridge)

**Verification:**
- Output should be 0
- Tests handling of impossible scenarios
- Note: Problem likely guarantees at least one component with port 0, so this is low priority

### Test 9: Actual Input Validation

**Input:** Use `input.md` (54 components)

**Expected Behavior:**
- Should complete in reasonable time (< 10 seconds)
- Result should be a positive integer
- May be different from Part 1 answer (1656) - could be higher or lower
- Part 2 optimizes for length first, so the strongest bridge (Part 1) and longest bridge (Part 2) may have different strengths

**Verification:**
- Run on actual input
- Time execution to ensure efficiency
- Check that result is reasonable (positive, not absurdly large)
- Manually verify a few bridge possibilities if answer seems suspicious

## Comparison with Part 1

### Sanity Check
- Run both Part 1 and Part 2 solutions on the same input
- Part 1 answer: 1656 (strongest bridge regardless of length)
- Part 2 answer: May differ from 1656
- Part 2 optimizes for maximum length first, then maximum strength among those longest bridges
- If the longest bridge happens to also be the strongest, answers will match
- Otherwise, Part 2 could be lower (longest bridge is weaker) or higher (longest bridges are stronger than the absolute strongest bridge)
- This is expected behavior based on different optimization criteria

## Edge Case Considerations

### 1. Component Reuse Prevention
- **Test**: Verify that `used` set properly prevents components from being used twice
- **Method**: Add debug logging to track which components are added to bridges
- **Expected**: Each component index should appear at most once per bridge path

### 2. Bidirectional Port Matching
- **Test**: Component `3/7` should match when looking for port 3 OR port 7
- **Method**: Use test case with asymmetric components
- **Expected**: Correct next_port calculation in both directions

### 3. Empty Input
- **Input**: Empty file or no valid components
- **Expected**: Should handle gracefully (likely return 0 or error)
- **Not critical**: Problem guarantees valid input

### 4. Backtracking Correctness
- **Test**: Ensure `used.remove()` is called after each recursive branch
- **Method**: Code review + verify test results
- **Expected**: Different branches explore different component combinations

## Testing Execution Plan

### Phase 1: Unit Testing (Manual)
1. Create test input files for Tests 1-8
2. Run solution against each test
3. Verify output matches expected value
4. Document any failures

### Phase 2: Example Validation
1. Run Test 1 (problem example) first
2. If it passes, high confidence in correctness
3. If it fails, debug before proceeding

### Phase 3: Actual Input
1. Run on `input.md`
2. Verify reasonable execution time
3. Check output format (single integer)

### Phase 4: Cross-Validation
1. Compare with Part 1 answer (should differ)
2. Manually trace one longest bridge to verify
3. Optional: Add debug output to show longest bridge composition

## Debug Output (Optional)

For validation, consider adding optional debug output to show final result:
```python
def solve(components):
    # ... existing code ...
    length, strength = find_longest_strongest(...)
    if DEBUG:
        print(f"Longest bridge: length={length}, strength={strength}")
    return strength
```

This helps verify:
- That longest bridges are actually being found
- The strength calculation is correct
- The comparison logic works properly

Note: To track the actual component path would require modifying the algorithm to pass and return a path list, which adds complexity without much benefit for this problem.

## Success Criteria

The solution passes testing if:
1. ✓ Example from problem statement returns 19
2. ✓ All manual test cases return expected values
3. ✓ Actual input runs without errors in < 10 seconds
4. ✓ Output is a reasonable positive integer
5. ✓ Code correctly prioritizes length over strength
