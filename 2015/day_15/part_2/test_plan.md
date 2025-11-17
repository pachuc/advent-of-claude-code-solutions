# Test Plan: Cookie Recipe Optimization with Calorie Constraint

## Testing Strategy
Verify correctness through unit tests, integration tests, and validation against known examples.

## Test Categories

### 1. Input Parsing Tests

#### Test 1.1: Parse Example Input
**Objective**: Verify correct parsing of the provided example input

**Input**:
```
Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
Sprinkles: capacity -3, durability 3, flavor 0, texture 0, calories 9
Candy: capacity -1, durability 0, flavor 4, texture 0, calories 1
Chocolate: capacity 0, durability 0, flavor -2, texture 2, calories 8
```

**Expected Output**:
```python
[
    {'capacity': 3, 'durability': 0, 'flavor': 0, 'texture': -3, 'calories': 2},
    {'capacity': -3, 'durability': 3, 'flavor': 0, 'texture': 0, 'calories': 9},
    {'capacity': -1, 'durability': 0, 'flavor': 4, 'texture': 0, 'calories': 1},
    {'capacity': 0, 'durability': 0, 'flavor': -2, 'texture': 2, 'calories': 8}
]
```

**Verification**: Check each ingredient's properties match expected values

#### Test 1.2: Handle Negative Values
**Objective**: Ensure parser correctly handles negative property values

**Method**: Verify that negative values in capacity, durability, flavor, texture are preserved as integers

#### Test 1.3: Handle Edge Case Inputs
**Objective**: Verify parser handles malformed or edge case inputs appropriately

**Test Cases**:
1. Empty input file → raise ValueError with helpful message
2. File with only whitespace or comments → raise ValueError
3. Single ingredient → parse successfully, return list with one element
4. Malformed line (missing properties) → skip line or raise clear error

**Verification**: Assert appropriate error handling or graceful degradation

---

### 2. Calorie Calculation Tests

#### Test 2.1: Basic Calorie Calculation
**Objective**: Verify calorie calculation logic

**Test Case**:
- Ingredients: `[{calories: 2}, {calories: 9}, {calories: 1}, {calories: 8}]`
- Amounts: `[25, 25, 25, 25]`
- Expected: `25*2 + 25*9 + 25*1 + 25*8 = 50 + 225 + 25 + 200 = 500`

**Verification**: Assert `calculate_calories([25, 25, 25, 25], ingredients) == 500`

#### Test 2.2: Example Calorie Constraint
**Objective**: Verify calorie calculation with actual input ingredients

**Test Case**:
- Ingredients: Sugar (2 cal), Sprinkles (9 cal), Candy (1 cal), Chocolate (8 cal)
- Find a combination that equals exactly 500 calories
- Example: Let's verify a specific combination works
  - Try [21, 29, 40, 10]: 21×2 + 29×9 + 40×1 + 10×8 = 42 + 261 + 40 + 80 = 423 (not 500)
  - Try [0, 44, 12, 44]: 0×2 + 44×9 + 12×1 + 44×8 = 0 + 396 + 12 + 352 = 760 (not 500)
  - Need to find valid combination through algorithm or manual calculation

**Verification**: Confirm that at least one valid combination exists with exactly 500 calories

#### Test 2.3: Zero Amount
**Objective**: Ensure zero amounts don't contribute to calories

**Test Case**:
- Amounts: `[100, 0, 0, 0]`
- Expected: Only first ingredient's calories count

---

### 3. Score Calculation Tests

#### Test 3.1: Basic Score Calculation
**Objective**: Verify score calculation with all positive property totals

**Test Case**:
- Amounts: `[50, 50, 0, 0]`
- Ingredients:
  ```python
  [
      {'capacity': 2, 'durability': 3, 'flavor': 4, 'texture': 5},
      {'capacity': 1, 'durability': 1, 'flavor': 1, 'texture': 1}
  ]
  ```
- Expected property totals:
  - Capacity: 50*2 + 50*1 = 150
  - Durability: 50*3 + 50*1 = 200
  - Flavor: 50*4 + 50*1 = 250
  - Texture: 50*5 + 50*1 = 300
- Expected score: 150 * 200 * 250 * 300 = 2,250,000,000

**Verification**: Assert calculated score matches expected

#### Test 3.2: Negative Property Totals Become Zero
**Objective**: Verify max(0, total) logic for negative property totals

**Test Case 1**: One negative property
- Property totals: [100, -50, 200, 150]
- After max(0, x): [100, 0, 200, 150]
- Expected score: 100 * 0 * 200 * 150 = 0

**Test Case 2**: All negative properties
- Property totals: [-10, -20, -30, -40]
- After max(0, x): [0, 0, 0, 0]
- Expected score: 0

**Verification**: Assert score is 0 when any property total is negative

