# Test Plan: Longest Path to Vault

## Testing Strategy Overview

The testing approach focuses on:
1. **Correctness verification** using known examples
2. **Edge case validation** for boundary and special conditions
3. **Component testing** of reused and new functions
4. **Integration testing** of complete solution

Since this is a script to solve a specific problem (not production code), we focus on functional correctness and handling the given input properly.

## Test Categories

### 1. Unit Tests - Core Functions

#### Test 1.1: `get_open_doors()` Function
**Purpose**: Verify MD5 hashing and door state logic (reused from Part 1)

**Test Cases**:
```python
# Test case from problem examples
passcode = "hijkl"
path = ""
expected = (True, True, True, False)  # c, e, d, 9
actual = get_open_doors(passcode, path)
assert actual == expected

# Test after one move
path = "D"
# hijklD -> f2bc
expected = (True, False, True, True)  # f, 2, b, c
actual = get_open_doors(passcode, path)
assert actual == expected

# Test with actual input passcode
passcode = "ioramepc"
path = ""
actual = get_open_doors(passcode, path)
# Verify it returns 4 booleans
assert len(actual) == 4
assert all(isinstance(x, bool) for x in actual)
```

**Validation**: These tests ensure the door mechanism works correctly.

#### Test 1.2: `get_valid_moves()` Function
**Purpose**: Verify boundary checking and door state integration

**Test Cases**:
```python
# Test at starting position (0,0)
passcode = "ioramepc"
path = ""
moves = get_valid_moves(0, 0, passcode, path)
# Should not include U or L (out of bounds)
for move in moves:
    assert move[2] not in ['U', 'L']

# Test at bottom-right corner (3,3) - vault position
# This shouldn't normally be called, but verify it works
moves = get_valid_moves(3, 3, passcode, "RDDRULDDRR")
# Should not include D or R (out of bounds)
for move in moves:
    assert move[2] not in ['D', 'R']

# Test at middle position (2,2)
moves = get_valid_moves(2, 2, passcode, "RDD")
# All 4 directions are within bounds, but door states vary
# Just verify function executes without error
assert isinstance(moves, list)
```

**Validation**: Ensures boundary logic and door checking work together.

### 2. Algorithm Tests - DFS Exploration

#### Test 2.1: DFS Termination at Vault
**Purpose**: Verify DFS correctly identifies when vault is reached

**Test Case**:
```python
# Test base case: if we're at vault, return path length immediately
# We can test this by manually creating a scenario where we reach (3,3)
# For example, trace Part 1's shortest path and verify each step
passcode = "ioramepc"
shortest = "RDDRULDDRR"

# Manually walk the path to verify it reaches (3,3)
x, y, path = 0, 0, ""
for i, move in enumerate(shortest):
    # Get valid moves at current position
    valid_moves = get_valid_moves(x, y, passcode, path)
    # Verify this move is valid
    move_found = any(m[2] == move for m in valid_moves)
    assert move_found, f"Move {move} not valid at step {i}"

    # Execute the move
    path += move
    if move == 'U': y -= 1
    elif move == 'D': y += 1
    elif move == 'L': x -= 1
    elif move == 'R': x += 1

# Should end at vault
assert (x, y) == (3, 3), f"Path didn't reach vault, ended at ({x}, {y})"
assert len(path) == 10, f"Path length should be 10, got {len(path)}"
```

**Validation**: Ensures paths correctly reach the vault and validates Part 1's answer.

#### Test 2.2: DFS Dead End Handling
**Purpose**: Verify DFS returns 0 for paths that don't reach vault

**Test Case**:
```python
# Create a scenario where no moves are available
# This is hard to construct manually, but DFS should handle it
# by returning 0 from branches with no valid moves
```

**Validation**: Ensures dead ends don't contribute to maximum.

#### Test 2.3: Safety Limit
**Purpose**: Verify safety limit prevents excessive depth

