# Implementation Plan: Plant Growth Simulation

## Problem Analysis

We need to simulate cellular automaton-like plant growth over 20 generations where each pot's next state depends on a 5-pot window (2 left, self, 2 right) matching against given rules.

### Key Observations:
1. **Infinite grid**: Pots extend infinitely left (negative) and right (positive)
2. **Local rules**: Each pot's next state depends only on itself and 4 neighbors
3. **Fixed iterations**: Exactly 20 generations (small number, no need for pattern detection)
4. **Sparse representation**: Most pots will be empty, so we should track only plant positions
5. **Bounded growth**: In 20 generations, plants can spread at most 2 pots per generation in each direction (based on the rule window size), giving a practical upper bound of roughly 40 pots expansion from the initial boundary

### Algorithm Choice:
**Data Structure**: Use a dictionary/set to store pot indices that contain plants (sparse representation)
- Time complexity: O(n) per generation where n = number of pots to check
- Space complexity: O(m) where m = number of pots with plants

### Runtime Considerations:
- Initial state string has ~100 characters (mix of plants and empty pots)
- After 20 generations, we'll have at most a few hundred pots to track
- Total runtime will be O(20 * n) which is very manageable

## Step-by-Step Implementation Plan

### Step 1: Parse Input
**Goal**: Extract initial state and spreading rules from input

**Implementation**:
1. Read all lines from input file
2. Parse first line to extract initial state:
   - Split on `: ` to get the state string
   - Enumerate through the state string, where index i corresponds to pot i
   - Add index i to the set if state[i] == '#'
   - Pot 0 corresponds to index 0 of the state string
   - Example:
     ```python
     initial_state = set()
     state_string = line.split(': ')[1].strip()
     for i, char in enumerate(state_string):
         if char == '#':
             initial_state.add(i)
     ```
3. Parse rule lines (skip empty lines):
   - Split each line on ` => `
   - Store pattern (5-char string) as key
   - Store result ('#' or '.') as value
   - Use a dictionary for O(1) lookup

**Data structures**:
```python
current_state = set()  # Set of pot indices with plants
rules = {}  # Dict mapping 5-char pattern to result char
```

### Step 2: Implement Pattern Matching Function
**Goal**: For a given pot index, determine the 5-character pattern

**Implementation**:
1. Create function `get_pattern(pot_index, state)`:
   - For positions [pot_index-2, pot_index-1, pot_index, pot_index+1, pot_index+2]
   - Check if each position exists in the state set
   - Build string with '#' if in set, '.' if not
   - Return 5-character pattern string

**Example**:
```python
def get_pattern(pot, state):
    pattern = ""
    for i in range(pot - 2, pot + 3):
        pattern += '#' if i in state else '.'
    return pattern
```

### Step 3: Determine Range of Pots to Check
**Goal**: Efficiently determine which pots need to be evaluated each generation

**Implementation**:
1. For each generation, we only need to check pots near existing plants
2. Find minimum and maximum pot indices with plants
3. Expand range by 2 in each direction (since rules check 2 pots away)
4. Check all pots in range [min_pot - 2, max_pot + 2]

**Rationale**:
- A pot can only get a plant if there's a plant within 2 pots of it
- This keeps our search space minimal and proportional to plant spread

**Example**:
```python
min_pot = min(current_state) - 2
max_pot = max(current_state) + 2
```

### Step 4: Simulate One Generation
**Goal**: Apply rules to transition from one generation to the next

**Implementation**:
1. Create new empty set for next generation
2. Determine range of pots to check (Step 3)
3. For each pot in range:
   - Get the 5-character pattern (Step 2)
   - Look up pattern in rules dictionary
   - If rule result is '#', add pot to next generation set
   - If pattern not in rules, default to '.' (no plant)
4. Replace current_state with next generation set

**Example**:
```python
def simulate_generation(state, rules):
    # Handle empty state edge case
    if not state:
        return set()

    next_state = set()
    # Expand range by 2 in each direction since rules check 2 pots away
    min_pot = min(state) - 2
    max_pot = max(state) + 2

    for pot in range(min_pot, max_pot + 1):
        pattern = get_pattern(pot, state)
        # Use .get() to default to '.' for patterns not in rules
        if rules.get(pattern, '.') == '#':
            next_state.add(pot)

    return next_state
```

### Step 5: Run Simulation for 20 Generations
**Goal**: Iterate the simulation exactly 20 times

**Implementation**:
1. Initialize state with parsed initial state
2. Loop 20 times:
   - Call simulate_generation function
   - Update current_state with result
3. Keep track of generation count for debugging

**Example**:
```python
state = initial_state
for generation in range(20):
    state = simulate_generation(state, rules)
```

### Step 6: Calculate Final Sum
**Goal**: Sum all pot indices that contain plants after 20 generations

**Implementation**:
1. After 20 generations, sum all elements in the final state set
2. Return/print the result

**Example**:
```python
result = sum(state)
print(result)
```

## Complete Program Structure

```
1. Main function:
   a. Parse input (Step 1)
   b. Initialize state
   c. Run 20 generations (Step 5, which uses Steps 2-4)
   d. Calculate and output sum (Step 6)

2. Helper functions:
   a. parse_input(filename) -> (initial_state, rules)
   b. get_pattern(pot, state) -> pattern_string
   c. simulate_generation(state, rules) -> next_state
```

## Edge Cases to Handle

1. **Empty state**: If state becomes empty, min/max will fail
   - Solution: Check if state is empty before finding min/max
   - If empty, skip generation or return empty

2. **Pattern not in rules**: Some 5-char patterns might not be in input (not all 32 possible patterns may be present)
   - Solution: Use dict.get(pattern, '.') to default to empty pot
   - This assumes missing patterns result in no plant, which is the logical default

3. **Negative pot indices**: Pots can be negative
   - Solution: Sets and range() handle negative numbers correctly

4. **Initial state offset**: Initial state starts at pot 0
   - Solution: When parsing, enumerate from index 0

## Optimization Notes

- Using a set for state is optimal: O(1) membership testing
- Dictionary for rules is optimal: O(1) pattern lookup
- Only checking relevant pot range keeps each generation fast
- No need for further optimization given 20 iterations and small input

## Expected Complexity

- **Time**: O(20 * n) where n is the number of pots to check per generation (~hundreds)
- **Space**: O(m) where m is the number of pots with plants (~hundreds)
- **Total runtime**: Negligible (< 1 second)
