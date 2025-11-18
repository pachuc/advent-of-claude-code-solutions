# Problem Report: Recursive Circus - Balancing the Tower (Part 2)

## Context from Part 1
We have a tower of programs arranged in a tree structure. Programs are stacked on top of each other, with one program at the bottom (root) supporting the entire tower. Each program holds a disc, and other programs can be balanced on that disc. In Part 1, we found that the bottom program is `wiapj`.

### Input Format (Same as Part 1)
The input is an unordered list of program descriptions. Each line contains:
- **Program name**: A string identifier
- **Weight**: An integer in parentheses - this is the program's OWN weight only
- **Children programs** (optional): If the program holds a disc with other programs on it, their names are listed after `->` and separated by commas

Example:
```
pbga (66)
fwft (72) -> ktlj, cntj, xhth
tknk (41) -> ugml, padx, fwft
```

## Part 2 Objective
The tower is currently **unbalanced** because exactly one program has the wrong weight. We need to find:
1. Which program has the wrong weight
2. What its weight should be to balance the entire tower

## Understanding Tower Balance

### Total Weight Calculation
The **total weight** (or "tower weight") of a program is:
- Its own weight PLUS
- The sum of the total weights of all programs above it (all its descendants)

### Balance Requirement
For a program's disc to be balanced:
- All programs standing directly on that disc must have the **same total weight**
- This means each sub-tower must weigh the same

### Example from Puzzle
For the example tree where `tknk` is at the bottom:
- `ugml` has weight 68 and holds `gyxo` (61), `ebii` (61), `jptl` (61)
  - Total weight of `ugml` = 68 + 61 + 61 + 61 = **251**
- `padx` has weight 45 and holds `pbga` (66), `havc` (66), `qoyq` (66)
  - Total weight of `padx` = 45 + 66 + 66 + 66 = **243**
- `fwft` has weight 72 and holds `ktlj` (57), `cntj` (57), `xhth` (57)
  - Total weight of `fwft` = 72 + 57 + 57 + 57 = **243**

For `tknk`'s disc to be balanced, all three sub-towers should weigh the same, but:
- `ugml`'s total weight is 251 (8 units too heavy)
- `padx` and `fwft` both have total weight 243

The problem is that `ugml` itself weighs 68, but should weigh 60 (8 units lighter) to make its total weight 243.

## Expected Output
A single integer: the corrected weight that the wrong program should have to balance the entire tower.

For the example above, the answer would be: `60`

## Algorithm Approach

1. **Parse the input** to build the tree structure:
   - Create a mapping of each program to its own weight
   - Create a mapping of each program to its children

2. **Calculate total weights** recursively:
   - For each program, calculate its total weight (own weight + sum of all children's total weights)

3. **Find the imbalanced program**:
   - Starting from the root, check each program's children
   - If children have different total weights, one is wrong
   - The imbalance will propagate up, so find the DEEPEST (lowest in the tree) imbalanced program

4. **Determine the correction**:
   - Find which child's total weight is different from its siblings
   - Calculate the difference between the wrong weight and the correct weight
   - The program's own weight needs to be adjusted by this difference

## Important Notes
- Exactly **one** program has the wrong weight
- The wrong program could be anywhere in the tree (not necessarily at the bottom)
- The imbalance will affect all ancestor nodes, so we need to find the actual source of the imbalance (the program whose own weight is wrong, not its descendants)
- All children of a balanced disc must have the same total weight, so if one is different, it's the problematic one
