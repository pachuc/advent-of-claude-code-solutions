# Problem Report: Eggnog Container Combinations (Part 2)

## Context
This is a combinatorial optimization problem involving fitting exactly 150 liters of eggnog into containers of various sizes.

## Objective
Find how many different ways you can use the **minimum number of containers** to hold exactly 150 liters of eggnog.

This is a two-step problem:
1. First, determine the minimum number of containers needed to hold exactly 150 liters
2. Then, count how many different combinations use exactly that minimum number of containers

## Input
- A target volume: **150 liters**
- A list of container sizes (in liters), one per line
- Each container can only be used once (no duplicates of the same container)

The input file contains 20 containers with the following capacities (in liters):
```
33, 14, 18, 20, 45, 35, 16, 35, 1, 13, 18, 13, 50, 44, 48, 6, 24, 41, 30, 42
```

## Expected Output
A single integer representing the number of different ways to select the minimum number of containers that sum to exactly 150 liters.

## Algorithm Requirements
1. Find all possible combinations of containers that sum to exactly 150 liters
2. Among these valid combinations, identify the minimum number of containers used
3. Count how many combinations use exactly this minimum number of containers
4. Return this count

## Example
Given containers [20, 15, 10, 5, 5]:
- To hold 25 liters, you could use:
  - [20, 5] (2 containers)
  - [20, 5] (2 containers, using the other 5)
  - [15, 10] (2 containers)
  - [15, 5, 5] (3 containers)
  - [10, 5, 5] (3 containers)
- The minimum number of containers is 2
- There are 3 ways to use exactly 2 containers
- Answer: 3

## Output Format
Output should be a single integer with no additional formatting.
