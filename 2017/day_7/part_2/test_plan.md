# Testing Plan - Part 2: Tower Balancing

## Overview
Verify that the solution correctly identifies the program with the wrong weight and calculates the corrected weight. This is a script for solving a puzzle, so we focus on essential tests rather than comprehensive coverage.

## Test 1: Example from Problem Description (CRITICAL)
**Objective:** Validate against the known example

**Priority:** MUST PASS - This is the litmus test for correctness

**Input:**
```
pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
```

**Expected Output:** `60`

**Testing Method:**
```python
# Create a test file or add this at the top of main():
example_input = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

result = solve_part2(example_input)
print(f"Example result: {result}")
assert result == 60, f"Expected 60, got {result}"
print("✓ Example test passed!")
```

**Validation:**
- Output must be exactly 60
- If not, debug the algorithm before running on actual input

## Test 2: Actual Puzzle Input (CRITICAL)
**Objective:** Solve the actual puzzle

**Priority:** MUST WORK - This is the goal

**Testing Method:**
```python
def main():
    # First test with example
    print("Testing with example...")
    example_input = """..."""  # (from Test 1)
    example_result = solve_part2(example_input)
    print(f"Example result: {example_result} (expected: 60)")

    # Now solve actual puzzle
    print("\nSolving actual puzzle...")
    with open('/app/agent_workspace/2017/day_7/part_2/input.md', 'r') as f:
        input_data = f.read()

    result = solve_part2(input_data)
    print(f"\nAnswer: {result}")
```

**Success Criteria:**
- Solution completes successfully (no crashes)
- Produces a single integer result
- Result is positive and reasonable (likely in range 1-1000)

## Test 3: Verify Root Identification
**Objective:** Ensure root is dynamically found correctly

**Priority:** SHOULD CHECK - Quick sanity check

**Testing Method:**
Add debug print to main():
```python
weights, children, root = parse_input(input_data)
print(f"Root identified: {root}")  # Should be "wiapj" for actual input
```

**Success Criteria:**
- For example input: root = "tknk"
- For actual input: root = "wiapj" (matches Part 1 answer)

## Test 4: Spot Check Total Weights (Optional)
**Objective:** Manually verify a calculation

**Priority:** NICE TO HAVE - Only if debugging needed

**Testing Method:**
Add debug output when running example:
```python
# After calculating total weights on example input
print(f"ugml total weight: {total_weights['ugml']}")  # Should be 251
print(f"padx total weight: {total_weights['padx']}")  # Should be 243
print(f"fwft total weight: {total_weights['fwft']}")  # Should be 243
```

**Note:** Only add this if Test 1 fails and you need to debug

## Test 5: Performance Check (Optional)
**Objective:** Ensure solution runs efficiently

**Priority:** INFORMATIONAL - Not a blocker

**Testing Method:**
```python
import time

start = time.time()
result = solve_part2(input_data)
elapsed = time.time() - start

print(f"Runtime: {elapsed:.3f}s")
# Should be well under 1 second for ~1300 programs
```

**Note:** This is informational only - don't fail if it takes longer than expected

## Summary: Practical Testing Strategy

Given this is a **script to solve a puzzle**, here's the minimal viable testing approach:

### Essential Tests (Must Do):
1. ✅ **Test 1**: Run on example, verify output is 60
2. ✅ **Test 2**: Run on actual input, get the answer
3. ✅ **Test 3**: Verify root is correctly identified

### Optional Tests (If Needed for Debugging):
4. ⚠️ **Test 4**: Spot check some total weight calculations
5. ⚠️ **Test 5**: Check performance (informational only)

### Not Needed for a Script:
- ❌ Extensive edge case testing
- ❌ Unit tests for every function
- ❌ Performance assertions
- ❌ Input validation tests

## Recommended Code Structure for Testing

```python
def solve_part2(input_data):
    # Main solution logic
    weights, children, root = parse_input(input_data)
    total_weights = {}
    calculate_total_weight(root, weights, children, total_weights)
    imbalance = find_imbalanced_node(root, weights, children, total_weights)
    wrong_program, wrong_total, correct_total = imbalance
    difference = correct_total - wrong_total
    corrected_weight = weights[wrong_program] + difference
    return corrected_weight

def main():
    # Test with example first
    print("=" * 50)
    print("Testing with example input...")
    print("=" * 50)

    example_input = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)"""

    example_result = solve_part2(example_input)
    print(f"Example result: {example_result}")
    print(f"Expected: 60")

    if example_result == 60:
        print("✓ Example test PASSED!\n")
    else:
        print("✗ Example test FAILED!")
        return

    # Now solve the actual puzzle
    print("=" * 50)
    print("Solving actual puzzle...")
    print("=" * 50)

    with open('/app/agent_workspace/2017/day_7/part_2/input.md', 'r') as f:
        input_data = f.read()

    result = solve_part2(input_data)
    print(f"\n{'=' * 50}")
    print(f"ANSWER: {result}")
    print(f"{'=' * 50}")

if __name__ == "__main__":
    main()
```

## Debugging Strategy (If Tests Fail)

If the example test fails, add debug prints in this order:

1. **Check parsing:**
   ```python
   print(f"Root: {root}")  # Should be "tknk" for example
   print(f"ugml weight: {weights['ugml']}")  # Should be 68
   ```

2. **Check total weights:**
   ```python
   print(f"ugml total: {total_weights['ugml']}")  # Should be 251
   print(f"padx total: {total_weights['padx']}")  # Should be 243
   ```

3. **Check imbalance detection:**
   ```python
   print(f"Wrong program: {wrong_program}")  # Should be "ugml"
   print(f"Wrong total: {wrong_total}, Correct total: {correct_total}")
   ```

4. **Check correction:**
   ```python
   print(f"Difference: {difference}")  # Should be -8
   print(f"Corrected weight: {corrected_weight}")  # Should be 60
   ```
