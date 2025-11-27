# Testing Plan: Part 2 - Elven Victory Without Casualties

## Testing Objectives

1. Verify that the minimum attack power is correctly identified
2. Ensure all Elves survive at the minimum power (zero casualties)
3. Confirm combat simulation produces correct outcomes
4. Validate that one less attack power would result in at least one Elf death
5. Test edge cases and boundary conditions

## Test Data Sources

### 1. Problem Examples
The problem statement provides 5 examples with known answers. However, these examples don't include the actual grid inputs, so they cannot be used directly for testing. They are listed here for reference only:

| Example | Min Elf Attack | Rounds | Outcome |
|---------|---------------|---------|---------|
| 1       | 15            | 29      | 4988    |
| 2       | 4             | 33      | 31284   |
| 3       | 15            | 37      | 3478    |
| 4       | 12            | 39      | 6474    |
| 5       | 34            | 30      | 1140    |

**Note**: These are for conceptual understanding only and cannot be used in automated tests.

### 2. Actual Input
- File: `input.md`
- Contains 32×32 grid with Elves and Goblins
- Initial Elf count: 8 (count from grid)
- Initial Goblin count: 14 (count from grid)

### 3. Comparison with Part 1
- Part 1 answer: 218272 (with attack power 3 for both sides)
- Part 2 should have different outcome due to higher Elf attack power
- Part 2 should result in zero Elf deaths (unlike Part 1, potentially)

## Testing Strategy

### Phase 1: Unit Tests for Modified Functions

#### Test 1.1: Unit Constructor with Attack Power
```python
def test_unit_with_custom_attack():
    # Test Elf with attack 15
    elf = Unit(5, 5, 'E', 15)
    assert elf.attack == 15
    assert elf.hp == 200
    assert elf.type == 'E'

    # Test Goblin with attack 3
    goblin = Unit(10, 10, 'G', 3)
    assert goblin.attack == 3

    # Test default parameter (backward compatibility with Part 1)
    default_unit = Unit(0, 0, 'E', 3)
    assert default_unit.attack == 3
```

**Expected**: All assertions pass

#### Test 1.2: Parse Input with Custom Attack Powers
```python
def test_parse_with_attack_powers():
    sample_input = """#######
#.G.E.#
#E..G.#
#.....#
#######"""

    # Test with positional arguments (matches implementation plan)
    grid, units = parse_input(sample_input, 15, 3)

    # Check Elf attack powers
    elves = [u for u in units if u.type == 'E']
    assert all(e.attack == 15 for e in elves)

    # Check Goblin attack powers
    goblins = [u for u in units if u.type == 'G']
    assert all(g.attack == 3 for g in goblins)

    # Check count
    assert len(elves) == 2
    assert len(goblins) == 2
```

**Expected**: All assertions pass

### Phase 2: Integration Tests for Simulation

#### Test 2.1: Elf Casualty Detection
```python
def test_elf_casualty_detection():
    # Create scenario where Elf attack power is too low
    sample_input = """#######
#.G.E.#
#######"""

    # With attack 3, Elf might die
    success, rounds, outcome = simulate_with_elf_check(sample_input, 3)
    # success might be False (Elf could die)

    # With attack 200, Elf should survive easily
    success, rounds, outcome = simulate_with_elf_check(sample_input, 200)
    assert success == True  # Elf should survive
```

**Expected**: High attack power ensures Elf survival

#### Test 2.1b: Determinism Test
```python
def test_simulation_is_deterministic():
    """Verify that multiple runs produce identical results"""
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Run simulation multiple times with same attack power
    results = []
    for _ in range(3):
        success, rounds, outcome = simulate_with_elf_check(input_text, 15)
        results.append((success, rounds, outcome))

    # All results should be identical
    assert all(r == results[0] for r in results)
```

**Expected**: All runs produce identical results

#### Test 2.1c: Attack Power Propagation
```python
def test_attack_power_actually_used():
    """Verify that Elves actually use the custom attack power in combat"""
    sample_input = """#######
#..G..#
#.E...#
#######"""

    # Run with attack 200 - should kill Goblin (200 HP) in one hit
    grid, units = parse_input(sample_input, 200, 3)

    # Verify Elf has attack 200
    elf = [u for u in units if u.type == 'E'][0]
    assert elf.attack == 200

    # Run simulation - should be very quick (1-2 rounds)
    rounds = simulate_combat(grid, units)

    # Should complete in very few rounds due to high damage
    assert rounds <= 2
```

**Expected**: High attack power leads to quick victory

