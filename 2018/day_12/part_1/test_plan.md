# Testing Plan: Plant Growth Simulation

## Testing Strategy Overview

The testing approach focuses on verifying:
1. **Parsing correctness**: Input is parsed correctly
2. **Pattern matching**: 5-pot windows are correctly identified
3. **Rule application**: Rules are applied correctly to generate next state
4. **Simulation mechanics**: State transitions work correctly over multiple generations
5. **Edge cases**: Boundary conditions and special scenarios
6. **Final calculation**: Sum is computed correctly

## Test 1: Input Parsing Verification

### Objective
Verify that initial state and rules are parsed correctly from the input file.

### Test Steps
1. Parse the input file
2. Print/verify the initial state:
   - Count number of pots with plants in initial state
   - Print indices of first few and last few plants
   - Expected: Should match visual inspection of input
3. Print/verify rules dictionary:
   - Count total number of rules
   - Print a few sample rules and verify they match the input file
   - Expected: All rules from input.md should be present (count may be less than 32 total possible patterns)

### Success Criteria
- Initial state has correct number of plants
- Initial state plant positions match input string
- All rules from input file are parsed correctly
- Sample rules (e.g., `.##.# => #`, `#..#. => .`) match input file exactly

### Manual Verification
Compare initial state string from input:
`..#..###...#####.#.#...####.#..####..###.##.#.#.##.#....#....#.####...#....###.###..##.#....#######`

Count '#' characters and verify positions.

## Test 2: Pattern Generation Verification

### Objective
Verify that the get_pattern function correctly generates 5-character patterns.

### Test Steps
1. Create a simple known state: `{0, 2, 4}` (plants at pots 0, 2, 4)
2. Test pattern generation for various pots (each checks a 5-pot window: [pot-2, pot-1, pot, pot+1, pot+2]):
   - `get_pattern(-2, state)` checks pots [-4,-3,-2,-1,0] → should be `....#`
   - `get_pattern(-1, state)` checks pots [-3,-2,-1,0,1] → should be `...#.`
   - `get_pattern(0, state)` checks pots [-2,-1,0,1,2] → should be `..#.#`
   - `get_pattern(1, state)` checks pots [-1,0,1,2,3] → should be `.#.#.`
   - `get_pattern(2, state)` checks pots [0,1,2,3,4] → should be `#.#.#`
   - `get_pattern(5, state)` checks pots [3,4,5,6,7] → should be `.#...` (pot 4 is at index 1)
3. Verify each pattern matches expected

### Success Criteria
All patterns match expected values for the known state.

## Test 3: Single Generation Simulation

### Objective
Verify that one generation of simulation works correctly.

### Test Steps
1. Use the example from the problem:
   - Initial state: `#..#.#..##......###...###`
   - Parse the example rules (we have actual rules from input.md)
2. Manually calculate what the next generation should be for a few pots:
   - Check first few pots manually
   - Compare with simulation result
3. Print the state after 1 generation
4. Verify number of plants seems reasonable

### Success Criteria
- State transitions correctly from generation 0 to generation 1
- Pattern matching and rule application work correctly
- Plants appear/disappear according to rules

### Manual Spot Check
For pot 0 in the example initial state `#..#.#..##......###...###`:
- `get_pattern(0, state)` checks pots [-2, -1, 0, 1, 2]
- Pot -2 and -1 are empty (beyond initial state boundary, treated as '.')
- Pot 0 has '#' (first character of initial state)
- Pots 1-2 have '..' (second and third characters)
- Expected pattern: `..#..`
- Look up `..#..` in rules to determine if pot 0 has a plant in next generation
- Verify the simulation result matches the rule outcome

## Test 4: Multiple Generation Simulation

### Objective
Verify simulation runs correctly for multiple generations.

### Test Steps
1. Run simulation for 5 generations
2. Track state size (number of plants) after each generation
3. Track min/max pot indices after each generation
4. Print states to verify:
   - Plants are spreading/changing
   - No obvious errors (e.g., all plants disappearing unexpectedly)
   - Min/max range is expanding as expected