**Test Case**:
```python
# Call DFS with very low max_depth
result_limited = dfs_explore(0, 0, "", "ioramepc", max_depth=5)
# Should terminate quickly and not exceed depth
# Result should be 0 (can't reach vault in ≤5 steps from Part 1 we know shortest is 10)
assert result_limited == 0, f"Expected 0 with depth limit 5, got {result_limited}"

# Verify that with a higher limit we get a real result
result_normal = dfs_explore(0, 0, "", "ioramepc", max_depth=5000)
assert result_normal > 0, "Should find paths with normal depth limit"
assert result_normal > result_limited, "Normal limit should find longer paths than restricted limit"
```

**Validation**: Ensures safety mechanism works correctly.

### 3. Integration Tests - Complete Solution

#### Test 3.1: Known Example Validation
**Purpose**: Verify solution against provided examples

**Critical Test Cases**:
```python
# Example 1
passcode = "ihgpwlah"
result = find_longest_path(passcode)
assert result == 370, f"Expected 370, got {result}"

# Example 2
passcode = "kglvqrro"
result = find_longest_path(passcode)
assert result == 492, f"Expected 492, got {result}"

# Example 3
passcode = "ulqzkmiv"
result = find_longest_path(passcode)
assert result == 830, f"Expected 830, got {result}"
```

**Validation**: These are the gold standard - if these pass, algorithm is highly likely correct.

**Priority**: **HIGHEST** - Must pass these before trusting the actual input result.

#### Test 3.2: Consistency with Part 1
**Purpose**: Verify Part 1 shortest path is found among all paths

**Test Case**:
```python
# The shortest path from Part 1 should definitely reach the vault
passcode = "ioramepc"
shortest_path = "RDDRULDDRR"  # Part 1 answer
assert len(shortest_path) == 10

# Verify this path is actually valid by walking through it with door checks
x, y, path = 0, 0, ""
for move in shortest_path:
    # Get valid moves at this position
    valid_moves = get_valid_moves(x, y, passcode, path)
    # Verify this move is in the valid moves list
    assert any(m[2] == move for m in valid_moves), \
        f"Move {move} not valid at ({x},{y}) with path '{path}'"

    # Execute the move
    path += move
    if move == 'U': y -= 1
    elif move == 'D': y += 1
    elif move == 'L': x -= 1
    elif move == 'R': x += 1

# Should reach vault
assert (x, y) == (3, 3), f"Path ended at ({x},{y}), not vault"

# The longest path must be >= 10 (at minimum, the shortest path exists)
longest = find_longest_path(passcode)
assert longest >= 10, f"Longest path {longest} shorter than known shortest {10}"
```

**Validation**: Validates Part 1's answer through the door mechanism and ensures longest >= shortest.

### 4. Edge Cases and Special Scenarios

#### Test 4.1: Empty Path Handling
**Purpose**: Verify starting condition is handled correctly

**Test Case**:
```python
# Starting with empty path at (0,0)
result = dfs_explore(0, 0, "", "ioramepc")
# Should return some positive integer > 0
assert result > 0
assert isinstance(result, int)
```

#### Test 4.2: Passcode Input Validation
**Purpose**: Ensure input is read correctly

**Test Case**:
```python
# Read actual input file
with open('input.md', 'r') as f:
    passcode = f.read().strip()

# Verify it's not empty
assert len(passcode) > 0
# Verify it matches expected
assert passcode == "ioramepc"
```

#### Test 4.3: Path Length Comparison
**Purpose**: Verify longest is significantly longer than shortest

**Test Case**:
```python
# Based on examples, longest is typically 30-80x the shortest
# ihgpwlah: shortest ~6, longest 370 (61x)
# kglvqrro: shortest ~12, longest 492 (41x)
# ulqzkmiv: shortest ~30, longest 830 (27x)

# For ioramepc, shortest is 10
# Expected: longest should be in range [200, 1000] based on pattern above
result = find_longest_path("ioramepc")
assert 200 <= result <= 1000, f"Unexpected longest path length: {result}"
print(f"Longest path length: {result}")
print(f"Ratio to shortest (10): {result/10:.1f}x")
```

**Validation**: Reasonableness check on final answer with tighter bounds.

### 5. Performance Tests

