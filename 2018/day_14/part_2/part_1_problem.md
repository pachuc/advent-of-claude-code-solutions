# Problem Report: Recipe Scoreboard Simulation

## Objective
Simulate a recipe generation process on a scoreboard and find the scores of 10 recipes that appear immediately after a specific number of recipes have been created.

## Context
Two Elves are generating recipes with quality scores (0-9). They maintain a scoreboard that grows as new recipes are created through a specific algorithm. We need to determine what the next 10 recipe scores will be after a certain number of recipes have been generated.

## Initial State
- Scoreboard starts with two recipes: `[3, 7]`
- Elf 1 starts at position 0 (recipe with score 3)
- Elf 2 starts at position 1 (recipe with score 7)

## Algorithm

### Step 1: Create New Recipes
- Add the scores of the two Elves' current recipes
- Split the sum into individual digits
- Append each digit as a new recipe score to the end of the scoreboard
- Examples:
  - Sum = 10 → creates two recipes: 1 and 0
  - Sum = 5 → creates one recipe: 5
  - Sum = 15 → creates two recipes: 1 and 5

### Step 2: Move to New Positions
Each Elf moves forward in the scoreboard:
- Steps to move = 1 + (current recipe score)
- Movement wraps around to the beginning if the end is reached
- Example: If Elf 1's current recipe has score 3, they move forward 4 positions

### Step 3: Repeat
Continue steps 1-2 until enough recipes have been generated.

## Input
A single integer representing the number of recipes after which we want to find the next 10 scores.

**Given input:** `047801` (which is 47801)

## Output
A string of 10 digits representing the scores of the 10 recipes immediately after the input number of recipes have been created.

**Format:** A 10-character string containing only digits 0-9 (no spaces or separators)

## Examples
- After 9 recipes: next 10 scores are `5158916779`
- After 5 recipes: next 10 scores are `0124515891`
- After 18 recipes: next 10 scores are `9251071085`
- After 2018 recipes: next 10 scores are `5941429882`

## Implementation Notes
- The scoreboard continuously grows as recipes are added
- Positions wrap around using modulo arithmetic
- The simulation must continue until at least (input + 10) recipes exist on the scoreboard
- Extract recipes at indices [input, input+1, ..., input+9] from the scoreboard
