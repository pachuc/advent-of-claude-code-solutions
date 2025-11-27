# Problem Report: Beverage Bandits Combat - Part 2 (Elven Victory Required)

## Context from Part 1

In Part 1, we simulated a turn-based combat between Elves (E) and Goblins (G) on a grid map. The combat followed specific rules for turn order, movement, and attack, ultimately calculating an outcome value. The Part 1 solution found that with standard attack powers (3 for both sides), the outcome was **218272**.

## Part 2 Objective

Find the **minimum integer attack power** (at least 4) that the Elves need to **win without a single Elf dying**. Then calculate the outcome of that specific battle.

**Key constraints:**
- Elves must win (all Goblins defeated)
- **Zero Elf casualties are acceptable** (even one Elf death is a failure)
- Elf attack power must be ≥ 4
- Goblins always have attack power = 3
- We need the **lowest** attack power that satisfies these conditions

## Input Format
Same as Part 1: A 2D grid map where:
- `#` = walls (impassable)
- `.` = open cavern (passable)
- `G` = Goblin starting position
- `E` = Elf starting position

## Combat Rules (Same as Part 1)

### Unit Stats
- All units start with **200 hit points**
- Goblins have **3 attack power** (fixed)
- **Elves have variable attack power** (to be determined)
- Units can only move/attack in 4 directions: up, down, left, right (no diagonals)

### Turn Order
- Combat proceeds in rounds
- Each round, all living units take turns in **reading order** (top-to-bottom, left-to-right based on current positions)
- If no targets remain at the start of any unit's turn, combat ends immediately

### Movement Phase
1. Identify all enemy units (targets)
2. If no targets exist, combat ends
3. Find all open squares (`.`) adjacent to any target (in-range squares)
4. If already adjacent to a target, skip movement
5. If not adjacent and no reachable in-range squares exist, end turn
6. Otherwise, move one step toward the nearest in-range square:
   - Use BFS/pathfinding to find reachable in-range squares
   - Choose the in-range square reachable in fewest steps
   - If tied, choose first in reading order
   - Move one step toward that square along the shortest path
   - If multiple first steps are equally short, choose first step in reading order

### Attack Phase
1. After moving (or if already in range), identify all adjacent enemies
2. If no adjacent enemies, end turn
3. Select target with lowest hit points
4. If tied on hit points, choose first in reading order
5. Deal damage to selected target (3 for Goblins, variable for Elves)
6. If target's HP ≤ 0, target dies and its square becomes `.`

### Tie-Breaking Rule
Whenever multiple options are equally valid, choose the first in **reading order**:
- Reading order = top-to-bottom, then left-to-right
- Applies to: turn order, target selection, destination selection, step selection

## Algorithm Approach

Since we need the minimum Elf attack power that results in zero Elf deaths:

1. **Binary search or linear search** starting from attack power = 4
2. For each attack power value:
   - Simulate the complete combat with Elves having that attack power
   - Track whether any Elf dies during the simulation
   - If all Elves survive and all Goblins are defeated: SUCCESS
   - If any Elf dies: try higher attack power
3. Once minimum successful attack power is found, use that simulation's outcome

**Important implementation notes:**
- Must reset the entire game state for each attempt (fresh grid, fresh units)
- Count initial number of Elves at start
- During simulation, check if any Elf dies (immediately fail that attempt)
- Combat must end with Elves winning (all Goblins dead)

## Output

Calculate and return the **outcome** value for the successful battle:
```
outcome = completed_full_rounds × sum_of_remaining_elf_hp
```

**Important**: Only count full rounds. If combat ends mid-round (a unit finds no targets), that round doesn't count.

## Examples from Puzzle

Example 1: Minimum Elf attack power = **15**
```
Combat ends after 29 full rounds
Elves remaining: E(158), E(14)
Sum of HP: 158 + 14 = 172
Outcome: 29 × 172 = 4988
```

Example 2: Minimum Elf attack power = **4**
```
Combat ends after 33 full rounds
Sum of HP: 948
Outcome: 33 × 948 = 31284
```

Example 3: Minimum Elf attack power = **15**
```
Outcome: 37 × 94 = 3478
```

Example 4: Minimum Elf attack power = **12**
```
Outcome: 39 × 166 = 6474
```

Example 5: Minimum Elf attack power = **34**
```
Outcome: 30 × 38 = 1140
```

## Key Implementation Differences from Part 1

1. **Elf attack power is variable** (not fixed at 3)
2. **Must track Elf casualties** during simulation
3. **Must iterate/search** for the minimum successful attack power
4. **Game state must be resetable** for multiple simulation attempts
5. Success condition: All Elves alive + All Goblins dead
