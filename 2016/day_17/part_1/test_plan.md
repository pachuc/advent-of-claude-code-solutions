# Test Plan: Vault Pathfinding with Dynamic Doors

## Testing Strategy Overview

Our testing approach will be **bottom-up**:
1. Unit tests for individual functions
2. Integration tests with known examples
3. Validation with actual input
4. Edge case verification

## Test 1: MD5 Hashing Function

**Function:** `get_open_doors(passcode, path)`

### Test Cases

#### Test 1.1: Initial State (Empty Path)
- **Input:** passcode = `"hijkl"`, path = `""`
- **Expected Hash:** First 4 chars of MD5(`"hijkl"`) = `"ced9"`
  - Verify: `hashlib.md5('hijkl'.encode()).hexdigest()[:4]`
- **Expected Output:** `(True, True, True, False)`
  - c = open (U)
  - e = open (D)
  - d = open (L)
  - 9 = closed (R)

#### Test 1.2: After One Move
- **Input:** passcode = `"hijkl"`, path = `"D"`
- **Expected Hash:** First 4 chars of MD5(`"hijklD"`) = `"f2bc"`
- **Expected Output:** `(True, False, True, True)`
  - f = open (U)
  - 2 = closed (D)
  - b = open (L)
  - c = open (R)

#### Test 1.3: Verify All Door States
- **Input:** Various hash results
- **Test:** Each character 0-9, a-f maps correctly:
  - `'bcdef'` → open (True)
  - `'0123456789a'` → closed (False)

### Verification Method
```python
# Manual hash verification
import hashlib
test_str = "hijkl"
hash_result = hashlib.md5(test_str.encode()).hexdigest()
print(hash_result[:4])  # Should be "ced9"
```

## Test 2: Movement Validation Function

**Function:** `get_valid_moves(x, y, passcode, path)`

### Test Cases

#### Test 2.1: Starting Position
- **Input:** x=0, y=0, passcode=`"hijkl"`, path=`""`
- **Doors:** (True, True, True, False) from Test 1.1
- **Expected Valid Moves:**
  - Up: INVALID (y=0, at top boundary)
  - Down: VALID → (0, 1, 'D')
  - Left: INVALID (x=0, at left boundary)
  - Right: INVALID (door closed)
- **Expected Output:** `[(0, 1, 'D')]`

#### Test 2.2: Interior Position with All Doors Open
- **Setup:** Create scenario where all 4 doors are open
- **Input:** x=1, y=1 (interior position)
- **Expected:** Should return 4 valid moves if all doors open
- **Verify:** Boundary checking doesn't interfere when not at edges

#### Test 2.3: Corner Positions
- **Top-left (0,0):** Max 2 possible directions (D, R)
- **Top-right (3,0):** Max 2 possible directions (D, L)
- **Bottom-left (0,3):** Max 2 possible directions (U, R)
- **Bottom-right (3,3):** Max 2 possible directions (U, L), but this is goal

#### Test 2.4: Edge Positions
- **Top edge (x, 0):** Cannot go up
- **Bottom edge (x, 3):** Cannot go down
- **Left edge (0, y):** Cannot go left
- **Right edge (3, y):** Cannot go right

#### Test 2.5: All Doors Locked
- **Setup:** Create passcode+path that generates hash like "0123"
- **Expected Output:** `[]` (empty list, no valid moves)

### Verification Method
- Print or assert move lists for each test case
- Verify move count matches expected
- Verify coordinates stay in [0, 3] range

## Test 3: BFS Algorithm with Known Examples

**Function:** `find_shortest_path(passcode)`

### Test Cases from Problem Statement

#### Test 3.1: Example 1
- **Input:** passcode = `"ihgpwlah"`
- **Expected Output:** `"DDRRRD"` (length 6)
- **Verify:**
  - Path leads from (0,0) to (3,3)
  - Path is exactly 6 moves
  - Each move follows open doors

