# Implementation Summary: Vault Pathfinding with Dynamic Doors

## Overview
Successfully implemented a BFS-based pathfinding solution to navigate through a 4x4 grid with dynamically locked/unlocked doors based on MD5 hashing.

## Solution Approach

### Algorithm: Breadth-First Search (BFS)
- **Why BFS?** Guarantees finding the shortest path in an unweighted graph where all moves have equal cost
- **State representation:** Each state is a tuple of (x, y, path_string)
- **No visited set needed:** Same position with different paths = different door states, so all must be explored
- **Early termination:** First path to reach (3,3) is guaranteed to be shortest due to BFS level-order exploration

### Core Components

#### 1. `get_open_doors(passcode, path)`
- Computes MD5 hash of concatenated passcode + current path
- Takes first 4 hexadecimal characters
- Maps each character to door state: 'bcdef' = open, '0-9a' = closed
- Returns tuple of 4 booleans for (Up, Down, Left, Right)

#### 2. `get_valid_moves(x, y, passcode, path)`
- Retrieves door states using `get_open_doors()`
- Checks each direction (U/D/L/R) for:
  - Door is open (from hash)
  - Position stays within grid bounds [0, 3]
- Returns list of valid (new_x, new_y, direction_char) tuples

#### 3. `find_shortest_path(passcode)`
- Initializes BFS queue with starting position (0, 0, "")
- Explores states level by level
- Returns path immediately when reaching goal (3, 3)
- Includes safety check to prevent infinite exploration (max 1000 moves)
- Returns None if no path exists

#### 4. `main()`
- Reads passcode from input.md
- Calls pathfinding algorithm
- Outputs result to stdout

## Files Created

1. **solution.py** - Main implementation file containing:
   - Hash computation function
   - Movement validation logic
   - BFS pathfinding algorithm
   - Input/output handling

## Testing Process

### Test Phase 1: Known Examples
Tested with all provided examples to verify correctness:

1. **Test Case 1: `ihgpwlah`**
   - Expected: `DDRRRD` (length 6)
   - Result: `DDRRRD` ✓
   - Status: PASS

2. **Test Case 2: `kglvqrro`**
   - Expected: `DDUDRLRRUDRD` (length 12)
   - Result: `DDUDRLRRUDRD` ✓
   - Status: PASS

3. **Test Case 3: `ulqzkmiv`**
   - Expected: `DRURDRUDDLLDLUURRDULRLDUUDDDRR` (length 30)
   - Result: `DRURDRUDDLLDLUURRDULRLDUUDDDRR` ✓
   - Status: PASS

4. **Test Case 4: `hijkl` (no solution)**
   - Expected: None/no path
   - Result: None ✓
   - Status: PASS

All known test cases passed successfully!

### Test Phase 2: Actual Input
**Input passcode:** `ioramepc`

**Result:** `RDDRULDDRR`
- Path length: 10 moves
- Final position: (3, 3) ✓
- All moves valid ✓

### Path Validation
Simulated the path step-by-step to verify:
- Each move follows an open door based on MD5 hash
- Each position stays within grid boundaries
- Path successfully reaches goal position (3, 3)
- No invalid moves attempted

**Validation trace:**
```
(0,0) --R--> (1,0) --D--> (1,1) --D--> (1,2) --R--> (2,2)
      --U--> (2,1) --L--> (1,1) --D--> (1,2) --D--> (1,3)
      --R--> (2,3) --R--> (3,3) [GOAL REACHED]
```

## Performance

- **Runtime:** < 0.1 seconds for all test cases
- **Path length:** 10 moves (efficient solution)
- **States explored:** Minimal due to BFS efficiency and door pruning
- **Memory usage:** Negligible for queue storage

## Key Implementation Details

1. **MD5 encoding:** Used `.encode()` to convert strings to bytes for MD5 hashing
2. **Coordinate system:** (0,0) = top-left, (3,3) = bottom-right, y increases downward
3. **Door ordering:** Hash characters map to [Up, Down, Left, Right] in that order
4. **Boundary checking:** Combined with door state checking to prevent invalid moves
5. **Early termination:** BFS returns immediately upon reaching goal, guaranteed to be shortest

## Conclusion

The implementation successfully solves the vault pathfinding problem using a clean BFS approach. All test cases pass, including the actual input, demonstrating correctness. The solution is efficient, readable, and handles edge cases appropriately.

**Final Answer:** `RDDRULDDRR`
