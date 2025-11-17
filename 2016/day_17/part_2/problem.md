# Problem Report: Finding the Longest Path to the Vault

## Background from Part 1

You are navigating through a secure vault with a 4x4 grid layout where doors are dynamically locked/unlocked based on MD5 hashing:
- Starting position: top-left corner (0,0)
- Goal position: bottom-right corner (3,3) - the vault
- The grid is 4x4 rooms connected by doors

### Door Mechanism (from Part 1)
1. Compute MD5 hash of: `passcode + path_taken_so_far`
2. Use only the first 4 hexadecimal characters of the hash
3. These 4 characters correspond to doors: Up, Down, Left, Right (in that order)
4. Door is **open** if character is `b`, `c`, `d`, `e`, or `f`
5. Door is **closed/locked** if character is `0-9` or `a`

### Path Representation
- `U` = move up (decrease y)
- `D` = move down (increase y)
- `L` = move left (decrease x)
- `R` = move right (increase x)

### Key Constraint
**Paths end the first time they reach the vault (3,3).** Once you reach the bottom-right room, the path terminates - you cannot pass through it to explore further.

## Part 1 Recap
In Part 1, we found the **shortest path** to reach the vault with passcode `ioramepc`.
- **Part 1 Answer:** `RDDRULDDRR` (10 steps)

## Part 2 Objective
Now we want to test the robustness of the security system by finding the **longest possible path** that still reaches the vault. This explores how many different routes exist through the dynamic door system.

## Input
The same passcode string from Part 1: `ioramepc`

## Expected Output
An integer representing the **length** (number of steps) of the longest path that reaches the vault.

**Format:** A single integer (e.g., `370`, `492`, `830`)

**Note:** Output is the LENGTH of the path, not the path string itself.

## Examples
For reference, known longest paths for other passcodes:
- Passcode `ihgpwlah` → longest path takes **370** steps
- Passcode `kglvqrro` → longest path takes **492** steps
- Passcode `ulqzkmiv` → longest path takes **830** steps

## Algorithm Considerations

### Key Differences from Part 1
1. **Part 1 used BFS** to find the shortest path (stops at first solution)
2. **Part 2 requires exhaustive search** to find the longest path (must explore all possible paths)
3. Need to explore ALL paths that reach the vault, not just the first one found

### Approach
- Use DFS (Depth-First Search) or exhaustive BFS to explore all possible paths
- Track the maximum length found among all paths that reach (3,3)
- Important: Paths are distinguished by their history, not just position
  - Same position can be visited multiple times via different paths
  - Each path creates different door states due to MD5 hashing
- No need to track visited states (unlike typical pathfinding) because:
  - The same position with different path histories represents different states
  - Door configurations change based on full path history
- Since paths terminate at (3,3), there's natural termination

### Implementation Notes
- Remove the early-exit when finding the vault (as in Part 1's BFS)
- Continue exploring until all possible paths are exhausted
- Return the maximum path length found
- The path length limit of 1000 in Part 1 code may need adjustment or removal
