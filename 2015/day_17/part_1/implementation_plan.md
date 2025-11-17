# Implementation Plan: Container Combination Counter

## Problem Analysis

This is a classic **subset sum counting problem** where we need to count all possible combinations of containers that sum exactly to 150 liters.

**Key Insights:**
- We have 20 containers with various capacities
- Each container is distinct (even if capacities are identical)
- We need to count combinations, not permutations (order doesn't matter)
- Target sum: 150 liters
- Maximum possible combinations: 2^20 = 1,048,576 (worst case)

## Algorithm Selection

### Approach 1: Recursive Backtracking (RECOMMENDED)
**Time Complexity:** O(2^n) where n = 20
**Space Complexity:** O(n) for recursion stack
**Reasoning:** With only 20 containers, 2^20 = ~1 million combinations is computationally feasible. This approach is simple, clear, and efficient enough.

### Approach 2: Dynamic Programming
**Time Complexity:** O(n * target) where n = 20, target = 150
**Space Complexity:** O(target)
**Reasoning:** While DP is often more efficient for subset sum, for counting we'd need to track which containers were used, making it more complex without significant performance gain for n=20.

### Selected Approach: Recursive Backtracking
Given n=20, the recursive approach is optimal for clarity and performance.

## Step-by-Step Implementation Plan

### Step 1: Input Parsing
**File:** `solution.py`

```python
def parse_input(filename):
    """
    Read container capacities from input file.

    Args:
        filename: Path to input file (expected: 'input.md')

    Returns:
        list of integers representing container capacities
    """
    - Open and read the input file
    - Parse each line as an integer
    - Strip whitespace and skip empty lines
    - Basic validation: skip non-integer lines, filter out negative values
    - Return list of container capacities
```

**Implementation Details:**
- Read file line by line
- Strip whitespace from each line
- Skip empty lines
- Convert each line to integer
- Skip lines that can't be converted to integers (basic error handling)
- Filter out any negative values (containers can't have negative capacity)
- Return list of integers

**Assumptions:**
- Input file `input.md` exists in the same directory
- Input contains one integer per line
- Invalid lines are silently skipped (appropriate for competition-style problem)

### Step 2: Core Algorithm - Recursive Backtracking
**Function:** `count_combinations(containers, target)`

```python
def count_combinations(containers, target, index=0, current_sum=0):
    """
    Count all combinations of containers that sum to target.

    Args:
        containers: List of container capacities
        target: Target volume (150 liters)
        index: Current position in containers list
        current_sum: Running sum of selected containers

    Returns:
        Number of valid combinations
    """
```

**Algorithm Logic:**
1. **Base Cases (order matters for efficiency):**
   - If `current_sum == target`: Found valid combination, return 1
     - *Note: We return immediately because adding any more containers would exceed target*
     - *This is a pruning optimization that stops exploring this branch*
   - If `current_sum > target`: Invalid combination, return 0
     - *Prune this branch as we've exceeded the target*
   - If `index >= len(containers)`: No more containers to check, return 0
     - *We've exhausted all containers without reaching target*

2. **Recursive Cases:**
   - **Include current container:** Recurse with `current_sum + containers[index]` and `index + 1`
   - **Exclude current container:** Recurse with `current_sum` unchanged and `index + 1`
   - Return sum of both recursive calls

**Pseudocode:**
```
function count_combinations(containers, target, index, current_sum):
    // Base case: found exact match (can return immediately - pruning optimization)
    if current_sum == target:
        return 1

    // Base case: exceeded target (prune branch)
    if current_sum > target:
        return 0

    // Base case: no more containers to check
    if index >= len(containers):
        return 0

    // Recursive case: try including and excluding current container
    include = count_combinations(containers, target, index + 1, current_sum + containers[index])
    exclude = count_combinations(containers, target, index + 1, current_sum)

    return include + exclude
```

### Step 3: Optimization with Memoization (Optional - Not Required)
**Purpose:** Avoid redundant calculations if there are repeated subproblems

**Note:** For n=20, memoization is NOT necessary. We're unlikely to revisit the same state (index, sum) multiple times in this problem, so the basic recursive approach is sufficient. Memoization is mentioned here for completeness but should NOT be implemented unless performance issues are observed.

**Why memoization isn't needed:**
- Each path through the recursion tree is unique based on which containers are included/excluded
- With only 20 containers, the 2^20 ≈ 1M operations complete in well under a second
- The overhead of dictionary lookups for memoization might actually slow down the solution

### Step 4: Main Function
**Function:** `main()`

```python
def main():
    """
    Main execution function.
    """
    1. Parse input from 'input.md'
    2. Call count_combinations with containers and target=150
    3. Print the result
```

### Step 5: File Structure
**Complete solution.py structure:**

```python
def parse_input(filename):
    # Implementation from Step 1
    pass

def count_combinations(containers, target, index=0, current_sum=0):
    # Implementation from Step 2
    pass

def main():
    # Parse input
    containers = parse_input('input.md')

    # Count combinations
    result = count_combinations(containers, target=150)

    # Output result
    print(result)

if __name__ == '__main__':
    main()
```

## Implementation Order

1. **First:** Implement `parse_input()` function
2. **Second:** Implement `count_combinations()` recursive function
3. **Third:** Implement `main()` function to tie everything together
4. **Fourth:** Test with example data
5. **Fifth:** Run with actual input

## Edge Cases to Handle

1. **Empty input:** If no containers provided, return 0
2. **Impossible target:** If sum of all containers < target, return 0 (automatically handled by algorithm)
3. **Single container match:** If one container exactly equals target, count it (automatically handled)
4. **All containers too large:** If smallest container > target, return 0 (automatically handled)
5. **Target is 0:** Not applicable for this problem (target is always 150), but would return 1 (empty set)
6. **All containers equal target:** Each container is counted as separate combination (correctly handled by algorithm)

**Note:** Most edge cases are automatically handled by the recursive algorithm without special code. We only need to explicitly check for empty input.

## Performance Considerations

**Expected Performance:**
- Number of containers: 20
- Maximum recursion depth: 20
- Maximum number of function calls: 2^20 ≈ 1 million
- Expected runtime: < 1 second for modern hardware

**Why This is Efficient Enough:**
- With n=20, even brute force O(2^n) is fast
- No need for complex optimizations
- Clean, readable code is more valuable than micro-optimizations

## Alternative Implementation (Iterative with Bit Manipulation)

For reference, an alternative approach using bit manipulation:

```python
def count_combinations_iterative(containers, target):
    """
    Use bit manipulation to iterate through all 2^n subsets.
    """
    count = 0
    n = len(containers)

    # Iterate through all possible subsets (2^n combinations)
    for mask in range(1 << n):  # 2^n
        subset_sum = 0
        for i in range(n):
            if mask & (1 << i):  # Check if i-th bit is set
                subset_sum += containers[i]

        if subset_sum == target:
            count += 1

    return count
```

**Pros:** Simple, no recursion
**Cons:** Same O(2^n) complexity, less intuitive

Both approaches are valid; recursive backtracking is recommended for clarity.
