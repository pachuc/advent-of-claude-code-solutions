# Implementation Plan: Plant Growth Simulation (Part 2)

## Overview
Simulate 50 billion generations of plant growth by detecting pattern stabilization and extrapolating rather than brute-force simulation.

## Updates Based on Critique
This plan has been updated to address the following key improvements:

1. **Added Pattern Consistency Verification (Step 3.5):** After detecting a pattern repetition, verify it continues for 3 more generations to prevent false positives from temporary matches or longer cycles.

2. **Enhanced Steady State Detection (Step 3):** Updated `detect_steady_state()` to call the new verification function and added clear documentation about generation numbering (gen=0 is initial state).

3. **Added Integer Rate Assertion (Step 4):** Added assertion in `calculate_rate_of_change()` to verify the rate is an exact integer, catching potential logic errors.

4. **Enhanced Main Function (Step 6):** Added verbose mode for debugging output, return value for testing, and detailed intermediate information printing.

5. **Clarified Implementation Order:** Provided explicit step-by-step instructions for copying Part 1 code and building on it.

## Core Strategy
1. Reuse Part 1's simulation logic for parsing and generation stepping
2. Run simulation until pattern stabilizes (same relative plant positions)
3. Detect steady state where pattern shifts by constant amount per generation
4. Extrapolate to generation 50 billion using linear projection

## Step-by-Step Implementation

### Step 1: Reuse Part 1 Foundation
**File:** Adapt from `part_1_solution.py`

Reuse existing functions:
- `parse_input(filename)`: Parse initial state and rules (unchanged)
- `get_pattern(pot, state)`: Get 5-character pattern for a pot (unchanged)
- `simulate_generation(state, rules)`: Simulate one generation (unchanged)

**Rationale:** The core simulation logic is identical; only the termination condition changes.

### Step 2: Implement Pattern Normalization
**Purpose:** Compare plant patterns independent of their absolute positions

```python
def normalize_pattern(state):
    """
    Normalize the state to make it position-independent.
    Returns the pattern relative to the leftmost plant.

    Args:
        state: Set of pot indices with plants

    Returns:
        frozenset: Relative positions (offset from leftmost plant)
    """
    if not state:
        return frozenset()

    min_pot = min(state)
    # Create a normalized pattern by subtracting the minimum
    normalized = frozenset(pot - min_pot for pot in state)
    return normalized
```

**Why frozenset:** Allows pattern comparison and hashing for cycle detection.

### Step 3: Implement Steady State Detection
**Purpose:** Detect when the pattern stops changing shape (only shifts)

```python
def detect_steady_state(initial_state, rules, max_generations=1000):
    """
    Simulate until pattern stabilizes or max_generations reached.

    Note on generation numbering:
        - gen=0 represents the initial state (before any simulation)
        - gen=1 represents state after 1 generation of simulation
        - When we check at loop iteration gen=N, we're checking the state
          after N generations have been simulated

    Returns:
        tuple: (generation_number, state, sum_of_indices, prev_gen, prev_state, prev_sum)
               If no pattern found: last 3 values will be None

    Algorithm:
        1. Track pattern history: {normalized_pattern: (generation, state, sum)}
        2. For each generation:
            a. Normalize the pattern (relative positions)
            b. Check if this normalized pattern was seen before
            c. If yes: verify shift is consistent over next few generations
            d. If no: continue simulating
        3. Return when stable pattern confirmed or max_generations reached
    """
    state = initial_state
    history = {}

    for gen in range(max_generations):
        normalized = normalize_pattern(state)
        current_sum = sum(state)

        if normalized in history:
            # Pattern repeats! Verify it's truly stable
            prev_gen, prev_state, prev_sum = history[normalized]

            # Verify consistency by checking next 3 generations
            if verify_pattern_consistency(state, normalized, rules, num_checks=3):
                return (gen, state, current_sum, prev_gen, prev_state, prev_sum)
            # If verification fails, continue (though this should be rare)

        history[normalized] = (gen, state, current_sum)
        state = simulate_generation(state, rules)

    # Fallback: return last state if no pattern found
    return (max_generations, state, sum(state), None, None, None)
```

**Key insight:** If the normalized pattern repeats, the plants have the same relative positions but shifted.

### Step 3.5: Verify Pattern Consistency
**Purpose:** Confirm that pattern continues to shift consistently (not a cycle)

```python
def verify_pattern_consistency(state, expected_normalized, rules, num_checks=3):
    """
    Verify that the pattern continues to match over the next few generations.

    This ensures we have a true steady state (consistent shift) rather than
    a longer cycle or temporary pattern match.

    Args:
        state: Current state to verify from
        expected_normalized: The normalized pattern we expect to see
        rules: Spreading rules
        num_checks: Number of generations to verify (default 3)

    Returns:
        bool: True if pattern is consistent, False otherwise
    """
    test_state = state
    for _ in range(num_checks):
        test_state = simulate_generation(test_state, rules)
        test_normalized = normalize_pattern(test_state)
        if test_normalized != expected_normalized:
            return False
    return True
```

**Why this matters:** Prevents false positives from temporary pattern matches or longer cycles.

### Step 4: Calculate Rate of Change
**Purpose:** Determine how much the sum increases per generation in steady state