#### Test 3.3: Zero in Property Totals
**Objective**: Verify that zero in any property results in zero score

**Test Case**:
- Property totals: [100, 0, 200, 150]
- Expected score: 0 (due to multiplication by zero)

---

### 4. Combination Generation Tests

#### Test 4.1: Sum Constraint
**Objective**: Verify all generated combinations sum to exactly 100

**Method**:
- Generate all combinations using the combination generator
- For each combination, assert `sum(amounts) == 100`
- Since this is a fundamental requirement, verify ALL combinations (not just a sample)
- Can test a subset for performance, but the generator logic must guarantee this property

#### Test 4.2: Non-Negative Constraint
**Objective**: Ensure all amounts are non-negative

**Method**:
- For each generated combination
- Assert `all(amount >= 0 for amount in amounts)`

#### Test 4.3: Calorie Filtering
**Objective**: Verify only combinations with exactly 500 calories are processed

**Method**:
- Track all combinations that pass calorie filter
- For each, assert `calculate_calories(amounts, ingredients) == 500`
- Ensure at least one valid combination exists for the given input

#### Test 4.4: Boundary Combinations
**Objective**: Verify edge combinations are explored correctly

**Test Cases**:
- [100, 0, 0, 0] - all in first ingredient
- [0, 100, 0, 0] - all in second ingredient
- [0, 0, 100, 0] - all in third ingredient
- [0, 0, 0, 100] - all in fourth ingredient
- [25, 25, 25, 25] - equal distribution

**Verification**: Ensure generator produces these combinations and sum constraint holds

---

### 5. Integration Tests

#### Test 5.1: Run with Actual Input
**Objective**: Verify the algorithm works with the actual input.md file

**Input**: Sugar, Sprinkles, Candy, Chocolate from input.md
**Expected**: A positive integer score

**Method**:
- Run full algorithm with actual input.md file
- Verify the result is a positive integer (> 0)
- This confirms that valid combinations exist for the 500-calorie constraint
- Log the best combination for manual verification

#### Test 5.2: Simple Two-Ingredient Case
**Objective**: Test with a simplified scenario for easier verification

**Input**:
```
A: capacity 1, durability 1, flavor 1, texture 1, calories 5
B: capacity 1, durability 1, flavor 1, texture 1, calories 5
```

**Analysis**:
- To get 500 calories with 100 teaspoons: Both have 5 cal/tsp → 100 tsp * 5 = 500
- Any distribution works for calories (any [a, b] where a+b=100 gives 500 calories)
- Since all ingredients have value 1 for all properties, the total for each property is always 100 (sum of amounts)
- Therefore: capacity_total = a×1 + b×1 = a+b = 100, same for all properties
- Expected: score = 100 × 100 × 100 × 100 = 100,000,000 for ANY valid distribution

**Verification**: Assert score equals 100,000,000

#### Test 5.3: Impossible Calorie Constraint
**Objective**: Handle case where no combination meets calorie constraint

**Input**:
```
A: capacity 1, durability 1, flavor 1, texture 1, calories 10
B: capacity 1, durability 1, flavor 1, texture 1, calories 10
```

**Analysis**:
- Minimum calories: 100 tsp * 10 cal/tsp = 1000
- Cannot achieve 500 calories
- Expected: max_score = 0 (no valid combinations)

**Verification**: Assert result is 0

---

### 6. Edge Case Tests

#### Test 6.1: All Ingredients Have Zero Calories
**Objective**: Handle edge case where calorie constraint cannot be met

**Input**: All ingredients with `calories: 0`
**Expected**: No combination achieves 500 calories → max_score = 0

#### Test 6.2: Single Valid Combination
**Objective**: Verify correctness when only one combination meets constraints

**Method**: Design input where calorie constraint allows only one specific distribution
**Verification**: Ensure algorithm finds and returns that combination's score

#### Test 6.3: Maximum Property Values
**Objective**: Test with large property values to check for overflow

**Input**: Properties with values around 1000
**Method**: Verify score calculation doesn't overflow (Python handles big integers)

#### Test 6.4: All Zero Amounts Except One
**Objective**: Test boundary where most ingredients are unused