### Success Criteria
- Simulation completes without errors
- State evolves reasonably (plants don't all disappear or explode to unreasonable numbers)
- Range expands by at most 2 pots per generation in each direction

### What to Look For
- Generation 0: initial configuration
- Generation 1-5: progressive changes
- If all plants disappear → bug in rule application
- If plants grow exponentially → possible bug

## Test 5: Full 20 Generation Simulation

### Objective
Verify the complete 20-generation simulation produces a valid result.

### Test Steps
1. Run full simulation with actual input for 20 generations
2. Print state summary after each generation:
   - Generation number
   - Number of plants
   - Min pot index
   - Max pot index
   - Current sum (for debugging)
3. After 20 generations, calculate final sum
4. Verify result is a reasonable integer

### Success Criteria
- Simulation completes all 20 generations without errors
- Final sum is calculated
- Result is a plausible integer (likely in thousands based on example)

### Expected Behavior
- Example gives 325 for similar input
- Our actual input might give different result
- Range should be bounded (roughly -40 to +140 given initial ~100 pots)

## Test 6: Edge Case - Empty State

### Objective
Verify the program handles an empty state gracefully.

### Test Steps
1. Create a test with initial state having no plants: `{}`
2. Run simulation for 1 generation
3. Verify result is also empty: `{}`
4. Verify sum is 0

### Success Criteria
- No crashes or errors when state is empty
- Empty state remains empty
- Sum of empty state is 0

### Implementation Note
May need to add check: `if not state: return set()` in simulate_generation

## Test 7: Edge Case - Single Plant

### Objective
Verify simulation works with minimal state.

### Test Steps
1. Create initial state with single plant at pot 0: `{0}`
2. Run simulation for 5 generations
3. Track how the single plant evolves
4. Verify no crashes

### Success Criteria
- Simulation runs without errors
- Single plant either disappears, stays, or spreads according to rules
- No infinite growth or unexpected behavior

## Test 8: Negative Pot Indices

### Objective
Verify the program correctly handles negative pot indices.

### Test Steps
1. Create initial state with plants in negative positions: `{-5, -2, 0, 3}`
2. Run simulation for 3 generations
3. Verify:
   - Pattern generation works with negative indices
   - Min/max calculations work correctly
   - Sum calculation handles negative numbers

### Success Criteria
- Negative indices are handled correctly
- Sum can be negative if more plants are in negative positions
- No index or range errors

## Test 9: Pattern Not in Rules

### Objective
Verify handling of patterns that don't exist in rules dictionary.

### Test Steps
1. Identify or create a 5-character pattern not in the rules
2. Create a state that would generate this pattern
3. Run simulation
4. Verify the default behavior (should treat as '.' = empty)

### Success Criteria
- Missing patterns default to empty (no plant)
- No KeyError or crashes
- Simulation continues normally

### Implementation Note
Must use `rules.get(pattern, '.')` instead of `rules[pattern]`

## Test 10: Final Sum Calculation

### Objective
Verify the final sum calculation is correct.

### Test Steps
1. Create a known final state: `{-10, -5, 0, 5, 10}`
2. Calculate sum manually: -10 + -5 + 0 + 5 + 10 = 0
3. Verify program calculates same sum
4. Try another state: `{1, 2, 3}` → sum = 6
5. Try negative-heavy state: `{-10, -5, 1}` → sum = -14

### Success Criteria
- Sum matches manual calculation
- Handles positive, negative, and mixed indices
- Handles zero correctly

## Test 11: Rule Application Verification

### Objective
Verify that rules are applied correctly by manually checking a few specific cases.

### Test Steps
1. Pick 3-5 specific rules from input, e.g.:
   - `.##.# => #`
   - `#..#. => .`
   - `#.#.# => #`
2. Create states that produce these exact patterns at specific pot positions
3. Verify the next generation has the correct result for those pots

### Example 1: `.##.# => #`
Pattern `.##.#` at pot 5 requires checking pots [3,4,5,6,7]:
- Pot 3: empty (.)
- Pot 4: plant (#)
- Pot 5: plant (#) - this is the center pot we're evaluating
- Pot 6: empty (.)
- Pot 7: plant (#)
Create state: `{4, 5, 7}`
After simulation, verify pot 5 has a plant in next generation (rule says `#`)

### Example 2: `#..#. => .`
Pattern `#..#.` at pot 10 requires checking pots [8,9,10,11,12]:
- Pot 8: plant (#)
- Pot 9: empty (.)
- Pot 10: empty (.) - center pot
- Pot 11: plant (#)
- Pot 12: empty (.)
Create state: `{8, 11}`
After simulation, verify pot 10 is empty in next generation (rule says `.`)

### Success Criteria
- Rules are applied correctly
- Pattern matching is accurate
- Next generation reflects rule outcomes

## Integration Test: Verify with Example Initial State

### Objective
Verify the simulation runs correctly using the example initial state from the problem.

### Test Steps
1. Use example initial state: `#..#.#..##......###...###`
2. Use the actual rules from our input.md
3. Run for 20 generations
4. Verify the simulation completes successfully

### Important Note
The example in the problem statement used DIFFERENT rules than our input.md file.
Therefore, we CANNOT expect our result to match the example's answer of 325.
This test verifies the simulation mechanics work correctly, not that we get a specific answer.

### Success Criteria
- Simulation completes successfully without errors
- Result is a reasonable integer (could be positive or negative)
- State evolves in a logical manner (no sudden disappearance or exponential explosion)
- The process demonstrates correct pattern matching and rule application

## Final Verification Strategy

### After All Tests Pass
1. Run the complete program with actual input
2. Print intermediate states for generations 0, 5, 10, 15, 20
3. Verify:
   - State is evolving reasonably
   - No anomalies (all plants dying, exponential growth)
   - Sum increases/changes as expected
4. Submit the final answer

### Debugging Checklist if Result Seems Wrong
- [ ] Verify initial state is parsed correctly (count plants, check positions)
- [ ] Verify all rules from input file are parsed correctly
- [ ] Print state after each generation to see evolution
- [ ] Check if any generation becomes empty unexpectedly
- [ ] Verify pattern generation with manual spot checks
- [ ] Check rule lookup is working (no default '.' when rule exists)
- [ ] Verify sum calculation with small test case
- [ ] Verify range expansion is working (min decreases, max increases or stays stable)
- [ ] Check a few specific pots manually to ensure pattern matching is correct

## Output Validation

### Expected Output Characteristics
- Single integer
- Sign depends on distribution of plants (could be positive or negative)
- Magnitude likely in hundreds to low thousands (based on ~100 character initial state and 20 generations)
- Should be reproducible (same input → same output)

### Red Flags
- Zero or very small result (suggests plants died out - check rules)
- Extremely large result (> 100,000 suggests infinite growth bug)
- Result changes between runs (suggests non-deterministic bug)
- All plants disappear before generation 20 (check rule application)

## Summary

This testing plan covers:
- ✅ Input parsing
- ✅ Core algorithm (pattern matching, rule application)
- ✅ Edge cases (empty state, negative indices, missing patterns)
- ✅ Integration (full 20 generations)
- ✅ Output validation

The tests progress from unit-level (parsing, pattern generation) to integration-level (full simulation), ensuring each component works before testing the complete system.
