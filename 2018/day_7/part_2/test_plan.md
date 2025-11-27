# Test Plan: Parallel Task Execution with Multiple Workers

## Testing Objectives
1. Verify correct simulation of parallel worker execution
2. Validate time calculations for step durations
3. Ensure proper dependency handling in parallel context
4. Confirm alphabetical ordering when multiple steps are available
5. Test with provided example and actual input

## Test Categories

### 1. Unit Tests

#### 1.1 Step Duration Calculation
**Function**: `get_step_duration(step_letter, base_time=60)`

**Test Cases with base_time=60** (actual problem):
```python
# Test boundaries
assert get_step_duration('A', 60) == 61  # First letter
assert get_step_duration('Z', 60) == 86  # Last letter

# Test middle values
assert get_step_duration('G', 60) == 67  # G is 7th letter
assert get_step_duration('M', 60) == 73  # M is 13th letter
assert get_step_duration('T', 60) == 80  # T is 20th letter
```

**Test Cases with base_time=0** (for example testing):
```python
# Test with base_time=0 for simplified example
assert get_step_duration('A', 0) == 1
assert get_step_duration('C', 0) == 3
assert get_step_duration('F', 0) == 6
assert get_step_duration('Z', 0) == 26
```

**Test default parameter**:
```python
# Test default parameter
assert get_step_duration('A') == 61  # Should use default base_time=60
```

**Why**: Ensures formula `base_time + letter_position` is correct and parameterization works.

---

#### 1.2 Available Steps Identification
**Function**: `get_available_steps()`

**Test Case 1**: Steps with no dependencies
```python
all_steps = {'A', 'B', 'C'}
completed = set()
in_progress = set()
dependencies = {'A': set(), 'B': set(), 'C': set()}

result = get_available_steps(all_steps, completed, in_progress, dependencies)
assert result == ['A', 'B', 'C']  # All available, alphabetically sorted
```

**Test Case 2**: Steps with dependencies
```python
all_steps = {'A', 'B', 'C'}
completed = {'A'}
in_progress = set()
dependencies = {'A': set(), 'B': {'A'}, 'C': {'A', 'B'}}

result = get_available_steps(all_steps, completed, in_progress, dependencies)
assert result == ['B']  # Only B available (A done, C still needs B)
```

**Test Case 3**: Exclude in-progress steps
```python
all_steps = {'A', 'B', 'C'}
completed = set()
in_progress = {'A'}
dependencies = {'A': set(), 'B': set(), 'C': set()}

result = get_available_steps(all_steps, completed, in_progress, dependencies)
assert result == ['B', 'C']  # A is in progress, not available again
```

**Test Case 4**: Multiple available, verify alphabetical order
```python
all_steps = {'D', 'A', 'Z', 'B'}
completed = set()
in_progress = set()
dependencies = {s: set() for s in all_steps}

result = get_available_steps(all_steps, completed, in_progress, dependencies)
assert result == ['A', 'B', 'D', 'Z']  # Alphabetically sorted
```

---

#### 1.3 Parsing (Reuse from Part 1)
**Function**: `parse_input_text()`

**Test Case**: Verify correct parsing
```python
input_text = """Step G must be finished before step S can begin.
Step T must be finished before step Q can begin.
Step A must be finished before step B can begin."""

result = parse_input_text(input_text)
assert result == [('G', 'S'), ('T', 'Q'), ('A', 'B')]
```

**Why**: Ensure positions 5 and 36 are still correct.

---

### 2. Integration Tests

#### 2.1 Provided Example Test
**Description**: Test with the simplified example from the problem

**Input**:
```
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
```

**Parameters**: 2 workers, base time = 0 (so A=1, B=2, C=3, etc.)

**Expected Result**: 15 seconds

**Execution Timeline Verification**:
```
Time 0: Start C (duration 3)
Time 3: C done, start A (duration 1) and F (duration 6)
Time 4: A done, start B (duration 2)
Time 6: B done, start D (duration 4)
Time 9: F done
Time 10: D done, start E (duration 5)
Time 15: E done
```

