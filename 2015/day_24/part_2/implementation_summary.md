# Implementation Summary: Sleigh Package Balancing (4 Groups)

## Problem Overview
Santa needs to divide packages into 4 equal-weight groups for his sleigh. The objective is to find the minimum quantum entanglement (QE) of the first group, where:
- All 4 groups must have the same total weight
- The first group should have the minimum number of packages
- Among all minimum-size first groups, we want the one with the smallest QE (product of weights)

## Solution Approach

### Algorithm
The solution uses an iterative approach with backtracking and memoization:

1. **Calculate target weight**: Sum all packages and divide by 4
2. **Generate first group candidates**: Use `itertools.combinations` to try all possible first groups, starting from size 1
3. **Filter by weight**: Only consider combinations that sum to the target weight
4. **Verify remaining packages**: For each candidate first group, verify that the remaining packages can be split into 3 equal-weight groups
5. **Track minimum QE**: Among all valid configurations at the minimum size, track the smallest quantum entanglement
6. **Early termination**: Once we find valid configurations at size k, stop searching (don't check size k+1)

### Key Implementation Details

#### Helper Functions

1. **`calculate_qe(group)`**: Uses `math.prod()` to calculate the product of all weights in a group

2. **`get_remaining(packages, first_group)`**: Uses `collections.Counter` to correctly handle duplicate package weights when removing the first group

3. **`can_split_into_three_groups(packages, target)`**: Verifies that remaining packages can form 3 equal-weight groups using recursive backtracking

4. **`can_split_into_n_groups_cached(packages_tuple, target, n_groups)`**: Cached recursive function using `@lru_cache` for efficient memoization. This is critical for performance with 28 packages.

#### Optimization Techniques

1. **Early termination**: Stop searching once we find valid configurations at the minimum first group size
2. **Memoization**: Use `@lru_cache` on the recursive verification function to avoid redundant subset sum calculations
3. **Counter-based removal**: Use `collections.Counter` to correctly handle duplicate weights without index confusion

## Files Created

- **solution.py**: Main solution file containing all implementation code

## Testing Process

### Test Results

#### 1. Example Test Case
- **Input**: [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
- **Expected QE**: 44
- **Actual QE**: 44
- **Status**: PASSED ✓

#### 2. Actual Input Test
- **Input**: 28 prime numbers from input.md
- **Total weight**: 1524
- **Target per group**: 381
- **Minimum first group size**: 5 packages
- **Best first group**: [1, 59, 101, 107, 113]
- **Quantum Entanglement**: **72050269**
- **Status**: PASSED ✓

#### 3. Edge Cases

All edge cases passed successfully:

| Test | Input | Expected | Actual | Status |
|------|-------|----------|--------|--------|
| 3.1: Not divisible by 4 | [1, 2, 3] | None | None | PASSED ✓ |
| 3.3: Perfect equal groups | [5,5,5,5,5,5,5,5] | 25 | 25 | PASSED ✓ |
| 3.4: Single element group | [10,5,5,5,5,5,5] | 10 | 10 | PASSED ✓ |
| 3.5: All same weight | [3,3,3,3,3,3,3,3,3,3,3,3] | 27 | 27 | PASSED ✓ |

### Verification

The solution was verified to be correct:
- The first group [1, 59, 101, 107, 113] sums to exactly 381 ✓
- The remaining 23 packages can be split into 3 groups of 381 each ✓
- The QE calculation (1 × 59 × 101 × 107 × 113 = 72050269) is correct ✓
- The first group size (5) is minimal - no valid configuration exists with 4 or fewer packages ✓

## Performance

- The solution completed in under 60 seconds
- Memoization significantly improved performance by caching subset sum computations
- Early termination prevented unnecessary exploration of larger first group sizes

## Final Answer

**Minimum Quantum Entanglement: 72050269**

This is the quantum entanglement of the optimal first group [1, 59, 101, 107, 113] when dividing all packages into 4 equal-weight groups.
