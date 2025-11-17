# Problem Report: Cookie Recipe Optimization with Calorie Constraint

## Objective
Find the highest-scoring cookie recipe using exactly 100 teaspoons of ingredients, with the constraint that the total calorie count must be exactly 500 calories.

## Context
We are creating a cookie recipe by mixing ingredients. Each ingredient has multiple properties that contribute to the overall cookie score. This is an optimization problem where we need to maximize the score while satisfying both the ingredient quantity constraint (100 teaspoons total) and the calorie constraint (exactly 500 calories).

## Input Format
The input consists of multiple ingredient definitions, one per line. Each line follows this format:
```
IngredientName: capacity X, durability Y, flavor Z, texture W, calories C
```

Where X, Y, Z, W, and C are integers (can be negative for capacity, durability, flavor, and texture).

### Example Input:
```
Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8
```

## Constraints
1. Must use exactly 100 teaspoons total (sum of all ingredient amounts = 100)
2. Must have exactly 500 calories total
3. Each ingredient amount must be a non-negative integer (0 or more teaspoons)

## Scoring Algorithm
1. For each property (capacity, durability, flavor, texture):
   - Calculate the total by summing: (teaspoons of ingredient × property value) for each ingredient
   - If the total for any property is negative, treat it as 0

2. Multiply the four property totals together to get the final score:
   - Score = capacity_total × durability_total × flavor_total × texture_total

3. Calculate total calories separately:
   - Total calories = sum of (teaspoons of ingredient × calories) for each ingredient

Note: The calorie property is NOT used in score calculation; it's only used for the constraint.

## Example
With 40 teaspoons butterscotch and 60 teaspoons cinnamon:
- If this combination results in exactly 500 calories (40×8 + 60×3 = 500)
- The score would be 57,600,000

## Expected Output
A single integer representing the maximum possible score for a cookie recipe that:
- Uses exactly 100 teaspoons of ingredients
- Has exactly 500 total calories

## Algorithm Approach
This requires finding the optimal distribution of 100 teaspoons across all available ingredients such that:
1. The calorie constraint (exactly 500) is satisfied
2. The score is maximized
3. All ingredient amounts are non-negative integers

This is a constrained optimization problem that can be solved by:
- Iterating through all valid combinations of ingredient amounts that sum to 100 and have exactly 500 calories
- Calculating the score for each valid combination
- Returning the maximum score found
