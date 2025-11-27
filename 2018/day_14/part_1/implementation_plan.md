# Implementation Plan: Recipe Scoreboard Simulation

## Problem Summary
Simulate a recipe generation process where two elves create new recipes based on their current positions on a scoreboard. Find the 10 recipe scores that appear immediately after a specific number of recipes (47801) have been created.

## Algorithm Analysis

### Time Complexity
- We need to generate at least `n + 10` recipes (where n = 47801)
- Each iteration adds 1-2 recipes to the scoreboard
- Expected iterations: ~24,000-48,000
- Each iteration involves:
  - Constant time addition and digit splitting: O(1)
  - Constant time position updates with modulo: O(1)
- **Overall time complexity: O(n)** where n is the input number

### Space Complexity
- We need to store all recipes up to index `n + 10`
- **Space complexity: O(n)** for the scoreboard list

### Efficiency Considerations
- For n = 47801, we need ~48,000 recipes total
- Python list append is amortized O(1), which is efficient
- Using a list is more efficient than alternatives (deque, string concatenation)
- The algorithm is already optimal for this problem

## Step-by-Step Implementation Plan

### Step 1: Parse Input
- Read the input file `input.md`
- Extract the integer value (47801)
- Strip any whitespace or newlines
- Convert to integer for use in calculations

**Implementation details:**
```python
with open('input.md', 'r') as f:
    num_recipes = int(f.read().strip())
```

### Step 2: Initialize the Scoreboard State
- Create a list to represent the scoreboard: `[3, 7]`
- Initialize Elf 1's position: `elf1_pos = 0`
- Initialize Elf 2's position: `elf2_pos = 1`

**Implementation details:**
```python
scoreboard = [3, 7]
elf1_pos = 0
elf2_pos = 1
```

### Step 3: Implement the Recipe Generation Loop
Create a while loop that continues until we have enough recipes.

**Loop condition:**
```python
while len(scoreboard) < num_recipes + 10:
```

**Loop body:**

#### 3a. Calculate New Recipes
- Get current recipe scores for both elves
- Add them together to get the sum
- Convert sum to digits (handle both single and double-digit sums)

**Implementation approaches:**
- Option 1: String conversion: `[int(d) for d in str(sum_value)]`
- Option 2: Mathematical: Check if sum >= 10, then split manually
- **Recommended: Option 2** for better performance

```python
score1 = scoreboard[elf1_pos]
score2 = scoreboard[elf2_pos]
recipe_sum = score1 + score2

if recipe_sum >= 10:
    scoreboard.append(1)
    scoreboard.append(recipe_sum - 10)
else:
    scoreboard.append(recipe_sum)
```

#### 3b. Update Elf Positions
- Calculate steps to move: 1 + current recipe score
- Use modulo to wrap around the scoreboard
- **Important timing:** Positions are calculated AFTER new recipes are added to the scoreboard

**The sequence is:**
1. Read current scores from elf positions (BEFORE adding new recipes)
2. Add new recipes to scoreboard (scoreboard length increases)
3. Calculate new positions using the UPDATED scoreboard length

```python
elf1_pos = (elf1_pos + 1 + score1) % len(scoreboard)
elf2_pos = (elf2_pos + 1 + score2) % len(scoreboard)
```

**Why this matters:** The modulo operation uses the current (updated) length of the scoreboard to ensure positions wrap correctly. The scores (score1, score2) were captured before adding recipes, but the position calculation uses the new length.

### Step 4: Extract the Result
- Once we have enough recipes, extract the 10 scores starting at index `num_recipes`
- Convert the list of digits to a string

**Implementation details:**
```python
result = ''.join(str(score) for score in scoreboard[num_recipes:num_recipes + 10])
```

### Step 5: Output the Result
- Print the result to stdout
- Optionally write to an output file

```python
print(result)
```

## Complete Code Structure

```python
def solve(num_recipes=None):
    """
    Solve the recipe scoreboard problem.

    Args:
        num_recipes: Number of recipes to skip before extracting result.
                    If None, reads from input.md file.

    Returns:
        String of 10 digits representing the next 10 recipe scores.
    """
    # Step 1: Parse input
    if num_recipes is None:
        with open('input.md', 'r') as f:
            num_recipes = int(f.read().strip())

    # Step 2: Initialize state
    scoreboard = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    # Step 3: Generate recipes
    while len(scoreboard) < num_recipes + 10:
        # 3a: Create new recipes
        score1 = scoreboard[elf1_pos]
        score2 = scoreboard[elf2_pos]
        recipe_sum = score1 + score2

        if recipe_sum >= 10:
            scoreboard.append(1)
            scoreboard.append(recipe_sum - 10)
        else:
            scoreboard.append(recipe_sum)

        # 3b: Update positions
        elf1_pos = (elf1_pos + 1 + score1) % len(scoreboard)
        elf2_pos = (elf2_pos + 1 + score2) % len(scoreboard)

    # Step 4: Extract result
    result = ''.join(str(score) for score in scoreboard[num_recipes:num_recipes + 10])

    # Step 5: Output
    print(result)
    return result

if __name__ == '__main__':
    solve()
```

## Optimization Considerations

### Current Approach is Optimal
- List operations are efficient for this problem size
- No need for advanced data structures
- The algorithm itself is inherently sequential

### Potential Micro-optimizations (not necessary)
- Pre-allocate list size if memory is a concern
- Use local variable caching for frequently accessed values
- These would provide minimal benefit for n=47801

## Edge Cases Handled
1. **Sum creates two digits (>= 10):** Handled by if-else check
2. **Position wrapping:** Handled by modulo operator
3. **Exactly 10 recipes needed:** Loop condition ensures we have at least n+10 recipes
4. **Initial state:** Correctly initialized with [3, 7] and positions 0, 1

## Expected Runtime
- For n = 47801: Well under 1 second on modern hardware (likely 100-300ms)
- The algorithm is efficient enough for the given input
- No optimization needed beyond the straightforward implementation

## Key Implementation Details (Summary)

### Critical Points to Remember:
1. **Position update timing:** Read scores BEFORE adding recipes, but calculate new positions AFTER adding recipes (using the updated scoreboard length)
2. **Digit splitting:** For sum >= 10, add [1, sum-10]; for sum < 10, add [sum]
3. **Parameterized function:** Accept optional `num_recipes` parameter to facilitate testing
4. **Loop condition:** Continue until `len(scoreboard) >= num_recipes + 10`
5. **Result extraction:** Extract 10 consecutive scores starting at index `num_recipes`

### Testing Strategy:
- Test against all 4 provided examples first (n=5, 9, 18, 2018)
- Verify first 10 recipes (n=0) match expected pattern: `3710101245`
- Ensure runtime < 1 second for n=47801
- Verify deterministic behavior (same result on multiple runs)
