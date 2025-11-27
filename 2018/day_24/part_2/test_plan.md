# Testing Plan: Immune System Simulator - Part 2 (Boosted Combat)

## Overview
This plan covers verification of the boost functionality, binary search correctness, and overall solution accuracy for Part 2.

## Test Strategy

### 1. Unit Tests (Component Level)

#### Test 1.1: Boost Application
**Purpose**: Verify boost correctly increases Immune System attack damage

**Test cases**:
- Apply boost of 0 → attack damage unchanged
- Apply boost of 100 → each immune group's attack damage increases by 100
- Apply boost to groups with different base damage values
- Verify Infection groups are NOT modified

**Validation**:
```python
# Parse original groups and record attack damages
immune_groups, infection_groups = parse_input("input.md")
original_damages = [g.attack_damage for g in immune_groups]

# Parse fresh groups and apply boost
immune_groups_2, _ = parse_input("input.md")
apply_boost(immune_groups_2, 50)
boosted_damages = [g.attack_damage for g in immune_groups_2]

# Verify each increased by exactly 50
for orig, boosted in zip(original_damages, boosted_damages):
    assert boosted == orig + 50

# Verify infection groups are not affected
_, infection_groups = parse_input("input.md")
infection_damages_before = [g.attack_damage for g in infection_groups]
apply_boost(immune_groups_2, 100)  # Apply another boost, infection should still be unchanged
_, infection_groups_2 = parse_input("input.md")
infection_damages_after = [g.attack_damage for g in infection_groups_2]
assert infection_damages_before == infection_damages_after
```

#### Test 1.2: Stalemate Detection
**Purpose**: Verify stalemate detection works correctly

**Test scenarios**:
- Combat where no damage is dealt → should return "Stalemate"
- Combat where groups can't select targets (all immune) → should return "Stalemate"
- Normal combat ending → should NOT return "Stalemate"

**Manual test**: Create artificial scenario where all remaining groups are immune to each other's attacks.

#### Test 1.3: simulate_combat() Return Values
**Purpose**: Verify simulate_combat() returns correct tuple (unchanged from Part 1)

**Validation**:
- Check return type is tuple with 2 elements: (winner, units_remaining)
- Verify winner is one of: "Immune System", "Infection", "Stalemate"
- Verify units_remaining is non-negative integer
- No third element needed - Part 1's implementation already handles stalemates

```python
immune, infection = parse_input("input.md")
winner, units = simulate_combat(immune, infection)
assert isinstance(winner, str)
assert winner in ["Immune System", "Infection", "Stalemate"]
assert isinstance(units, int)
assert units >= 0
```

### 2. Integration Tests (Algorithm Level)

#### Test 2.1: Known Example Validation
**Purpose**: Verify solution works on the provided example

**Given** (from problem statement):
- Example input from puzzle (has 2 Immune System groups and 2 Infection groups)
- Expected minimum boost: 1570
- Expected units remaining: 51

**Test procedure**:
1. Create `example_input.md` file with the example data from the puzzle description:
   - 2 Immune System groups with attack damages 4507 and 25
   - 2 Infection groups
2. Temporarily modify code to use "example_input.md" instead of "input.md"
3. Run find_minimum_boost() on example
4. Verify returned boost is 1570
5. Simulate with boost 1570
6. Verify Immune System wins with 51 units

**Success criteria**:
- Minimum boost found = 1570
- Final answer = 51 units

**Note**: Extract example data from puzzle description into separate file for this test.

#### Test 2.2: Binary Search Correctness
**Purpose**: Verify binary search finds the true minimum

**Test procedure**:
1. Find minimum boost using binary search: `min_boost`
2. Verify boost `min_boost - 1` does NOT result in Immune System win
3. Verify boost `min_boost` DOES result in Immune System win
4. Verify boost `min_boost + 1` DOES result in Immune System win

**Validation code**:
```python
min_boost = find_minimum_boost()

# Test min_boost - 1 (should fail)
immune, infection = parse_input("input.md")
apply_boost(immune, min_boost - 1)
winner, units = simulate_combat(immune, infection)
assert winner != "Immune System", f"Boost {min_boost-1} should not win, but got {winner}"

# Test min_boost (should win)
immune, infection = parse_input("input.md")
apply_boost(immune, min_boost)
winner, units = simulate_combat(immune, infection)
assert winner == "Immune System", f"Boost {min_boost} should win"
assert units > 0, "Winning army should have units remaining"

# Test min_boost + 1 (should also win)
immune, infection = parse_input("input.md")
apply_boost(immune, min_boost + 1)
winner, units = simulate_combat(immune, infection)
assert winner == "Immune System", f"Boost {min_boost+1} should win"
```