#### Test 3.2: Example 2
- **Input:** passcode = `"kglvqrro"`
- **Expected Output:** `"DDUDRLRRUDRD"` (length 12)
- **Verify:** Path reaches goal in 12 moves

#### Test 3.3: Example 3
- **Input:** passcode = `"ulqzkmiv"`
- **Expected Output:** `"DRURDRUDDLLDLUURRDULRLDUUDDDRR"` (length 30)
- **Verify:**
  - Longer path still found correctly
  - BFS explores many states before finding solution

#### Test 3.4: No Path Case
- **Input:** passcode = `"hijkl"`
- **Expected Output:** None or empty string
- **Reason:** Problem states this passcode has no solution
- **Verify:** Algorithm terminates without finding path

#### Test 3.5: Shortest Path Guarantee
- **Objective:** Verify BFS returns the *shortest* path, not just any valid path
- **Method:** For known examples, verify that:
  1. The returned path matches the expected shortest path
  2. The path length matches expected length
  3. No shorter valid path exists (guaranteed by BFS)
- **Note:** This confirms BFS explores in breadth-first order and returns immediately upon reaching goal

### Verification Method
```python
# For each test case
result = find_shortest_path(test_passcode)
assert result == expected_path, f"Expected {expected_path}, got {result}"
assert len(result) == len(expected_path), f"Expected length {len(expected_path)}, got {len(result)}"
print(f"✓ Test passed: {test_passcode} → {result}")
```

## Test 4: Path Validation

**Objective:** Verify that returned paths actually work

### Test Method: Path Simulator

For each test case, simulate walking the path:

```python
def validate_path(passcode, path):
    x, y = 0, 0
    current_path = ""
    step_details = []

    for i, move in enumerate(path):
        # Check if move is valid from current position
        valid_moves = get_valid_moves(x, y, passcode, current_path)
        doors = get_open_doors(passcode, current_path)

        step_details.append({
            'step': i,
            'position': (x, y),
            'path_so_far': current_path,
            'doors': doors,
            'valid_moves': valid_moves,
            'attempting': move
        })

        # Find matching move
        move_found = False
        for nx, ny, direction in valid_moves:
            if direction == move:
                x, y = nx, ny
                current_path += move
                move_found = True
                break

        if not move_found:
            return False, f"Invalid move '{move}' at position ({x},{y}) after {current_path}", step_details

    if (x, y) != (3, 3):
        return False, f"Path ends at ({x},{y}), not goal (3,3)", step_details

    return True, "Path valid", step_details
```

Apply to all test cases to ensure returned paths are actually walkable.

## Test 5: Actual Input

**Input:** passcode = `"ioramepc"`

### Verification Steps

1. **Run Algorithm:**
   ```bash
   python solution.py
   ```

2. **Check Output Format:**
   - Should be string of characters from {U, D, L, R}
   - Should not be empty
   - Should not contain invalid characters
   - Should contain no whitespace, newlines, or other characters
   - Verify: `all(c in 'UDLR' for c in result)` and `result.strip() == result`

3. **Validate Path:**
   - Use path simulator from Test 4
   - Verify path reaches (3,3)
   - Verify each move follows open doors

4. **Check Optimality (Manual):**
   - Can run modified BFS to find multiple paths
   - Verify no shorter path exists
   - BFS guarantee ensures first found is shortest

### Expected Results
- Solution exists (passcode likely valid)
- Path length: probably 6-20 moves (typical range)
- Runtime: < 1 second
- No errors or crashes

## Test 6: Edge Cases and Special Scenarios

### Test 6.1: First Move Constrained
- **Scenario:** From (0,0), test when most doors are locked
- **Expected:** Algorithm still finds path even with limited initial options
- **Method:** Observe initial door states for actual passcode and verify correct first move is taken

### Test 6.2: Single Move Solution
- **Scenario:** Create passcode where direct path of 1-6 moves works
- **Expected:** Return shortest possible path
- **Verification:** BFS should find this quickly

