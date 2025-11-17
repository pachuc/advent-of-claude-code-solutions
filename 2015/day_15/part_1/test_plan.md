# Testing Plan: Cookie Recipe Optimization

## Testing Strategy Overview

Our testing approach will validate both the correctness of individual components and the overall solution. We'll use a combination of unit tests, integration tests, and validation against known examples.

## Test Categories

### 1. Unit Tests for Parsing

**Test 1.1: Basic Parsing**
- **Input**: Single ingredient line from the example
  ```
  Sugar: capacity 3, durability 0, flavor 0, texture -3, calories 2
  ```
- **Expected Output**: Dictionary with keys: name, capacity, durability, flavor, texture, calories
- **Validation**:
  - Check all fields are present
  - Verify correct data types (strings for name, integers for properties)
  - Verify values match input (capacity=3, durability=0, flavor=0, texture=-3, calories=2)

**Test 1.2: Negative Values**
- **Purpose**: Ensure negative property values are parsed correctly
- **Input**: Ingredient with negative properties
  ```
  Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
  ```
- **Expected**: All negative values preserved as negative integers
- **Validation**: Check that capacity=-1, durability=-2

**Test 1.3: Complete File Parsing**
- **Input**: Full input.md file with 4 ingredients
- **Expected Output**: List of 4 ingredient dictionaries
- **Validation**:
  - Length of list is 4
  - Each ingredient has all required properties
  - Spot-check first and last ingredient values

### 2. Unit Tests for Score Calculation

**Test 2.1: Example from Problem Statement**
- **Purpose**: Verify score calculation against known example
- **Input**:
  - Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
  - Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
  - Amounts: [44, 56]
- **Expected Calculation**:
  - Capacity: 44×(-1) + 56×2 = -44 + 112 = 68
  - Durability: 44×(-2) + 56×3 = -88 + 168 = 80
  - Flavor: 44×6 + 56×(-2) = 264 - 112 = 152
  - Texture: 44×3 + 56×(-1) = 132 - 56 = 76
  - Score: 68 × 80 × 152 × 76 = 62,842,880
- **Validation**: Score equals exactly 62,842,880

**Test 2.2: Zero Property Handling**
- **Purpose**: Verify that negative property totals are replaced with 0
- **Test Case A**: One property total is negative
  - Create ingredients where one property sum would be negative
  - Expected: That property treated as 0, final score = 0
- **Test Case B**: All property totals are negative
  - Expected: Score = 0

**Test 2.3: All Zero Amounts**
- **Purpose**: Edge case where no ingredients are used
- **Input**: Amounts [0, 0, 0, 0]
- **Expected**: Score = 0 (all property totals are 0)

**Test 2.4: Single Ingredient Maximum**
- **Purpose**: Edge case where all 100 teaspoons are one ingredient
- **Input**: Amounts [100, 0, 0, 0] for the actual input ingredients
- **Expected**: Calculate manually and verify
  - Capacity: 100×3 = 300
  - Durability: 100×0 = 0
  - Score: 0 (because durability is 0)

**Test 2.5: Equal Distribution**
- **Purpose**: Test with evenly distributed amounts
- **Input**: Amounts [25, 25, 25, 25]
- **Expected**: Calculate expected score manually:
  - Capacity: 25×3 + 25×(-3) + 25×(-1) + 25×0 = 75 - 75 - 25 + 0 = -25 → 0
  - Score: 0

### 3. Unit Tests for Distribution Generation

**Test 3.1: Count Validation**
- **Purpose**: Verify correct number of distributions generated
- **Input**: num_ingredients=4, total_teaspoons=100
- **Expected**: 176,851 distributions (C(103, 3))
- **Validation**: Count all generated distributions

**Test 3.2: Sum Constraint**
- **Purpose**: Verify all distributions sum to 100
- **Method**: Check the first 1000 distributions from the generator
- **Validation**: Each tuple sums to exactly 100
- **Note**: We use "first 1000" rather than "random sample" because the generator yields deterministically

**Test 3.3: Non-negative Constraint**
- **Purpose**: Verify all amounts are non-negative
- **Method**: Check the first 1000 distributions from the generator
- **Validation**: All values >= 0 in each distribution
- **Note**: Combined with 3.2, can verify both constraints simultaneously

