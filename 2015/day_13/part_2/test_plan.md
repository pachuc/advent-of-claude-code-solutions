# Test Plan: Optimal Seating Arrangement with Self Included

## Testing Strategy

We need to verify:
1. **Parsing correctness**: Input is correctly parsed into data structures
2. **Self-addition correctness**: Ourselves added with proper 0-happiness relationships
3. **Happiness calculation correctness**: Individual arrangements scored properly
4. **Optimization correctness**: The maximum is correctly identified
5. **Overall solution correctness**: Final answer matches expected result

## Test Cases

### Test 1: Parse Input Correctness

**Purpose**: Verify that input parsing extracts all relationships correctly

**Method**:
1. Run `parse_input()` on the actual input
2. Verify the happiness map structure
3. Check sample relationships:
   - `happiness["Alice"]["Bob"]` should be `-2`
   - `happiness["Bob"]["Alice"]` should be `93`
   - `happiness["George"]["Mallory"]` should be `7`
   - `happiness["Mallory"]["George"]` should be `-99`

**Expected Results**:
- Total of 8 people in the set: Alice, Bob, Carol, David, Eric, Frank, George, Mallory
- Each person should have 7 relationships (with all other people)
- Total of 56 directed relationships (8 * 7)

**Verification**:
```python
assert len(people) == 8, "Expected exactly 8 people from input"
assert len(happiness_map) == 8
for person in people:
    assert len(happiness_map[person]) == 7
# Total relationships should be 8 * 7 = 56
total_relationships = sum(len(happiness_map[p]) for p in happiness_map)
assert total_relationships == 56
```

### Test 2: Self Addition Correctness

**Purpose**: Verify that we are added correctly with neutral relationships

**Method**:
1. After adding self, verify:
   - People set now contains 9 people (8 original + "Me")
   - "Me" has relationships with all 8 original people
   - All relationships involving "Me" are 0
   - All original people have "Me" in their happiness map

**Expected Results**:
```python
assert len(people) == 9
assert "Me" in people
# Verify bidirectional 0 relationships: both Me→Person and Person→Me equal 0
for person in original_people:
    assert happiness_map["Me"][person] == 0, f"Me's happiness with {person} should be 0"
    assert happiness_map[person]["Me"] == 0, f"{person}'s happiness with Me should be 0"
# Total of 16 zero-relationships (8 to us, 8 from us)
assert len(happiness_map["Me"]) == 8
```

### Test 3: Happiness Calculation - Simple Cases

**Purpose**: Verify happiness calculation for known arrangements

**Method**: Test with small, manually verifiable arrangements

**Test Case 3a - Three Person Circle**:
```python
# Simple test: Alice - Bob - Carol (circular)
arrangement = ["Alice", "Bob", "Carol"]
happiness_map = {
    "Alice": {"Bob": 10, "Carol": 5},
    "Bob": {"Alice": 20, "Carol": 15},
    "Carol": {"Alice": 30, "Bob": 25}
}
# Expected calculation:
# Alice: neighbors are Carol (left) and Bob (right) = 5 + 10 = 15
# Bob: neighbors are Alice (left) and Carol (right) = 20 + 15 = 35
# Carol: neighbors are Bob (left) and Alice (right) = 25 + 30 = 55
# Total = 15 + 35 + 55 = 105
```

**Expected Result**: `calculate_happiness()` returns 105

**Test Case 3b - Circular Property**:
```python
# Verify that first and last are neighbors in circular arrangement
arrangement = ["A", "B", "C", "D"]
# In circular arrangement [A, B, C, D]:
# A's left neighbor is D (index -1 = 3), right neighbor is B (index +1 = 1)
# D's left neighbor is C (index -1 = 2), right neighbor is A (index +1 % 4 = 0)
```

### Test 4: Happiness Calculation - With Self

**Purpose**: Verify that adding ourselves (with 0 happiness) affects the optimization correctly

**Method**:
1. Create a small test case without "Me"
2. Calculate optimal happiness
3. Add "Me" with 0 relationships
4. Calculate new optimal happiness
5. Verify that the algorithm completes successfully and returns a valid result

**Important Note**: Adding a neutral person can increase, decrease, or maintain the optimal happiness:
- **Likely decrease**: If we break up a mutually positive adjacency
- **Could increase**: If we optimally break up mutually negative adjacencies, allowing a better overall arrangement
- **Could stay same**: In rare symmetric cases

**Reasoning**: The key test is that the algorithm runs correctly, not assuming a specific directional change in happiness.

### Test 5: Permutation Coverage

**Purpose**: Ensure all unique arrangements are considered

**Method**:
1. For 9 people with first person fixed, verify we generate 8! = 40,320 permutations
2. Check that rotations are not double-counted
3. Verify no duplicate arrangements

**Verification**:
```python
from itertools import permutations
people_list = list(people)
fixed_person = people_list[0]
others = people_list[1:]
perms = list(permutations(others))
assert len(perms) == 40320  # 8!
# Note: We generate 8! = 40,320 permutations (not 8!/2) because happiness
# relationships are asymmetric, making clockwise and counter-clockwise
# arrangements different
```

### Test 6: Actual Input Solution

**Purpose**: Verify the solution on the actual input

**Method**:
1. Run the complete solution on the provided input file
2. Verify the result is a reasonable number
3. Check that it's different from Part 1 (without self)

**Expected Properties**:
- Result should be an integer
- Result should be positive (likely, given the input has many positive relationships)
- Result will likely be less than the Part 1 answer (adding ourselves with 0 relationships typically reduces optimal happiness, though not guaranteed)
- The optimal arrangement should be printed for manual inspection

