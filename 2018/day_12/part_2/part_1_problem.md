# Problem Report: Plant Growth Simulation

## Overview
We need to simulate the growth and spread of plants in numbered pots over 20 generations, following specific spreading rules.

## Problem Description

### Context
There is a row of pots arranged in a line, numbered with pot `0` in the center. Pots extend infinitely to the left (negative numbers: -1, -2, -3, ...) and to the right (positive numbers: 1, 2, 3, ...). Some pots contain plants and others are empty.

### Input Format
The input consists of two parts:

1. **Initial State**: A line that starts with `initial state: ` followed by a string of `#` (plant present) and `.` (empty pot) characters. This represents the state of pots starting from pot 0 and extending to the right.
   - Example: `initial state: #..#.#..##......###...###`
   - In this example, pot 0 has a plant (`#`), pots 1-2 are empty (`.`), pot 3 has a plant, etc.

2. **Spreading Rules**: Multiple lines in the format `LLCRR => N` where:
   - `LLCRR` is a 5-character pattern representing: two pots to the left (LL), current pot (C), two pots to the right (RR)
   - `N` is either `#` (plant will be present) or `.` (pot will be empty) in the next generation
   - Each pattern can contain `#` (plant) or `.` (empty)
   - Example: `.##.# => #` means if the pattern is `.##.#`, then the center pot will have a plant in the next generation

### Simulation Rules
For each generation:
1. For each pot, examine a 5-pot window: the pot itself, 2 pots to its left, and 2 pots to its right
2. Match this pattern against the spreading rules
3. Apply the rule to determine if the pot will have a plant in the next generation
4. All pots outside the initial state start as empty (`.`)
5. The row can grow to the left and right as needed (assume infinite pots)

### Task
Simulate exactly **20 generations** of plant growth starting from the initial state.

### Expected Output
After 20 generations, calculate the **sum of the numbers (pot indices) of all pots that contain a plant**.

For example:
- If after 20 generations, plants are in pots -2, 0, 3, and 34
- The answer would be: -2 + 0 + 3 + 34 = 35

### Output Format
A single integer representing the sum of all pot numbers containing plants after 20 generations.

### Example
Given the example in the puzzle:
- Initial state: `#..#.#..##......###...###`
- After 20 generations, plants span from pot -2 to pot 34
- Sum of all pot numbers with plants = **325**