**Test Implementation**:
```python
example_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

# Use parameterized solve function
result = solve(input_text=example_input, num_workers=2, base_time=0)
assert result == 15, f"Expected 15, got {result}"
print("✓ Example test passed: 15 seconds")
```

**Critical**: This is the gold standard test. Must pass before proceeding to other tests.

---

#### 2.2 Actual Problem Input Test
**Description**: Run with actual input using real parameters

**Parameters**: 5 workers, base time = 60

**Expected Behavior**:
- Should return an integer (total seconds)
- Should be greater than 0
- Should be reasonable (probably between 500-2000 seconds)

**Test**:
```python
result = solve()  # Uses default input.md, 5 workers, 60 base
assert isinstance(result, int), f"Result should be int, got {type(result)}"
assert result > 0, "Result should be positive"
assert 400 < result < 2000, f"Result {result} outside reasonable range (400-2000)"
print(f"✓ Actual input result: {result} seconds")
```

**Rationale for Range**:
- Upper bound: Sequential execution would take ~1800+ seconds (sum of all step durations)
- Lower bound: With 5 workers, can't be faster than ~400 seconds (some critical path exists)
- Actual result should fall in this range

**Manual Verification Steps**:
1. Re-run to verify determinism (same result each time)
2. Verify total time is less than sequential time
3. Calculate sequential time for comparison: sum all step durations

---

#### 2.3 Dependency Validation
**Description**: Verify that all dependencies are respected in the completion order

**Test Strategy**:
- Track the order in which steps complete (not start) in Part 2
- The completion order will likely differ from Part 1 due to parallelism
- But must still respect all dependencies (prerequisites complete before dependents)

**Implementation**:
```python
# Modify simulation to track completion order
def simulate_with_tracking(...):
    ...
    completion_order = []
    # When a step completes, append to completion_order
    ...
    return total_time, completion_order

time, order = simulate_with_tracking(...)

# Verify all dependencies are respected in completion order
for i, step in enumerate(order):
    for prereq in original_dependencies[step]:
        prereq_idx = order.index(prereq)
        assert prereq_idx < i, f"{prereq} should complete before {step}"
```

**Why**: Ensures dependency logic is correct even with parallelism.

**Note**: This test validates dependencies are respected, NOT that the order matches Part 1. Part 2's completion order can differ significantly due to parallel execution while still being correct.

---

### 3. Edge Case Tests

#### 3.1 Single Step (No Dependencies)
**Description**: Test with minimal input - single step with no dependencies

**Test**:
```python
all_steps = {'A'}
dependencies = {'A': set()}
result = simulate_parallel_execution(all_steps, dependencies, num_workers=5, base_time=60)
assert result == 61, f"Expected 61, got {result}"  # Just the time for A
```

**Why**: Ensures basic execution works without parallelism complexity

#### 3.2 Linear Chain (No Parallelism Possible)
**Input**:
```
Step A must be finished before step B can begin.
Step B must be finished before step C can begin.
```

**Expected**: Should equal sequential time (A + B + C) since no parallelism

```python
# A=61, B=62, C=63
result = simulate_parallel_execution({'A', 'B', 'C'},
                                     {'A': set(), 'B': {'A'}, 'C': {'B'}})
assert result == 61 + 62 + 63  # 186 seconds
```

#### 3.3 Fully Parallel (All Independent)
**Input**: Steps with no dependencies

```python
all_steps = {'A', 'B', 'C', 'D', 'E'}  # 5 steps for 5 workers
dependencies = {s: set() for s in all_steps}

result = simulate_parallel_execution(all_steps, dependencies, num_workers=5)
# All start at time 0, finish at their individual durations
# Longest is E at 65 seconds
assert result == 65
```

**With 6 steps and 5 workers**:
```python
all_steps = {'A', 'B', 'C', 'D', 'E', 'F'}
dependencies = {s: set() for s in all_steps}

result = simulate_parallel_execution(all_steps, dependencies, num_workers=5)
# First 5 start at 0: A,B,C,D,E
# A finishes at 61, F starts at 61
# F finishes at 61 + 66 = 127
# But E finishes at 65, so if F waits for first available...
# Actually: A(61), B(62), C(63), D(64), E(65)
# A finishes first at 61, F starts at 61, finishes at 127
assert result == 127
```

