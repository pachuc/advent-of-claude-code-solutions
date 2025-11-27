# Testing Plan: Beverage Bandits Combat Simulation

## Updates from Critique
This plan has been updated to address the following key issues from the critique:
1. **Concrete expected values**: Added specific calculations and expected results to weak assertions (Test 1.6, 1.7)
2. **Fixed Test 3.4 calculation**: Corrected the round counting for adjacent units (66 completed rounds, not 67)
3. **Clarified direction order**: Updated Test 1.7 to distinguish direction order from reading order
4. **Added missing test case**: Test 2.1 now covers multiple units dying in same round
5. **Improved Test 2.3**: Added detailed step-by-step expected sequence with corrected calculations
6. **Max rounds handling**: Updated Test 3.5 to reflect the 10000 round safety limit
7. **Better test organization**: Reordered and renumbered tests for better flow
8. **Outcome range clarification**: Marked expected range as "rough sanity check only"

## Testing Strategy

Since this is a script to solve a specific problem (not production code), our testing will focus on:
1. Correctness of core algorithms
2. Proper handling of tie-breaking rules
3. Edge cases specific to the problem
4. Validation against known examples

We will NOT test for:
- Invalid inputs (malformed grids, negative HP, etc.)
- Performance at extreme scales
- Concurrent access or thread safety
- Extensive input validation

## Test Levels

### Level 1: Unit Tests (Component Testing)
Test individual functions in isolation.

### Level 2: Integration Tests
Test combinations of components.

### Level 3: Scenario Tests
Test full combat scenarios with known outcomes.

### Level 4: Final Validation
Test against actual input.

---

## Level 1: Unit Tests

### Test 1.1: Parse Input
**Purpose**: Verify grid and units are created correctly.

**Test Case**:
```
#######
#.G.E.#
#######
```

**Expected**:
- Grid: 7x3 with walls, open spaces, G, E
- Units: 2 units
  - Unit 1: (2, 1), type='G', hp=200
  - Unit 2: (4, 1), type='E', hp=200

**Validation**:
```python
assert len(units) == 2
assert units[0].type == 'G'
assert units[0].x == 2 and units[0].y == 1
assert units[1].type == 'E'
```

---

### Test 1.2: Reading Order Sort
**Purpose**: Verify reading order sorting.

**Test Case**:
Units at positions: (5, 2), (1, 1), (3, 1), (2, 3)

**Expected Order**: (1, 1), (3, 1), (5, 2), (2, 3)

**Validation**:
```python
sorted_positions = [(u.x, u.y) for u in sort_units(units)]
assert sorted_positions == [(1, 1), (3, 1), (5, 2), (2, 3)]
```

---

### Test 1.3: Find Targets
**Purpose**: Verify enemy detection.

**Test Case**:
- 3 Goblins
- 2 Elves
- Test from Goblin perspective

**Expected**: Should find 2 Elves only

**Validation**:
```python
targets = find_targets(goblin_unit, all_units)
assert len(targets) == 2
assert all(t.type == 'E' for t in targets)
```

---

### Test 1.4: BFS Pathfinding
**Purpose**: Verify BFS returns correct distances.

**Test Case**:
```
#######
#.....#
#.###.#
#.....#
#######
```
Start at (1, 1), target (5, 3).

**Expected**:
- Distance to (1, 1): 0
- Distance to (2, 1): 1
- Distance to (1, 2): 1
- Distance to (5, 3): 6
- Unreachable squares inside ### not in dict

**Validation**:
```python
distances = bfs_distances(grid, 1, 1, [])
assert distances[(1, 1)] == 0
assert distances[(2, 1)] == 1
assert distances[(5, 3)] == 6
assert (2, 2) not in distances  # Inside wall
```

---

### Test 1.5: In-Range Squares
**Purpose**: Verify finding adjacent open squares.

**Test Case**:
```
#######
#..G..#
#.....#
#..E..#
#######
```
Goblin at (3, 1), Elf at (3, 3)

