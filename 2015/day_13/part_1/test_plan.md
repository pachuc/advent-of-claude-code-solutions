# Testing Plan: Optimal Circular Seating Arrangement

## Testing Strategy Overview

This plan focuses on verifying correctness through:
1. **Input validation** to ensure we're working with expected data
2. **Unit tests** for individual components
3. **Integration test** with the actual input
4. **Manual verification** with small examples
5. **Edge case validation**

Since this is a scripting problem, we focus on functional correctness rather than production-grade testing.

## Test 0: Input File Content Validation

**Objective**: Verify that the input file contains the expected data before running other tests

**Test Steps**:
1. Read the input file (verify correct filename: 'input.txt' or 'input.md')
2. Verify it contains expected person names from the problem
3. Verify basic format of lines (matches regex pattern)
4. Count total number of lines

**Expected Results**:
- Input file exists and is readable
- Contains lines matching format: "X would gain/lose N happiness units by sitting next to Y."
- Should have 56 lines (8 people × 7 relationships each)
- Should contain the people: Alice, Bob, Carol, David, Eric, Frank, George, Mallory

**Implementation**:
```python
def test_input_file():
    import os

    # Check if file exists
    filename = 'input.txt'  # or 'input.md' - adjust as needed
    assert os.path.exists(filename), f"Input file {filename} not found"

    with open(filename, 'r') as f:
        lines = f.readlines()

    # Check line count
    assert len(lines) == 56, f"Expected 56 lines, got {len(lines)}"

    # Verify format of first line
    pattern = r'(\w+) would (gain|lose) (\d+) happiness units by sitting next to (\w+)\.'
    import re
    assert re.match(pattern, lines[0].strip()), f"First line doesn't match expected format"

    # Check for expected people
    content = ''.join(lines)
    expected_people = ['Alice', 'Bob', 'Carol', 'David', 'Eric', 'Frank', 'George', 'Mallory']
    for person in expected_people:
        assert person in content, f"Expected person {person} not found in input"

    print("✓ Input file validation passed")
```

## Test 1: Input Parsing Validation

**Objective**: Verify that input parsing correctly extracts all relationships

**Test Steps**:
1. Parse the full input file
2. Verify the number of unique people extracted: **Should be 8**
   - Alice, Bob, Carol, David, Eric, Frank, George, Mallory
3. Verify the number of relationships: **Should be 56** (8 people × 7 relationships each)
4. Spot-check specific relationships:
   - `happiness['Alice']['Bob']` should be `-2`
   - `happiness['Alice']['David']` should be `65`
   - `happiness['Bob']['Alice']` should be `93`
   - `happiness['George']['Mallory']` should be `7`
5. Verify gain/lose parsing:
   - All "gain" lines should have positive values
   - All "lose" lines should have negative values

**Success Criteria**:
- Correct person count
- Correct relationship count
- Spot-checks pass
- Bidirectional relationships exist (both person1→person2 and person2→person1)

**Implementation**:
```python
def test_parsing():
    happiness_map, people = parse_input(input_text)

    assert len(people) == 8, f"Expected 8 people, got {len(people)}"

    total_relationships = sum(len(neighbors) for neighbors in happiness_map.values())
    assert total_relationships == 56, f"Expected 56 relationships, got {total_relationships}"

    # Spot checks
    assert happiness_map['Alice']['Bob'] == -2
    assert happiness_map['Alice']['David'] == 65
    assert happiness_map['Bob']['Alice'] == 93
    assert happiness_map['George']['Mallory'] == 7

    print("✓ Parsing test passed")
```

## Test 2: Happiness Calculation - Simple Example

**Objective**: Verify circular happiness calculation with a known small example

**Test Case**: 4-person arrangement
- Arrangement: `['Alice', 'David', 'Carol', 'Bob']` (circular)

**Expected Calculation**:
1. Alice (index 0):
   - Left neighbor: Bob (index 3) → Alice loses 2 → -2
   - Right neighbor: David (index 1) → Alice gains 65 → +65
   - Alice subtotal: 63