#### 3.4 More Available Steps Than Workers
**Scenario**: 10 steps with no dependencies, 5 workers

**Expected**: First 5 start alphabetically (A-E), then next 5 (F-J)

```python
all_steps = {chr(65+i) for i in range(10)}  # A-J
dependencies = {s: set() for s in all_steps}

result = simulate_parallel_execution(all_steps, dependencies, num_workers=5)

# Wave 1 at time 0: A(61), B(62), C(63), D(64), E(65)
# A finishes at 61, F starts
# B finishes at 62, G starts
# C finishes at 63, H starts
# D finishes at 64, I starts
# E finishes at 65, J starts
# F finishes at 61+66=127
# G finishes at 62+67=129
# H finishes at 63+68=131
# I finishes at 64+69=133
# J finishes at 65+70=135

assert result == 135
```

#### 3.5 Worker Becomes Idle Mid-Simulation
**Scenario**: Worker finishes but no steps available yet

**Test**: Use the example input - worker 2 finishes F at time 9, but E isn't available until D finishes at time 10.

This is covered by the example test (section 2.1).

---

#### 3.6 Worker Actually Becomes Idle After Completing Work (Bug Detection Test)
**Description**: Critical test to detect Bug #1 from critique - workers must properly transition to idle state

**Test Case**:
```python
# Simple sequential chain where worker must complete A, become idle, then start B
all_steps = {'A', 'B'}
dependencies = {'A': set(), 'B': {'A'}}

# With any number of workers >= 1:
# Time 0: Worker 0 starts A (duration 61)
# Time 61: Worker 0 finishes A, becomes idle, starts B (duration 62)
# Time 123: Worker 0 finishes B
# Total: 61 + 62 = 123 seconds

result = simulate_parallel_execution(all_steps, dependencies, num_workers=2, base_time=60)
assert result == 123, f"Expected 123, got {result}"

# If bug exists (worker doesn't become idle), simulation would hang or crash
```

**Why Critical**: This test would FAIL if workers don't properly become idle (Bug #1). The worker must:
1. Complete step A at time 61
2. Set itself to None (become idle)
3. Be available to start step B
4. Without proper idle state management, B would never start

---

#### 3.7 Alphabetical Worker Assignment Priority (Bug Detection Test)
**Description**: Verify workers pick available steps in alphabetical order

**Test Case**:
```python
# 4 independent steps, 2 workers
# Should assign A, B first (not C, D)
all_steps = {'D', 'A', 'C', 'B'}
dependencies = {s: set() for s in all_steps}

result = simulate_parallel_execution(all_steps, dependencies, num_workers=2, base_time=60)

# Expected timeline:
# Time 0: Worker 0 starts A (61s), Worker 1 starts B (62s)
# Time 61: A completes, Worker 0 starts C (63s)
# Time 62: B completes, Worker 1 starts D (64s)
# Time 124: C completes (61 + 63)
# Time 126: D completes (62 + 64)
# Total: 126 seconds

assert result == 126, f"Expected 126, got {result}"
```

**Why**: Ensures alphabetical priority is maintained when assigning work

---

#### 3.8 Multiple Steps Complete Simultaneously
**Description**: Test when multiple workers finish at the same time

**Test Case**:
```python
# Two steps with same duration, finishing together
all_steps = {'A', 'C'}  # Both have odd durations: A=61, C=63
dependencies = {'A': set(), 'C': set()}

# Actually they don't finish together. Better test:
all_steps = {'A', 'B', 'D', 'E'}
dependencies = {
    'A': set(),
    'B': set(),
    'D': {'A', 'B'},  # D waits for both
    'E': {'A', 'B'}   # E waits for both
}

# Time 0: Workers start A (61s) and B (62s)
# Time 61: A completes
# Time 62: B completes, both D and E become available
#          D and E should be assigned alphabetically: D then E
# Time 62: D (64s) and E (65s) start
# Time 126: D completes (62 + 64)
# Time 127: E completes (62 + 65)

result = simulate_parallel_execution(all_steps, dependencies, num_workers=3, base_time=60)
assert result == 127, f"Expected 127, got {result}"
```

