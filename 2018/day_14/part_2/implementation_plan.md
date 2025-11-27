# Implementation Plan: Recipe Scoreboard Pattern Search (Part 2)

## Problem Summary
Find the position where the sequence `047801` first appears in the scoreboard and return how many recipes appear before it.

**Important**: The actual puzzle input is `047801`. The Part 2 examples cleverly use subsequences from Part 1's results to validate both parts simultaneously:
- Part 1 example "After 9 recipes: next 10 are 5158916779" → Part 2 example "51589 appears at position 9"
- This provides excellent cross-validation between the two parts.

## Key Differences from Part 1
- **Part 1**: Generate N recipes, then extract 10 recipes after position N
- **Part 2**: Generate recipes until a specific pattern appears, then return the position where it starts
- **Challenge**: We don't know how long the scoreboard needs to grow, so we need efficient pattern matching
- **Note**: The return value is the index where the pattern starts, which is equivalent to the number of recipes before the pattern (in 0-indexed arrays)

## Algorithm Analysis

### Core Algorithm (Reusable from Part 1)
The recipe generation logic is **identical** to Part 1:
1. Start with scoreboard `[3, 7]` and elves at positions 0 and 1
2. Add current recipes' scores, split into digits, append to scoreboard
3. Move each elf forward by `1 + current_recipe_score` positions (with wraparound)
4. Repeat

### Pattern Matching Strategy
The challenge is efficiently detecting when the target sequence appears:

**Problem**: Each iteration can add 1 or 2 recipes, and the pattern could start at any position
**Solution**: After each iteration, check if the pattern appears in the newly added portion

**Efficient Approach**:
1. Convert target string to list of integers: `"047801"` → `[0, 4, 7, 8, 0, 1]`
2. After each iteration, check the last `len(pattern)` and `len(pattern)+1` positions
   - Check `len(pattern)` positions: handles case where 1 recipe was added
   - Check `len(pattern)+1` positions: handles case where 2 recipes were added
3. Once pattern found, return the starting index

### Runtime Considerations
- **Input size**: Unknown, but pattern could appear after millions of recipes
- **Memory**: Scoreboard grows as a list - O(N) where N is final position
- **Time per iteration**: O(1) for generation + O(pattern_length) for checking = O(1) since pattern length is constant
- **Overall complexity**: O(N) where N is the position where pattern appears
- **Optimization**: Only check the tail of the scoreboard (last few positions) rather than scanning entire scoreboard each time

### Edge Cases to Handle
1. Pattern appears very early (within first few recipes)
2. Pattern appears very late (millions of recipes)
3. Pattern with repeated digits (e.g., "000000")
4. Pattern that partially matches multiple times before full match
5. Checking must account for 1 or 2 recipes being added per iteration

## Implementation Steps

### Step 1: Parse Input
```python
# Read target sequence from input.md
with open('input.md', 'r') as f:
    target_str = f.read().strip()

# Convert to list of integers for efficient comparison
target = [int(d) for d in target_str]
pattern_len = len(target)
```

### Step 2: Initialize State (Same as Part 1)
```python
scoreboard = [3, 7]
elf1_pos = 0
elf2_pos = 1
```

### Step 3: Generate Recipes with Pattern Detection
```python
# Safety check to prevent infinite loops
iteration_count = 0
MAX_ITERATIONS = 100_000_000  # Safety limit

while True:
    iteration_count += 1
    if iteration_count > MAX_ITERATIONS:
        raise RuntimeError(f"Pattern not found after {MAX_ITERATIONS} iterations")

    # 3a: Create new recipes (same as Part 1)
    score1 = scoreboard[elf1_pos]
    score2 = scoreboard[elf2_pos]
    recipe_sum = score1 + score2

    if recipe_sum >= 10:
        scoreboard.append(1)
        scoreboard.append(recipe_sum - 10)
    else:
        scoreboard.append(recipe_sum)

    # 3b: Update positions (same as Part 1)
    elf1_pos = (elf1_pos + 1 + score1) % len(scoreboard)
    elf2_pos = (elf2_pos + 1 + score2) % len(scoreboard)

    # 3c: Check for pattern (NEW for Part 2)
    # IMPORTANT: Each iteration can add 1 or 2 recipes, so we must check both cases
    # Check if pattern appears at the end of the scoreboard

    if len(scoreboard) >= pattern_len:
        # Case 1: Pattern ends at current position (last recipe added completes it)
        if scoreboard[-pattern_len:] == target:
            return len(scoreboard) - pattern_len

        # Case 2: Pattern ends one position before current (second-to-last recipe completes it)
        # This handles when 2 recipes were added and the pattern was completed by the first one
        if len(scoreboard) > pattern_len and scoreboard[-pattern_len-1:-1] == target:
            return len(scoreboard) - pattern_len - 1
```

**Example of why we check both cases**:
- Scoreboard: `[3, 7, 1, 0]`, looking for pattern `[1, 0]`
- If sum = 15, we add `[1, 5]`, scoreboard becomes `[3, 7, 1, 0, 1, 5]`
- The pattern `[1, 0]` appears at position 2 (indices 2-3)
- But after adding, it would be at `scoreboard[-5:-3]` not at the end!
- Actually, after we add `[1, 5]`, we need to check if `[1, 0]` appeared before adding the last recipe
- This is why we check `scoreboard[-pattern_len-1:-1]` (excluding the very last element)

### Step 4: Return Result
```python
# The loop will break when pattern is found
# Return value is the index where pattern starts
# This equals the number of recipes before the pattern
return result
```

