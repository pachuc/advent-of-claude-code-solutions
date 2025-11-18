# Testing Plan: Recursive Circus - Finding the Bottom Program

## Testing Strategy

We need to verify that our solution correctly identifies the root program (bottom of the tower) across various input scenarios.

## Test Categories

### 1. Basic Functionality Tests

#### Test 1.1: Simple Example from Problem Statement
```
Input:
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

Expected Output: tknk
```
**Rationale**: Verify basic correctness with known example

#### Test 1.2: Single Program
```
Input:
solo (100)

Expected Output: solo
```
**Rationale**: A single program with no children is the root

#### Test 1.3: Linear Chain
```
Input:
bottom (10) -> middle
middle (20) -> top
top (30)

Expected Output: bottom
```
**Rationale**: Verify correct identification in a simple linear hierarchy

### 2. Parsing Edge Cases

#### Test 2.1: Programs with No Children at Various Positions
```
Input:
leaf1 (50)
root (100) -> branch1, branch2
leaf2 (60)
branch1 (75) -> leaf1
branch2 (75) -> leaf2
leaf3 (55)

Expected Output: root
```
**Rationale**: Multiple programs without children; only one is never referenced

#### Test 2.2: Varying Whitespace
```
Input:
prog1(50)->child1,child2
prog2  (60)  ->  child3 , child4
root(70)->prog1,prog2
child1(10)
child2(20)
child3(30)
child4(40)

Expected Output: root
```
**Rationale**: Ensure robust whitespace handling

#### Test 2.3: Single Child
```
Input:
root (100) -> only_child
only_child (50)

Expected Output: root
```
**Rationale**: Edge case with minimal children count

#### Test 2.4: Empty Children List
```
Input:
root (100) ->
child (50)

Expected Output: root
```
**Rationale**: Handle arrow present but no children after it (edge case)

### 3. Scale Tests

#### Test 3.1: Actual Input File
```
Input: Read from /app/agent_workspace/2017/day_7/part_1/input.md (1337 lines)
Expected: Should return a valid program name in reasonable time (<1 second)
Verification: Use Test 4.1 to validate correctness (since we don't know expected answer)
```
**Rationale**: Verify performance on real input size and that solution doesn't crash

### 4. Correctness Verification Tests

#### Test 4.1: Verify No False Positives
```
After finding root from actual input:
1. Parse input again to build parent->children mapping
2. Verify found root appears as a parent (has children or is standalone)
3. Verify found root never appears in any children list
```
**Rationale**: Double-check our answer makes logical sense

#### Test 4.2: Uniqueness Check
```
Verify that (all_programs - all_children) returns exactly 1 element
This is handled by the assertion in the implementation
```
**Rationale**: Problem guarantees single root; assertion detects malformed input

### 5. Input Preprocessing Tests

#### Test 5.1: Empty Lines in Input
```
Input:
root (100) -> child1

child1 (50)


Expected Output: root
```
**Rationale**: Verify empty lines are filtered correctly

#### Test 5.2: Whitespace-Only Lines
```
Input:
root (100) -> child1

child1 (50)

Expected Output: root
```
**Rationale**: Verify whitespace-only lines don't cause issues

## Test Execution Plan

### Phase 1: Unit Tests
1. Run Test 1.1 (basic example) - **CRITICAL**
2. Run Test 1.2 (single program)
3. Run Test 1.3 (linear chain)
4. Run Test 2.1-2.4 (parsing variations)

### Phase 2: Integration Tests
5. Run Test 3.1 (actual input) - **CRITICAL**
6. Run Test 4.1 (verification on actual input) - **CRITICAL**

### Phase 3: Edge Cases (Optional)
7. Run Test 5.1 (empty lines)
8. Run Test 5.2 (whitespace-only lines)

## Acceptance Criteria

### Must Pass:
- ✅ Test 1.1: Correct output "tknk" for problem example
- ✅ Test 3.1: Finds valid root in actual input.md
- ✅ Test 4.1: Found root is logically valid (not in any children list)

### Should Pass:
- Test 1.2, 1.3: Simple cases work correctly
- Test 2.1-2.4: Parser handles whitespace and formatting
- Test 4.2: Exactly one root found (via assertion)

### Optional:
- Test 5.1-5.2: Input preprocessing handles empty/whitespace lines

## Testing Implementation Approach

```python
def test_find_bottom_program():
    # Test 1.1: Basic example
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

    result = find_bottom_program(example_input)
    assert result == "tknk", f"Expected 'tknk', got '{result}'"

    # Test 1.2: Single program
    single_input = "solo (100)"
    result = find_bottom_program(single_input)
    assert result == "solo", f"Expected 'solo', got '{result}'"

    # Test 3.1: Actual input
    with open('/app/agent_workspace/2017/day_7/part_1/input.md', 'r') as f:
        actual_input = f.read()
    result = find_bottom_program(actual_input)

    # Test 4.1: Verify result validity
    verify_root_not_in_children(actual_input, result)

    print(f"All tests passed! Answer: {result}")
```

## Manual Verification Steps

After running the solution on actual input:
1. Print the found root name
2. Search input.md for that name - should appear exactly once on left side
3. Search all right sides (after `->`) - should never appear
4. Confirm this program exists in the input file

## Success Metrics

- ✅ All critical tests pass
- ✅ Solution completes in < 1 second
- ✅ Code is clean and readable
- ✅ Root name can be verified manually in input file
