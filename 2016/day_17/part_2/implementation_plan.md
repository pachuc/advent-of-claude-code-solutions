# Implementation Plan: Finding the Longest Path to the Vault

## Problem Summary
Find the **length** of the longest possible path that reaches the vault at position (3,3) in a 4x4 grid where doors are dynamically locked/unlocked based on MD5 hashing of `passcode + path_history`.

## Key Differences from Part 1
- **Part 1**: Used BFS to find shortest path (10 steps: `RDDRULDDRR`)
- **Part 2**: Must explore ALL paths exhaustively to find the maximum length
- **Output Change**: Return integer length, not the path string itself

## Algorithm Analysis

### Why BFS Won't Work Directly
- BFS finds paths level-by-level (shortest first)
- We need to explore ALL paths to completion, not stop at first solution
- Cannot use early-exit optimization when reaching (3,3)

### Optimal Approach: Exhaustive DFS
**Time Complexity**: O(4^n) where n is the maximum path length
- Each position can have up to 4 possible moves
- Must explore all branches until they terminate at (3,3) or have no valid moves
- Given examples show paths up to ~830 steps, this is manageable

**Space Complexity**: O(n) for recursion stack depth
- DFS uses recursion stack proportional to maximum path length
- Much more memory-efficient than BFS which would store all active paths in queue

**Why DFS is Better Than BFS Here**:
1. **Memory efficiency**: DFS stack uses O(n), BFS queue could use O(4^n) in worst case
2. **Natural exhaustive search**: DFS explores each branch to completion
3. **No visited set needed**: Same position with different paths = different states
4. **Early termination per branch**: Each path terminates at (3,3)

### Critical Insight: No Cycle Detection Needed
- Paths terminate when reaching (3,3) - cannot pass through vault
- Door states change with each move (based on full path history)
- Same position visited via different paths has different door configurations
- Therefore, standard "visited set" would be incorrect here
- Natural termination prevents infinite loops

## Step-by-Step Implementation Plan

### Step 1: Reuse Core Functions from Part 1
**Rationale**: The door mechanism is identical
- Copy `get_open_doors(passcode, path)` - computes MD5 hash and returns door states
- Copy `get_valid_moves(x, y, passcode, path)` - returns valid moves considering doors and boundaries
- These are proven correct from Part 1 solution

### Step 2: Implement DFS Search Function
**Function Signature**: `find_longest_path(passcode) -> int`

**Algorithm**:
```
def dfs_explore(x, y, path, passcode):
    # Base case: reached the vault
    if (x, y) == (3, 3):
        return len(path)

    # Initialize max length for this branch
    max_length = 0

    # Explore all valid moves from current position
    for (new_x, new_y, direction) in get_valid_moves(x, y, passcode, path):
        new_path = path + direction
        # Recursively explore this branch
        branch_length = dfs_explore(new_x, new_y, new_path, passcode)
        # Track maximum length found
        max_length = max(max_length, branch_length)

    return max_length
```

**Key Points**:
- Recursive DFS that explores all branches
- Returns length when vault is reached
- Returns 0 if branch terminates without reaching vault (dead end)
- Tracks maximum across all child branches

### Step 3: Set Python Recursion Limit
**Rationale**: Prevent RecursionError during deep path exploration
- Examples show paths up to ~830 steps deep
- Python's default recursion limit (~1000) may be exceeded
- Must be done at module level before running DFS

**Implementation**:
```python
import sys
sys.setrecursionlimit(5000)
```

**Note**: This must be included in the main implementation file, not as an optional optimization.

### Step 4: Add Safety Limit to DFS
**Rationale**: Prevent potential infinite loops or excessive recursion
- Examples show max ~830 steps
- Set limit at 5000 steps as safety margin (allows for 6x the known maximum)
- If path exceeds limit, treat as dead end and return 0

**Implementation**:
```python
def dfs_explore(x, y, path, passcode, max_depth=5000):
    # Safety: prevent excessive recursion
    if len(path) > max_depth:
        return 0

    # Base case: reached vault
    if (x, y) == (3, 3):
        return len(path)

    # Explore all valid moves
    max_length = 0
    for new_x, new_y, direction in get_valid_moves(x, y, passcode, path):
        new_path = path + direction
        branch_length = dfs_explore(new_x, new_y, new_path, passcode, max_depth)
        max_length = max(max_length, branch_length)

    # If no valid moves existed, max_length remains 0 (dead end)
    return max_length
```

