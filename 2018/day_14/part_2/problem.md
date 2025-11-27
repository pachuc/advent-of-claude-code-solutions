# Problem Report: Recipe Scoreboard Pattern Search (Part 2)

## Objective
Find the position where a specific sequence of recipe scores first appears in the scoreboard, and report how many recipes appear before it.

## Context from Part 1
Two Elves are generating recipes with quality scores (0-9). They maintain a scoreboard that grows as new recipes are created through a specific algorithm:

### Initial State
- Scoreboard starts with two recipes: `[3, 7]`
- Elf 1 starts at position 0 (recipe with score 3)
- Elf 2 starts at position 1 (recipe with score 7)

### Recipe Generation Algorithm

**Step 1: Create New Recipes**
- Add the scores of the two Elves' current recipes
- Split the sum into individual digits
- Append each digit as a new recipe score to the end of the scoreboard
- Examples:
  - Sum = 10 → creates two recipes: 1 and 0
  - Sum = 5 → creates one recipe: 5
  - Sum = 15 → creates two recipes: 1 and 5

**Step 2: Move to New Positions**
Each Elf moves forward in the scoreboard:
- Steps to move = 1 + (current recipe score)
- Movement wraps around to the beginning if the end is reached
- Example: If Elf 1's current recipe has score 3, they move forward 4 positions

**Step 3: Repeat**
Continue steps 1-2, growing the scoreboard indefinitely.

## Part 2 Task
Instead of finding the recipes that appear *after* a certain number of iterations, we need to find *when* a specific sequence of digits first appears in the scoreboard.

## Input
A sequence of digits representing recipe scores to search for.

**Given input:** `047801`

This means we are looking for the sequence `0, 4, 7, 8, 0, 1` appearing consecutively in the scoreboard.

## Output
A single integer representing the number of recipes that appear on the scoreboard **to the left of** (before) the first occurrence of the input sequence.

**Format:** A single integer (no formatting required)

## Examples
- Sequence `51589` first appears after `9` recipes (meaning 9 recipes exist before it)
- Sequence `01245` first appears after `5` recipes
- Sequence `92510` first appears after `18` recipes
- Sequence `59414` first appears after `2018` recipes

## Implementation Notes
- Continue the recipe generation algorithm until the target sequence appears in the scoreboard
- Need to check for the pattern after each recipe addition (since 1 or 2 recipes may be added per iteration)
- The answer is the index position where the sequence starts (i.e., the number of recipes before it)
- Optimization consideration: Since the scoreboard can grow very large, efficient pattern matching is important
- The pattern may appear at any point as the scoreboard grows - need to check continuously during generation