#### Test 2.3: Boost Range Adequacy
**Purpose**: Verify binary search range is sufficient

**Test**:
- If minimum boost found is close to upper bound (e.g., > 9000 when upper = 10000)
- Warning: may need to increase search range

**Validation**:
```python
UPPER_BOUND = 10000  # Should match the upper bound used in find_minimum_boost()
min_boost = find_minimum_boost()
# Warn if boost is close to upper bound (may need larger range)
if min_boost > 0.9 * UPPER_BOUND:
    print(f"Warning: min_boost ({min_boost}) is close to upper bound ({UPPER_BOUND})")
    print("Consider increasing the search range if this seems unreasonable")
```

### 3. Functional Tests (End-to-End)

#### Test 3.1: No Boost Scenario (Regression Test)
**Purpose**: Verify boost=0 gives same result as Part 1

**Note**: Binary search starts at boost=1, but we can test boost=0 separately for regression.

**Test**:
1. Parse fresh groups
2. Apply boost of 0 (should have no effect)
3. Run simulation
4. Compare result to Part 1 answer (22244 units for Infection)

**Expected**: Winner = "Infection", units = 22244

**Validation**:
```python
immune, infection = parse_input("input.md")
apply_boost(immune, 0)  # No boost
winner, units = simulate_combat(immune, infection)
assert winner == "Infection", "Without boost, Infection should win (Part 1 result)"
assert units == 22244, f"Expected 22244 units (Part 1 answer), got {units}"
```

#### Test 3.2: Incremental Boost Testing (Monotonic Property)
**Purpose**: Verify monotonic property - once Immune System wins, it keeps winning at higher boosts

**Test procedure**:
```python
results = []
for boost in [0, 10, 50, 100, 500, 1000, 2000, 5000]:
    immune, infection = parse_input("input.md")
    apply_boost(immune, boost)
    winner, units = simulate_combat(immune, infection)
    results.append((boost, winner, units))
    print(f"Boost {boost:5d}: {winner:15s} with {units:5d} units")

# Verify monotonic property: once Immune System wins, it keeps winning
immune_started_winning = False
for boost, winner, units in results:
    if winner == "Immune System":
        immune_started_winning = True
    if immune_started_winning:
        assert winner == "Immune System", \
            f"Monotonic property violated: Immune System stopped winning at boost {boost}"
```

**Expected pattern**:
```
Boost 0-X: Infection wins or stalemate
Boost X+1 onwards: Immune System wins (with potentially more units at higher boosts)
```

#### Test 3.3: Actual Input Validation
**Purpose**: Final answer verification

**Test procedure**:
1. Run solution on actual input.md
2. Record minimum boost found
3. Record final units remaining
4. Manually verify a few simulations around the found minimum:
   - Run with (min_boost - 1): should not win
   - Run with (min_boost): should win
   - Run with (min_boost + 1): should win

### 4. Edge Cases and Boundary Conditions

#### Test 4.1: Boost = 1
**Purpose**: Test smallest possible boost

**Test**: Apply boost=1, verify it likely doesn't win (unless problem is trivial)

#### Test 4.2: Very Large Boost
**Purpose**: Test upper boundary behavior

**Test**: Apply boost=100000, verify Immune System wins decisively

#### Test 4.3: Empty Group Handling
**Purpose**: Verify groups with 0 units don't cause issues

**Validation**: Already handled by Part 1 code with `is_alive()` checks

#### Test 4.4: Rounding and Integer Division
**Purpose**: Verify damage calculations remain correct with boosted values

**Test**:
- Check that units killed still uses integer division
- Verify no floating-point errors introduced
- Test with groups that have varying hit points

### 5. Performance and Efficiency Tests

#### Test 5.1: Runtime Measurement
**Purpose**: Verify solution runs in reasonable time

