# Implementation Plan: Permutation Promenade Part 2

## Problem Analysis

We need to determine the order of 16 programs after performing the same dance sequence **1 billion times**. Since executing the dance once takes ~10,000 moves and we need to do it 1 billion times, a naive simulation would require ~10 trillion operations, which is computationally infeasible.

**Key Insight**: Permutations form cycles. Since we're applying the same transformation repeatedly starting from a fixed initial state (`abcdefghijklmnop`), the state must eventually cycle back to the initial configuration. The cycle length will be much smaller than 1 billion, allowing us to use modulo arithmetic to skip ahead.

## Algorithm Strategy

### Approach: Simple Cycle Detection

1. **Start from the initial state** (`abcdefghijklmnop`)
2. **Repeatedly apply the dance** until we return to the initial state
3. **Count iterations to get cycle length**
4. **Use modulo arithmetic**: `effective_iterations = 1_000_000_000 % cycle_length`
5. **Handle the modulo edge case**: If result is 0, we need `cycle_length` iterations
6. **Apply the dance `effective_iterations` times** to get the final answer

### Why This Works

- The dance moves form a permutation operation P
- Starting from initial state I: P(I), P²(I), P³(I), ..., Pⁿ(I)
- Since we start from a fixed state and apply the same operation, we will return to that state: Pᵏ(I) = I for some k
- Once we know k (the cycle length), we compute `1,000,000,000 mod k` to find the answer
- **Important**: The cycle always starts at iteration 0 (the initial state) for this type of problem

## Implementation Steps

### Step 1: Reuse Part 1 Code

Copy the three move functions from `part_1_solution.py`:
- `spin(programs, x)` - rotates last x programs to front (modifies in-place)
- `exchange(programs, a, b)` - swaps positions a and b (modifies in-place)
- `partner(programs, name_a, name_b)` - swaps programs by name (modifies in-place)

**Note**: These functions modify the list in-place. We'll need to make copies when necessary to avoid unwanted mutations.

### Step 2: Create Dance Iteration Function

```python
def perform_dance(programs, moves):
    """
    Execute one complete dance sequence on the programs.

    Args:
        programs: List of program names (will be modified in-place)
        moves: List of move strings

    Note: Modifies programs in-place for efficiency.
    """
    for move in moves:
        if not move:  # Skip empty strings
            continue

        if move[0] == 's':
            x = int(move[1:])
            spin(programs, x)

        elif move[0] == 'x':
            parts = move[1:].split('/')
            a, b = int(parts[0]), int(parts[1])
            exchange(programs, a, b)

        elif move[0] == 'p':
            parts = move[1:].split('/')
            name_a, name_b = parts[0], parts[1]
            partner(programs, name_a, name_b)
```

### Step 3: Implement Simple Cycle Detection

```python
def find_cycle_length(initial_state, moves):
    """
    Find the cycle length by repeatedly applying the dance
    until we return to the initial state.

    Args:
        initial_state: The starting configuration (list)
        moves: List of move strings

    Returns:
        The number of iterations to return to initial_state
    """
    current = initial_state.copy()
    cycle_length = 0

    while True:
        # Apply one complete dance
        perform_dance(current, moves)
        cycle_length += 1

        # Check if we've returned to initial state
        if current == initial_state:
            return cycle_length

        # Safety check to prevent infinite loops
        if cycle_length > 10_000_000:
            raise Exception(f"Cycle detection exceeded limit. Something is wrong.")

    return cycle_length
```

**Why this is simple and correct**:
- We start from a fixed initial state
- Permutations always cycle back to the starting point
- No need to track a dictionary of states or handle "tails"
- The cycle always begins at iteration 0 (the initial state)

### Step 4: Calculate Final State with Proper Edge Case Handling