2. David (index 1):
   - Left neighbor: Alice (index 0) → David gains 43 → +43
   - Right neighbor: Carol (index 2) → David loses 53 → -53
   - David subtotal: -10

3. Carol (index 2):
   - Left neighbor: David (index 1) → Carol loses 37 → -37
   - Right neighbor: Bob (index 3) → Carol loses 70 → -70
   - Carol subtotal: -107

4. Bob (index 3):
   - Left neighbor: Carol (index 2) → Bob gains 19 → +19
   - Right neighbor: Alice (index 0) → Bob gains 93 → +93
   - Bob subtotal: 112

**Expected Total**: 63 + (-10) + (-107) + 112 = **58**

**IMPORTANT NOTE**: These expected values are based on the actual input provided in input.md. Before running this test, verify these specific relationship values match the input:
- Alice→Bob = -2, Alice→David = 65
- David→Alice = 43, David→Carol = -53
- Carol→David = -37, Carol→Bob = -70
- Bob→Carol = 19, Bob→Alice = 93

**Test Steps**:
1. Create test arrangement: `['Alice', 'David', 'Carol', 'Bob']`
2. Call `calculate_happiness(arrangement, happiness_map)`
3. Verify result equals 58

**Implementation**:
```python
def test_happiness_calculation():
    # Use parsed happiness map from actual input
    arrangement = ['Alice', 'David', 'Carol', 'Bob']
    result = calculate_happiness(arrangement, happiness_map)

    expected = 58
    assert result == expected, f"Expected {expected}, got {result}"

    print("✓ Happiness calculation test passed")
```

## Test 3: Circular Property Validation

**Objective**: Verify that the circular table property works correctly

**Test Case**: Ensure first and last persons are neighbors

**Test Steps**:
1. Create a small test arrangement: `['Alice', 'Bob', 'Carol']`
2. Calculate happiness
3. Manually verify that:
   - Alice's neighbors are Carol (left) and Bob (right)
   - Bob's neighbors are Alice (left) and Carol (right)
   - Carol's neighbors are Bob (left) and Alice (right)

**Expected Calculation** (3-person circular):
- Alice: Carol (left) + Bob (right) = -62 + (-2) = -64
- Bob: Alice (left) + Carol (right) = 93 + 19 = 112
- Carol: Bob (left) + Alice (right) = -70 + (-54) = -124
- Total: -64 + 112 + (-124) = **-76**

**IMPORTANT NOTE**: These expected values are based on the actual input provided in input.md. Verify:
- Alice→Bob = -2, Alice→Carol = -62
- Bob→Alice = 93, Bob→Carol = 19
- Carol→Bob = -70, Carol→Alice = -54

**Implementation**:
```python
def test_circular_property():
    arrangement = ['Alice', 'Bob', 'Carol']
    result = calculate_happiness(arrangement, happiness_map)

    expected = -76
    assert result == expected, f"Expected {expected}, got {result}"

    print("✓ Circular property test passed")
```

## Test 4: Permutation Generation Count and Uniqueness

**Objective**: Verify correct number of permutations are generated and all are unique

**Test Steps**:
1. Count the number of permutations generated when fixing first person
2. With 8 people, fixing one person leaves 7 people to permute
3. Expected count: 7! = 5,040 permutations
4. Verify all permutations are unique
5. Verify all permutations start with the fixed person

**Implementation**:
```python
def test_permutation_count():
    people_sorted = sorted(people)
    fixed_person = people_sorted[0]
    remaining_people = people_sorted[1:]

    seen_arrangements = set()
    count = 0

    for perm in permutations(remaining_people):
        arrangement = tuple([fixed_person] + list(perm))

        # Verify first person is fixed
        assert arrangement[0] == fixed_person, f"First person should be {fixed_person}, got {arrangement[0]}"

        # Verify uniqueness
        assert arrangement not in seen_arrangements, f"Duplicate permutation found: {arrangement}"

        seen_arrangements.add(arrangement)
        count += 1

    expected = 5040  # 7!
    assert count == expected, f"Expected {expected} permutations, got {count}"

    print(f"✓ Permutation count test passed - {count} unique arrangements verified")
```

