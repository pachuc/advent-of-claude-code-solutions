# Problem Report: Sporifica Virus Simulation

## Objective
Simulate a virus carrier moving through a 2D grid, infecting and cleaning nodes according to specific rules. Count how many bursts of activity result in a node becoming infected after 10,000 bursts.

## Context
A grid computing cluster has been infected with a virus. A virus carrier moves through an infinite 2D grid, alternating between infecting clean nodes and cleaning infected nodes. We need to track how many times the carrier infects a node (not counting nodes that start infected).

## Input Format
- A 2D grid map showing the initial state of the center portion of an infinite grid
- `.` represents a clean node
- `#` represents an infected node
- The grid dimensions are odd (e.g., 25x25), allowing for a center node
- The input is provided as lines of text where each character is a node

## Initial Conditions
- The virus carrier starts at the center node of the input grid
- The carrier initially faces UP (north)
- The grid extends infinitely in all directions beyond the input map
- All nodes outside the input map start as clean

## Virus Carrier Behavior (Per Burst)
Each burst consists of the following steps executed in order:

1. **Turn**:
   - If the current node is INFECTED: turn RIGHT (90 degrees clockwise)
   - If the current node is CLEAN: turn LEFT (90 degrees counter-clockwise)

2. **Toggle infection state**:
   - If the current node is CLEAN: mark it as INFECTED (count this)
   - If the current node is INFECTED: mark it as CLEAN

3. **Move forward**:
   - Move one node in the direction the carrier is currently facing

## Output Requirements
- A single integer: the count of how many bursts caused a node to become infected
- Run the simulation for exactly **10,000 bursts**
- Do NOT count nodes that were already infected at the start

## Example
For the input:
```
..#
#..
...
```

After 10,000 bursts, the answer should be **5587** infections.

After 7 bursts, 5 infections should have occurred.
After 70 bursts, 41 infections should have occurred.

## Implementation Notes
- The grid is infinite, so a dynamic data structure (like a dictionary/hash map) is recommended to track only infected nodes
- Track the carrier's position (x, y coordinates) and direction (up, down, left, right)
- Directions: UP = (0, -1), RIGHT = (1, 0), DOWN = (0, 1), LEFT = (-1, 0) in terms of (dx, dy)
- Only count infections that occur during the simulation, not the initial infected nodes