**Test**:
```python
import time
start = time.time()
result = find_minimum_boost()
elapsed = time.time() - start
print(f"Binary search completed in {elapsed:.3f} seconds")
assert elapsed < 2.0, f"Should complete in under 2 seconds, took {elapsed:.3f}s"
```

**Expected**: Typically < 1 second on modern hardware, allow up to 2 seconds for conservative margin

#### Test 5.2: Binary Search Iterations
**Purpose**: Verify binary search efficiency

**Test**: Add logging to count number of simulations run
- Expected: ~13-15 simulations for range [1, 10000]
- If significantly higher: investigate binary search logic

### 6. Regression Tests

#### Test 6.1: Part 1 Compatibility
**Purpose**: Verify Part 1 functionality not broken

**Test**:
1. Run simulation with boost=0
2. Compare to Part 1 answer (22244)

**Expected**: Identical result to Part 1

### 7. Debugging and Verification Tests

#### Test 7.1: Manual Combat Verification
**Purpose**: Manually trace through one combat round with boost

**Procedure**:
1. Enable DEBUG flag
2. Run with specific boost value
3. Manually verify:
   - Effective power calculations include boost
   - Target selection is correct
   - Damage calculations are accurate
   - Unit deaths are correct

#### Test 7.2: Boost Isolation
**Purpose**: Verify boost only affects Immune System groups, not Infection groups

**Test**:
```python
# Parse and record original damages
immune, infection = parse_input("input.md")
original_immune_damages = [g.attack_damage for g in immune]
original_infection_damages = [g.attack_damage for g in infection]

# Apply boost to immune system
apply_boost(immune, 1000)

# Verify immune groups were boosted
for i, group in enumerate(immune):
    assert group.attack_damage == original_immune_damages[i] + 1000, \
        f"Immune group {i} not boosted correctly"

# Verify infection groups unchanged (they're in the same list)
for i, group in enumerate(infection):
    assert group.attack_damage == original_infection_damages[i], \
        f"Infection group {i} should not be modified by boost"
```

## Testing Checklist

### Component Tests
- [ ] Boost application increases attack damage correctly (in-place modification)
- [ ] Boost only affects Immune System groups, not Infection
- [ ] Stalemate detection works (inherited from Part 1, returns "Stalemate")
- [ ] simulate_combat() returns correct 2-tuple (unchanged from Part 1)

### Algorithm Tests
- [ ] Binary search finds correct minimum boost
- [ ] Boost (min - 1) does not win
- [ ] Boost (min) does win
- [ ] Boost (min + 1) does win

### Example Validation
- [ ] Example input yields boost=1570, units=51

### Edge Cases
- [ ] Boost=0 matches Part 1 result
- [ ] Very large boost wins decisively
- [ ] No infinite loops or stalemates

### Performance
- [ ] Solution completes in < 2 seconds (typically < 1 second)
- [ ] Binary search runs ~13-15 iterations for range [1, 10000]
- [ ] Upper bound validation detects if range is insufficient

### Final Validation
- [ ] Run on actual input.md
- [ ] Verify answer makes logical sense
- [ ] Record final answer for submission

## Success Criteria

1. **Correctness**: Example test passes (boost=1570, units=51)
2. **Minimum verification**: Boost (min-1) doesn't win, boost (min) does win
3. **Efficiency**: Completes in < 5 seconds
4. **Regression**: Boost=0 matches Part 1 answer
5. **Final answer**: Solution outputs single integer for actual input

## Common Issues to Watch For

1. **Off-by-one errors** in binary search (should converge to minimum winning boost)
2. **Stalemate handling** (must treat stalemates as non-wins, requiring higher boost)
3. **Group mutation** between simulations (must parse fresh groups each time)
4. **Boost not applied** to all Immune System groups
5. **Wrong army boosted** (accidentally boosting Infection instead of Immune System)
6. **Insufficient search range** (upper bound too low - should validate after search)
7. **Return value unpacking** (simulate_combat returns 2-tuple, not 3-tuple)
8. **In-place modification** (apply_boost modifies groups in-place, not creating copies)

## Final Validation Procedure

Before submitting the answer:
1. Run solution on actual input
2. Note the minimum boost value found
3. Manually verify with boost-1 and boost+1
4. Check answer is a reasonable positive integer
5. Review any debug output for anomalies
6. Submit the final answer
