# Problem Report: A Regular Map

## Objective
Find the largest number of doors you would need to pass through to reach the furthest room from your starting position. Specifically, find the room where the shortest path from your starting location requires passing through the most doors.

## Context
You are navigating a facility made up of rooms arranged in a grid. Rooms only connect to adjacent rooms when a door is present between them. You have been given a regular expression (regex) that describes routes through every door in the facility.

## Input Format
The input is a single-line regular expression string that:
- Starts with `^` (marks the beginning of routes)
- Ends with `$` (marks the end of routes)
- Contains the characters `N` (north), `S` (south), `E` (east), and `W` (west) representing directional movements
- Uses parentheses `()` to indicate branching paths
- Uses pipes `|` to separate branch options within parentheses
- May contain empty options in branches (e.g., `(NEWS|)` means the branch can be skipped)

### Regex Interpretation Rules
1. **Simple sequences**: `WNE` means move west, then north, then east
2. **Branches**: `N(E|W)N` means go north, then choose either east OR west, then go north again
3. **Nested branches**: Branches can contain other branches, e.g., `SSE(EE|N)`
4. **Empty options**: `(NEWS|)` means you can either follow the route NEWS or skip it entirely
5. **Branch behavior**: All options in a branch start from the same position (where the opening parenthesis begins)

## Map Building
The regex describes all possible routes that pass through every door in the facility at least once. By tracing all routes described by the regex, you can construct a complete map of the facility showing all rooms and doors.

Map representation:
- Rooms: `.`
- Walls: `#`
- Horizontal doors: `-`
- Vertical doors: `|`
- Starting position: `X`

## Output Requirements
Return a single integer: the maximum number of doors that must be passed through on the shortest path to any room from the starting position.

## Examples
1. `^WNE$` → Answer: 3 (reaches north-east corner)
2. `^ENWWW(NEEE|SSE(EE|N))$` → Answer: 10 (reaches south-east corner)
3. `^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$` → Answer: 18 (reaches north-east corner)
4. `^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$` → Answer: 23
5. `^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$` → Answer: 31

## Algorithm Requirements
1. Parse the regex to understand all possible routes
2. Build a map/graph of the facility by tracing all routes
3. Track all doors encountered during route tracing
4. Use shortest-path algorithm (e.g., BFS) from the starting position to find the minimum doors needed to reach each room
5. Return the maximum of all these minimum distances
