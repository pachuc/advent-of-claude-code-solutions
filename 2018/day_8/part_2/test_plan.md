# Test Plan: Tree Node Value Calculator (Part 2)

## Testing Objectives
1. Verify correct value calculation for both node types (leaf and internal)
2. Validate proper handling of metadata as child indexes
3. Ensure edge cases are handled correctly
4. Confirm the solution works on the actual puzzle input

## Test Cases

### Test 1: Example from Problem Statement
**Purpose:** Verify basic correctness against known example

**Input:**
```
2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2
```

**Tree Structure:**
- Node A: 2 children, metadata [1, 1, 2]
- Node B: 0 children, metadata [10, 11, 12]
- Node C: 1 child, metadata [2]
- Node D: 0 children, metadata [99]

**Expected Calculation:**
- Node D value: 99 (leaf: sum metadata)
- Node B value: 10 + 11 + 12 = 33 (leaf: sum metadata)
- Node C value: 0 (metadata [2] references child 2, but C only has 1 child)
- Node A value: 33 + 33 + 0 = 66 (metadata [1,1,2] → child1 + child1 + child2)

**Expected Output:** 66

**Verification Method:**
- Create test file with this input
- Run solution and compare output
- Manually verify intermediate node values with debug output if needed

### Test 2: Single Leaf Node
**Purpose:** Test simplest case - root is a leaf

**Input:**
```
0 3 10 20 30
```

**Expected:** 60 (sum of metadata)

**Rationale:** Ensures leaf node value calculation works correctly

### Test 3: Single Internal Node with Children
**Purpose:** Test internal node with valid child references

**Input:**
```
2 2 0 1 5 0 1 10 1 2
```

**Structure:**
- Root: 2 children, metadata [1, 2]
- Child 1: 0 children, metadata [5]
- Child 2: 0 children, metadata [10]

**Expected:** 15 (child1=5, child2=10, metadata [1,2] → 5 + 10)

### Test 4: Metadata with Invalid Child References
**Purpose:** Test that invalid indexes are properly skipped

**Input:**
```
2 4 0 1 5 0 1 10 0 3 5 4
```

**Structure:**
- Root: 2 children, metadata [0, 3, 5, 4]
  - 0 → invalid (not 1-based)
  - 3 → invalid (only 2 children)
  - 5 → invalid (only 2 children)
  - 4 → invalid (only 2 children)
- Child 1: value 5
- Child 2: value 10

**Expected:** 0 (all metadata references are invalid)

**Rationale:** Ensures bounds checking on child indexes works

### Test 5: Duplicate Child References
**Purpose:** Test that same child can be counted multiple times

**Input:**
```
1 3 0 1 7 1 1 1
```

**Structure:**
- Root: 1 child, metadata [1, 1, 1]
- Child 1: value 7

**Expected:** 21 (7 + 7 + 7)

**Rationale:** Confirms that metadata can reference same child multiple times

### Test 6: Deep Nesting
**Purpose:** Test recursion with deeper tree

**Input:**
```
1 1 1 1 1 1 0 1 5 1 1 1
```

**Structure (4 levels deep):**
- Level 0 (Root): 1 child, metadata [1]
  - Level 1: 1 child, metadata [1]
    - Level 2: 1 child, metadata [1]
      - Level 3 (Leaf): 0 children, metadata [5]

**Value Calculation (bottom-up):**
- Level 3 (Leaf): value = 5 (sum of metadata)
- Level 2: metadata [1] → child 1 (value 5) = 5
- Level 1: metadata [1] → child 1 (value 5) = 5
- Level 0 (Root): metadata [1] → child 1 (value 5) = 5