**Key Points**:
- Increased from 2000 to 5000 to ensure we don't artificially limit valid paths
- If no valid moves exist from current position, loop never executes and function returns 0 (dead end)
- Only paths that reach (3,3) contribute positive values to the maximum

### Step 5: Main Search Function
**Function**: `find_longest_path(passcode) -> int`

```python
def find_longest_path(passcode):
    """
    Find the length of the longest path to the vault.
    Uses DFS to exhaustively explore all possible paths.
    Returns 0 if no path exists to the vault.
    """
    return dfs_explore(0, 0, "", passcode)
```

**Starting Conditions**:
- Start at (0, 0)
- Empty path ""
- DFS will explore all reachable paths
- Returns 0 if no path reaches the vault (unlikely for valid inputs)

### Step 6: Update Main Function
**Changes from Part 1**:
- Call `find_longest_path()` instead of `find_shortest_path()`
- Print the integer length result
- Remove string path output logic

**Implementation**:
```python
def main():
    with open('input.md', 'r') as f:
        passcode = f.read().strip()

    result = find_longest_path(passcode)
    print(result)
```

## Complete Implementation Structure

```python
import hashlib
import sys

# Step 3: Set recursion limit before any DFS calls
sys.setrecursionlimit(5000)

# Step 1: Reuse from Part 1
def get_open_doors(passcode, path):
    """Same as Part 1"""
    hash_input = passcode + path
    hash_result = hashlib.md5(hash_input.encode()).hexdigest()[:4]
    return tuple(c in 'bcdef' for c in hash_result)

def get_valid_moves(x, y, passcode, path):
    """Same as Part 1"""
    # ... implementation from Part 1

# Step 2 & 4: New DFS implementation
def dfs_explore(x, y, path, passcode, max_depth=5000):
    """Recursively explore all paths, return max length found"""
    # Safety limit
    if len(path) > max_depth:
        return 0

    # Base case: reached vault
    if (x, y) == (3, 3):
        return len(path)

    # Explore all branches
    max_length = 0
    for new_x, new_y, direction in get_valid_moves(x, y, passcode, path):
        new_path = path + direction
        branch_length = dfs_explore(new_x, new_y, new_path, passcode, max_depth)
        max_length = max(max_length, branch_length)

    # If no valid moves existed, returns 0 (dead end)
    return max_length

# Step 5: Main search function
def find_longest_path(passcode):
    """Find longest path length using DFS"""
    return dfs_explore(0, 0, "", passcode)

# Step 6: Updated main
def main():
    with open('input.md', 'r') as f:
        passcode = f.read().strip()
    result = find_longest_path(passcode)
    print(result)

if __name__ == "__main__":
    main()
```

## Performance Expectations

### Expected Runtime
- Given examples: 370, 492, 830 steps
- DFS with early termination at vault
- Should complete in < 1 minute for typical inputs
- Worst case: few seconds to tens of seconds

### Memory Usage
- Recursion depth: up to ~5000 frames (with safety limit)
- Each frame: minimal state (x, y, path string)
- Path strings grow up to ~5000 characters in worst case
- Total memory: < 50 MB

### Optimization Notes
- **No further optimization needed** for this problem size
- Recursion limit increased to 5000 (handled in Step 3)
- Alternative iterative DFS using explicit stack possible if needed, but not expected to be necessary

## Edge Cases Handled

1. **Dead ends**: Paths with no valid moves return 0
2. **Multiple paths to vault**: DFS explores all, returns maximum
3. **Excessive depth**: Safety limit prevents stack overflow
4. **Empty path**: Valid starting condition
5. **Boundary checks**: Already in `get_valid_moves()` from Part 1

## Validation Against Examples

The implementation should be tested against known examples:
- `ihgpwlah` → 370
- `kglvqrro` → 492
- `ulqzkmiv` → 830

These provide sanity checks before running with actual input `ioramepc`.