```python
def calculate_rate_of_change(gen, current_sum, prev_gen, prev_sum):
    """
    Calculate the rate at which the sum changes per generation.

    Args:
        gen: Current generation where pattern repeated
        current_sum: Sum of pot indices at current generation
        prev_gen: Previous generation where this pattern appeared
        prev_sum: Sum at previous generation

    Returns:
        int: Change in sum per generation
    """
    generations_elapsed = gen - prev_gen
    sum_change = current_sum - prev_sum

    # Verify the rate is an exact integer (should always be true for this problem)
    assert sum_change % generations_elapsed == 0, \
        f"Rate should be exact integer: {sum_change} / {generations_elapsed}"

    # Rate of change per generation
    rate = sum_change // generations_elapsed

    return rate
```

**Example:** If at gen 100 sum=5000, and at gen 101 sum=5050 (same pattern), rate = 50/generation.

### Step 5: Extrapolate to 50 Billion Generations
**Purpose:** Use linear projection to calculate final sum

```python
def extrapolate_to_target(target_generation, steady_gen, steady_sum, rate):
    """
    Extrapolate the sum at target generation using steady state.

    Args:
        target_generation: Target (50 billion)
        steady_gen: Generation where steady state was detected
        steady_sum: Sum at steady state generation
        rate: Change in sum per generation

    Returns:
        int: Projected sum at target generation
    """
    remaining_generations = target_generation - steady_gen
    final_sum = steady_sum + (remaining_generations * rate)

    return final_sum
```

**Formula:** `final_sum = current_sum + (50_billion - current_gen) × rate`

### Step 6: Main Function Integration
**Purpose:** Orchestrate the entire solution

```python
def main(verbose=False):
    """
    Main function to solve Part 2.

    Args:
        verbose: If True, print debugging information

    Returns:
        int: The final sum at 50 billion generations
    """
    TARGET_GENERATION = 50_000_000_000

    # Parse input (reuse Part 1)
    initial_state, rules = parse_input('input.md')

    # Detect steady state
    result = detect_steady_state(initial_state, rules, max_generations=1000)
    gen, state, current_sum, prev_gen, prev_state, prev_sum = result

    # Check if steady state was found
    if prev_gen is None:
        # No pattern found - should not happen with valid input
        print("No steady state detected")
        return None

    # Calculate rate of change
    rate = calculate_rate_of_change(gen, current_sum, prev_gen, prev_sum)

    if verbose:
        print(f"Steady state detected at generation {gen}")
        print(f"Previous occurrence at generation {prev_gen}")
        print(f"Pattern repeats every {gen - prev_gen} generation(s)")
        print(f"Current sum: {current_sum}")
        print(f"Rate of change: {rate} per generation")
        print(f"Number of plants: {len(state)}")
        print(f"Extrapolating to generation {TARGET_GENERATION:,}...")

    # Extrapolate to 50 billion
    final_sum = extrapolate_to_target(TARGET_GENERATION, gen, current_sum, rate)

    print(final_sum)
    return final_sum


if __name__ == '__main__':
    main()
```

## Algorithm Complexity

### Time Complexity
- **Simulation phase:** O(N × M) where N = generations until steady state (~100-1000), M = number of pots per generation (~100-200)
- **Expected:** O(100,000) operations - extremely fast
- **Space:** O(N × M) for history tracking

### Why This Works
- Plant patterns governed by deterministic rules must eventually stabilize
- The state space is finite (for practical pot ranges)
- Once stable, the pattern shifts linearly (each plant moves same direction)
- Linear shift means constant rate of sum change

## Edge Cases to Handle

1. **Empty state:** Should not occur but handle gracefully
2. **No steady state in 1000 generations:** Increase max_generations (unlikely)
3. **Pattern oscillates vs shifts:** Current approach handles shifts; true cycles are unlikely with typical rules
4. **Very early stabilization:** Works fine, just less simulation needed

## Data Structures

- **state:** `set` of integers (pot indices with plants) - O(1) lookup, efficient for sparse data
- **normalized pattern:** `frozenset` - hashable for dictionary keys
- **history:** `dict` mapping patterns to generation data - O(1) lookups

## File Structure
```
solution.py
├── parse_input()              # From Part 1 (unchanged)
├── get_pattern()              # From Part 1 (unchanged)
├── simulate_generation()      # From Part 1 (unchanged)
├── normalize_pattern()        # New for Part 2
├── verify_pattern_consistency() # New for Part 2
├── detect_steady_state()      # New for Part 2
├── calculate_rate_of_change() # New for Part 2
├── extrapolate_to_target()    # New for Part 2
└── main()                     # Modified from Part 1
```

## Implementation Order
1. **Copy Part 1 solution as base**
   - `cp part_1_solution.py solution.py`
   - Keep: `parse_input()`, `get_pattern()`, `simulate_generation()`

2. **Add pattern detection functions**
   - Implement `normalize_pattern()` function
   - Implement `verify_pattern_consistency()` function

3. **Implement steady state detection**
   - Implement `detect_steady_state()` with pattern tracking
   - Include verification step for consistency

4. **Add calculation helpers**
   - Implement `calculate_rate_of_change()` with assertion
   - Implement `extrapolate_to_target()`

5. **Update main function**
   - Replace old `main()` with new version
   - Add verbose mode for debugging
   - Add return value for testing

6. **Test implementation**
   - Run with verbose=True to see detection details
   - Verify Part 1 compatibility (20 generations = 2767)
   - Run full solution for Part 2