**Expected In-Range** (from Goblin's perspective, targeting Elf):
- (2, 3), (4, 3), (3, 2) - squares adjacent to Elf

**Validation**:
```python
in_range = find_in_range_squares([elf], grid, units)
assert (2, 3) in in_range
assert (4, 3) in in_range
assert (3, 2) in in_range
assert len(in_range) == 3
```

---

### Test 1.6: Choose Destination - Distance Tie
**Purpose**: Verify reading order tie-breaking for equal distances.

**Test Case**:
```
#######
#.....#
#..G..#
#.....#
#E...E#
#######
```
Goblin at (3, 2). Two Elves at (1, 4) and (5, 4).

**Expected Calculation**:
- Elf1 at (1, 4): in-range squares are (1, 3), (2, 4), (0, 4) if exists
- Elf2 at (5, 4): in-range squares are (5, 3), (4, 4), (6, 4) if exists
- From Goblin at (3, 2):
  - Distance to (1, 3): 3 steps (left 2, down 1)
  - Distance to (2, 4): 3 steps (left 1, down 2)
  - Distance to (5, 3): 3 steps (right 2, down 1)
  - Distance to (4, 4): 3 steps (right 1, down 2)
- All equidistant at distance 3
- Reading order: (1, 3) is first (topmost, then leftmost)

**Expected Destination**: (1, 3)

**Validation**:
```python
dest = choose_destination(goblin, [elf1, elf2], grid)
assert dest == (1, 3)
```

---

### Test 1.7: Choose Next Step - Direction Order
**Purpose**: Verify step selection uses direction order properly.

**Test Case 1** (simple path):
```
#######
#.....#
#..G..#
#.....#
#..E..#
#######
```
Goblin at (3, 2), Elf at (3, 4). Destination is (3, 3).

**Expected**:
- Only one valid path: down
- Next step: (3, 3)

**Test Case 2** (multiple equal paths):
```
#########
#.......#
#...G...#
#.......#
#...E...#
#########
```
Goblin at (4, 2), Elf at (4, 4), destination (4, 3).

**Expected**:
- BFS from destination (4, 3) gives distance 1 to (4, 2)
- Only adjacent square to Goblin toward destination: (4, 3) - down
- Next step: (4, 3)

**Test Case 3** (true tie - two equal paths):
```
#######
#..G..#
#.###.#
#.....#
#..E..#
#######
```
Goblin at (3, 1), wall in middle, Elf at (3, 4).
If destination is (3, 3), Goblin can go left or right with equal path length.

**Expected**:
- Check adjacent squares in direction order: up (wall), left (open), right (open), down (wall)
- BFS from destination: both left and right are on shortest paths
- Choose LEFT because it's checked first in direction order

**Note**: Direction order (up, left, right, down) determines which square is selected when
multiple adjacent squares have equal distance to destination. This is NOT the same as
reading order for positions.

---

### Test 1.8: Attack Target Selection - HP Tie
**Purpose**: Verify lowest HP and reading order tie-breaking.

**Test Case**:
```
#####
#GEE#
#####
```
Goblin at (1, 1), two Elves at (2, 1) and (3, 1).
- Elf1 HP: 100
- Elf2 HP: 100

**Expected**: Attack Elf1 (reading order: earlier position).

**Test Case 2**:
- Elf1 HP: 50
- Elf2 HP: 100

**Expected**: Attack Elf1 (lower HP).

**Validation**:
```python
target = choose_attack_target(goblin, [elf1, elf2], grid)
assert target == elf1
```

---

## Level 2: Integration Tests

### Test 2.1: Multiple Units Die Same Round
**Purpose**: Verify multiple units can die in the same round and remaining units still act.

**Test Case**:
```
#########
#.G.E.G.#
#########
```
- Goblin1 at (2, 1), HP: 200
- Elf at (4, 1), HP: 6 (will die in 2 hits)
- Goblin2 at (6, 1), HP: 200

**Round Sequence**:
- Round 1:
  1. Goblin1 (2,1) attacks Elf (HP: 6 → 3)
  2. Elf (4,1) attacks Goblin1 (HP: 200 → 197)
  3. Goblin2 (6,1) attacks Elf (HP: 3 → 0, dies)
- Round 2:
  1. Goblin1 sees no targets, combat ends mid-round

**Expected**:
- Completed rounds: 1
- Goblin1 HP: 197
- Goblin2 HP: 200
- Elf dead

**Validation**:
```python
rounds = simulate_combat(grid, units)
assert rounds == 1
assert sum(1 for u in units if u.alive) == 2
assert all(u.type == 'G' for u in units if u.alive)
```

---

### Test 2.2: Move and Attack in One Turn
**Purpose**: Verify a unit can move and attack in same turn.

**Test Case**:
```
#####
#G.E#
#####
```
Goblin at (1, 1), Elf at (3, 1). One empty space between.

**Expected**:
- Round 1:
  - Goblin moves to (2, 1), now adjacent to Elf, attacks (Elf HP: 197)
  - Elf already adjacent (after Goblin moved), attacks Goblin (Goblin HP: 197)
- Subsequent rounds: Both attack each other

**Validation**:
```python
# After round 1
assert goblin.x == 2 and goblin.y == 1
assert elf.hp == 197
assert goblin.hp == 197
```

---

### Test 2.3: Unit Death During Round
**Purpose**: Verify dead units don't take turns.

**Test Case**:
```
#####
#GEG#
#####
```
- Goblin1 at (1, 1), HP: 200
- Elf at (2, 1), HP: 6 (will die in 2 hits)
- Goblin2 at (3, 1), HP: 200

**Round Execution**:
1. Round 1, Turn 1: Goblin1 attacks Elf (HP: 6 → 3)
2. Round 1, Turn 2: Elf attacks Goblin1 (HP: 200 → 197)
3. Round 1, Turn 3: Goblin2 attacks Elf (HP: 3 → 0, Elf dies)
4. Round 2 starts: Goblin1 sees no targets, combat ends

**Validation**:
```python
# After combat
assert elf.alive == False
assert grid[2][1] == '.'  # Elf position cleared (note: x=2, y=1)
assert rounds == 1  # Only 1 complete round, round 2 ended mid-round
```

---

### Test 2.4: Combat Ends Mid-Round
**Purpose**: Verify incomplete round doesn't count.

**Test Case**:
```
#######
#G...E#
#######
```
Only 2 units, Goblin at (1, 1), Elf at (5, 1).

**Expected Sequence**:
- Distance between them: 4 squares
- Round 1: G moves right (2,1), E moves left (4,1) - now distance 2
- Round 2: G moves right (3,1), E moves left (3,1)? NO - they'd collide
  Actually: G moves to (2,1), sees E not adjacent. E moves to (4,1), sees G not adjacent.
  Let me recalculate: After round 1: G at (2,1), E at (4,1), distance = 2
- Round 2: G moves to (3,1), now adjacent. E already adjacent, no move. Both attack.
  - G attacks E (197 HP), E attacks G (197 HP)
- Rounds 3-68: They fight (66 more rounds total = 67 rounds of combat)
- After round 68: Both have 200 - 67*3 = -1 HP...

**Corrected Calculation**:
Starting distance: 4, approaching takes 2 rounds to be adjacent.
Then 67 rounds of fighting (200 HP / 3 damage per round).
After 66 fight rounds: both at 2 HP.
Round 69 starts: Goblin acts first (reading order), kills Elf. Combat ends mid-round.
Final completed rounds: 68 (2 approach + 66 fight rounds).

**Validation**:
```python
rounds = simulate_combat(grid, units)
# Verify the round where combat ended wasn't counted
assert len([u for u in units if u.alive]) == 1
# Exact round count depends on starting positions and approach time
```

---

## Level 3: Scenario Tests

### Test 3.1: Simple Example from Problem
**Purpose**: Validate against problem example if provided.

Use any worked example from the problem statement.

**Expected**: Match exact outcome value.

---

### Test 3.2: Movement Around Obstacles
**Purpose**: Verify pathfinding navigates walls.

**Test Case**:
```
#########
#G..#..E#
#...#...#
#########
```

**Expected**:
- Goblin takes longer path around wall
- Eventually reaches Elf

---

### Test 3.3: Multiple Units Same Type
**Purpose**: Verify combat with multiple units per side.

**Test Case**:
```
#######
#.G.G.#
#.....#
#.E.E.#
#######
```

**Expected**:
- All 4 units participate
- Turn order follows reading order each round
- Combat proceeds until one side eliminated

---

### Test 3.4: No Movement Needed
**Purpose**: Test scenario where units start adjacent.

**Test Case**:
```
#####
#GE##
#####
```
Goblin at (1, 1), Elf at (2, 1). They are already adjacent.

**Expected Combat Sequence**:
- Round 1: G attacks E (197 HP), E attacks G (197 HP)
- Round 2: G attacks E (194 HP), E attacks G (194 HP)
- ...
- Round 66: G attacks E (2 HP), E attacks G (2 HP)
- Round 67: G attacks first in reading order (E dies with -1 HP), combat ends mid-round

**Expected Result**:
- Completed rounds: 66 (not 67, because round 67 ended mid-round)
- Winner: Goblin with 2 HP remaining
- Outcome: 66 × 2 = 132

**Validation**:
```python
rounds = simulate_combat(grid, units)
assert rounds == 66
living = [u for u in units if u.alive]
assert len(living) == 1
assert living[0].type == 'G'
assert living[0].hp == 2
outcome = calculate_outcome(rounds, units)
assert outcome == 132
```

---

### Test 3.5: No Valid Path
**Purpose**: Verify units skip movement if unreachable.

**Test Case**:
```
#########
#G..###E#
#...###.#
#########
```
Wall separates units completely.

**Expected**:
- Units cannot reach each other
- Each turn: unit finds targets exist, but no in-range squares are reachable
- Units don't move, don't attack
- Combat continues indefinitely

**Handling**: The implementation includes max_rounds = 10000 safety limit to prevent infinite loops.

**Validation**:
```python
rounds = simulate_combat(grid, units)
# Should hit max_rounds limit
assert rounds == 10000
# Both units still alive
assert len([u for u in units if u.alive]) == 2
```

**Note**: This scenario is unlikely in actual AoC input, but the safety limit prevents hangs during development.

---

### Test 3.6: Target Selection with Multiple Options
**Purpose**: Test complex target selection.

**Test Case**:
```
#######
#.EEE.#
#E.G.E#
#.EEE.#
#######
```
Goblin surrounded by Elves with varying HP.

**Expected**:
- Goblin attacks lowest HP Elf
- If tied, attacks first in reading order
- Elves converge and eventually kill Goblin

---

## Level 4: Final Validation

### Test 4.1: Actual Input
**Purpose**: Solve the actual problem.

**Steps**:
1. Run solution on provided input.md
2. Calculate outcome
3. Verify result is reasonable (positive integer)

**Validation Checks**:
- Rounds > 0
- Remaining units > 0
- All remaining units are same type (E or G)
- Outcome value is positive

**Expected Outcome Range** (rough sanity check only):
- Typical AoC Day 15 Part 1: 150,000 - 250,000
- This is only a rough check; exact value depends on specific input

---

### Test 4.2: Trace First 3 Rounds
**Purpose**: Manually verify early rounds for correctness.

**Steps**:
1. Print grid after each turn
2. Print unit positions and HP
3. Manually verify:
   - Turn order is reading order
   - Movement is correct
   - Attacks hit correct targets
   - Grid updates properly

**This catches**:
- Reading order bugs
- Movement logic errors
- Grid synchronization issues

---

## Edge Cases Checklist

### Critical Edge Cases
- [ ] Combat ends mid-round (last enemy dies)
- [ ] Multiple units at same HP (attack selection)
- [ ] Multiple paths of equal length (step selection)
- [ ] Multiple destinations at equal distance (destination selection)
- [ ] Unit already adjacent to enemy (no movement)
- [ ] No valid path to any enemy (skip movement)
- [ ] Dead unit doesn't act in same round

### Reading Order Edge Cases
- [ ] Turn order: units sorted by current position each round
- [ ] Target selection: reading order tie-break
- [ ] Destination selection: reading order tie-break
- [ ] Step selection: reading order tie-break
- [ ] All tie-breaks use (y, x) not (x, y)

### Grid State Edge Cases
- [ ] Grid updated when unit moves
- [ ] Grid updated when unit dies
- [ ] Grid cell shows current unit position
- [ ] Multiple units don't occupy same cell

### Combat End Conditions
- [ ] No enemies at start of unit's turn
- [ ] Round counter doesn't increment for incomplete round
- [ ] Combat ends immediately (no partial turn)

---

## Test Execution Order

1. **Run Unit Tests**: Verify each component works
2. **Run Integration Tests**: Verify components work together
3. **Run Scenario Tests**: Verify full combat logic
4. **Run Final Validation**: Solve actual problem
5. **Manual Trace**: Verify first few rounds by hand if answer seems wrong

---

## Debugging Strategy

If final answer is wrong:

1. **Add Logging**:
   - Print grid after each round
   - Print turn order
   - Print movement decisions
   - Print attack decisions

2. **Compare to Example**:
   - Run on worked example from problem
   - Compare step-by-step

3. **Check Common Bugs**:
   - Reading order (y, x) vs (x, y)
   - Round counting (off by one)
   - Dead units acting
   - Grid not updated

4. **Visualize**:
   - Print grid with HP values
   - Trace specific unit's path

---

## Success Criteria

### Minimum Requirements
- [ ] Solution runs without errors
- [ ] Produces an integer outcome
- [ ] All remaining units are same type (one side won)

### Full Correctness
- [ ] Passes all unit tests
- [ ] Passes scenario tests
- [ ] Produces correct answer for actual input
- [ ] Answer accepted by AoC (if submitting)

---

## Testing Implementation Notes

For this script, we'll implement tests as:

1. **Simple assertions** in a separate test function or at bottom of main file
2. **Print statements** to verify intermediate steps
3. **Manual verification** of first few rounds

We do NOT need:
- Formal test framework (unittest, pytest)
- Mocking or fixtures
- Extensive test coverage metrics
- Automated CI/CD testing

Simple, focused tests that verify correctness are sufficient.