**Why**: Tests handling of simultaneous completions and alphabetical ordering

---

### 4. Stress Tests

#### 4.1 Maximum Steps (Full Alphabet)
**Description**: Ensure algorithm handles all 26 letters efficiently

**Test**: Create a scenario with all 26 steps in a linear chain (worst case for parallelism)

```python
# Create a linear chain: Z -> Y -> X -> ... -> B -> A
all_steps = {chr(65+i) for i in range(26)}
dependencies = {}

# Build linear chain dependencies
letters = sorted(all_steps, reverse=True)  # Z, Y, X, ..., B, A
for i, letter in enumerate(letters):
    if i == 0:
        dependencies[letter] = set()  # Z has no deps
    else:
        dependencies[letter] = {letters[i-1]}  # Each depends on previous

result = simulate_parallel_execution(all_steps, dependencies, num_workers=5, base_time=60)

# Sequential time: 60+26 + 60+25 + ... + 60+1 = 60*26 + (26+25+...+1)
# = 1560 + 351 = 1911 seconds
# With parallelism: same (linear chain prevents parallelism)
assert result == 1911, f"Expected 1911, got {result}"
```

**Alternative Test - Maximum Parallelism**:
```python
# All 26 steps independent
all_steps = {chr(65+i) for i in range(26)}
dependencies = {s: set() for s in all_steps}

result = simulate_parallel_execution(all_steps, dependencies, num_workers=5, base_time=60)

# First 5: A(61), B(62), C(63), D(64), E(65) start at time 0
# A finishes at 61, F starts
# ... complex timeline ...
# Last to finish: Z started at time when E finished (65), duration 86
# So Z finishes at 65 + 86 = 151
# Actually need to calculate properly:
# Wave 1 (t=0): A,B,C,D,E -> finish at 61,62,63,64,65
# Wave 2 (t=61-65): F,G,H,I,J -> start at 61,62,63,64,65
# F finishes at 61+66=127
# ...
# This gets complex, so use a range check
assert 140 < result < 200, f"Expected 140-200, got {result}"
```

#### 4.2 Runtime Performance
**Description**: Ensure algorithm runs quickly for actual input

**Test**:
```python
import time

start = time.time()
result = solve()
elapsed = time.time() - start

assert elapsed < 1.0, f"Too slow: {elapsed:.3f}s"  # Should be near-instantaneous
print(f"✓ Performance test passed: {elapsed*1000:.2f}ms")
```

**Why**: Verifies time-jumping optimization works (not second-by-second simulation)

---

#### 4.3 Time Advancement Efficiency (Bug Detection Test)
**Description**: Verify simulation uses time jumping, not second-by-second iteration

**Test**:
```python
import time

# Create scenario with large time duration
all_steps = {'A', 'B'}
dependencies = {'A': set(), 'B': {'A'}}

# This should take 123 seconds in simulation time
start = time.time()
result = simulate_parallel_execution(all_steps, dependencies, num_workers=1, base_time=60)
elapsed = time.time() - start

# Simulation time should be 123 seconds, but wall-clock time should be microseconds
assert result == 123, f"Simulation time: expected 123, got {result}"
assert elapsed < 0.1, f"Wall-clock time too slow: {elapsed:.3f}s (should be <0.1s)"
print(f"✓ Time jumping works: simulated 123s in {elapsed*1000:.2f}ms")
```

**Why**: Detects if implementation incorrectly loops second-by-second instead of jumping to events

---

### 5. Validation Tests

#### 5.1 Time Is Monotonically Increasing
**Description**: In simulation tracking, time should never decrease

```python
# Modify simulation to track time at each step
def simulate_with_time_tracking(...):
    time_history = []
    # Record current_time at each iteration
    ...
    return total_time, time_history

_, history = simulate_with_time_tracking(...)

for i in range(len(history) - 1):
    assert history[i] <= history[i+1], "Time should not decrease"
```

#### 5.2 All Steps Eventually Complete
**Description**: Ensure no steps are left behind

```python
# Track which steps completed
_, completed_order = simulate_with_tracking(...)

assert set(completed_order) == all_steps, "All steps should complete"
assert len(completed_order) == len(all_steps), "No duplicates"
```

