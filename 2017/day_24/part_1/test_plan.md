# Test Plan: Electromagnetic Moat Bridge Builder

## Testing Strategy Overview

We need to verify:
1. **Correctness**: Solution finds the actual maximum strength
2. **Edge case handling**: Handles unusual inputs properly
3. **Algorithm completeness**: Explores all valid paths
4. **Performance**: Runs in reasonable time for given input

## Test Categories

### 1. Example Test Case (from Problem Statement)

**Purpose:** Verify basic correctness against known example

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

**Expected Output:** `31`

**Validation:**
- Strongest bridge is: `0/1`--`10/1`--`9/10`
- Strength calculation: (0+1) + (1+10) + (10+9) = 1 + 11 + 19 = 31

**Test Method:**
1. Create a test file with this input
2. Run solution
3. Assert output equals 31

**Success Criteria:** Output matches expected value exactly

---

### 2. Simple Linear Chain Test

**Purpose:** Test basic chaining without branching

**Input:**
```
0/1
1/2
2/3
3/4
```

**Expected Output:** `20`

**Validation:**
- Only one possible bridge: `0/1`--`1/2`--`2/3`--`3/4`
- Strength: (0+1) + (1+2) + (2+3) + (3+4) = 1 + 3 + 5 + 7 = 20

**Success Criteria:** Correctly builds the full chain

---

### 3. Multiple Starting Options Test

**Purpose:** Verify algorithm chooses best starting component

**Input:**
```
0/1
0/10
10/5
```

**Expected Output:** `25`

**Validation:**
- Option 1: `0/1` alone = 1 (dead end)
- Option 2: `0/10`--`10/5` = 10 + 15 = 25 (best)
- Must choose option 2

**Success Criteria:** Selects the higher-strength path

---

### 4. Branching Paths Test

**Purpose:** Verify algorithm explores all branches and finds maximum

**Input:**
```
0/2
2/3
2/5
3/1
5/10
```

**Expected Output:** `24`

**Validation:**
- Must start with `0/2` (strength = 0+2 = 2, port 2 free)
- Then two possible branches from port 2:
  - **Branch A**: `0/2`--`2/3`--`3/1` = (0+2) + (2+3) + (3+1) = 2 + 5 + 4 = 11
  - **Branch B**: `0/2`--`2/5`--`5/10` = (0+2) + (2+5) + (5+10) = 2 + 7 + 15 = 24 (best)
- Algorithm should explore both branches and return the maximum (24)

**Success Criteria:** Explores both branches and returns maximum (24)

---

### 5. Component with Same Ports Test

**Purpose:** Handle components like 5/5 correctly

**Input:**
```
0/5
5/5
5/3
```

**Expected Output:** `23`

**Validation:**
- Bridge: `0/5`--`5/5`--`5/3`
- Strength: (0+5) + (5+5) + (5+3) = 5 + 10 + 8 = 23
- The 5/5 component can connect on either port (both are 5)

**Success Criteria:** Correctly handles bidirectional component with same values

---

### 6. Single Component Test

**Purpose:** Test minimal valid bridge

**Input:**
```
0/7
```

**Expected Output:** `7`

**Validation:**
- Only one component, starts with 0
- Strength: 0 + 7 = 7

**Success Criteria:** Returns strength of single component

---

### 7. No Valid Bridge Test

**Purpose:** Handle case where no bridge can be built

**Input:**
```
5/7
3/4
10/11
```

**Expected Output:** `0`

**Validation:**
- No component has port 0
- Cannot build any bridge
- Should return 0

**Success Criteria:** Returns 0 when no valid bridge exists

---

### 8. All Components Have Port 0 Test

**Purpose:** Test when multiple starting options available

**Input:**
```
0/5
0/3
0/10
```

**Expected Output:** `10`

**Validation:**
- Three separate bridges possible (no chaining):
  - `0/5` = 5
  - `0/3` = 3
  - `0/10` = 10 (best)

**Success Criteria:** Returns strength of strongest single component

---

### 9. Circular Potential Test

**Purpose:** Ensure algorithm doesn't get confused by components that could form cycles

