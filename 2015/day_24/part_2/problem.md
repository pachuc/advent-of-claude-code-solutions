# Problem Report: Sleigh Package Balancing (4 Groups)

## Context
Santa needs to load packages onto his sleigh for Christmas Eve deliveries. The sleigh must be perfectly balanced to defy physics and fly. Santa initially forgot about the trunk compartment, so the packages must now be divided into FOUR equal-weight groups instead of three.

## Objective
Find the quantum entanglement (QE) of the optimal first group of packages.

## Problem Requirements

### Constraints
1. **Equal Weight Groups**: All packages must be divided into exactly FOUR groups, where each group has the exact same total weight
2. **All Packages Used**: Every package must be placed in exactly one group
3. **Minimize First Group Size**: The first group (passenger compartment) must contain the minimum possible number of packages to give Santa legroom
4. **Minimize Quantum Entanglement**: Among all valid configurations with the minimum number of packages in the first group, choose the one with the smallest quantum entanglement

### Quantum Entanglement Definition
The quantum entanglement of a group is the product of all package weights in that group.

Example: If the first group contains packages with weights [11, 4], then QE = 11 × 4 = 44

## Input Format
The input is a list of positive integers, one per line, representing the weight of each package.

Example input structure:
```
1
3
5
11
13
...
```

## Output Format
A single integer representing the quantum entanglement of the optimal first group.

## Solution Approach
1. Calculate the target weight per group: (sum of all package weights) ÷ 4
2. Find all possible combinations for the first group that sum to the target weight
3. Among these, identify the combinations with the minimum number of packages
4. For each minimum-size combination, verify that the remaining packages CAN be divided into three equal-weight groups (each with target weight)
5. Among all valid configurations, select the one with the smallest quantum entanglement
6. Return that quantum entanglement value

## Example
For packages with weights [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]:
- Total weight = 60
- Target weight per group = 60 ÷ 4 = 15

Some valid first groups with 2 packages (minimum):
- [11, 4] with QE = 44
- [10, 5] with QE = 50
- [8, 7] with QE = 56

The answer would be 44 (the smallest QE among minimum-size valid first groups).

## Key Considerations
- The problem only asks for the QE of the first group; we don't need to output the actual groups
- We must verify that the remaining packages can actually form three equal-weight groups (not just assume it's possible)
- Optimization is important as there may be many combinations to check