## Test 5: Symmetry Validation

**Objective**: Verify that different rotations of the same arrangement yield the same happiness

**Test Case**: Test that rotating an arrangement doesn't change total happiness

**Test Steps**:
1. Create arrangement: `['Alice', 'Bob', 'Carol', 'David']`
2. Calculate happiness for this arrangement
3. Rotate to: `['Bob', 'Carol', 'David', 'Alice']`
4. Calculate happiness for rotated arrangement
5. Verify both give the same result

**Implementation**:
```python
def test_rotational_symmetry():
    arr1 = ['Alice', 'Bob', 'Carol', 'David']
    arr2 = ['Bob', 'Carol', 'David', 'Alice']  # Rotated by 1
    arr3 = ['Carol', 'David', 'Alice', 'Bob']  # Rotated by 2

    h1 = calculate_happiness(arr1, happiness_map)
    h2 = calculate_happiness(arr2, happiness_map)
    h3 = calculate_happiness(arr3, happiness_map)

    assert h1 == h2 == h3, f"Rotational symmetry broken: {h1}, {h2}, {h3}"

    print("✓ Rotational symmetry test passed")
```

## Test 6: Main Algorithm - Full Input Test

**Objective**: Run the complete algorithm on the actual input and verify reasonable output

**Test Steps**:
1. Run `find_optimal_seating()` with the full 8-person input
2. Verify the result is:
   - An integer
   - Within reasonable bounds (given input values range from -99 to 95)
   - Positive (optimal arrangement should have net positive happiness)
3. Record the result for reference

**Expected Characteristics**:
- Result should be > 0 (some arrangement should be positive)
- Result should be < 16 × 95 = 1,520 (theoretical max if all edges were +95)
- Commentary: Result will likely be in range 400-800 based on input distribution (not enforced)

**Reasonableness Check**:
- 8 people × 2 neighbors = 16 relationship values summed
- The actual result depends on the specific input values
- The loose upper bound (1520) prevents false failures while catching obvious errors

**Implementation**:
```python
def test_full_algorithm():
    result = find_optimal_seating(happiness_map, people)

    assert isinstance(result, (int, float)), f"Result should be numeric, got {type(result)}"
    assert result > 0, f"Optimal arrangement should have positive happiness, got {result}"
    assert result < 1520, f"Result suspiciously high: {result}"

    # Print result for reference (no specific assertion on exact value)
    print(f"✓ Full algorithm test passed - Maximum happiness: {result}")

    # Optional: Print range commentary
    if 400 <= result <= 800:
        print("  (Result is within expected range 400-800)")
    else:
        print(f"  (Result is outside typical range 400-800, but may be correct for this input)")
```

## Test 7: Edge Case - All Negative Values

**Objective**: Verify algorithm works when best option is "least negative"

**Test Case**: Create a mini scenario where all relationships are negative

**Test Steps**:
1. Create a small happiness map with only negative values:
   ```python
   test_happiness = {
       'A': {'B': -10, 'C': -20},
       'B': {'A': -5, 'C': -15},
       'C': {'A': -25, 'B': -30}
   }
   ```
2. Find optimal arrangement
3. Verify it returns the least negative total (maximum value)

**Expected**: Should return -80 for arrangement `['A', 'B', 'C']`
- A: C (left) + B (right) = -20 + (-10) = -30
- B: A (left) + C (right) = -5 + (-15) = -20
- C: B (left) + A (right) = -30 + (-25) = -55
- Total: -105

vs arrangement `['A', 'C', 'B']`:
- A: B (left) + C (right) = -10 + (-20) = -30
- C: A (left) + B (right) = -25 + (-30) = -55
- B: C (left) + A (right) = -15 + (-5) = -20
- Total: -105 (same due to symmetry)

