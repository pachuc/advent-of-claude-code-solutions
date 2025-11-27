# Test Plan: Recipe Scoreboard Simulation

## Testing Strategy
We need to verify that our simulation correctly implements the recipe generation algorithm and produces the correct output for various inputs. Since this is a deterministic algorithm, we can validate against known examples.

## Test Categories

### 1. Example Test Cases (Given in Problem)
These are the most critical tests as they validate the core algorithm.

#### Test 1.1: After 9 recipes
**Input:** 9
**Expected Output:** `5158916779`
**Purpose:** Verify basic algorithm with small input

**Manual trace verification:**
- Start: [3, 7], elf1=0, elf2=1
- Iteration 1: sum=10 → add [1,0], positions: elf1=4, elf2=3
- Continue until 19 recipes exist
- Extract recipes[9:19]

#### Test 1.2: After 5 recipes
**Input:** 5
**Expected Output:** `0124515891`
**Purpose:** Verify algorithm with very small input

#### Test 1.3: After 18 recipes
**Input:** 18
**Expected Output:** `9251071085`
**Purpose:** Verify algorithm with medium-small input

#### Test 1.4: After 2018 recipes
**Input:** 2018
**Expected Output:** `5941429882`
**Purpose:** Verify algorithm scales correctly to larger inputs

#### Test 1.5: Actual Input (47801)
**Input:** 47801
**Expected Output:** To be determined on first successful run
**Purpose:** Generate the actual solution

**Validation approach:**
- Run the solution and record the output
- Re-run to ensure deterministic behavior
- Verify output format (10 digits, all 0-9)
- **Important:** Once the correct answer is obtained, add it to the test suite as a regression test

### 2. Algorithm Correctness Tests

#### Test 2.1: Initial State Verification
**Test:** Verify scoreboard starts correctly
**Check:**
- Scoreboard = [3, 7]
- elf1_pos = 0
- elf2_pos = 1

#### Test 2.2: Single Recipe Creation (sum < 10)
**Test:** When sum < 10, only one recipe is added
**Example:**
- Scores: 2 + 3 = 5
- Should add: [5]
- Should NOT add: [0, 5]

#### Test 2.3: Double Recipe Creation (sum >= 10)
**Test:** When sum >= 10, two recipes are added
**Example:**
- Scores: 7 + 8 = 15
- Should add: [1, 5]
- Scores: 5 + 5 = 10
- Should add: [1, 0]

#### Test 2.4: Position Wrapping
**Test:** Positions wrap correctly using modulo
**Scenario:**
- Scoreboard has 10 recipes
- Elf at position 7 with score 5
- Next position = (7 + 1 + 5) % 10 = 3 ✓

#### Test 2.5: Position Update Timing
**Test:** Positions update AFTER new recipes are added, using the UPDATED scoreboard length
**Concrete test case:**
- Scoreboard: [3, 7, 1, 0], elf1_pos=0, elf2_pos=1
- score1=3, score2=7
- sum=10 → add [1, 0] → scoreboard becomes [3, 7, 1, 0, 1, 0] (length 6)
- elf1_pos = (0 + 1 + 3) % 6 = 4 ✓ (using NEW length 6, not old length 4)
- elf2_pos = (1 + 1 + 7) % 6 = 3 ✓ (using NEW length 6, not old length 4)
**Verification:** Modulo must use the length AFTER adding recipes

### 3. Edge Cases and Boundary Conditions

#### Test 3.1: Minimum Input (n=0)
**Input:** 0
**Expected Output:** `3710101245` (the first 10 recipes)
**Purpose:** Test when we need recipes starting from index 0

**Expected behavior:**
- Generate until len(scoreboard) >= 10
- Return scoreboard[0:10]
**Note:** Can be verified by manually tracing first few iterations

#### Test 3.2: Very Small Input (n=1)
**Input:** 1
**Expected:** Recipes from index 1 to 10
**Purpose:** Verify off-by-one errors don't occur

#### Test 3.3: Input Less Than Initial Length (n < 2)
**Input:** 1
**Purpose:** Test when n is less than initial scoreboard size
**Expected behavior:**
- Still need to generate more recipes
- Extract starting from valid index

