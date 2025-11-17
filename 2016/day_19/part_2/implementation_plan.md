# Implementation Plan - Part 2: Elf Gift Exchange (Across Circle)

## Problem Analysis

### Key Differences from Part 1
- **Part 1**: Eliminate next elf (constant distance of 1) - Classic Josephus with k=2
- **Part 2**: Eliminate elf across the circle (variable distance = floor(M/2) where M is remaining elves)
- **Part 1**: Has closed-form mathematical solution (2*L + 1 formula)
- **Part 2**: No known closed-form solution - requires simulation

### Constraints
- Input size: N = 3,017,957 elves
- Must handle ~3 million iterations efficiently
- Need efficient data structure for deletions
- Cannot use naive array approach with O(n) deletions (O(n²) total would be too slow)
- Note: Part 1's answer (1841611) is not needed for Part 2 - they are independent problems with the same N value

### Algorithm Choice
Use a **Python deque** (double-ended queue) for:
- O(k) deletion at arbitrary index where k is distance from nearest end (amortized, much better than O(n) for lists)
- O(1) navigation to next element
- Simple, clean implementation
- Built-in efficiency optimizations
- Expected performance: 2-5 seconds for N=3,017,957 (possibly up to 15 seconds)

**Why not reuse Part 1's linked list approach?**
Part 1 used a dictionary-based circular linked list (`next_elf = {i: i+1}`) which was optimal for eliminating the next elf (constant distance of 1). For Part 2, we need to eliminate the elf at distance ~n/2, which would require O(n/2) traversal with a linked list. In contrast, deque provides O(1) index access and O(k) deletion where k is distance from nearest end. For "across the circle" eliminations (near index n/2), deque is the better choice despite non-constant deletion time.

## Implementation Steps

### Step 1: Input Parsing (Reuse from Part 1)
```python
def read_input(filename='input.md'):
    """Read and parse the input file."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    match = re.search(r'\d+', content)
    if match:
        return int(match.group())
    raise ValueError("No integer found in input file")
```
- Reuse the regex-based parsing from part_1_solution.py
- Handles the input format robustly

### Step 2: Data Structure Implementation
Use `collections.deque` to store elf numbers:
- Store elf numbers directly in deque: `deque([1, 2, 3, ..., n])`
- Track current position as an index into the deque
- Navigate using modulo arithmetic for wraparound
- Delete elements efficiently with `del circle[index]`

### Step 3: Core Simulation Function
```python
def solve_across_circle(n, debug=False):
    """
    Simulate the elf gift exchange where each elf steals from
    the elf directly across the circle.

    Args:
        n: Total number of elves (1 to n)
        debug: If True, print each elimination step (default: False)
               Used for manual verification on small examples only

    Returns:
        The position number of the winning elf
    """
    if n == 1:
        return 1

    # Initialize circle with all elves
    from collections import deque
    circle = deque(range(1, n + 1))
    current_index = 0

    while len(circle) > 1:
        # Calculate position of elf across the circle
        # floor(M/2) positions away
        remaining = len(circle)
        across_offset = remaining // 2

        # Safety assertions: ensure valid state
        assert across_offset > 0, f"Invalid across_offset: {across_offset}"

        # Calculate target index (wrapping around)
        target_index = (current_index + across_offset) % remaining

        # Additional safety: ensure we never target ourselves
        assert target_index != current_index, "Cannot target self"

        # Debug output
        if debug:
            print(f"Circle: {list(circle)}, Current: {circle[current_index]} (idx={current_index}), "
                  f"Target: {circle[target_index]} (idx={target_index})")

        # Remove the elf across
        eliminated = circle[target_index]
        del circle[target_index]

        # Adjust current_index after deletion
        # If we deleted someone before current position, we shifted left
        if target_index < current_index:
            current_index -= 1
        # If target_index >= current_index, no adjustment needed
        # (current_index still points to the same elf)

        # Move to next elf in sequence (the elf after current in circle order)
        current_index = (current_index + 1) % len(circle)

    return circle[0]
```

### Step 4: Index Management Logic (CRITICAL)

This is the most error-prone part. Understanding what happens after deletion:

**Key Insight**: After deletion, we need to:
1. Adjust `current_index` if necessary to still point to the same elf
2. Move to the next elf in the circle (the elf that was after the current elf)

**Detailed Logic**:

1. **If target_index < current_index**:
   - We deleted someone before us in the deque
   - All elements after the deleted one (including us) shifted left by 1
   - Decrement current_index to compensate: `current_index -= 1`
   - Now current_index still points to the same elf as before deletion

2. **If target_index >= current_index**:
   - We deleted someone at or after us in the deque
   - Our position (current_index) is unaffected by the deletion
   - No adjustment needed

3. **Moving to next elf**:
   - After adjusting (if needed), current_index points to the same elf as before
   - The "next" elf is the next position in the circle: `(current_index + 1) % len(circle)`
   - Use modulo to handle wraparound when we're at the end

**Example Trace (n=5, see problem.md)**:
```
Initial: [1,2,3,4,5], current_index=0 (Elf 1)
- across=2, target=(0+2)%5=2 (Elf 3)
- Delete index 2 → [1,2,4,5]
- target(2) >= current(0), no adjustment
- Next: (0+1)%4=1 → Elf 2 ✓

Circle: [1,2,4,5], current_index=1 (Elf 2)
- across=2, target=(1+2)%4=3 (Elf 5)
- Delete index 3 → [1,2,4]
- target(3) >= current(1), no adjustment
- Next: (1+1)%3=2 → Elf 4 ✓

Circle: [1,2,4], current_index=2 (Elf 4)
- across=1, target=(2+1)%3=0 (Elf 1)
- Delete index 0 → [2,4]
- target(0) < current(2), adjust: current_index=1
- Next: (1+1)%2=0 → Elf 2 ✓

Circle: [2,4], current_index=0 (Elf 2)
- across=1, target=(0+1)%2=1 (Elf 4)
- Delete index 1 → [2]
- Winner: Elf 2 ✓
```