**Validation Steps**:
1. Run solution and record answer
2. Manually verify a few arrangements if answer seems wrong
3. Check edge cases in the optimal arrangement

### Test 7: Edge Cases

**Purpose**: Test boundary conditions and special cases

**Test Case 7a - All Negative Relationships**:
- Verify solution works when all happiness values are negative
- Result should be the "least negative" arrangement

**Test Case 7b - All Zero Relationships**:
- If everyone has 0 happiness with everyone, result should be 0
- Any arrangement should give same result

**Test Case 7c - Symmetric Relationships**:
- If happiness[A][B] == happiness[B][A] for all pairs
- Verify calculation is still correct (doesn't double-count)
- Note: Each adjacency still contributes twice (once from each person's perspective)

**Test Case 7d - Regex Pattern Test**:
- Test parsing with sample input lines to verify regex correctness
- Test lines: "Alice would gain 50 happiness units by sitting next to Bob."
- Test lines: "Carol would lose 100 happiness units by sitting next to Dave."
- Verify periods are handled, names of different lengths work correctly

### Test 8: Manual Spot Check

**Purpose**: Manually verify the optimal arrangement makes logical sense

**Method**:
1. After finding optimal arrangement, print it
2. Examine the happiness relationships
3. Verify that high-happiness pairs are adjacent
4. Verify that low/negative pairs are separated

**Analysis**:
- Look at where "Me" sits in optimal arrangement
- "Me" should ideally break up a pair with negative or low combined happiness
- People with mutually high happiness should be adjacent

### Test 9: Calculation Verification

**Purpose**: Double-check arithmetic in happiness calculation

**Method**:
1. For the optimal arrangement found, manually calculate total happiness
2. For each person in the arrangement:
   - List their two neighbors
   - Look up happiness values
   - Sum them
3. Compare manual calculation to algorithm result

**Example**:
```
Arrangement: [Alice, Bob, Carol, David, Eric, Frank, George, Mallory, Me]
(Circular, so Me's right neighbor wraps to Alice)

Alice: neighbors are Me (left, index -1) and Bob (right, index +1)
  happiness[Alice][Me] = 0
  happiness[Alice][Bob] = -2
  Alice's contribution = 0 + (-2) = -2

Bob: neighbors are Alice (left) and Carol (right)
  happiness[Bob][Alice] = 93
  happiness[Bob][Carol] = 19
  Bob's contribution = 93 + 19 = 112

Me: neighbors are Mallory (left) and Alice (right)
  happiness[Me][Mallory] = 0
  happiness[Me][Alice] = 0
  Me's contribution = 0 + 0 = 0
...
Sum all contributions to get total happiness
```

### Test 10: Regression Test

**Purpose**: Ensure solution is stable and reproducible

**Method**:
1. Run the solution multiple times
2. Verify same answer each time
3. Verify deterministic behavior

**Expected**: Consistent results across runs

## Testing Execution Order

1. **Unit Tests** (Tests 1-3): Test individual components
   - Parse input
   - Add self
   - Calculate happiness for known arrangements

2. **Integration Tests** (Tests 4-5): Test component interactions
   - Effect of adding self
   - Permutation generation

3. **System Tests** (Tests 6-10): Test complete solution
   - Run on actual input
   - Verify result correctness
   - Manual validation

## Success Criteria

The solution passes if:
1. ✓ All unit tests pass
2. ✓ Happiness calculation matches manual calculation for test cases
3. ✓ Solution completes in reasonable time (< 5 seconds, ideally < 1 second)
4. ✓ Result is consistent across multiple runs (deterministic)
5. ✓ Result is different from Part 1 (expected to be lower, but not guaranteed)
6. ✓ Optimal arrangement is printed and makes logical sense when inspected
7. ✓ Parsing extracts all 56 relationships (8 people × 7 each)
8. ✓ "Me" is correctly added with 16 zero-relationships (bidirectional)

## Debugging Strategy

If tests fail:

**If parsing fails**:
- Print raw parsed data
- Check regex pattern
- Verify all lines are processed

**If happiness calculation is wrong**:
- Print each person's contribution separately
- Verify neighbor identification (circular indexing)
- Check that we're not double-counting or missing relationships

**If optimization gives wrong answer**:
- Print top 5 arrangements and their happiness values
- Manually verify the top arrangement
- Check that all permutations are being generated

**If result seems unreasonable**:
- Compare with Part 1 result
- Print the optimal arrangement
- Manually spot-check the happiness values

## Manual Verification Checklist

- [ ] Parse 56 relationships (8 people × 7 relationships each)
- [ ] Verify sample relationships: Alice-Bob = -2, Bob-Alice = 93
- [ ] Add ourselves with 16 zero-relationships (8 to us, 8 from us)
- [ ] Verify bidirectionality: both Me→Person and Person→Me equal 0
- [ ] Generate 40,320 circular permutations (8!, not 8!/2 due to asymmetry)
- [ ] Calculate happiness correctly for circular arrangements (wrap-around indexing)
- [ ] Find maximum happiness across all arrangements
- [ ] Result is an integer
- [ ] Result is likely lower than Part 1 (if Part 1 was solved)
- [ ] Optimal arrangement printed and inspected for logical sense
- [ ] "Me" sits in a position that makes strategic sense (breaks bad adjacencies)

## Notes

- Since this is a scripting problem, we don't need exhaustive edge case testing
- Focus on verifying correctness for the given input
- The main risk is calculation errors or off-by-one errors in circular indexing
- The brute force approach is simple enough that bugs are unlikely if tests pass
