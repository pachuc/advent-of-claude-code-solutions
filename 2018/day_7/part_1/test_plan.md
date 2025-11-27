# Testing Plan: Topological Sort with Alphabetical Ordering

## Testing Strategy Overview

We need to verify:
1. **Correctness**: The solution produces the correct topological ordering
2. **Alphabetical Ordering**: When multiple steps are available, we select alphabetically first
3. **Completeness**: All steps are included in the output exactly once
4. **Dependency Respect**: No step is executed before its prerequisites

## Test Categories

### 1. Example Test Case Validation
**Purpose**: Verify against the known example from problem.md

**Test Case**: Example from problem statement
```
Input dependencies:
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
```

**Expected Output**: `CABDFE`

**Validation Steps**:
1. Run the solution on this input
2. Compare output with expected result
3. Verify character by character match

**Pass Criteria**: Exact match with `CABDFE`

---

### 2. Actual Input Validation
**Purpose**: Solve the actual puzzle input

**Test Case**: The 101-line input from input.md

**Validation Approach**:
Since we don't have a known correct answer, we validate correctness by:

1. **Completeness Check**:
   - Count unique steps in input
   - Verify output length matches unique step count
   - Verify each step appears exactly once

2. **Dependency Validation**:
   - For each dependency (X → Y) in input:
     - Find position of X in output
     - Find position of Y in output
     - Verify position_of_X < position_of_Y
   - All dependencies must be satisfied

3. **Alphabetical Ordering Check**:
   - Simulate the algorithm step-by-step
   - At each position, verify the selected step was alphabetically first among available steps
   - See validation function below for implementation

**Implementation**:
```python
def validate_solution(input_deps, output_order):
    """
    Validate that output_order is a correct topological sort.
    Returns (is_valid, error_message)
    """
    # Check 1: Completeness
    steps_in_input = set()
    for prereq, dep in input_deps:
        steps_in_input.add(prereq)
        steps_in_input.add(dep)

    if len(output_order) != len(steps_in_input):
        return False, f"Length mismatch: expected {len(steps_in_input)}, got {len(output_order)}"

    if set(output_order) != steps_in_input:
        return False, "Steps in output don't match steps in input"

    if len(output_order) != len(set(output_order)):
        return False, "Duplicate steps in output"

    # Check 2: Dependency satisfaction
    position = {step: idx for idx, step in enumerate(output_order)}

    for prereq, dependent in input_deps:
        # Safety check in case steps are missing
        if prereq not in position or dependent not in position:
            return False, f"Missing steps in output"

        if position[prereq] >= position[dependent]:
            return False, f"Dependency violated: {prereq} must come before {dependent}"

    return True, "Valid"

def verify_alphabetical_ordering(all_steps, dependencies, output_order):
    """
    Verify that at each step, the alphabetically first available step was chosen.
    This re-simulates the algorithm to verify correctness.

    Returns (is_valid, error_message)
    """
    completed = set()
    remaining_deps = {k: v.copy() for k, v in dependencies.items()}

    for i, step in enumerate(output_order):
        # Find all available steps at this point
        available = [s for s in all_steps
                     if s not in completed and len(remaining_deps[s]) == 0]

        if not available:
            return False, f"No available steps at position {i}, but output has {step}"

        # Verify the chosen step is alphabetically first
        expected = min(available)
        if step != expected:
            return False, f"At position {i}, should have chosen {expected}, not {step}. Available: {sorted(available)}"

        # Mark as completed and update dependencies
        completed.add(step)
        for other_step in remaining_deps:
            remaining_deps[other_step].discard(step)

    return True, "Alphabetical ordering verified"
```

---

### 3. Edge Case Testing

#### Test 3.1: Minimal Case - Two Steps
**Input**:
```
Step A must be finished before step B can begin.
```
**Expected**: `AB`
**Rationale**: Minimal case with one dependency

#### Test 3.2: Two Independent Branches
**Input**:
```
Step A must be finished before step C can begin.
Step B must be finished before step C can begin.
```
**Expected**: `ABC`
**Rationale**: Tests alphabetical ordering when multiple steps are available (both A and B start with no prerequisites)

#### Test 3.3: Simple Chain
**Input**:
```
Step A must be finished before step B can begin.
Step B must be finished before step C can begin.
```
**Expected**: `ABC`
**Rationale**: Tests linear dependency chain

