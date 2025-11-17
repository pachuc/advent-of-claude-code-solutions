# Implementation Plan: Eggnog Container Combinations (Part 2)

## Problem Analysis

This is a constrained subset-sum problem with two phases:
1. Find the minimum number of containers that can hold exactly 150 liters
2. Count all combinations using exactly that minimum number of containers

**Input Size:** 20 containers
**Target Sum:** 150 liters
**Constraint:** Each container used at most once

## Algorithm Efficiency Considerations

- **Total Combinations:** With 20 containers, there are 2^20 = 1,048,576 possible subsets
- **Early Termination:** We can prune combinations that exceed 150 liters
- **Optimization Strategy:** Generate combinations incrementally by size (1 container, 2 containers, etc.) and stop once we find valid combinations at a certain size

### Chosen Approach: Iterative Combination Generation by Size

**Rationale:**
- Instead of generating all 2^20 subsets, generate combinations of size k (k=1, 2, 3, ...) until we find valid solutions
- Once we find the first size k that produces valid combinations summing to 150, we know k is the minimum
- Only need to count combinations at that specific size k
- Time Complexity: O(C(n,k) * k) where k is the minimum number of containers
- This is much more efficient than checking all 2^20 subsets

## Step-by-Step Implementation Plan

### Step 1: Input Parsing
**File:** `solution.py`
**Function:** `parse_input(filename)`

```python
def parse_input(filename):
    """
    Read and parse container sizes from input file.

    Returns:
        list[int]: List of container capacities
    """
```

**Implementation Details:**
- Open and read the input file (`input.md`)
- Parse each line as an integer
- Strip whitespace from each line to handle trailing/leading spaces
- Skip empty lines if present
- Return list of container sizes

### Step 2: Core Algorithm Function
**Function:** `find_minimum_container_ways(containers, target)`

```python
def find_minimum_container_ways(containers, target):
    """
    Find number of ways to use minimum containers to reach target sum.

    Args:
        containers: list of container sizes
        target: target volume (150)

    Returns:
        int: Number of ways using minimum containers
    """
```

**Implementation Details:**
1. Import `itertools.combinations` for generating combinations
2. Iterate through possible combination sizes (k = 1, 2, 3, ...)
3. For each size k:
   - Generate all combinations of k containers using `combinations(containers, k)`
   - Check each combination to see if sum equals target
   - If any valid combinations found, this k is the minimum
   - Count all valid combinations at this size k
   - Return the count
4. If no valid combinations found (shouldn't happen with valid input), return 0

**Pseudocode:**
```
for k from 1 to len(containers):
    valid_count = 0
    for each combination of k containers:
        if sum(combination) == target:
            valid_count += 1

    if valid_count > 0:
        return valid_count  # k is minimum, return count

return 0  # No solution found
```

### Step 3: Main Execution Function
**Function:** `main()`

```python
def main():
    """
    Main execution function.
    """
```

**Implementation Details:**
1. Define target volume as constant: `TARGET = 150`
2. Call `parse_input('input.md')` to get containers
   - Note: Input file is `input.md` (verified filename)
3. Call `find_minimum_container_ways(containers, TARGET)`
4. Print the result as a single integer with no additional formatting

### Step 4: Script Entry Point

```python
if __name__ == "__main__":
    main()
```

## Complete File Structure

```
solution.py
├── parse_input(filename) -> list[int]
├── find_minimum_container_ways(containers, target) -> int
└── main()
```

## Algorithm Complexity Analysis

**Time Complexity:**
- Best case: O(n) if single container equals 150
- Worst case: O(2^n) if we need to check all subsets
- Expected case: O(C(n, k)) where k is typically small (4-6 containers)
- For n=20, k=4: C(20,4) = 4,845 combinations (very manageable)

**Space Complexity:**
- O(k) for storing each combination
- O(1) for counting (no storage of all valid combinations needed)

## Key Implementation Notes

1. **No need for memoization:** We only traverse each size once and don't revisit
2. **Early termination:** Stop as soon as we find valid combinations at size k
3. **No recursion needed:** Use itertools.combinations for cleaner, more efficient code
4. **Simple counting:** Just increment counter, don't store combinations
5. **Edge cases handled:**
   - Empty container list: loop completes with 0 count
   - No valid solution: returns 0
   - Single container solution: found at k=1

## Expected Runtime

For the given input (20 containers, target 150):
- Estimated minimum containers: 4-6 (based on average container size ~27 liters)
- Estimated combinations to check: ~5,000-20,000
- Expected runtime: < 100ms on modern hardware

## Code Style

- Use clear variable names
- Add brief comments for clarity
- Keep functions focused and simple
- No complex data structures needed
- Direct, procedural approach