**Input:**
```
0/1
1/2
2/1
1/3
```

**Expected Output:** `11`

**Validation:**
- Start with `0/1` (strength = 0+1 = 1, port 1 free)
- From port 1, can choose `1/2` or `1/3`:
  - **Path A**: `0/1`--`1/2` (strength = 1 + 3 = 4, port 2 free)
    - From port 2, use `2/1` (strength = 4 + 3 = 7, port 1 free)
    - From port 1, use `1/3` (strength = 7 + 4 = 11, port 3 free)
    - No more components, return 11
  - **Path B**: `0/1`--`1/3` (strength = 1 + 4 = 5, port 3 free)
    - No component has port 3, return 5
- Maximum is 11

**Success Criteria:** Handles components that could create cycles correctly by using each once

---

### 10. Empty Input Test

**Purpose:** Handle edge case of empty input file

**Input:**
```
(empty file or only whitespace)
```

**Expected Output:** `0`

**Validation:**
- No components means no bridge can be built
- Should return 0

**Success Criteria:** Returns 0 for empty input

---

### 11. Component with 0/0 Test

**Purpose:** Test unusual edge case of component with both ports being 0

**Input:**
```
0/0
0/5
5/3
```

**Expected Output:** `8`

**Validation:**
- **Path 1**: `0/0` alone = 0+0 = 0
- **Path 2**: `0/5`--`5/3` = (0+5) + (5+3) = 5 + 8 = 13... wait, that's wrong
- Let me recalculate:
  - `0/5`: strength = 0+5 = 5, port 5 free
  - `5/3`: strength = 5+3 = 8, port 3 free
  - Total: 5 + 8 = 13
- **Path 3**: `0/0`--`0/5`--`5/3`
  - `0/0`: strength = 0, port 0 free
  - `0/5`: strength = 0 + 5 = 5, port 5 free
  - `5/3`: strength = 5 + 8 = 13, port 3 free
  - Total: 0 + 5 + 8 = 13

**Expected Output:** `13`

**Success Criteria:** Correctly handles 0/0 component (both paths yield 13)

---

### 12. Real Input Validation

**Purpose:** Verify solution works on actual puzzle input

**Test Method:**
1. Run solution on provided `input.md`
2. Verify it completes in reasonable time (< 10 seconds)
3. Check output is a positive integer
4. Manually trace a few promising paths to verify algorithm is working

**Success Criteria:**
- Completes execution
- Returns an integer > 0
- Runtime < 10 seconds

---

## Manual Verification Approach

For the real input, manually verify the algorithm logic:

1. **Identify components with port 0:**
   - Search the input file for components containing "/0" or "0/"
   - These are the only valid starting points

2. **Spot-check a promising path:**
   - Choose one starting component (e.g., if `50/0` exists: strength = 50, port 50 free)
   - Look for components with the free port (e.g., port 50)
   - Continue tracing one branch to verify algorithm explores correctly
   - This demonstrates the backtracking mechanism

3. **Verify backtracking works:**
   - Optionally add debug prints to show when components are added/removed from used set
   - Ensure used set is properly maintained (component removed after recursive call)
   - Check that algorithm doesn't reuse components

---

## Testing Edge Cases in Code

### Edge Case Checklist:

- [x] Empty input file (Test 10)
- [x] Input with only whitespace (Test 10)
- [x] Single component with port 0 (Test 6)
- [x] Single component without port 0 (Test 7)
- [x] Multiple components, none with port 0 (Test 7)
- [x] All components have port 0 (Test 8)
- [x] Component with same ports (Test 5 - handles 5/5)
- [x] Component 0/0 (Test 11)
- [x] Maximum possible chain (Test 2 - uses all components)
- [x] Components with large values (Test 12 - real input)
- [x] Branching paths (Test 4)
- [x] Circular potential (Test 9)

---

## Correctness Verification Strategy

### Method 1: Small Test Cases with Known Answers
- Use examples from problem statement
- Create custom small inputs where answer can be computed by hand
- Verify output matches expected

### Method 2: Property-Based Checks
- Output should always be >= 0
- Output should be >= strength of any single component with port 0
- If we have component `0/X`, output should be >= X