**Expected:** 5 (each level passes through its only child's value)

**Rationale:** Verifies recursion works correctly with depth

### Test 7: Wide Tree
**Purpose:** Test node with many children

**Input:**
```
3 3 0 1 10 0 1 20 0 1 30 1 2 3
```

**Structure:**
- Root: 3 children, metadata [1, 2, 3]
- Child 1: value 10
- Child 2: value 20
- Child 3: value 30

**Expected:** 60 (10 + 20 + 30)

**Rationale:** Ensures handling of multiple children works

### Test 8: Node with Zero Metadata
**Purpose:** Test edge case of node with no metadata entries

**Input:**
```
1 0 0 1 5
```

**Structure:**
- Root: 1 child, 0 metadata entries []
- Child 1: 0 children, metadata [5], value = 5

**Expected:** 0 (no metadata to reference children)

**Rationale:** Verifies that nodes with 0 metadata return value of 0

**Alternative Test (Leaf with Zero Metadata):**
```
0 0
```
- Single leaf node with no metadata
- Expected: 0 (sum of empty list)

### Test 9: Actual Puzzle Input
**Purpose:** Verify solution on real input

**Input:** Contents of input.md (~19k integers)

**Expected:** Unknown (to be determined by running solution)

**Verification Method:**
1. Run the solution on input.md
2. Verify it completes without errors
3. Verify result is a reasonable integer
4. Verify all input data was consumed (no parsing errors)
5. Check execution time is reasonable (< 1 second)
   - Use `time` command or `time.time()` to measure execution duration
   - Log execution time for reference

**Additional Checks:**
- Compare with Part 1 answer (49180) - Part 2 answer should be different
- No exceptions raised during execution
- Output is a single integer value

## Edge Cases to Consider

### Edge Case 1: Zero in Metadata
- Metadata value of 0 should be skipped (not a valid 1-based index)
- Should not cause errors or crashes

### Edge Case 2: Large Metadata Values
- Metadata values much larger than child count
- Should be skipped gracefully

### Edge Case 3: All Children Are Leaves
- Internal node where all children are leaves
- Should properly sum child values based on metadata indexes

### Edge Case 4: Mix of Valid and Invalid Indexes
- Some metadata entries valid, some not
- Should sum only valid references

## Test Execution Strategy

### Phase 1: Unit Tests (Small Examples)
1. Run Tests 1-8 in order
2. For each test:
   - Create a temporary test input file
   - Run the solution
   - Compare actual vs expected output
   - Print PASS/FAIL with details

### Phase 2: Integration Test (Real Input)
1. Run Test 9 on actual puzzle input
2. Verify completion and correctness
3. Note the final answer
4. Record execution time

### Phase 3: Validation Checks
- Ensure no Python exceptions occurred
- Verify data was fully consumed (validation in code)
- Check performance is acceptable

## Success Criteria
- All small tests (1-8) produce expected outputs
- Puzzle input (test 9) completes without errors
- Solution runs in under 1 second
- Code properly handles all edge cases
- Final answer is a positive integer different from Part 1's answer (49180)

## Testing Implementation Approach

Create a simple test runner:
```python
def test_solution(input_data, expected_value, test_name):
    """
    Test runner that bypasses file I/O for simplicity.
    Parses input string directly and calls calculate_root_value.
    """
    data = [int(x) for x in input_data.split()]
    result = calculate_root_value(data)
    if result == expected_value:
        print(f"PASS: {test_name} (result={result})")
        return True
    else:
        print(f"FAIL: {test_name} (expected={expected_value}, got={result})")
        return False

def run_all_tests():
    """Run all test cases in sequence."""
    tests = [
        ("2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2", 66, "Test 1: Example from problem"),
        ("0 3 10 20 30", 60, "Test 2: Single leaf node"),
        ("2 2 0 1 5 0 1 10 1 2", 15, "Test 3: Internal node with children"),
        ("2 4 0 1 5 0 1 10 0 3 5 4", 0, "Test 4: Invalid child references"),
        ("1 3 0 1 7 1 1 1", 21, "Test 5: Duplicate child references"),
        ("1 1 1 1 1 1 0 1 5 1 1 1", 5, "Test 6: Deep nesting"),
        ("3 3 0 1 10 0 1 20 0 1 30 1 2 3", 60, "Test 7: Wide tree"),
        ("1 0 0 1 5", 0, "Test 8: Node with zero metadata"),
    ]

    passed = 0
    for input_data, expected, name in tests:
        if test_solution(input_data, expected, name):
            passed += 1

    print(f"\n{passed}/{len(tests)} tests passed")
    return passed == len(tests)
```

For the actual puzzle, run main() and time it:
```python
import time
start = time.time()
result = main()
elapsed = time.time() - start
print(f"Execution time: {elapsed:.3f}s")
```

## Debugging Strategy
If tests fail:
1. Add debug output to show node values during recursion
2. Print child_values list at each internal node
3. Print metadata and how it maps to children
4. Verify tree structure is parsed correctly
5. Check off-by-one errors in index conversion (1-based to 0-based)

## Notes
- No need for extensive error handling beyond what's in Part 1
- Focus on correctness of the value calculation logic
- The algorithm is O(n) so performance should not be an issue
- Most critical: proper handling of metadata as 1-based indexes
