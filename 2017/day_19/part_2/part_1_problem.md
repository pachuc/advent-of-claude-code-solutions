# Problem Report: Network Packet Routing

## Overview
A network packet needs to follow a routing diagram to reach its destination. The packet will traverse a path marked by ASCII characters and collect letters along the way.

## Objective
Determine which letters the packet encounters (and in what order) as it follows the path from start to finish.

## Input Description
The input is an ASCII art routing diagram consisting of:
- **Path characters**:
  - `|` - vertical path segment
  - `-` - horizontal path segment
  - `+` - corner/junction point
- **Letter markers**: Capital letters (A-Z) placed along the path
- **Empty spaces**: Areas with no path

The input will be provided as a text file with multiple lines representing the 2D grid of the routing diagram.

## Path Following Rules

### Starting Position
- The packet starts just off the top of the diagram
- It begins by moving DOWN onto the only line (vertical `|`) that connects to the top row

### Movement Rules
1. **Continue in current direction** when possible
2. **Turn only when**:
   - Encountering a `+` character (corner marker)
   - Reaching the end of a line segment with only one perpendicular direction available
3. **When lines cross**: Continue straight in the current direction (don't turn)
4. **Letters (A-Z)**: Pass through them without changing direction, but record them
5. **End condition**: Stop when reaching the end of the path (no valid moves available)

### Direction Changes
- When moving vertically (`|`), can only turn at `+` or dead ends
- When moving horizontally (`-`), can only turn at `+` or dead ends
- At a `+`, turn to follow the only available continuing path (left, right, up, or down)

## Expected Output
A string containing all the letters encountered along the path, in the order they were visited.

**Format**: Plain text string of capital letters with no separators (e.g., "ABCDEF")

## Example
Given this diagram:
```
     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+
```

The packet's path:
1. Start at top, go DOWN through the `|`
2. Pass through letter `A`
3. Continue to first `+`, turn RIGHT
4. Go UP and RIGHT, passing through `B`
5. Continue DOWN (collecting `C`), RIGHT, and UP (collecting `D`)
6. Go LEFT through `E`, ending at `F`

**Output**: `ABCDEF`

## Implementation Notes
- The routing diagram may be very wide; handle accordingly without line wrapping issues
- Only one starting point exists (the only vertical line touching the top edge)
- The path is continuous with exactly one route to follow
- There are no ambiguous junctions (always exactly one valid direction to continue)
