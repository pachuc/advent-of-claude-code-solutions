# Problem Report: Beverage Bandits Combat Simulation

## Objective
Simulate a turn-based combat between Elves (E) and Goblins (G) on a grid map and calculate the outcome of the battle. The outcome is defined as: **number of full rounds completed × sum of remaining units' hit points**.

## Input Format
A 2D grid map where:
- `#` = walls (impassable)
- `.` = open cavern (passable)
- `G` = Goblin starting position
- `E` = Elf starting position

## Combat Rules

### Turn Order
- Combat proceeds in rounds
- Each round, all living units take turns in **reading order** (top-to-bottom, left-to-right based on their current positions)
- If no targets remain at the start of any unit's turn, combat ends immediately

### Unit Stats
- All units start with **200 hit points**
- All units have **3 attack power**
- Units can only move/attack in 4 directions: up, down, left, right (no diagonals)

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
5. Deal 3 damage to selected target
6. If target's HP ≤ 0, target dies and its square becomes `.`

### Tie-Breaking Rule
Whenever multiple options are equally valid, choose the first in **reading order**:
- Reading order = top-to-bottom, then left-to-right
- Applies to: turn order, target selection, destination selection, step selection

## Output
Calculate and return the **outcome** value:
```
outcome = completed_full_rounds × sum_of_remaining_hp
```

**Important**: Only count full rounds. If combat ends mid-round (a unit finds no targets), that round doesn't count.

## Example
```
47 full rounds completed
Remaining units: G(200), G(131), G(59), G(200)
Sum of HP: 200 + 131 + 59 + 200 = 590
Outcome: 47 × 590 = 27730
```

## Key Implementation Considerations
1. Units act in reading order **each round** based on current positions
2. Combat ends immediately when a unit finds no targets (mid-round possible)
3. Unit death is immediate - dead units don't take remaining turns
4. Pathfinding must find shortest paths and break ties correctly
5. When choosing next step, must consider ALL shortest paths to destination
6. Movement happens on current game state (no prediction of future positions)