#### 5.3 Workers Never Exceed Capacity
**Description**: Never more than 5 steps in progress simultaneously

```python
# Track in_progress set size over time
def simulate_with_progress_tracking(...):
    max_concurrent = 0
    # Track max size of in_progress_steps
    ...
    return total_time, max_concurrent

_, max_concurrent = simulate_with_progress_tracking(...)

assert max_concurrent <= 5, "Never more than 5 workers"
```

---

## Test Execution Order

1. **Unit tests first** (1.1 - 1.3)
   - Verify individual components work
   - Fast feedback loop

2. **Provided example** (2.1)
   - Critical validation against known answer
   - Must pass before proceeding

3. **Edge cases** (3.1 - 3.5)
   - Verify boundary conditions
   - Ensure robustness

4. **Actual input** (2.2)
   - Verify solution works on real problem
   - Generate actual answer

5. **Consistency check** (2.3)
   - Validate against Part 1 logic
   - Cross-reference

6. **Validation tests** (5.1 - 5.3)
   - Sanity checks on simulation
   - Confirm invariants

7. **Stress tests** (4.1 - 4.2)
   - Performance validation
   - Scalability check

## Test Implementation Approach

### Quick Manual Tests
For rapid development, create a test section at the bottom of solution.py:

```python
if __name__ == '__main__':
    # Quick unit tests
    print("Testing step durations...")
    assert get_step_duration('A', 60) == 61
    assert get_step_duration('Z', 60) == 86
    assert get_step_duration('A', 0) == 1  # For example testing
    print("✓ Step durations correct")

    # Test the provided example (CRITICAL - must pass)
    print("\nTesting provided example...")
    example_input = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""

    result = solve(input_text=example_input, num_workers=2, base_time=0)
    assert result == 15, f"Example failed: expected 15, got {result}"
    print(f"✓ Example test passed: {result} seconds")

    # Test worker idle bug
    print("\nTesting worker idle transition...")
    all_steps = {'A', 'B'}
    deps = {'A': set(), 'B': {'A'}}
    result = simulate_parallel_execution(all_steps, deps, num_workers=1, base_time=60)
    assert result == 123, f"Worker idle test failed: expected 123, got {result}"
    print("✓ Worker idle test passed")

    # Solve actual problem
    print("\nSolving actual problem...")
    answer = solve()
    print(f"Answer: {answer} seconds")

    # Sanity check
    assert 400 < answer < 2000, f"Answer {answer} outside expected range"
    print("✓ Answer is in reasonable range")
```

### Comprehensive Test File (Optional)
Create `test_solution.py` with proper test framework if desired:

```python
import pytest
from solution import *

def test_step_duration():
    assert get_step_duration('A') == 61
    # ... more tests

def test_example():
    # ... example test
```

## Success Criteria

**Must Pass**:
- [ ] All unit tests pass (step duration, available steps, parsing)
- [ ] Example test returns exactly 15
- [ ] Worker idle transition test passes (Bug #1 detection)
- [ ] Alphabetical assignment test passes
- [ ] Actual input returns integer in range 400-2000
- [ ] Completion order respects all dependencies (dependency validation)
- [ ] Runtime < 1 second for actual input
- [ ] No errors or exceptions during execution

**Validation**:
- [ ] Result is deterministic (same answer on multiple runs)
- [ ] Time advancement is efficient (not second-by-second)
- [ ] All steps complete (no steps left behind)
- [ ] Never more than num_workers steps in progress simultaneously

## Expected Answer Range

Based on the input:
- Unique steps: All letters appearing in input.md (count from G,T,A,H,V,Z,R,L,Y,W,X,K,Q,U,M,P,I,B,C,J,F,E,D,N,S,O)
- Sequential time estimate: Sum of all step durations ≈ 1800+ seconds
- Parallel time with 5 workers: Significantly less, estimated 400-1200 seconds
- Must be less than sequential time
- Must be greater than the longest critical path through the dependency graph

**Range**: 400-2000 seconds is reasonable, with actual answer likely in 700-1100 range

The answer should be:
- A specific integer
- Deterministic (same result on every run)
- Verifiable by re-running the simulation