#### Test 3.4: Maximum Possible Sum (9 + 9 = 18)
**Test:** Verify largest possible sum is handled
**Check:**
- 9 + 9 = 18 → should add [1, 8]
- Not [18] or any other combination

#### Test 3.5: Exact Recipe Count
**Test:** When loop terminates exactly at n+10
**Purpose:** Ensure we don't generate too few or too many
**Verification:**
- If after iteration scoreboard has exactly n+10 recipes, extraction works
- If after iteration scoreboard has n+11 or n+12 recipes, extraction still works

### 4. Output Format Validation

#### Test 4.1: Output Length
**Check:** Result string has exactly 10 characters
**Validation:** `len(result) == 10`

#### Test 4.2: Output Content
**Check:** All characters are digits 0-9
**Validation:** `all(c.isdigit() for c in result)`

#### Test 4.3: No Separators
**Check:** No spaces, commas, or other separators
**Validation:** Result is a continuous string of digits

### 5. Performance and Scalability Tests

#### Test 5.1: Runtime for Given Input (n=47801)
**Measure:** Execution time should be < 1 second (realistically < 0.5 seconds)
**Purpose:** Ensure algorithm is efficient enough

**Measurement approach:**
```python
import time
start = time.time()
result = solve()
elapsed = time.time() - start
assert elapsed < 1.0, f"Too slow: {elapsed:.3f}s"
print(f"Runtime: {elapsed:.3f}s")
```

#### Test 5.2: Memory Usage
**Check:** Program doesn't crash or use excessive memory
**Expected:** ~48KB for storing ~48,000 integers

#### Test 5.3: Deterministic Behavior
**Test:** Running multiple times produces same result
**Validation:**
- Run solution 3 times
- Verify all outputs are identical

### 6. Implementation Detail Tests

#### Test 6.1: Scoreboard Growth Pattern
**Test:** Verify scoreboard grows correctly in early iterations
**Manual trace for first few iterations:**
```
Initial: [3, 7], elf1=0, elf2=1

Iter 1:
  scores: 3+7=10 → add [1,0]
  scoreboard: [3,7,1,0]
  elf1=(0+1+3)%4=0, elf2=(1+1+7)%4=1

Iter 2:
  scores: 3+7=10 → add [1,0]
  scoreboard: [3,7,1,0,1,0]
  elf1=(0+1+3)%6=4, elf2=(1+1+7)%6=3

Iter 3:
  scores: scoreboard[4]+scoreboard[3]=1+0=1 → add [1]
  scoreboard: [3,7,1,0,1,0,1]
  elf1=(4+1+1)%7=6, elf2=(3+1+0)%7=4

Iter 4:
  scores: scoreboard[6]+scoreboard[4]=1+1=2 → add [2]
  scoreboard: [3,7,1,0,1,0,1,2]
  elf1=(6+1+1)%8=0, elf2=(4+1+1)%8=6

Iter 5:
  scores: scoreboard[0]+scoreboard[6]=3+1=4 → add [4]
  scoreboard: [3,7,1,0,1,0,1,2,4]
  elf1=(0+1+3)%9=4, elf2=(6+1+1)%9=8

After 10+ recipes: [3,7,1,0,1,0,1,2,4,5,1,5,8,9,1,6,7,7,9,2,...]
First 10: 3710101245
```

#### Test 6.2: Position Calculation Correctness
**Test:** Verify position formula: (current_pos + 1 + current_score) % len
**Example cases:**
- pos=0, score=3, len=4 → (0+1+3)%4 = 0
- pos=5, score=7, len=20 → (5+1+7)%20 = 13
- pos=18, score=9, len=20 → (18+1+9)%20 = 8 (wraps)

## Test Execution Plan

### Phase 1: Unit Testing (Manual or Automated)
1. Run all example test cases (1.1-1.4)
2. Verify each produces expected output
3. If any fail, debug the algorithm

### Phase 2: Edge Case Testing
1. Test boundary conditions (3.1-3.5)
2. Test output format validation (4.1-4.3)
3. Ensure no crashes or errors

