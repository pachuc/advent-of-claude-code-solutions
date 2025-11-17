# Problem Report: Cookie Recipe Optimization

## Objective
Find the optimal combination of ingredient amounts to maximize the total score of a cookie recipe.

## Context
We are creating a cookie recipe that uses exactly 100 teaspoons of ingredients total. Each ingredient has multiple properties that contribute to the cookie's overall score. We need to determine how many teaspoons of each ingredient to use to achieve the highest possible score.

## Input Format
The input consists of a list of ingredients, where each ingredient is described on a single line with the following format:

```
IngredientName: capacity X, durability Y, flavor Z, texture W, calories C
```

Where:
- `IngredientName` is the name of the ingredient
- `capacity`, `durability`, `flavor`, `texture` are property values (can be positive or negative integers)
- `calories` is a positive integer (not used in score calculation for this part)

Example input:
```
Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8
```

## Constraints
1. Must use exactly 100 teaspoons of ingredients in total
2. Can only use whole teaspoon amounts (integers)
3. All teaspoon amounts must be non-negative (≥ 0)

## Scoring Algorithm
1. For each property (capacity, durability, flavor, texture):
   - Calculate the total by summing: (teaspoons of ingredient i) × (property value for ingredient i) for all ingredients
   - If the total is negative, replace it with 0

2. Multiply all four property totals together to get the final score
   - Note: calories are NOT included in the score calculation

3. Find the combination of teaspoon amounts that produces the maximum score

## Example Calculation
Given two ingredients:
- Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
- Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

Using 44 teaspoons of Butterscotch and 56 teaspoons of Cinnamon:
- Capacity: 44×(-1) + 56×2 = 68
- Durability: 44×(-2) + 56×3 = 80
- Flavor: 44×6 + 56×(-2) = 152
- Texture: 44×3 + 56×(-1) = 76

Total score: 68 × 80 × 152 × 76 = 62,842,880

## Expected Output
A single integer representing the maximum total score achievable with the given ingredients.

Format: `[integer value]`

Example: `62842880`
