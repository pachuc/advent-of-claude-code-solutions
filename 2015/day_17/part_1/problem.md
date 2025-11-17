# Problem Report: Container Combination Counter

## Objective
Find the number of different combinations of containers that can exactly fit a specific target volume of liquid (150 liters).

## Context
We need to store 150 liters of eggnog into a refrigerator by distributing it across various smaller containers. Each container must be either completely filled or not used at all. We need to count how many different ways we can select containers to exactly match the target volume.

## Input
- **Target volume**: 150 liters
- **Available containers**: A list of container capacities (in liters), provided as integers, one per line

The input file contains 20 container capacities:
```
33, 14, 18, 20, 45, 35, 16, 35, 1, 13, 18, 13, 50, 44, 48, 6, 24, 41, 30, 42
```

## Rules
1. Each container must be used entirely or not at all (no partial filling)
2. Multiple containers can have the same capacity, but they are considered distinct containers
3. Different combinations using the same container sizes in different orders count as the same combination
4. We need combinations that sum exactly to the target volume (150 liters)

## Example
Given containers of size: 20, 15, 10, 5, 5 liters
Target volume: 25 liters

There are **4 valid combinations**:
1. 15 + 10 = 25
2. 20 + 5 (first container) = 25
3. 20 + 5 (second container) = 25
4. 15 + 5 + 5 = 25

Note that combinations 2 and 3 are counted separately because they use different physical containers, even though both are 5-liter containers.

## Expected Output
A single integer representing the total number of distinct combinations of containers that sum exactly to 150 liters.

## Algorithm Approach
This is a combinatorial problem similar to the "subset sum" problem where we need to count all subsets of the container list that sum to exactly 150. Since containers with identical capacities are treated as distinct, we need to consider each container individually by its position in the input list.
