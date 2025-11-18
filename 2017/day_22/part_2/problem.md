# Problem Report: Evolved Sporifica Virus Simulation (Part 2)

## Objective
Simulate an evolved version of the virus carrier with a 4-state infection cycle instead of the original 2-state toggle. Count how many bursts of activity result in a node becoming infected after **10,000,000 bursts**.

## Context from Part 1
In Part 1, we simulated a virus carrier on an infinite 2D grid with simple behavior:
- Nodes had 2 states: CLEAN or INFECTED
- The carrier toggled between these states
- After 10,000 bursts, we counted infections

**Part 1 Answer**: 5404 infections occurred in 10,000 bursts.

## Part 2 Evolution
The virus has evolved to resist removal. It now uses a **4-state infection cycle** with more complex turning logic.

## Input Format
Same as Part 1:
- A 2D grid map showing the initial state of the center portion of an infinite grid
- `.` represents a CLEAN node
- `#` represents an INFECTED node
- The grid dimensions are odd (25x25), allowing for a center node
- The input is provided as lines of text where each character is a node

## Initial Conditions
- The virus carrier starts at the center node of the input grid
- The carrier initially faces UP (north)
- The grid extends infinitely in all directions beyond the input map
- All nodes outside the input map start as CLEAN
- No nodes start as WEAKENED or FLAGGED (only CLEAN or INFECTED)

## Four-State Infection Cycle
Each node transitions through these states in order:
1. **CLEAN** → **WEAKENED**
2. **WEAKENED** → **INFECTED** (count this!)
3. **INFECTED** → **FLAGGED**
4. **FLAGGED** → **CLEAN** (cycle repeats)

## Virus Carrier Behavior (Per Burst)
Each burst consists of the following steps executed in order:

1. **Turn based on current node state**:
   - If CLEAN: turn LEFT (90 degrees counter-clockwise)
   - If WEAKENED: do NOT turn (continue same direction)
   - If INFECTED: turn RIGHT (90 degrees clockwise)
   - If FLAGGED: REVERSE direction (180 degrees)

2. **Advance node state** (according to the 4-state cycle above):
   - CLEAN → WEAKENED
   - WEAKENED → INFECTED (increment infection counter)
   - INFECTED → FLAGGED
   - FLAGGED → CLEAN

3. **Move forward**:
   - Move one node in the direction the carrier is currently facing

## Output Requirements
- A single integer: the count of how many bursts caused a node to become infected
- Run the simulation for exactly **10,000,000 bursts** (10 million, much longer than Part 1's 10,000)
- Only count when WEAKENED nodes become INFECTED
- Do NOT count nodes that were already infected at the start

## Example Validation
For the small example input from Part 1:
```
..#
#..
...
```

- After 100 bursts: **26 infections**
- After 10,000,000 bursts: **2,511,944 infections**

## Implementation Notes
- Use a data structure to track node states (e.g., dictionary mapping positions to states)
- States can be represented as integers: CLEAN=0, WEAKENED=1, INFECTED=2, FLAGGED=3
- Nodes not in the dictionary are implicitly CLEAN
- Directions: UP = (0, -1), RIGHT = (1, 0), DOWN = (0, 1), LEFT = (-1, 0)
- The simulation is significantly longer (10 million vs 10 thousand bursts), so efficiency matters
- Only increment the infection counter when a WEAKENED node becomes INFECTED

## Key Differences from Part 1
1. **4 states instead of 2**: CLEAN → WEAKENED → INFECTED → FLAGGED → CLEAN
2. **More complex turning**: 4 different turn actions based on state
3. **10 million bursts instead of 10 thousand**: 1000x longer simulation
4. **Only count WEAKENED→INFECTED transitions**: Not all state changes