#### Test 3.4: Reverse Alphabetical Dependencies
**Input**:
```
Step Z must be finished before step A can begin.
Step Y must be finished before step A can begin.
Step X must be finished before step A can begin.
```
**Expected**: `XYZA`
**Rationale**: Tests that prerequisites are selected alphabetically when multiple are available

#### Test 3.5: Diamond Dependency
**Input**:
```
Step A must be finished before step B can begin.
Step A must be finished before step C can begin.
Step B must be finished before step D can begin.
Step C must be finished before step D can begin.
```
**Expected**: `ABCD`
**Rationale**: Tests proper handling of multiple paths to a node

#### Test 3.6: Complex Branch and Merge
**Input**:
```
Step A must be finished before step C can begin.
Step B must be finished before step C can begin.
Step C must be finished before step E can begin.
Step D must be finished before step E can begin.
```
**Expected**: `ABCDE`
**Rationale**: Tests alphabetical selection at multiple decision points

#### Test 3.7: Duplicate Dependencies
**Input**:
```
Step A must be finished before step B can begin.
Step A must be finished before step B can begin.
Step A must be finished before step B can begin.
```
**Expected**: `AB`
**Rationale**: Tests that duplicates are handled correctly (using sets)

---

### 4. Property-Based Testing

**Property 1: Every dependency is satisfied**
- For all (X, Y) in dependencies: position[X] < position[Y]
- Verified by `validate_solution()` function

**Property 2: Output contains all and only the steps from input**
- set(output) == set(all steps in input)
- len(output) == len(set(all steps in input))
- Verified by `validate_solution()` function

**Property 3: Alphabetical ordering of available steps**
- At each step in the algorithm, the selected step should be the alphabetically first among available steps
- Verified by `verify_alphabetical_ordering()` function

**Property 4: Acyclic graph assumption**
- Advent of Code guarantees input is a valid DAG (no cycles)
- If the algorithm completes and produces output of correct length, this property is implicitly satisfied
- No need for explicit cycle detection in this script

---

### 5. Performance Testing

**Test**: Large input handling
- The actual input has 101 dependency lines
- Maximum possible steps: 26 (A-Z)
- Verify solution completes quickly (serves as infinite loop detector)

**Measurement**:
```python
import time

start = time.time()
result = solve()
end = time.time()

print(f"Execution time: {end - start:.6f} seconds")
# Very lenient threshold - mainly to catch infinite loops or pathological cases
assert end - start < 1.0, "Solution took too long - possible infinite loop"
```

**Note**: With only 26 possible steps, even inefficient algorithms complete in microseconds. This test mainly serves to catch implementation bugs that cause infinite loops.

---

## Manual Verification Steps

For the actual input.md, perform these manual checks:

### Step 1: Identify Starting Steps
- Look through all dependencies
- Find steps that never appear as dependents (right side)
- These should be the earliest steps in the output

**How to verify**:
```python
def find_root_steps(dependencies):
    """Find steps with no prerequisites."""
    all_steps = set()
    dependent_steps = set()

    for prereq, dep in dependencies:
        all_steps.add(prereq)
        all_steps.add(dep)
        dependent_steps.add(dep)

    root_steps = all_steps - dependent_steps
    return sorted(root_steps)
```

### Step 2: Verify First Few Steps Manually
- Take the solution output
- For first 3-5 steps, manually verify:
  - All prerequisites are met
  - It was the alphabetically first available option

### Step 3: Verify Last Few Steps
- Check that final steps are those with many dependencies
- Verify they couldn't have been done earlier

---

## Test Execution Plan

### Phase 1: Example Validation
1. Create test with example input
2. Run solution
3. Compare with expected output `CABDFE`
4. **If mismatch, STOP and debug before proceeding** - this indicates a fundamental algorithm issue

### Phase 2: Actual Input Testing
1. Run solution on input.md
2. Apply validation functions to verify:
   - All steps present exactly once (completeness)
   - All dependencies satisfied (topological order)
   - Alphabetical ordering correct (tie-breaking)
3. Manually spot-check first few and last few steps
4. **If validation fails, STOP and fix before proceeding**