### Phase 3: Performance Testing
1. Run performance tests (5.1-5.2)
2. Verify acceptable runtime
3. Check deterministic behavior (5.3)

### Phase 4: Final Validation
1. Run with actual input (47801)
2. Verify output format
3. Record result for submission

## Test Implementation Example

```python
def test_examples():
    """Test all provided examples"""
    test_cases = [
        (9, "5158916779"),
        (5, "0124515891"),
        (18, "9251071085"),
        (2018, "5941429882"),
    ]

    for num_recipes, expected in test_cases:
        result = solve(num_recipes)
        assert result == expected, f"Failed for n={num_recipes}: got {result}, expected {expected}"
        print(f"✓ Test passed for n={num_recipes}")

def test_output_format():
    """Verify output format is correct"""
    result = solve()  # Uses input.md
    assert len(result) == 10, f"Output length is {len(result)}, expected 10"
    assert all(c.isdigit() for c in result), "Output contains non-digit characters"
    print("✓ Output format is valid")

def test_deterministic():
    """Verify solution is deterministic"""
    result1 = solve()
    result2 = solve()
    result3 = solve()
    assert result1 == result2 == result3, "Solution is not deterministic"
    print("✓ Solution is deterministic")

def test_first_10_recipes():
    """Test that the first 10 recipes match expected pattern"""
    result = solve(0)
    expected = "3710101245"
    assert result == expected, f"First 10 recipes: got {result}, expected {expected}"
    print("✓ First 10 recipes are correct")
```

## Success Criteria

The implementation is considered correct if:
1. ✓ All example test cases pass (1.1-1.4)
2. ✓ First 10 recipes test passes (n=0 → `3710101245`)
3. ✓ Output format is valid (10 digits, all 0-9)
4. ✓ Algorithm handles edge cases correctly
5. ✓ Runtime is under 1 second for n=47801
6. ✓ Solution is deterministic (same result every time)
7. ✓ No crashes or errors during execution

## Summary of Key Improvements (Based on Critique)

### Fixes Applied:
1. **Corrected manual trace** (Section 6.1): Fixed the iteration-by-iteration trace to show correct position updates
2. **Clarified position timing** (Section 2.5): Added concrete test case showing positions update using NEW scoreboard length
3. **Added expected value for n=0** (Section 3.1): Specified that first 10 recipes should be `3710101245`
4. **Tightened performance requirement** (Section 5.1): Changed from < 5 seconds to < 1 second (more realistic)
5. **Chose testing approach** (Test Data Management): Decided on parameterized `solve()` function over separate test files
6. **Added regression test note** (Section 1.5): Reminder to add actual answer to test suite once found

### Critical Test Cases to Run First:
1. **n=9 → `5158916779`** - Small example, easy to debug
2. **n=0 → `3710101245`** - Validates first 10 recipes are correct
3. **n=5, 18, 2018** - Remaining examples
4. **n=47801** - Actual solution

### What to Watch For:
- Position calculations must use length AFTER adding new recipes
- Digit splitting: 10→[1,0], 15→[1,5], 9→[9]
- Loop must continue until at least n+10 recipes exist

## Debugging Strategy

If tests fail:
1. **Wrong output for examples:** Trace through algorithm manually for small inputs
2. **Off-by-one errors:** Check position calculations and array indexing
3. **Wrong recipe creation:** Verify sum-to-digits conversion logic
4. **Performance issues:** Profile code to find bottlenecks (unlikely for this problem)

## Test Data Management

**Chosen approach:** Modify the solve function to accept an optional input parameter for easier testing.

```python
def solve(num_recipes=None):
    """
    Solve the recipe scoreboard problem.

    Args:
        num_recipes: Number of recipes to skip before extracting result.
                    If None, reads from input.md file.
    """
    if num_recipes is None:
        with open('input.md', 'r') as f:
            num_recipes = int(f.read().strip())

    # ... rest of implementation
```

This approach:
- Allows easy testing without creating multiple files
- Preserves ability to read from input.md for actual solution
- Makes test code cleaner and more maintainable
