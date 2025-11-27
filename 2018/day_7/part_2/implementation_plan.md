# Implementation Plan: Parallel Task Execution with Multiple Workers

## Overview
We need to simulate parallel execution of tasks (steps) by 5 workers, where each step has dependencies and takes time based on its letter. The goal is to calculate the total time to complete all steps.

## Key Differences from Part 1
- Part 1: Sequential execution, output is the order string
- Part 2: Parallel execution with 5 workers, output is total time in seconds
- Part 2 adds: Worker management, time simulation, step duration calculation

## Core Algorithm: Event-Driven Simulation

We'll use a **time-stepping simulation** approach:
1. Track current time (starting at 0)
2. Track worker states (idle or busy with time remaining)
3. Assign available steps to idle workers
4. Advance time to next event (step completion)
5. Continue until all steps are complete

## Reusable Components from Part 1

From `part_1_solution.py`, we can reuse:
- ✅ `parse_input_text()` - Exactly the same parsing logic
- ✅ `build_dependency_graph()` - Same graph construction
- ❌ `topological_sort_alphabetical()` - Need to replace with simulation logic

## Data Structures

### 1. Worker State (Chosen Approach)
```python
# List of num_workers workers
# Idle worker: None
# Busy worker: {'step': str, 'time_remaining': int}

workers = [
    None,                                    # Worker 0 (idle)
    {'step': 'A', 'time_remaining': 15},    # Worker 1 (working on A, 15s left)
    {'step': 'B', 'time_remaining': 42},    # Worker 2 (working on B, 42s left)
    None,                                    # Worker 3 (idle)
    {'step': 'C', 'time_remaining': 3},     # Worker 4 (working on C, 3s left)
]
```

**Why This Approach**:
- Simple: None clearly indicates idle
- Direct: Access worker state via index
- Efficient: Dictionary provides both step name and time in one object

**Alternative Rejected**: Separate lists for steps and times would require keeping them synchronized, increasing complexity.

### 2. Step States
```python
completed_steps = set()      # Steps that have finished execution
in_progress_steps = set()    # Steps currently being worked on by some worker
```

**Why Sets**: O(1) membership testing and insertion

### 3. Dependencies Tracking
```python
# Reuse pattern from Part 1
# Maps each step to set of its remaining prerequisites
remaining_dependencies = {
    'A': set(),           # A has no prerequisites
    'B': {'A'},          # B requires A
    'C': {'A', 'B'},     # C requires both A and B
    ...
}
```

**Key Operations**:
- When step completes: `remaining_dependencies[step].discard(completed_step)`
- Step is available when: `len(remaining_dependencies[step]) == 0`

## Implementation Steps

### Step 1: Reuse Part 1 Parsing and Graph Building
**File**: Copy functions from `part_1_solution.py`
- Copy `parse_input_text()` function as-is
- Copy `build_dependency_graph()` function as-is

**Why**: The dependency graph structure is identical; only execution logic changes.

### Step 2: Implement Step Duration Calculator
**Function**: `get_step_duration(step_letter, base_time=60)`

**Logic**:
```python
def get_step_duration(step_letter, base_time=60):
    """Calculate duration for a step: base_time + position in alphabet.

    Args:
        step_letter: Single uppercase letter (A-Z)
        base_time: Base seconds to add (default 60 for actual problem, 0 for example)

    Returns:
        Duration in seconds
    """
    # A=1, B=2, ..., Z=26
    return base_time + (ord(step_letter) - ord('A') + 1)
```

**Examples with base_time=60**:
- A: 60 + 1 = 61 seconds
- G: 60 + 7 = 67 seconds
- Z: 60 + 26 = 86 seconds

**Examples with base_time=0** (for testing with provided example):
- A: 0 + 1 = 1 second
- C: 0 + 3 = 3 seconds

**Complexity**: O(1)

**Why Parameterize**: Allows testing with the provided example (base_time=0) and actual problem (base_time=60) using the same code.

### Step 3: Implement Available Steps Finder
**Function**: `get_available_steps(all_steps, completed_steps, in_progress_steps, remaining_dependencies)`

**Logic**:
```python
def get_available_steps(...):
    """Find steps that are ready to start (all prerequisites done, not started yet)."""
    available = []
    for step in all_steps:
        if step not in completed_steps and step not in in_progress_steps:
            if len(remaining_dependencies[step]) == 0:
                available.append(step)
    return sorted(available)  # Return in alphabetical order
```