**Test Case**:
- Amounts: `[100, 0, 0, 0]` with Sugar (capacity 3, durability 0, flavor 0, texture -3, calories 2)
- Capacity: 100×3 = 300
- Durability: 100×0 = 0
- Flavor: 100×0 = 0
- Texture: 100×(-3) = -300 → max(0, -300) = 0
- Score: 300 × 0 × 0 × 0 = 0
- Calories: 100×2 = 200 (not 500, so this wouldn't be considered anyway)

**Verification**: Verify score calculation works correctly even with zeros

#### Test 6.5: Variable Number of Ingredients
**Objective**: Verify solution works with different numbers of ingredients

**Test Cases**:
1. 2 ingredients
2. 3 ingredients
3. 5 ingredients

**Verification**: Algorithm adapts to different ingredient counts without hardcoding

---

### 7. Performance Tests

#### Test 7.1: Execution Time
**Objective**: Ensure algorithm completes in reasonable time

**Method**:
- Run with actual input (4 ingredients, 100 teaspoons)
- Measure execution time using time.time() or timeit
- Expected: 1-3 seconds for typical execution
- Maximum acceptable: < 5 seconds (upper bound)

**Verification**:
- Assert `execution_time < 5.0` seconds
- Log execution time for performance analysis
- If execution time > 3 seconds, investigate for inefficiencies

#### Test 7.2: Number of Valid Combinations
**Objective**: Understand how many combinations meet the calorie constraint

**Method**:
- Count combinations where calories == 500
- Log this number for analysis
- Verify it's > 0 for the given input

---

### 8. Correctness Validation

#### Test 8.1: Manual Verification of Small Sample
**Objective**: Manually verify score calculation for a specific combination

**Method**:
1. Find a valid combination that equals 500 calories
2. Example with Sugar (2 cal), Sprinkles (9 cal), Candy (1 cal), Chocolate (8 cal):
   - Try [27, 23, 18, 32]: 27×2 + 23×9 + 18×1 + 32×8 = 54 + 207 + 18 + 256 = 535 (not 500)
   - Use the algorithm to find one valid combination, then verify manually
3. For the found combination, manually calculate:
   - Each property total: capacity, durability, flavor, texture
   - Apply max(0, total) to each
   - Multiply to get final score
   - Calculate calories to verify = 500
4. Assert algorithm produces the same score for this combination

**Alternative**: Run algorithm, get best combination, then manually verify that specific result

#### Test 8.2: Verify Best Solution Makes Sense
**Objective**: Sanity check that the maximum score is reasonable

**Method**:
- Run algorithm and get max_score
- Verify max_score > 0 (assuming valid combinations exist)
- Optionally: Check that max_score is not suspiciously low/high
- Log the best combination for manual inspection

---

## Test Execution Plan

### Phase 1: Unit Tests (Run First)
1. Input parsing tests (1.1, 1.2)
2. Calorie calculation tests (2.1, 2.2, 2.3)
3. Score calculation tests (3.1, 3.2, 3.3)

**Goal**: Ensure individual components work correctly

### Phase 2: Component Integration Tests
1. Combination generation tests (4.1, 4.2, 4.3, 4.4)

**Goal**: Verify the combination generator works with constraints

### Phase 3: Full Integration Tests
1. Integration tests (5.1, 5.2, 5.3)
2. Edge case tests (6.1, 6.2, 6.3, 6.4, 6.5)

**Goal**: Verify end-to-end functionality

### Phase 4: Validation & Performance
1. Correctness validation (8.1, 8.2)
2. Performance tests (7.1, 7.2)

**Goal**: Confirm algorithm finds optimal solution efficiently

---

## Acceptance Criteria

The solution is considered correct if:
1. ✓ All unit tests pass
2. ✓ Integration tests produce expected results for known examples
3. ✓ Edge cases are handled appropriately (return 0 when no valid solution, errors for invalid input)
4. ✓ Algorithm completes in < 5 seconds for the given input (ideally 1-3 seconds)
5. ✓ Final answer for actual input.md is a positive integer
6. ✓ Manual verification of at least one sample combination matches algorithm output
7. ✓ Best combination found has exactly 100 teaspoons and 500 calories
8. ✓ Solution works for variable number of ingredients (not hardcoded for 4)

---

## Test Implementation Approach

### Using pytest:
```python
def test_parse_ingredients():
    ingredients = parse_ingredients('test_input.txt')
    assert len(ingredients) == 4
    assert ingredients[0]['capacity'] == 3
    # ... more assertions

def test_calculate_calories():
    ingredients = [{'calories': 2}, {'calories': 9}]
    amounts = [50, 50]
    assert calculate_calories(amounts, ingredients) == 550

def test_score_with_negative_property():
    # Test case where property total is negative
    # ...
```

### Manual Verification:
- Run solution with actual input
- Print the best combination found
- Manually verify:
  - Sum of amounts = 100 ✓
  - Calories = 500 ✓
  - Score calculation is correct ✓

---

## Debugging Strategy

If tests fail:
1. **Parsing issues**: Print parsed ingredients, check format
2. **Score mismatch**: Print intermediate property totals for failing case
3. **No valid combinations**: Print first 10 combinations and their calories to diagnose
4. **Wrong maximum**: Print top 5 scores with their combinations to compare

## Final Validation

Before submitting solution:
- [ ] All tests pass
- [ ] Solution runs successfully on actual input
- [ ] Output is a single positive integer
- [ ] Manual spot-check confirms at least one calculation
- [ ] Performance is acceptable (< 5 seconds)