**Implementation**:
```python
def test_all_negative():
    test_happiness = {
        'A': {'B': -10, 'C': -20},
        'B': {'A': -5, 'C': -15},
        'C': {'A': -25, 'B': -30}
    }
    test_people = ['A', 'B', 'C']

    result = find_optimal_seating(test_happiness, test_people)
    assert result == -105, f"Expected -105, got {result}"

    print("✓ All negative test passed")
```

## Test 8: Edge Case - Single Optimal Solution

**Objective**: Verify that algorithm finds THE best arrangement when one clearly exists

**Test Case**: Create scenario with one obviously optimal arrangement

**Test Steps**:
1. Create happiness map where specific pairing is highly favorable:
   ```python
   test_happiness = {
       'A': {'B': 100, 'C': 0, 'D': 0},
       'B': {'A': 100, 'C': 0, 'D': 0},
       'C': {'A': 0, 'B': 0, 'D': 100},
       'D': {'A': 0, 'B': 0, 'C': 100}
   }
   ```
2. Optimal arrangement should pair A-B and C-D as neighbors
3. Arrangement like `['A', 'B', 'C', 'D']` or `['A', 'B', 'D', 'C']`

**Expected**:
- Best: A-B-C-D (circular): A↔B (+200), B↔C (0), C↔D (+200), D↔A (0) = 400
- Compare with: A-C-B-D (circular): A↔C (0), C↔B (0), B↔D (0), D↔A (0) = 0

**Implementation**:
```python
def test_optimal_pairing():
    test_happiness = {
        'A': {'B': 100, 'C': 0, 'D': 0},
        'B': {'A': 100, 'C': 0, 'D': 0},
        'C': {'A': 0, 'B': 0, 'D': 100},
        'D': {'A': 0, 'B': 0, 'C': 100}
    }
    test_people = ['A', 'B', 'C', 'D']

    result = find_optimal_seating(test_happiness, test_people)
    assert result == 400, f"Expected 400, got {result}"

    print("✓ Optimal pairing test passed")
```

## Test Execution Plan

### Phase 0: Input Validation
Run before all other tests:
0. Test 0: Input File Content Validation

### Phase 1: Unit Tests
Run tests in order:
1. Test 1: Input Parsing
2. Test 4: Permutation Count and Uniqueness
3. Test 2: Happiness Calculation (simple)
4. Test 3: Circular Property

**Important**: If Test 2 or Test 3 fails, verify the expected values match the actual input file before assuming the algorithm is wrong.

### Phase 2: Integration Tests
5. Test 5: Rotational Symmetry
6. Test 6: Full Algorithm

### Phase 3: Edge Cases
7. Test 7: All Negative Values
8. Test 8: Optimal Pairing

### Phase 4: Final Verification
9. Run the complete solution and verify output is reasonable
10. Manually trace through one or two arrangements to validate calculation
11. Compare against any known expected answer (if available from problem source)

## Success Criteria

**All tests pass AND:**
- Final answer is a positive integer
- Final answer is within expected range (400-800)
- Algorithm completes in under 1 second
- No runtime errors or exceptions

## Manual Verification Procedure

After automated tests, perform manual spot-check:

1. Pick a random arrangement from the permutations
2. Manually calculate happiness for that arrangement:
   - Write down each person's two neighbors
   - Look up happiness values in input
   - Sum all values
3. Verify this matches the calculated value
4. Confirm this value is ≤ the maximum found by algorithm

## Performance Validation

While running tests, observe:
- Execution time should be < 1 second total
- No memory issues (should use < 10MB)
- All 5,040 permutations should be evaluated

## Debugging Checklist

If tests fail, check:
- [ ] Input file exists and has correct filename ('input.txt' vs 'input.md')
- [ ] Regex pattern correctly captures all parts of input lines
- [ ] Gain/lose are correctly converted to positive/negative
- [ ] Circular indexing uses modulo operator correctly
- [ ] Both left and right neighbors are counted for each person
- [ ] Fixed person optimization doesn't skip any valid permutations
- [ ] Dictionary keys are spelled correctly and case-sensitive
- [ ] Test expected values match the actual input data (Tests 2 & 3)
- [ ] All relationships are directional (not assumed symmetric)