**Key Points**:
- Step must not be completed
- Step must not be in progress
- All prerequisites must be in `completed_steps` (not just started)
- Return sorted for alphabetical assignment priority

**Complexity**: O(n log n) where n is number of steps

### Step 4: Implement Worker Assignment
**Function**: `assign_workers(workers, available_steps, base_time=60)`

**Logic**:
```python
def assign_workers(workers, available_steps, base_time=60):
    """Assign available steps to idle workers in alphabetical order."""
    assigned = []

    for step in available_steps:
        # Find an idle worker
        idle_worker_idx = None
        for i in range(len(workers)):
            if workers[i] is None:  # Worker is idle
                idle_worker_idx = i
                break

        if idle_worker_idx is None:
            break  # No more idle workers available

        # Assign step to this worker
        workers[idle_worker_idx] = {
            'step': step,
            'time_remaining': get_step_duration(step, base_time)
        }
        assigned.append(step)

    return assigned
```

**Key Points**:
- Iterate through available steps in alphabetical order (already sorted)
- Find first idle worker (None value in list)
- Check for idle worker BEFORE assignment (prevents index errors)
- Assign step to worker with duration calculated using base_time parameter
- Stop when no more idle workers or no more available steps

**Complexity**: O(w × s) where w=5 workers, s=available steps (typically small)

### Step 5: Implement Main Simulation Loop
**Function**: `simulate_parallel_execution(all_steps, dependencies, num_workers=5, base_time=60)`

**Complete Implementation**:
```python
def simulate_parallel_execution(all_steps, dependencies, num_workers=5, base_time=60):
    """Simulate parallel execution of steps with multiple workers.

    Args:
        all_steps: Set of all step names
        dependencies: Dict mapping step -> set of prerequisites
        num_workers: Number of workers available (default 5)
        base_time: Base time for step duration calculation (default 60)

    Returns:
        Total time in seconds to complete all steps
    """
    current_time = 0
    workers = [None] * num_workers  # All workers start idle
    completed_steps = set()
    in_progress_steps = set()

    # Deep copy dependencies to track remaining prerequisites
    remaining_dependencies = {k: v.copy() for k, v in dependencies.items()}

    while len(completed_steps) < len(all_steps):
        # 1. Check for completed work at current time
        # CRITICAL: Use index-based iteration to properly modify the list
        for i in range(len(workers)):
            if workers[i] is not None and workers[i]['time_remaining'] == 0:
                # Step just completed
                completed_step = workers[i]['step']
                completed_steps.add(completed_step)
                in_progress_steps.remove(completed_step)

                # Update dependencies - remove this step from all prerequisites
                for step in all_steps:
                    remaining_dependencies[step].discard(completed_step)

                # Worker becomes idle - MUST use index assignment
                workers[i] = None

        # 2. Assign new work to idle workers
        available = get_available_steps(all_steps, completed_steps,
                                        in_progress_steps, remaining_dependencies)
        newly_assigned = assign_workers(workers, available, base_time)
        in_progress_steps.update(newly_assigned)

        # 3. Advance time to next event
        busy_workers = [w for w in workers if w is not None]
        if busy_workers:
            # Find minimum time until next completion
            min_time = min(w['time_remaining'] for w in busy_workers)
            current_time += min_time

            # Decrement all workers' remaining time
            # CRITICAL: Must modify the dict in the list directly
            for i in range(len(workers)):
                if workers[i] is not None:
                    workers[i]['time_remaining'] -= min_time
        else:
            # All workers idle but steps remain
            if len(completed_steps) < len(all_steps):
                raise RuntimeError(
                    f"Simulation stuck: {len(completed_steps)} steps completed, "
                    f"{len(all_steps)} total, no workers busy, "
                    f"available steps: {get_available_steps(all_steps, completed_steps, in_progress_steps, remaining_dependencies)}"
                )
            break

    return current_time
```

**Key Algorithm Details**:

1. **Completion Check**: At each time point, first check which workers finished
2. **Assignment**: Then assign new work to idle workers
3. **Time Advancement**: Jump to next completion event (not second-by-second)
4. **Termination**: When all steps are completed

**Critical Implementation Notes**:

1. **Worker State Updates**: MUST use index-based iteration (`for i in range(len(workers))`) when modifying worker states. Using `for worker in workers` creates a local variable that doesn't modify the list.
   - ✗ WRONG: `worker = None` (doesn't modify list)
   - ✓ CORRECT: `workers[i] = None` (modifies list)

2. **Dictionary Modifications**: When modifying nested dictionaries in the workers list, either approach works:
   - `workers[i]['time_remaining'] -= min_time` (modifies dict in place)
   - But for consistency and clarity, use index notation throughout

3. **Error Handling**: If all workers are idle but steps remain, raise an error instead of silently breaking. This helps catch bugs in dependency logic.

4. **Deep Copy**: Use dict comprehension `{k: v.copy() for k, v in dependencies.items()}` to copy the dependency sets. Each step's prerequisite set must be independent.

**Time Advancement Strategy**:
- Instead of incrementing by 1 second each iteration (inefficient)
- Jump directly to the next completion event by finding minimum remaining time
- This reduces iterations from ~1000+ seconds to ~26 events (number of steps)

**Complexity**:
- Iterations: O(n) where n = number of steps (at most one iteration per step completion)
- Per iteration: O(n) for updating dependencies
- Overall: O(n²) where n ≤ 26, very efficient
- Time jumps reduce wall-clock iterations from 1000+ to ~26

### Step 6: Implement Main Solver
**Function**: `solve(input_text=None, input_file='input.md', num_workers=5, base_time=60)`

**Logic**:
```python
def solve(input_text=None, input_file='input.md', num_workers=5, base_time=60):
    """Solve the parallel task execution problem.

    Args:
        input_text: Optional string containing input data. If None, reads from input_file
        input_file: Path to input file (default: 'input.md')
        num_workers: Number of workers available (default: 5)
        base_time: Base seconds for duration calculation (default: 60)

    Returns:
        int: Total time in seconds to complete all steps
    """
    # Parse input (reuse from Part 1)
    if input_text is not None:
        deps_list = parse_input_text(input_text)
    else:
        with open(input_file) as f:
            deps_list = parse_input_text(f.read())

    # Build graph (reuse from Part 1)
    all_steps, dependencies = build_dependency_graph(deps_list)

    # Simulate parallel execution (new)
    total_time = simulate_parallel_execution(all_steps, dependencies,
                                             num_workers=num_workers,
                                             base_time=base_time)

    return total_time
```

**Parameters**:
- Default values (5 workers, 60 base time) match actual problem requirements
- Parameterization allows testing with example values (2 workers, 0 base time)
- Makes the function flexible without code duplication

### Step 7: Main Entry Point
```python
if __name__ == '__main__':
    answer = solve()
    print(answer)
```

## Algorithm Efficiency Analysis

### Time Complexity
- Parsing: O(m) where m = number of dependency lines (~100)
- Graph building: O(m + n) where n = number of steps (~26)
- Simulation loop:
  - Iterations: O(n) - at most one iteration per step completion
  - Per iteration: O(n) for updating dependencies
  - Total: O(n²)
- **Overall**: O(n²) ≈ O(676) for n=26, very efficient

### Space Complexity
- Dependency graph: O(n + m)
- Worker array: O(5) = O(1)
- Completed/in-progress sets: O(n)
- **Overall**: O(n + m)

### Optimization Notes
- **Time jumping** instead of second-by-second simulation is crucial
  - Reduces ~1000+ iterations to ~26 iterations
- For the given input size (26 letters max), any reasonable approach works
- The input has 101 dependencies, so graph is reasonably connected

## Edge Cases Handled

1. **Multiple steps available**: Alphabetical ordering ensures deterministic assignment
2. **More available steps than workers**: Workers filled first come first served (alphabetically)
3. **No available steps while work in progress**: Workers continue, no assignment happens
4. **All workers busy**: Wait for next completion
5. **Step with no dependencies**: Can start immediately at time 0

## Implementation Structure

```
solution.py
├── parse_input_text()           [from Part 1]
├── build_dependency_graph()     [from Part 1]
├── get_step_duration()          [new]
├── get_available_steps()        [new]
├── simulate_parallel_execution() [new - main logic]
└── solve()                      [modified from Part 1]
```

## Testing Strategy (Summary)
- Verify with provided example (2 workers, 0 base time → 15 seconds)
- Test with actual input (5 workers, 60 base time)
- Validate against Part 1 order (steps should complete in compatible order)
- Check edge cases (see test_plan.md for details)