### Test 6.3: Long Path Required
- **Scenario:** Some passcodes require 20+ moves
- **Expected:** Algorithm still finds solution
- **Verification:** Example 3 tests this (30 moves)
- **Safety Check:** If runtime exceeds 5 seconds, investigate whether algorithm is exploring unnecessarily deep paths. Maximum path length safety check (1000 moves) should prevent infinite exploration

### Test 6.4: Many States Explored
- **Monitor:** Number of states dequeued from BFS
- **Expected:** Thousands of states possible
- **Verification:** Algorithm completes in reasonable time

### Test 6.5: Coordinate System Verification
- **Test:** Ensure (0,0) = top-left, (3,3) = bottom-right
- **Method:**
  - D increases y (move down)
  - R increases x (move right)
  - U decreases y (move up)
  - L decreases x (move left)

## Test 7: Performance Testing

### Test 7.1: Runtime Measurement
```python
import time

start = time.time()
result = find_shortest_path("ioramepc")
end = time.time()

print(f"Solution: {result}")
print(f"Length: {len(result)}")
print(f"Time: {end - start:.4f} seconds")
```

**Expected:**
- Time < 1 second
- Memory usage reasonable

### Test 7.2: State Space Analysis
- Add counter for states explored
- Print total states processed
- **Expected Range:** For actual input, expect 1,000-10,000 states explored
- **Red Flag:** If significantly higher (>100,000), investigate potential inefficiencies
- Verify algorithm efficiency

## Test 8: Error Handling

### Test 8.1: Empty Passcode
- **Input:** `""`
- **Expected:** Should still run (hash of empty string is valid)
- **Likely:** No solution found

### Test 8.2: Special Characters in Passcode
- **Input:** Passcode with spaces, symbols
- **Expected:** MD5 handles any string, should work
- **Note:** Problem doesn't specify restrictions

### Test 8.3: Missing or Empty Input File
- **Input:** Delete or empty input.md
- **Expected:** Program should fail gracefully with clear error message
- **Verify:** Try/except catches file I/O errors and reports them clearly

## Testing Execution Order

1. ✅ **Test 1:** Hash function (quick validation)
2. ✅ **Test 2:** Movement validation (unit test)
3. ✅ **Test 3:** Known examples (critical validation)
4. ✅ **Test 4:** Path validation (correctness check)
5. ✅ **Test 5:** Actual input (main objective)
6. ✅ **Test 6:** Edge cases (thoroughness)
7. ✅ **Test 7:** Performance (efficiency check)

## Success Criteria

**Implementation is correct if:**
1. All known examples produce expected outputs
2. All returned paths are valid (simulator confirms)
3. Actual input produces a valid shortest path
4. Algorithm completes in < 1 second
5. No crashes or errors

**Red flags:**
- Known examples fail
- Path simulator rejects returned path
- Infinite loop or timeout
- Path reaches wrong destination

## Debugging Strategy

If tests fail:

1. **Hash function wrong:** Print hash values, compare with manual MD5
2. **Movement wrong:** Print valid moves at each step, verify doors
3. **BFS wrong:** Print queue contents, verify states explored
4. **Path wrong:** Use simulator to find where path breaks

## Manual Verification Tools

### Quick Hash Checker
```python
import hashlib
def check_hash(s):
    h = hashlib.md5(s.encode()).hexdigest()[:4]
    doors = [c in 'bcdef' for c in h]
    print(f"{s} → {h} → U:{doors[0]} D:{doors[1]} L:{doors[2]} R:{doors[3]}")
```

### Path Visualizer
```python
def visualize_path(path):
    x, y = 0, 0
    print(f"Start: ({x},{y})")
    for move in path:
        if move == 'U': y -= 1
        elif move == 'D': y += 1
        elif move == 'L': x -= 1
        elif move == 'R': x += 1
        print(f"  {move} → ({x},{y})")
    print(f"Goal reached: {(x,y) == (3,3)}")
```