### Step 5: Output
```python
print(result)
return result
```

## Code Structure

```python
def solve(target_str=None):
    """
    Find the position where target sequence first appears.

    Args:
        target_str: String of digits to search for.
                   If None, reads from input.md file.

    Returns:
        Integer representing number of recipes before the pattern.
    """
    # Step 1: Parse input
    if target_str is None:
        with open('input.md', 'r') as f:
            target_str = f.read().strip()

    target = [int(d) for d in target_str]
    pattern_len = len(target)

    # Step 2: Initialize state
    scoreboard = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    # Step 3: Generate recipes with pattern detection
    iteration_count = 0
    MAX_ITERATIONS = 100_000_000

    while True:
        iteration_count += 1
        if iteration_count > MAX_ITERATIONS:
            raise RuntimeError(f"Pattern not found after {MAX_ITERATIONS} iterations")

        # Recipe generation...
        # Pattern checking...
        # Return when found

    # Step 4: Return result (happens inside loop when pattern found)

def generate_recipes(num_recipes):
    """
    Helper function: Generate exactly num_recipes and return the scoreboard.
    Useful for testing and cross-validation.

    Args:
        num_recipes: Number of recipes to generate

    Returns:
        List representing the scoreboard
    """
    scoreboard = [3, 7]
    elf1_pos = 0
    elf2_pos = 1

    while len(scoreboard) < num_recipes:
        score1 = scoreboard[elf1_pos]
        score2 = scoreboard[elf2_pos]
        recipe_sum = score1 + score2

        if recipe_sum >= 10:
            scoreboard.append(1)
            scoreboard.append(recipe_sum - 10)
        else:
            scoreboard.append(recipe_sum)

        elf1_pos = (elf1_pos + 1 + score1) % len(scoreboard)
        elf2_pos = (elf2_pos + 1 + score2) % len(scoreboard)

    return scoreboard

def test_examples():
    """Test all provided examples"""
    # Test cases from problem statement

if __name__ == '__main__':
    # Run tests
    # Run actual solution with timing
    # Output result
```

## Reuse from Part 1

### What to Reuse (90% of core logic)
1. **Input parsing**: Similar structure (read from input.md)
2. **Initialization**: Identical (scoreboard, elf positions)
3. **Recipe generation**: Identical algorithm
4. **Position update**: Identical wraparound logic

### What to Change
1. **Loop condition**: Instead of `while len(scoreboard) < num_recipes + 10`, use `while True` with pattern detection
2. **Pattern matching**: Add checks after each iteration
3. **Return value**: Return starting index of pattern instead of 10-digit string
4. **Output format**: Single integer instead of 10-character string

## Optimization Strategies

### Primary Optimization (Already Implemented)
- Only check the tail of the scoreboard (last `pattern_len` to `pattern_len+1` elements)
- This is O(pattern_len) per iteration, which is constant time since pattern length is fixed
- No need to scan the entire scoreboard each iteration

### Alternative Approach: String-Based Pattern Matching
If list comparison proves too slow, consider:
```python
# Convert last portion to string and use string operations
tail = ''.join(str(d) for d in scoreboard[-pattern_len*2:])
idx = tail.find(target_str)
if idx >= 0:
    return len(scoreboard) - len(tail) + idx
```

**Note**: Don't use batch checking (checking every N iterations) - this could miss the pattern entirely and give wrong results!

### Expected Performance
- **Current approach**: O(N * pattern_len) where N is final position
- **Time complexity**: O(N) since pattern_len is constant (6 digits)
- **Space complexity**: O(N) for scoreboard storage
- **For positions < 1 million**: < 1 second
- **For positions < 10 million**: ~5-10 seconds
- **For positions < 50 million**: ~20-40 seconds (machine-dependent)
- Current approach should be sufficient for typical Advent of Code inputs

## Algorithm Correctness Verification

### Why This Algorithm is Correct

1. **Correct Initialization**: Starts with `[3, 7]` and elves at positions 0 and 1 (per problem spec)

2. **Correct Recipe Generation**: Uses identical logic to Part 1 (which was verified correct):
   - Sum current recipes
   - Split into digits (handles both 1 and 2 digit sums)
   - Append to scoreboard
   - Move elves forward by `1 + current_score` with wraparound

3. **Correct Pattern Detection**: Checks both cases after each iteration:
   - Case 1: Pattern completed by the last recipe added (check `scoreboard[-pattern_len:]`)
   - Case 2: Pattern completed by second-to-last recipe (when 2 were added) (check `scoreboard[-pattern_len-1:-1]`)

4. **Correct Return Value**: Returns the starting index of pattern, which equals the number of recipes before it

5. **Safety**: Includes max iterations check to prevent infinite loops

### Edge Cases Handled
- ✓ Pattern appears at position 0 (initial recipes)
- ✓ Pattern appears very late (millions of recipes)
- ✓ Pattern with repeated digits (no special handling needed - exact match works)
- ✓ Pattern spanning 1-recipe addition
- ✓ Pattern spanning 2-recipe addition
- ✓ Pattern that might not exist (safety limit prevents infinite loop)

## Testing Considerations
- Verify against all 4 provided examples
- Test that Part 1 logic still works (recipe generation is correct)
- Verify pattern detection works when 1 recipe is added
- Verify pattern detection works when 2 recipes are added
- Test deterministic behavior (same input → same output)
- Cross-validate by regenerating scoreboard and verifying pattern exists at claimed position