#### Test 2.2: All Elves Must Survive
```python
def test_all_elves_must_survive():
    # Load actual input
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Count initial Elves
    grid, units = parse_input(input_text, 3, 3)
    initial_elves = sum(1 for u in units if u.type == 'E')

    # Run search for minimum power
    min_power, rounds, outcome = find_minimum_elf_attack_power(input_text)

    # Use the success flag from simulate_with_elf_check
    success, _, _ = simulate_with_elf_check(input_text, min_power)

    # Success means all Elves survived
    assert success == True

    # Verify by counting: all Elves should survive
    grid, units = parse_input(input_text, min_power, 3)
    simulate_combat(grid, units)
    surviving_elves = sum(1 for u in units if u.alive and u.type == 'E')
    assert surviving_elves == initial_elves
```

**Expected**: All Elves survive with minimum power

#### Test 2.3: All Goblins Must Die
```python
def test_all_goblins_must_die():
    with open('input.md', 'r') as f:
        input_text = f.read()

    min_power, rounds, outcome = find_minimum_elf_attack_power(input_text)

    # Verify Goblins are eliminated
    grid, units = parse_input(input_text, min_power, 3)
    rounds = simulate_combat(grid, units)

    surviving_goblins = sum(1 for u in units if u.alive and u.type == 'G')

    assert surviving_goblins == 0
```

**Expected**: No Goblins survive

### Phase 3: Boundary Tests

#### Test 3.1: Minimum Power is Actually Minimum
```python
def test_minimum_is_actually_minimum():
    """Verify that (min_power - 1) would fail"""
    with open('input.md', 'r') as f:
        input_text = f.read()

    min_power, _, _ = find_minimum_elf_attack_power(input_text)

    # Test that one less fails
    if min_power > 4:  # Only test if min_power > 4
        success, _, _ = simulate_with_elf_check(input_text, min_power - 1)
        assert success == False  # Should fail (Elf dies or Goblins win)

    # Test that min_power succeeds
    success, _, _ = simulate_with_elf_check(input_text, min_power)
    assert success == True
```

**Expected**: min_power works, min_power-1 fails

#### Test 3.2: Attack Power Must Be At Least 4
```python
def test_attack_power_minimum():
    min_power, _, _ = find_minimum_elf_attack_power(input_text)
    assert min_power >= 4
```

**Expected**: Minimum power is at least 4

### Phase 4: Outcome Verification

#### Test 4.1: Outcome Calculation
```python
def test_outcome_calculation():
    """Verify outcome = rounds × sum(HP)"""
    with open('input.md', 'r') as f:
        input_text = f.read()

    min_power, rounds, outcome = find_minimum_elf_attack_power(input_text)

    # Re-simulate to verify
    grid, units = parse_input(input_text, min_power, 3)
    actual_rounds = simulate_combat(grid, units)

    # Calculate outcome manually
    surviving_units = [u for u in units if u.alive]
    total_hp = sum(u.hp for u in surviving_units)
    expected_outcome = actual_rounds * total_hp

    assert outcome == expected_outcome
    assert rounds == actual_rounds
```

**Expected**: Outcome matches formula

### Phase 5: Performance Tests

#### Test 5.1: Runtime Performance
```python
def test_performance():
    """Ensure solution completes in reasonable time"""
    import time

    with open('input.md', 'r') as f:
        input_text = f.read()

    start_time = time.time()
    min_power, rounds, outcome = find_minimum_elf_attack_power(input_text)
    elapsed_time = time.time() - start_time

    print(f"Found solution in {elapsed_time:.2f} seconds")

    # Should complete within 5 seconds (based on complexity analysis)
    assert elapsed_time < 5.0
```

**Expected**: Completes in < 5 seconds

### Phase 6: Regression Tests Against Part 1

#### Test 6.1: Part 1 Behavior Still Works
```python
def test_part1_still_works():
    """Verify we didn't break Part 1 functionality"""
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Simulate with attack power 3 for both (Part 1 scenario)
    grid, units = parse_input(input_text, 3, 3)
    rounds = simulate_combat(grid, units)
    outcome = calculate_outcome(rounds, units)

    # Should match Part 1 answer
    assert outcome == 218272
```

**Expected**: Part 1 answer is reproduced

### Phase 7: Edge Cases

#### Test 7.1: Combat Termination Conditions
```python
def test_combat_termination():
    """Verify combat ends correctly when one side is eliminated"""
    sample_input = """#######
#..G..#
#.E...#
#######"""

    # Run with very high Elf attack
    grid, units = parse_input(sample_input, 200, 3)
    rounds = simulate_combat(grid, units)

    # Verify Goblins eliminated
    goblins = [u for u in units if u.alive and u.type == 'G']
    assert len(goblins) == 0

    # Verify Elves survive
    elves = [u for u in units if u.alive and u.type == 'E']
    assert len(elves) == 1
```

**Expected**: Combat ends with correct winner

