# Implementation Plan: Vault Pathfinding with Dynamic Doors

## Problem Analysis

This is a **dynamic graph pathfinding problem** where:
- State space: (position, path_history) tuples
- Graph edges (available moves) change based on path history through MD5 hashing
- Goal: Find shortest path from (0,0) to (3,3) in a 4x4 grid
- Optimal algorithm: **BFS (Breadth-First Search)** guarantees shortest path

## Algorithm Choice: BFS

**Why BFS?**
- All moves have equal cost (length 1)
- BFS guarantees finding the shortest path in unweighted graphs
- Will explore paths level-by-level (path length 1, then 2, then 3, etc.)
- Time complexity: O(V + E) where V = number of states, E = transitions
- Space complexity: O(V) for queue and visited states

**State Representation:**
- Each state = (x, y, path_string)
- Position (x, y) ranges from 0-3
- Path string grows with each move
- States are NOT reusable: same position with different paths = different states

**Expected Performance:**
- Grid size is only 4x4 (16 positions)
- Most states will be pruned by locked doors
- Expected solution length: 6-30 characters based on examples
- Should run in milliseconds even with thousands of state explorations

## Step-by-Step Implementation Plan

### Step 1: Setup and Input Handling
**File: solution.py**

1. Import required modules:
   - `hashlib` for MD5 hashing
   - `collections.deque` for BFS queue

2. Read input:
   - Read passcode from `input.md`
   - Strip whitespace

### Step 2: Implement MD5 Hash Function
**Function: `get_open_doors(passcode, path)`**

1. Concatenate passcode + path
2. **IMPORTANT**: MD5 requires bytes, not strings. Must call `.encode()` on the concatenated string
3. Compute MD5 hash using `hashlib.md5()`
4. Get hexdigest and take first 4 characters
5. For each character (U, D, L, R order):
   - Check if character is in 'bcdef' (open doors)
   - Return tuple/list of 4 booleans: (up_open, down_open, left_open, right_open)

**Example:**
```python
hash_str = hashlib.md5((passcode + path).encode()).hexdigest()[:4]
return tuple(c in 'bcdef' for c in hash_str)
```

### Step 3: Implement Movement Validation
**Function: `get_valid_moves(x, y, passcode, path)`**

1. Get door states using `get_open_doors(passcode, path)`
2. Define potential moves with their deltas:
   - Up: (x, y-1, 'U') - requires doors[0] and y > 0
   - Down: (x, y+1, 'D') - requires doors[1] and y < 3
   - Left: (x-1, y, 'L') - requires doors[2] and x > 0
   - Right: (x+1, y, 'R') - requires doors[3] and x < 3
3. Filter moves based on:
   - Door is open (from hash)
   - Position stays within grid bounds [0, 3]
4. Return list of valid (new_x, new_y, direction_char) tuples

**Coordinate System:**
- (0, 0) = top-left
- (3, 3) = bottom-right
- x increases rightward, y increases downward

### Step 4: Implement BFS Algorithm
**Function: `find_shortest_path(passcode)`**

1. **Initialize:**
   - Queue: `deque([(0, 0, "")])` - start at (0,0) with empty path
   - No visited set needed (each state with different path is unique)

2. **BFS Loop:**
   ```
   while queue is not empty:
       dequeue (x, y, path)

       if (x, y) == (3, 3):
           return path  # Found shortest path!

       # Safety check: limit maximum path length
       if len(path) >= 1000:
           continue  # Skip exploring beyond reasonable depth

       for each valid move from (x, y):
           new_x, new_y, direction = move
           new_path = path + direction
           enqueue (new_x, new_y, new_path)
   ```

3. **Return:**
   - Return path string when goal is reached
   - Return None or empty string if no path exists

**Why no visited set?**
- No visited set keyed by position alone is needed
- Same position with different paths = different door states
- Must explore all unique (position, path) combinations
- BFS ordering ensures first path to (3,3) is shortest, so we return immediately
- State space is naturally pruned by locked doors and grid boundaries

### Step 5: Main Execution
**Function: `main()`**

1. Read passcode from input file with basic error handling:
   - Use try/except for file operations
   - Strip whitespace from passcode
   - Validate that passcode is non-empty
2. Call `find_shortest_path(passcode)`
3. Print result to stdout (plain string, no extra whitespace)
4. Optionally write to output file

### Step 6: Code Structure
```python
import hashlib
from collections import deque

def get_open_doors(passcode, path):
    """Return tuple of 4 booleans for U,D,L,R door states"""
    # Implementation here
    pass

def get_valid_moves(x, y, passcode, path):
    """Return list of valid (new_x, new_y, direction) tuples"""
    # Implementation here
    pass

def find_shortest_path(passcode):
    """BFS to find shortest path from (0,0) to (3,3)"""
    # Implementation here
    pass

def main():
    """Main entry point"""
    # Read input
    # Run algorithm
    # Print result
    pass

if __name__ == "__main__":
    main()
```

## Potential Optimizations (if needed)

### Early Termination
- Since BFS explores by path length, first solution found is optimal
- Can immediately return when reaching (3,3)

### Memory Optimization (unlikely to be needed)
- Current approach: queue stores full path strings
- Alternative: store parent pointers and reconstruct path
- Given expected path length < 30, full strings are fine

### Pruning (not applicable)
- Cannot prune based on position alone (different paths = different states)
- Cannot use A* effectively (heuristic doesn't help with dynamic doors)
- BFS is already optimal for this problem

## Expected Runtime Analysis

**Worst Case Bounds:**
- Grid positions: 16
- Maximum reasonable path length: ~50 moves before cycles
- State space: potentially 16 * 4^50, but heavily pruned by:
  - Locked doors (on average 50% of doors locked)
  - Physical boundaries
  - BFS early termination

**Practical Expectation:**
- Based on examples, solutions are 6-30 moves
- BFS will explore a few thousand states at most
- Runtime: < 100ms for typical inputs
- Memory: < 10MB for queue storage

**Input Size Consideration:**
- Input is a single passcode string (constant size)
- Grid size is fixed at 4x4
- Algorithm complexity doesn't scale with input size
- No risk of timeout or memory issues

## Error Handling

**Basic error handling needed:**
- Handle missing or empty input file with try/except
- Validate passcode is non-empty after stripping whitespace
- Handle case where no path exists (return empty string or message)
- Maximum path length check (1000 moves) prevents infinite exploration

## Implementation Order

1. ✅ Implement `get_open_doors()` - testable in isolation
2. ✅ Implement `get_valid_moves()` - testable with sample cases
3. ✅ Implement `find_shortest_path()` - core BFS logic
4. ✅ Implement `main()` - I/O and execution
5. ✅ Test with provided examples
6. ✅ Run with actual input

## Validation Strategy

- Test hash function with known examples from problem
- Verify movement logic with boundary cases
- Test BFS with sample passcodes that have known solutions
- Validate returned paths by simulating each move and checking door states
- Verify final answer matches expected format (only U/D/L/R characters, no whitespace)