```python
def solve(target_iterations=1_000_000_000):
    """
    Solve the permutation problem for a given number of iterations.

    Args:
        target_iterations: Number of times to apply the dance (default: 1 billion)

    Returns:
        String representing the final program order
    """
    # Read and parse input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()

    # Parse moves, filtering out empty strings
    moves = [m for m in input_data.split(',') if m]

    # Initial state: programs in alphabetical order
    initial = list('abcdefghijklmnop')

    # Find cycle length
    print("Finding cycle length...")
    cycle_length = find_cycle_length(initial, moves)
    print(f"Cycle detected at length: {cycle_length}")

    # Calculate effective iterations using modulo arithmetic
    # Example: If cycle_length = 60 and target = 1_000_000_000
    #   - 1_000_000_000 % 60 = 40
    #   - So we need the state after 40 iterations
    effective_iterations = target_iterations % cycle_length

    # Edge case: If modulo is 0, we're at a multiple of the cycle length
    # Example: If cycle_length = 60 and target = 120
    #   - 120 % 60 = 0
    #   - But we don't want iteration 0 (the initial state)
    #   - We want iteration 60 (which equals the initial state due to cycling)
    #   - However, since we already know it cycles, we can use cycle_length
    if effective_iterations == 0:
        effective_iterations = cycle_length

    print(f"Effective iterations needed: {target_iterations} % {cycle_length} = {effective_iterations}")

    # Apply the dance effective_iterations times
    current = initial.copy()
    for i in range(effective_iterations):
        perform_dance(current, moves)

    result = ''.join(current)
    print(f"Final result after {target_iterations} iterations: {result}")

    return result
```

### Step 5: Verification Against Part 1

```python
def verify_part1(moves):
    """
    Verify that one iteration produces the Part 1 answer.
    This is a critical sanity check.
    """
    initial = list('abcdefghijklmnop')
    perform_dance(initial, moves)
    result = ''.join(initial)

    expected = 'eojfmbpkldghncia'
    if result == expected:
        print(f"✓ Part 1 verification passed: {result}")
        return True
    else:
        print(f"✗ Part 1 verification FAILED!")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        return False
```

### Step 6: Main Function

```python
def main():
    """Main entry point."""
    # Read and parse input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]

    # Verify against Part 1 answer first
    print("Verifying Part 1 answer...")
    if not verify_part1(moves):
        print("ERROR: Part 1 verification failed. Aborting.")
        return

    # Solve Part 2
    print("\nSolving Part 2...")
    result = solve(1_000_000_000)

    # Output final answer
    print(f"\nFinal Answer: {result}")

if __name__ == '__main__':
    main()
```

## Complete Implementation Structure