#### Test 7.2: Elf Dies on Last Turn Edge Case
```python
def test_elf_death_counts_as_failure():
    """Even if Elves win, any Elf death is a failure"""
    sample_input = """#######
#.G.E.#
#######"""

    # Try with low attack power where Elf might die
    success1, _, _ = simulate_with_elf_check(sample_input, 4)

    # Try with high attack power where Elf definitely survives
    success2, _, _ = simulate_with_elf_check(sample_input, 200)

    # At least one should succeed (high power)
    assert success2 == True

    # If low power fails, verify it's due to Elf casualties
    if not success1:
        grid, units = parse_input(sample_input, 4, 3)
        initial_elves = sum(1 for u in units if u.type == 'E')
        simulate_combat(grid, units)
        surviving_elves = sum(1 for u in units if u.alive and u.type == 'E')
        # Should have casualties
        assert surviving_elves < initial_elves
```

**Expected**: Elf death is correctly detected as failure

## Manual Verification Steps

### Step 1: Count Initial Units
```bash
# Count Elves in input.md
grep -o E input.md | wc -l

# Count Goblins in input.md
grep -o G input.md | wc -l
```

**Expected**: Get exact counts to verify later

### Step 2: Run Solution
```bash
python solution.py
```

**Expected output format**:
```
Minimum Elf attack power: <number>
Completed rounds: <number>
Outcome: <number>
<number>
```

### Step 3: Verify Zero Casualties
- Check that "Minimum Elf attack power" is ≥ 4
- Outcome should be different from Part 1 (218272)
- Outcome should be positive

### Step 4: Verify Minimum is Actually Minimum
Manually test with one less attack power:

```python
# If solution says min_power = 15, test with 14
grid, units = parse_input(input_text, 14, 3)
initial_elves = sum(1 for u in units if u.type == 'E')
simulate_combat(grid, units)
surviving_elves = sum(1 for u in units if u.alive and u.type == 'E')

# Should have casualties
assert surviving_elves < initial_elves
```

### Step 5: Test Error Handling
Test what happens if no solution exists in range:

```python
# Artificially create impossible scenario (optional test)
# This tests the error handling added to the implementation
```

**Expected**: Should never occur with valid inputs, but implementation should handle gracefully

## Test Execution Order

1. **Unit tests first** (Phase 1) - Fast, focused tests
   - Test 1.1: Unit constructor
   - Test 1.2: Parse input
2. **Integration tests** (Phase 2) - Verify core functionality
   - Test 2.1: Elf casualty detection
   - Test 2.1b: Determinism (moved from manual)
   - Test 2.1c: Attack power propagation
   - Test 2.2: All Elves survive
   - Test 2.3: All Goblins die
3. **Boundary tests** (Phase 3) - Ensure correctness at edges
4. **Outcome verification** (Phase 4) - Validate calculations
5. **Regression tests** (Phase 6) - Ensure Part 1 still works
6. **Edge cases** (Phase 7) - Cover unusual scenarios
7. **Performance tests** (Phase 5) - Last, since they're slowest
8. **Manual verification** - Final human check

## Success Criteria

The solution is correct if:

1. ✅ Minimum attack power is ≥ 4
2. ✅ All Elves survive with that power
3. ✅ All Goblins die with that power
4. ✅ Attack power (min - 1) results in failure
5. ✅ Outcome = rounds × sum(surviving_HP)
6. ✅ Solution is deterministic (same answer every run)
7. ✅ Solution completes in < 5 seconds
8. ✅ Part 1 regression test passes (outcome = 218272 with attack 3)
9. ✅ Elves actually use the custom attack power in combat
10. ✅ Error handling works for edge cases

## Debugging Strategies

### If Answer Seems Wrong

1. **Print intermediate results**:
   - Print attack power being tested
   - Print whether Elves survived for each attempt
   - Print number of casualties

2. **Visualize final state**:
   - Print grid after combat
   - Print surviving units and their HP

3. **Trace binary search**:
   - Print each binary search iteration
   - Show which powers succeed vs. fail

4. **Compare with Part 1**:
   - Verify Part 1 still produces 218272
   - If not, core simulation is broken

### If Performance is Slow

1. **Profile the code**:
   - Measure simulation time per attack power
   - Count number of simulations run

2. **Check search algorithm**:
   - Verify binary search is working correctly
   - Should be ~8 iterations for range 4-200

3. **Check combat loop**:
   - Ensure simulation terminates
   - Check for infinite loops in combat

## Expected Results for Actual Input

Based on the problem:
- Minimum Elf attack power: Unknown (to be determined)
- Should be between 4 and 200
- Outcome: Unknown positive integer
- Runtime: < 5 seconds expected

The answer will be validated by:
1. All tests passing
2. Consistent results across multiple runs
3. Logical outcome value
4. Different from Part 1 answer (218272)