### Step 5: Main Function and Test Suite Structure
```python
def main():
    """Main function to solve the puzzle"""
    n = read_input()
    result = solve_across_circle(n)
    print(result)

def run_all_tests():
    """Run comprehensive test suite (see test_plan.md for details)"""
    print("\n" + "="*50)
    print("PART 2 TEST SUITE - ACROSS CIRCLE")
    print("="*50)

    # Run all tests (implementation details in test plan)
    test_example()
    test_edge_cases()
    test_sequential_small()
    test_powers_of_two()
    test_medium_values()
    test_actual_input()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)

if __name__ == '__main__':
    # Run tests first to validate correctness
    run_all_tests()
    print("\n=== Solution for Actual Input ===")
    main()
```

## Edge Cases to Handle

1. **n = 1**: Single elf wins immediately (return 1 without simulation)
2. **n = 2**: Two elves, across_offset=1, Elf 1 eliminates Elf 2, winner is Elf 1
3. **n = 5**: Provided example, should return 2 (CRITICAL validation)
4. **Even vs Odd remaining elves**: Different "across" calculations (floor division handles both)
5. **Wraparound**: When target index wraps past end of circle (modulo handles this)
6. **Self-targeting**: Never possible since across_offset >= 1 for n >= 2

## Performance Considerations

### Time Complexity
- **Per iteration**: O(k) amortized for deque deletion where k is distance from nearest end
- **Total iterations**: O(n) iterations (one elf eliminated per turn)
- **Overall**: O(n*k) average case, where k averages to n/4, giving O(n²/4) worst case
- **In practice**: For "across the circle" deletions near index n/2, k ≈ n/4. Despite this, deque's highly optimized C implementation makes it the best standard library choice.

### Space Complexity
- O(n) for storing the circle

### Expected Runtime
- For n = 3,017,957: Should complete in 2-10 seconds (possibly up to 15 seconds on slower machines)
- For n = 100,000: Should complete in under 2 seconds

## Testing Strategy Reference
- Start with example (n=5 → 2)
- Test edge cases (n=1, n=2, n=3, n=4)
- Test powers of 2 (n=8, 16, 32, etc.)
- Validate with manual simulation for small values
- Run on actual input (n=3,017,957)

## Implementation Order

1. Import required modules at module level:
   ```python
   import re
   from collections import deque
   ```
2. Copy read_input() from Part 1 (unchanged)
3. Implement solve_across_circle(n, debug=False) with deque
4. Handle edge case n=1 at the start
5. Add assertion: across_offset > 0
6. Implement index adjustment logic carefully
7. Add debug output capability
8. Implement all test functions (following test_plan.md)
9. Implement main() function
10. Add if __name__ == '__main__' guard with test suite
11. Run tests to validate correctness before submitting

## Potential Pitfalls and How to Avoid Them

1. **Off-by-one errors in "across" calculation**:
   - Use floor(M/2) which is `remaining // 2` in Python
   - Verify with n=5 example where across should be 2,2,1,1

2. **Index adjustment after deletion**:
   - Only decrement current_index if target_index < current_index
   - Remember: deletion shifts all subsequent elements left

3. **Next elf logic**:
   - After deletion and adjustment, current_index points to SAME elf
   - Next elf is always (current_index + 1) % len(circle)
   - Do NOT confuse "next elf" with "eliminated elf"

4. **Modulo arithmetic for wraparound**:
   - Always use % len(circle) after computing next index
   - Never access circle[index] without bounds checking

5. **Debug output is essential**:
   - Add debug=True parameter to trace first few eliminations
   - Verify against problem.md example step-by-step
   - Debug output should clearly show: current circle, current elf/position, target elf/position, result after elimination

6. **Assertions for safety**:
   - Assert across_offset > 0 to catch impossible states
   - Assert target_index != current_index to prevent self-targeting
   - These should always be true but catch bugs early

## Code Structure

```
solution.py
├── Imports (re, collections.deque)
├── read_input()                [Reused from Part 1, unchanged]
├── solve_across_circle(n, debug=False)  [New - core simulation logic]
├── test_example()              [Critical test: n=5 → 2]
├── test_edge_cases()           [Test n=1,2,3,4]
├── test_sequential_small()     [Pattern analysis n=1-20]
├── test_powers_of_two()        [Special cases]
├── test_medium_values()        [Performance check]
├── test_actual_input()         [Final answer validation]
├── run_all_tests()             [Test suite orchestrator]
├── main()                      [Main puzzle solver]
└── __name__ == '__main__' block [Run tests then main]
```

## Final Notes

- **Part 1's Josephus formula does NOT apply** - Part 2 requires simulation
- The simulation is mandatory because the elimination distance changes dynamically
- Focus on correct index management after deletions - this is where bugs hide
- The example walkthrough in problem.md (n=5 → 2) is crucial for validation
- With deque, expected runtime is 2-5 seconds for n=3,017,957 (possibly up to 10 seconds)
- Debug mode is essential for verifying correctness on small examples
- The assertions (`across_offset > 0` and `target_index != current_index`) provide safety against logic errors
- Part 1's testing structure can be adapted for Part 2
- **Key difference in testing**: Part 1 had formula cross-validation; Part 2 relies on manual step-by-step verification