### Phase 3: Edge Case Testing
1. Run all edge case tests (3.1 - 3.7)
2. Verify expected outputs
3. Any failures indicate algorithm bugs - fix before proceeding

### Phase 4: Performance Check
1. Measure execution time
2. Verify completes quickly (catches infinite loops)

---

## Success Criteria

The solution is considered correct if:

1. ✅ Example test case produces `CABDFE`
2. ✅ Actual input validation passes all checks:
   - All unique steps included exactly once
   - All dependencies satisfied
   - No dependency violations
3. ✅ All edge cases produce expected results
4. ✅ Execution completes in < 1 second
5. ✅ Manual verification of first 3 steps confirms alphabetical selection

---

## Debugging Strategy

If tests fail:

1. **Wrong output length**:
   - Check if all steps are being added to the graph
   - Verify steps without dependents are included
   - Check for duplicate additions

2. **Dependency violation**:
   - Print the specific violation
   - Trace through algorithm to see when dependent was added to available list
   - Check prerequisite removal logic

3. **Wrong alphabetical order**:
   - Verify sorting is happening after each step
   - Check that we're selecting index 0 (first element)
   - Ensure available list is maintained correctly

4. **Example doesn't match**:
   - Step through algorithm manually
   - Print available list at each iteration
   - Compare with expected execution order from problem

---

## Test Implementation Template

```python
def test_example():
    """Test against the example from problem statement."""
    input_text = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    expected = "CABDFE"
    result = solve(input_text=input_text)
    assert result == expected, f"Expected {expected}, got {result}"
    print("✅ Example test passed")

def test_actual_input():
    """Test with actual input and validate properties."""
    # Solve the actual input
    result = solve(input_file='input.md')

    # Parse input for validation
    deps_list = parse_input_file('input.md')
    all_steps, dependencies = build_dependency_graph(deps_list)

    # Validate completeness and dependency satisfaction
    is_valid, message = validate_solution(deps_list, result)
    assert is_valid, f"Validation failed: {message}"

    # Validate alphabetical ordering
    is_valid, message = verify_alphabetical_ordering(all_steps, dependencies, result)
    assert is_valid, f"Alphabetical ordering failed: {message}"

    print(f"✅ Actual input test passed: {result}")
    return result

def test_edge_cases():
    """Run all edge case tests."""
    tests = [
        # Test 3.1: Minimal case
        ("Step A must be finished before step B can begin.", "AB"),

        # Test 3.2: Two independent branches
        ("Step A must be finished before step C can begin.\nStep B must be finished before step C can begin.", "ABC"),

        # Test 3.3: Simple chain
        ("Step A must be finished before step B can begin.\nStep B must be finished before step C can begin.", "ABC"),

        # Test 3.4: Reverse alphabetical dependencies
        ("Step Z must be finished before step A can begin.\nStep Y must be finished before step A can begin.\nStep X must be finished before step A can begin.", "XYZA"),

        # Test 3.5: Diamond
        ("Step A must be finished before step B can begin.\nStep A must be finished before step C can begin.\nStep B must be finished before step D can begin.\nStep C must be finished before step D can begin.", "ABCD"),

        # Test 3.6: Complex branch and merge
        ("Step A must be finished before step C can begin.\nStep B must be finished before step C can begin.\nStep C must be finished before step E can begin.\nStep D must be finished before step E can begin.", "ABCDE"),

        # Test 3.7: Duplicate dependencies
        ("Step A must be finished before step B can begin.\nStep A must be finished before step B can begin.\nStep A must be finished before step B can begin.", "AB"),
    ]

    for i, (input_text, expected) in enumerate(tests, 1):
        result = solve(input_text=input_text)
        assert result == expected, f"Test 3.{i} failed: expected {expected}, got {result}"
        print(f"✅ Test 3.{i} passed")

def run_all_tests():
    """Run all tests in order."""
    print("Running Phase 1: Example Validation")
    test_example()

    print("\nRunning Phase 2: Actual Input Testing")
    answer = test_actual_input()

    print("\nRunning Phase 3: Edge Case Testing")
    test_edge_cases()

    print("\n" + "="*50)
    print("✅ All tests passed!")
    print(f"Final answer: {answer}")
    print("="*50)

if __name__ == '__main__':
    run_all_tests()
```
