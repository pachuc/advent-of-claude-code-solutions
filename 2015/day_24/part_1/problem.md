# Problem Report: Package Balancing and Quantum Entanglement Optimization

## Context
We need to divide a set of packages into three groups of equal weight, optimizing for specific criteria related to the first group.

## Objective
Find the quantum entanglement (QE) of the optimal first group of packages, where quantum entanglement is defined as the product of all package weights in that group.

## Input
- A list of positive integers representing package weights (one per line)
- Input file: `input.md`
- Example input contains weights: 1, 3, 5, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113

## Constraints
1. All packages must be used exactly once
2. The packages must be divided into exactly 3 groups
3. Each of the 3 groups must have the exact same total weight
4. The sum of all package weights must be divisible by 3 (for equal division to be possible)

## Optimization Criteria (in order of priority)
1. **Minimize the number of packages in Group 1** (the first group)
2. **Among configurations with the minimum number of packages in Group 1, choose the one with the smallest quantum entanglement**

Notes:
- Only Group 1 needs to be minimized in terms of package count
- Groups 2 and 3 can have any number of packages, as long as their weights equal Group 1's weight
- We only need to verify that Groups 2 and 3 CAN be formed with the remaining packages

## Expected Output
A single integer: the quantum entanglement (product of weights) of the optimal first group.

## Algorithm Approach
1. Calculate the total weight of all packages
2. Verify it's divisible by 3; if not, no solution exists
3. Calculate target weight per group = total_weight / 3
4. Starting with the smallest possible group size, find all combinations of packages that sum to the target weight
5. For each valid Group 1 combination (in order of increasing size):
   - Verify that the remaining packages can be split into two groups of equal weight (target weight each)
   - Calculate the quantum entanglement (product of package weights in Group 1)
6. Return the smallest quantum entanglement among all valid configurations with the minimum group size

## Example
Given packages with weights 1, 2, 3, 4, 5, 7, 8, 9, 10, 11:
- Total weight: 60
- Target weight per group: 20
- Minimum packages in Group 1: 2 packages
- Optimal Group 1: [11, 9] with QE = 99
- Groups 2 and 3 can be: [10, 8, 2] and [7, 5, 4, 3, 1]

**Answer: 99**
