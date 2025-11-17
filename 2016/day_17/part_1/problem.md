# Problem Report: Vault Pathfinding with Dynamic Doors

## Objective
Find the shortest path to navigate from the top-left room (start) to the bottom-right room (vault) in a 4x4 grid of rooms where door accessibility is dynamically determined by MD5 hashing.

## Context
You are navigating through a secure vault with a 4x4 grid layout. The grid has:
- Starting position: top-left corner (0,0)
- Goal position: bottom-right corner (3,3)
- Doors between rooms that are dynamically locked/unlocked based on cryptographic hashing

## Input
A passcode string that serves as the base for MD5 hashing.

**Given input:** `ioramepc`

## Door Mechanism
Doors in your current room are open or locked based on:
1. Compute MD5 hash of: `passcode + path_taken_so_far`
2. Use only the first 4 hexadecimal characters of the hash
3. These 4 characters correspond to doors: Up, Down, Left, Right (in that order)
4. Door is **open** if character is `b`, `c`, `d`, `e`, or `f`
5. Door is **closed/locked** if character is `0-9` or `a`

## Path Representation
- `U` = move up
- `D` = move down
- `L` = move left
- `R` = move right

The path is a sequence of these characters representing moves taken from the start.

## Rules and Constraints
1. You start at position (0,0) with an empty path
2. At each position, hash `passcode + current_path` to determine which doors are open
3. You cannot move through walls (grid boundaries)
4. You cannot move through locked doors
5. The goal is to reach position (3,3)
6. Doors change state based on your path history, so returning to a previously visited room may have different open doors

## Examples
For passcode `hijkl`:
- Initial hash of `hijkl` = `ced9` → up(c)=open, down(e)=open, left(d)=open, right(9)=locked
- After moving down, hash `hijklD` = `f2bc` → different door states

Known solutions for other passcodes:
- Passcode `ihgpwlah` → shortest path: `DDRRRD`
- Passcode `kglvqrro` → shortest path: `DDUDRLRRUDRD`
- Passcode `ulqzkmiv` → shortest path: `DRURDRUDDLLDLUURRDULRLDUUDDDRR`

## Expected Output
A string representing the shortest path from start to vault using the characters U, D, L, R.

**Format:** Plain string of directional characters (e.g., `DDRRRD`)

## Algorithm Considerations
This is a pathfinding problem where:
- The state space includes both position AND path history
- Standard shortest-path algorithms like BFS can be used
- Each state is unique based on (current_position, path_taken)
- The "cost" is path length, and we want the minimum