#### Test 5.1: Runtime Verification
**Purpose**: Ensure solution completes in reasonable time

**Test Case**:
```python
import time

passcode = "ioramepc"
start_time = time.time()
result = find_longest_path(passcode)
end_time = time.time()

elapsed = end_time - start_time
print(f"Execution time: {elapsed:.2f} seconds")

# Should complete in under 60 seconds
assert elapsed < 60, f"Took too long: {elapsed} seconds"
```

**Expected**: < 10 seconds for most inputs

#### Test 5.2: Memory Safety
**Purpose**: Verify recursion limit is properly set

**Test Case**:
```python
import sys

# Verify recursion limit has been set (should be done in implementation)
current_limit = sys.getrecursionlimit()
print(f"Current recursion limit: {current_limit}")

# Should be at least 5000 as per implementation plan
assert current_limit >= 5000, \
    f"Recursion limit {current_limit} too low, should be >= 5000"

# This ensures the implementation includes the sys.setrecursionlimit(5000) call
```

## Testing Execution Order

### Phase 1: Component Validation
1. Run Test 1.1 - `get_open_doors()`
2. Run Test 1.2 - `get_valid_moves()`
3. **Gate**: Only proceed if these pass (they're from Part 1, should work)

### Phase 2: Algorithm Validation
4. Run Test 2.1 - DFS termination
5. Run Test 2.3 - Safety limit
6. **Gate**: Basic DFS logic must work before full testing

### Phase 3: Known Examples (CRITICAL)
7. Run Test 3.1 - All three known examples
   - `ihgpwlah` → 370
   - `kglvqrro` → 492
   - `ulqzkmiv` → 830
8. **Gate**: **MUST PASS ALL THREE** before trusting actual input result

### Phase 4: Final Solution
9. Run Test 4.2 - Input validation
10. Run Test 5.2 - Verify recursion limit is set
11. Run Test 3.2 - Verify Part 1 path is valid and longest >= shortest (10)
12. Run Test 5.1 - Performance check with actual solution
13. Run Test 4.3 - Reasonableness check on result

## Success Criteria

### Minimum Requirements
- ✅ All three known examples produce correct results (370, 492, 830)
- ✅ Solution completes in < 60 seconds
- ✅ Longest path >= 10 (shortest path length from Part 1)
- ✅ Result is positive integer in reasonable range [200, 1000]
- ✅ Recursion limit is set to at least 5000

### Output Validation
- Single integer printed to stdout
- No errors or exceptions
- Format matches expected output (just the number)

## Debugging Strategy

If tests fail:

1. **Known examples fail**: Algorithm is wrong
   - Check DFS logic for max tracking
   - Verify base cases
   - Check that all branches are explored

2. **Performance issues**: Optimization needed
   - Add memoization if same states revisited (unlikely here)
   - Reduce safety limit if excessive
   - Consider iterative DFS instead of recursive

3. **Recursion errors**: Stack overflow
   - Increase `sys.setrecursionlimit()`
   - Or switch to iterative DFS with explicit stack

4. **Result seems wrong**: Validation issues
   - Re-check against Part 1 consistency
   - Manually trace small example
   - Add debug logging to track max length updates

## Manual Verification Approach

For additional confidence during debugging, add temporary debug output:
1. Add print statements to track maximum length updates in DFS
2. Verify that maximum increases over time as longer paths are found
3. Confirm that the search completes (all branches explored)

Example debug code:
```python
def dfs_explore(x, y, path, passcode, max_depth=5000):
    if len(path) > max_depth:
        return 0
    if (x, y) == (3, 3):
        print(f"Found path of length {len(path)}")  # Debug output
        return len(path)

    max_length = 0
    for new_x, new_y, direction in get_valid_moves(x, y, passcode, path):
        new_path = path + direction
        branch_length = dfs_explore(new_x, new_y, new_path, passcode, max_depth)
        if branch_length > max_length:
            max_length = branch_length
            if branch_length > 100 and branch_length % 50 == 0:  # Debug milestones
                print(f"New max found: {max_length}")
    return max_length
```

Remove debug statements once tests pass.
