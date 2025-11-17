# Implementation Plan: Cookie Recipe Optimization with Calorie Constraint

## Problem Overview
Maximize cookie recipe score using exactly 100 teaspoons of ingredients with exactly 500 calories constraint.

## Algorithm Choice: Exhaustive Search with Constraint Pruning

**Rationale**:
- With 4 ingredients and 100 teaspoons, the search space is manageable (~176,851 combinations without constraints)
- The calorie constraint dramatically reduces valid combinations
- Exhaustive search guarantees finding the global optimum
- Runtime: O(n^(k-1)) where n=100 teaspoons, k=number of ingredients → O(100^3) ≈ 1 million iterations for 4 ingredients (acceptable)
- **Note**: The implementation will support a variable number of ingredients for robustness

## Step-by-Step Implementation

### Step 1: Parse Input Data
**Goal**: Extract ingredient properties from input file

**Implementation**:
1. Read input file line by line
2. For each line, use regex to extract ingredient properties:
   - Pattern: `r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)'`
   - Ingredient name (for debugging, optional)
   - capacity, durability, flavor, texture, calories (integers, can be negative)
3. Store each ingredient as a dictionary with properties:
   ```python
   {
       'capacity': int,
       'durability': int,
       'flavor': int,
       'texture': int,
       'calories': int
   }
   ```
4. Store all ingredients in a list
5. **Input Validation**:
   - Verify file exists and is readable
   - Ensure at least one ingredient is parsed (raise error if empty)
   - Skip or warn about malformed lines

**Data Structure**: List of dictionaries
```python
ingredients = [
    {'capacity': 3, 'durability': 0, 'flavor': 0, 'texture': -3, 'calories': 2},
    {'capacity': -3, 'durability': 3, 'flavor': 0, 'texture': 0, 'calories': 9},
    # ... etc
]
```

### Step 2: Generate Valid Combinations
**Goal**: Iterate through all combinations of ingredient amounts that satisfy constraints

**Implementation**:
- Use a recursive generator function to handle variable number of ingredients
- This ensures the solution works regardless of how many ingredients are in the input
- For N ingredients, we need N-1 nested loops, with the last amount derived
- Recursive approach:
  ```python
  def generate_combinations(total, num_ingredients):
      """Generate all non-negative integer combinations that sum to total"""
      if num_ingredients == 1:
          yield [total]
      else:
          for i in range(0, total + 1):
              for rest in generate_combinations(total - i, num_ingredients - 1):
                  yield [i] + rest
  ```
- **Example for 4 ingredients**: Generates [a, b, c, d] where a+b+c+d=100
- **Optimization**: The last variable is derived, reducing complexity from O(n^k) to O(n^(k-1))

### Step 3: Filter by Calorie Constraint
**Goal**: Only process combinations with exactly 500 calories

**Implementation**:
1. For each combination of amounts, calculate total calories:
   ```python
   total_calories = sum(amounts[i] * ingredients[i]['calories'] for i in range(len(ingredients)))
   ```
2. Skip combinations where `total_calories != 500` using `continue` statement
3. **Optimization**: Calculate calories immediately after generating each combination and before calculating score:
   ```python
   for amounts in generate_combinations(100, len(ingredients)):
       if calculate_calories(amounts, ingredients) != 500:
           continue  # Skip to next combination without calculating score
       score = calculate_score(amounts, ingredients)
       # ... rest of logic
   ```
   This avoids the expensive score calculation for invalid combinations

### Step 4: Calculate Score for Valid Combinations
**Goal**: Compute the cookie score for each valid combination

**Implementation**:
1. For each property (capacity, durability, flavor, texture):
   ```python
   capacity_total = sum(amounts[i] * ingredients[i]['capacity'] for i in range(len(ingredients)))
   durability_total = sum(amounts[i] * ingredients[i]['durability'] for i in range(len(ingredients)))
   flavor_total = sum(amounts[i] * ingredients[i]['flavor'] for i in range(len(ingredients)))
   texture_total = sum(amounts[i] * ingredients[i]['texture'] for i in range(len(ingredients)))
   ```

2. Apply the "negative becomes zero" rule:
   ```python
   capacity_total = max(0, capacity_total)
   durability_total = max(0, durability_total)
   flavor_total = max(0, flavor_total)
   texture_total = max(0, texture_total)
   ```

3. Calculate final score:
   ```python
   score = capacity_total * durability_total * flavor_total * texture_total
   ```