```python
# === Move Functions from Part 1 ===

def spin(programs, x):
    """Rotate last x programs to the front (modifies in-place)"""
    if x == 0:
        return
    programs[:] = programs[-x:] + programs[:-x]

def exchange(programs, a, b):
    """Swap programs at positions a and b (modifies in-place)"""
    programs[a], programs[b] = programs[b], programs[a]

def partner(programs, name_a, name_b):
    """Swap programs named name_a and name_b (modifies in-place)"""
    idx_a = programs.index(name_a)
    idx_b = programs.index(name_b)
    programs[idx_a], programs[idx_b] = programs[idx_b], programs[idx_a]

# === Part 2 Specific Functions ===

def perform_dance(programs, moves):
    """Execute one complete dance sequence (modifies in-place)"""
    for move in moves:
        if not move:
            continue

        if move[0] == 's':
            spin(programs, int(move[1:]))
        elif move[0] == 'x':
            parts = move[1:].split('/')
            exchange(programs, int(parts[0]), int(parts[1]))
        elif move[0] == 'p':
            parts = move[1:].split('/')
            partner(programs, parts[0], parts[1])

def find_cycle_length(initial_state, moves):
    """Find cycle length by iterating until we return to initial state"""
    current = initial_state.copy()
    cycle_length = 0

    while True:
        perform_dance(current, moves)
        cycle_length += 1

        if current == initial_state:
            return cycle_length

        if cycle_length > 10_000_000:
            raise Exception("Cycle detection exceeded limit")

def verify_part1(moves):
    """Verify one iteration produces Part 1 answer"""
    initial = list('abcdefghijklmnop')
    perform_dance(initial, moves)
    result = ''.join(initial)
    expected = 'eojfmbpkldghncia'

    if result == expected:
        print(f"✓ Part 1 verification passed: {result}")
        return True
    else:
        print(f"✗ Part 1 verification FAILED!")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")
        return False

def solve(target_iterations=1_000_000_000):
    """Solve for the given number of iterations"""
    # Read input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]

    # Initial state
    initial = list('abcdefghijklmnop')

    # Find cycle length
    print("Finding cycle length...")
    cycle_length = find_cycle_length(initial, moves)
    print(f"Cycle detected at length: {cycle_length}")

    # Calculate effective iterations
    effective_iterations = target_iterations % cycle_length
    if effective_iterations == 0:
        effective_iterations = cycle_length

    print(f"Effective iterations: {target_iterations} % {cycle_length} = {effective_iterations}")

    # Apply dance effective_iterations times
    current = initial.copy()
    for _ in range(effective_iterations):
        perform_dance(current, moves)

    result = ''.join(current)
    print(f"Final result: {result}")
    return result

def main():
    """Main entry point"""
    # Read input
    with open('input.md', 'r') as f:
        input_data = f.read().strip()
    moves = [m for m in input_data.split(',') if m]

    # Verify Part 1
    print("Verifying Part 1 answer...")
    if not verify_part1(moves):
        print("ERROR: Part 1 verification failed!")
        return

    # Solve Part 2
    print("\nSolving Part 2...")
    result = solve(1_000_000_000)
    print(f"\nFinal Answer: {result}")

if __name__ == '__main__':
    main()
```

## Counting Convention Clarification

To avoid off-by-one errors, we use this convention:
- **Iteration 0**: Initial state `abcdefghijklmnop` (before any dances)
- **Iteration 1**: State after 1 dance = `eojfmbpkldghncia` (Part 1 answer)
- **Iteration N**: State after N dances

When we find the cycle:
- We iterate until we return to the initial state
- If this takes `k` iterations, the cycle length is `k`
- Iteration `k` produces the same state as iteration 0

For the target of 1,000,000,000:
- We compute `1_000_000_000 % cycle_length`
- If the result is 0, we need `cycle_length` iterations (not 0)
- Otherwise, we need `result` iterations

## Expected Runtime Analysis

**Time Complexity**: O(cycle_length × moves_per_dance)
- Cycle detection phase: Iterates until return to initial state
- Expected cycle length: 10-1000 (based on permutation theory for 16 elements)
- Moves per dance: ~10,000
- Total operations: ~100,000 to ~10,000,000
- **Expected runtime**: < 1 second

**Space Complexity**: O(number_of_programs)
- Only storing current state and initial state: 2 × 16 elements
- **Expected memory**: < 1 KB

## Implementation Priority Checklist

1. ✓ Copy move functions from Part 1 (`spin`, `exchange`, `partner`)
2. ✓ Implement `perform_dance()` function
3. ✓ Implement `verify_part1()` and test that 1 dance gives Part 1 answer
4. ✓ Implement simple `find_cycle_length()` function
5. ✓ Implement `solve()` with proper modulo arithmetic
6. ✓ Add debugging output (cycle length, effective iterations)
7. ✓ Test with small values before running with 1 billion

## Key Differences from Critique's "Complex Approach"

The critique correctly identified that we should **NOT** use:
- Dictionary-based state tracking
- Complex tail-handling logic
- State caching for all iterations

Instead, we use the **simple approach**:
- Iterate until we return to initial state
- Count iterations to get cycle length
- Apply modulo arithmetic
- Iterate the effective number of times

This is simpler, clearer, and sufficient for this problem.