**Test 3.4: Boundary Cases**
- **Purpose**: Verify extreme distributions are included
- **Check for**:
  - (100, 0, 0, 0) - all first ingredient
  - (0, 100, 0, 0) - all second ingredient
  - (0, 0, 100, 0) - all third ingredient
  - (0, 0, 0, 100) - all fourth ingredient
  - (0, 0, 0, 0) - should NOT exist (doesn't sum to 100)

**Test 3.5: Small Scale Verification**
- **Purpose**: Manually verify with smaller numbers (easy to check by hand)
- **Input**: num_ingredients=2, total_teaspoons=3
- **Expected Distributions**: (0,3), (1,2), (2,1), (3,0) - exactly 4
- **Validation**: Generate all and verify completeness and correctness
- **Why this is valuable**: With only 4 combinations, we can manually verify each one is correct
- **Implementation**: This test is included in the verify_solution() function

### 4. Integration Tests

**Test 4.1: End-to-End with Example Data**
- **Purpose**: Verify complete solution with problem example
- **Input**: Create a test file with Butterscotch and Cinnamon
- **Expected Output**: 62,842,880
- **Validation**: Exact match

**Test 4.2: End-to-End with Actual Input**
- **Purpose**: Solve the actual problem
- **Input**: input.md file
- **Expected**: Some positive integer (we don't know the answer yet)
- **Validation Process**:
  1. Run the solution
  2. Record the answer
  3. Verify the optimal amounts sum to 100
  4. Recalculate the score manually for those amounts
  5. Confirm it matches the output

**Test 4.3: Symmetry Test**
- **Purpose**: Verify that ingredient order doesn't materially affect the result
- **Input**: Create test data with 2 identical ingredients
- **Expected**: If two ingredients have identical properties, swapping their amounts in the optimal solution should yield the same score
- **Validation**: Create ingredients A and B with identical properties, verify score([a, b, ...]) == score([b, a, ...])
- **Note**: This is more of an academic exercise than a critical test

### 5. Validation Tests

**Test 5.1: Manual Spot Check**
- **Purpose**: Manually verify a few random distributions from the search
- **Method**:
  - Pick 3-5 random distributions
  - Manually calculate their scores on paper/calculator
  - Compare with function output
- **Validation**: All match exactly

**Test 5.2: Boundary Score Verification**
- **Purpose**: Verify that the optimal solution is actually better than neighbors
- **Method**:
  - Once optimal amounts are found, test several "neighbor" distributions
  - Neighbors: amounts where one ingredient is +1/-1 and another is -1/+1
- **Expected**: All neighbors should have score <= optimal score

**Test 5.3: Property Total Sign Check**
- **Purpose**: Verify the optimal solution's property totals
- **Method**: For the optimal solution, calculate each property total
- **Validation**:
  - Check if any are negative (should be treated as 0)
  - Verify the multiplication manually

### 6. Edge Cases and Special Scenarios

**Test 6.1: All Properties Positive**
- **Purpose**: Test with ingredients that have all positive properties
- **Expected**: Likely maximized when properties with higher values get more teaspoons

**Test 6.2: All Properties Negative**
- **Purpose**: Test with ingredients where all properties are negative
- **Expected**: Score should be 0 (all property totals become 0)

**Test 6.3: Mixed Signs**
- **Purpose**: Current actual input has mixed positive/negative values
- **Validation**: This is the standard case, should work as designed

**Test 6.4: Zero Calories Impact**
- **Purpose**: Conceptually verify calories don't affect the score
- **Method**: Review the scoring function to confirm calories are excluded
- **Expected**: Calories property is not used in calculate_score()
- **Note**: This is more of a code review than a runtime test, since the implementation explicitly excludes calories from scoring

## Test Execution Order

1. **Phase 1: Component Testing**
   - Run parsing tests (1.1 - 1.3)
   - Run score calculation tests (2.1 - 2.5)
   - Run distribution generation tests (3.1 - 3.5)

2. **Phase 2: Integration Testing**
   - Run end-to-end test with example (4.1)
   - If passes, run with actual input (4.2)

3. **Phase 3: Validation**
   - Run validation tests (5.1 - 5.3)
   - Run edge case tests (6.1 - 6.4)

## Success Criteria

**Minimum Requirements**:
- ✓ Parse all ingredients correctly from input.md
- ✓ Score calculation matches problem example (62,842,880)
- ✓ Generate exactly 176,851 distributions
- ✓ All distributions sum to 100 and are non-negative
- ✓ Find an optimal score for the actual input
- ✓ Optimal solution's score can be manually verified

**Quality Indicators**:
- All verification tests pass (verify_solution() runs without errors)
- Manual verification confirms correctness
- Neighbor solutions have lower or equal scores
- Execution completes in reasonable time (< 5 seconds expected, < 10 seconds acceptable)

## Testing Implementation Approach

Since we're writing a script (not production code), testing will be pragmatic:

1. **Create test cases directly in the solution file or a separate test script**
2. **Use simple assert statements** rather than a full testing framework
3. **Focus on the most critical tests**:
   - Test 2.1 (example validation)
   - Test 3.2 and 3.3 (distribution constraints)
   - Test 4.1 (end-to-end with known answer)
   - Test 5.2 (neighbor verification)

4. **Manual verification**:
   - Print intermediate results for inspection
   - Manually recalculate final answer

## Quick Verification Script

Create a simple verification function (included in implementation plan as Step 5):
```python
def verify_solution():
    """Quick verification of the solution."""
    # Test 1: Known example from problem statement
    test_ingredients = [
        {'capacity': -1, 'durability': -2, 'flavor': 6, 'texture': 3},
        {'capacity': 2, 'durability': 3, 'flavor': -2, 'texture': -1}
    ]
    score = calculate_score(test_ingredients, [44, 56])
    assert score == 62842880, f"Example failed: got {score}, expected 62842880"

    # Test 2: Distribution count
    count = sum(1 for _ in generate_distributions(4, 100))
    assert count == 176851, f"Wrong distribution count: {count}, expected 176851"

    # Test 3: Distribution constraints (first 1000)
    for i, dist in enumerate(generate_distributions(4, 100)):
        if i >= 1000:
            break
        assert sum(dist) == 100, f"Distribution {dist} doesn't sum to 100"
        assert all(x >= 0 for x in dist), f"Distribution {dist} has negative values"

    # Test 4: Small scale verification (2 ingredients, 3 teaspoons)
    small_dists = list(generate_distributions(2, 3))
    expected_small = [(0,3), (1,2), (2,1), (3,0)]
    assert len(small_dists) == 4, f"Small test: expected 4, got {len(small_dists)}"
    assert small_dists == expected_small, f"Small test: distributions don't match"

    print("All verification tests passed!")
```

This provides a comprehensive sanity check before running the full solution.