**Note**: If any property total is 0 or negative (before max), the entire score becomes 0.

### Step 5: Track Maximum Score
**Goal**: Keep track of the best score found

**Implementation**:
1. Initialize `max_score = 0` before the loops
2. After calculating each valid combination's score:
   ```python
   if score > max_score:
       max_score = score
   ```
3. **Track the best combination for verification** (important for debugging and validation):
   ```python
   best_amounts = amounts.copy()
   ```
   This allows manual verification of the result

### Step 6: Output Result
**Goal**: Return or print the maximum score

**Implementation**:
1. After all iterations complete, output `max_score`
2. Format: Single integer on stdout

## Code Structure

```python
def parse_ingredients(filename):
    """Parse ingredient data from input file"""
    # Read and parse each line
    # Return list of ingredient dictionaries
    pass

def calculate_score(amounts, ingredients):
    """Calculate score for given ingredient amounts"""
    # Calculate property totals
    # Apply max(0, total) rule
    # Return product of all property totals
    pass

def calculate_calories(amounts, ingredients):
    """Calculate total calories for given amounts"""
    # Return sum of amount * calories
    pass

def find_max_score(ingredients, total_teaspoons=100, target_calories=500):
    """Find maximum score with constraints"""
    max_score = 0

    # Generate all valid combinations
    # For each combination:
    #   - Check calorie constraint
    #   - Calculate score
    #   - Update max_score

    return max_score

def main():
    import sys
    # Use command-line argument if provided, otherwise default to 'input.md'
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.md'

    ingredients = parse_ingredients(filename)
    result, best_amounts = find_max_score(ingredients)

    # Print result
    print(result)

    # Optional: Print best combination for verification
    # print(f"Best combination: {best_amounts}")
    # print(f"Calories: {calculate_calories(best_amounts, ingredients)}")
```

## Optimization Considerations

### Time Complexity
- **Worst case**: O(n^(k-1)) where n=100, k=number of ingredients
- **For 4 ingredients**: O(100^3) = ~1,000,000 iterations
- **With calorie pruning**: Significantly fewer score calculations (only valid combinations)
- **Expected runtime**: 1-3 seconds on modern hardware
- **Maximum acceptable runtime**: < 5 seconds (allows for Python's interpreted nature and arithmetic operations)

### Space Complexity
- O(k) for storing ingredient data (k = number of ingredients)
- O(1) for tracking current combination and max score
- Total: O(k) which is negligible

### Micro-optimizations (if needed)
1. **Early termination**: If we find a score that seems optimal, we could potentially terminate early (but we can't know the optimum without checking all)
2. **Calorie-first filtering**: Calculate calories before computing all property totals
3. **Avoid redundant calculations**: Reuse property totals if possible
4. **Use numpy**: For very large inputs, numpy array operations might be faster

## Alternative Approaches Considered (and why not chosen)

### 1. Dynamic Programming
- **Issue**: Two constraints (teaspoons + calories) make DP state space complex
- **State**: Would need (teaspoons_used, calories_used, ingredients_considered) → large state space
- Not worth the complexity for this problem size

### 2. Integer Linear Programming
- **Issue**: Multiplying property totals makes this non-linear
- Would need specialized optimization libraries (scipy.optimize, CVXPY)
- Overkill for this problem size

### 3. Genetic Algorithm / Simulated Annealing
- **Issue**: No guarantee of finding global optimum
- Exhaustive search is fast enough for this problem

### 4. Branch and Bound
- Could potentially prune branches based on upper bounds
- Added complexity not justified given exhaustive search is already fast

## Implementation Priority
1. ✓ Parse input correctly
2. ✓ Generate all valid combinations (sum to 100)
3. ✓ Filter by calorie constraint
4. ✓ Calculate scores correctly (handle negatives)
5. ✓ Track and return maximum

## Edge Cases to Handle
1. All property totals are negative → score = 0 (handled by max(0, total))
2. No valid combination meets calorie constraint → return 0 (handled by max_score initialization)
3. Multiple combinations with same max score → any one is fine (we just need the score)
4. Zero teaspoons of some ingredients → valid combination (handled naturally by loops)
5. Input file doesn't exist → raise FileNotFoundError with helpful message
6. Input file is empty or has no valid ingredients → raise ValueError
7. Only 1 ingredient → still works (combination is [100])
8. Negative ingredient property values → handled correctly by parsing and max(0, total) in scoring