### Method 3: Algorithm Trace
For a small input, trace the recursion:
```
Input: 0/2, 2/3

Trace:
- Start: port=0, used={}, strength=0
  - Try 0/2: port=2, used={0}, strength=2
    - Try 2/3: port=3, used={0,1}, strength=7
      - No more matches, return 7
    - Backtrack: used={0}, return 7
  - Backtrack: used={}, return 7
- Final: 7
```

Expected: (0+2) + (2+3) = 7 ✓

---

## Performance Testing

### Expected Performance:
- Input size: ~54 components
- Worst case: O(n! * n) but heavily pruned
- Expected runtime: < 5 seconds

### Performance Test:
1. Measure execution time
2. Should complete well under 10 seconds
3. If slow, consider optimizations from implementation plan

### Profiling Points:
- Count number of recursive calls (add counter)
- Measure time spent in recursion
- Verify pruning is working (not exploring impossible branches)

---

## Test Execution Plan

### Phase 1: Basic Correctness Tests
1. **Test 1**: Example from problem statement (output = 31)
2. **Test 6**: Single component test (simplest case)
3. **Test 2**: Linear chain (basic chaining)

### Phase 2: Edge Case Tests
1. **Test 7**: No valid bridge (no port 0)
2. **Test 10**: Empty input
3. **Test 5**: Component with same ports (5/5)
4. **Test 11**: Component 0/0
5. **Test 8**: All components have port 0

### Phase 3: Complex Logic Tests
1. **Test 3**: Multiple starting options
2. **Test 4**: Branching paths (must explore all)
3. **Test 9**: Circular potential (backtracking verification)

### Phase 4: Real Input Validation
1. Run on real input (Test 12)
2. Verify completion in < 10 seconds
3. Check output is reasonable (positive integer)
4. Optionally spot-check a few paths manually

### Phase 5: Performance Verification
1. Measure execution time
2. Ensure runtime < 10 seconds (should be much faster with port_map optimization)
3. If needed, add instrumentation to count recursive calls

---

## Test Implementation Approach

Create a separate test file `test_solution.py`:

```python
def test_example_case():
    # Use example from problem
    components = [(0,2), (2,2), (2,3), (3,4), (3,5), (0,1), (10,1), (9,10)]
    result = solve(components)
    assert result == 31, f"Expected 31, got {result}"

def test_linear_chain():
    components = [(0,1), (1,2), (2,3), (3,4)]
    result = solve(components)
    assert result == 20, f"Expected 20, got {result}"

# ... more tests
```

Or simply run solution on various input files and check outputs manually.

---

## Success Criteria Summary

The solution is correct if:
1. ✓ Passes example test case (Test 1: output = 31)
2. ✓ Passes all edge case tests (Tests 2-11)
3. ✓ Completes real input in < 10 seconds (Test 12)
4. ✓ Returns a reasonable positive integer for real input
5. ✓ Algorithm logic can be traced and verified for small inputs
6. ✓ Handles all edge cases correctly (empty input, no port 0, 0/0 component, etc.)

## Test Case Summary Table

| Test | Description | Input Components | Expected Output | Key Validation |
|------|-------------|------------------|-----------------|----------------|
| 1 | Example case | 8 components | 31 | Known answer from problem |
| 2 | Linear chain | 4 components | 20 | Uses all components |
| 3 | Multiple starts | 3 components | 25 | Chooses best starting path |
| 4 | Branching paths | 5 components | 24 | Explores all branches |
| 5 | Same ports | 3 components | 23 | Handles 5/5 component |
| 6 | Single component | 1 component | 7 | Minimal valid bridge |
| 7 | No valid bridge | 3 components | 0 | No port 0 components |
| 8 | All port 0 | 3 components | 10 | Multiple isolated bridges |
| 9 | Circular potential | 4 components | 11 | Backtracking works correctly |
| 10 | Empty input | 0 components | 0 | Handles empty file |
| 11 | Component 0/0 | 3 components | 13 | Special case: both ports are 0 |
| 12 | Real input | ~54 components | TBD | Performance and correctness |
