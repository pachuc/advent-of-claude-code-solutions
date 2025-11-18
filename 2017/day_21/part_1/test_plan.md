# Testing Plan: Fractal Art Pattern Enhancement

## Testing Strategy
Validate the implementation through unit tests for individual components and integration tests for the complete workflow. Focus on correctness of transformations, rule matching, and grid evolution.

## 1. Unit Tests for Helper Functions

### Test 1.1: Pattern/Grid Conversion
**Function**: `pattern_to_grid()` and `grid_to_pattern()`

**Test Cases**:
- Convert `"../.#"` → `["..", ".#"]` → back to `"../.#"`
- Convert `".#./..#/###"` → `[".#.", "..#", "###"]` → back to `".#./..#/###"`
- Convert `"##./#../.../.#.#"` (4×4) and verify round-trip

**Expected Results**: All conversions should be reversible (round-trip = identity)

**Validation**: Assert equality at each step

### Test 1.2: Grid Rotation
**Function**: `rotate_grid()`

**Test Cases**:
- Rotate 2×2 grid: `["..", ".#"]`
  - 90° clockwise: `["..", "#."]`
  - 180°: `["#.", ".."]`
  - 270°: `[".#", ".."]`
  - 360°: back to original

- Rotate 3×3 grid: `[".#.", "..#", "###"]`
  - 90° clockwise: Verify manually during implementation (rotation of 3×3 grids requires careful validation)
  - Verify 4 rotations return to original (this is the key test)

**Expected Results**:
- 4 consecutive rotations should return original grid
- Each rotation should maintain grid dimensions

**Validation**:
- Compare rotated grids with manually calculated expected results
- Assert `rotate(rotate(rotate(rotate(grid)))) == grid`

### Test 1.3: Grid Flipping
**Function**: `flip_grid()`

**Test Cases**:
- Flip `[".#.", "..#", "###"]` → `[".#.", "#..", "###"]`
- Flip `["##.", ".#.", "..."]` → `[".##", ".#.", "..."]`
- Double flip should return original

**Expected Results**: Horizontal reflection of each row

**Validation**:
- Compare with manual calculation
- Assert `flip(flip(grid)) == grid`

### Test 1.4: All Orientations Generation
**Function**: `generate_all_orientations()`

**Test Cases**:
- Symmetric pattern `"../.."` should produce 1 unique orientation
- Asymmetric pattern `"#./.."` should produce up to 8 unique orientations
- Test with `".#./..#/###"` and verify all 8 orientations are distinct

**Expected Results**:
- Return set of all unique orientations
- Symmetric patterns produce fewer unique results
- Maximum 8 unique orientations

**Validation**:
- Check set size
- Manually verify a few orientations are correct
- Ensure no duplicates

## 2. Unit Tests for Grid Operations

### Test 2.1: Grid Division
**Function**: `divide_grid()`

**Test Cases**:
- Divide 4×4 grid into 2×2 blocks
  ```
  ##..
  #...
  ..##
  ...#
  ```
  Should produce: **4 blocks** (2×2 grid of blocks)
  - Top-left: `["##", "#."]`
  - Top-right: `["..", ".."]`
  - Bottom-left: `["..", ".."]`
  - Bottom-right: `["##", ".#"]`

- Divide 6×6 grid into 3×3 blocks: **4 blocks** (2×2 grid of blocks)
- Divide 9×9 grid into 3×3 blocks: **9 blocks** (3×3 grid of blocks)

**Expected Results**:
- Correct number of blocks: (grid_size/block_size)²
- Each block is the correct size
- No overlap or gaps

**Validation**:
- Count number of blocks
- Verify block dimensions
- Reassemble and compare with original

### Test 2.2: Grid Reassembly
**Function**: `reassemble_grid()`

**Test Cases**:
- Take four 3×3 blocks and reassemble into 6×6 grid
- Take nine 4×4 blocks and reassemble into 12×12 grid
- Verify reassembly after division returns original grid (for identity transformation)

**Expected Results**:
- Assembled grid has correct dimensions
- Content is correctly positioned
- Round-trip (divide then reassemble) preserves grid

**Validation**:
- Check final grid dimensions
- Compare with expected pattern
- Assert `reassemble(divide(grid)) == grid` (for same block size)

## 3. Integration Tests

### Test 3.1: Rule Parsing and Lookup
**Function**: `parse_rules()`

**Test Cases**:
- Parse a small set of test rules
- Verify that looking up any of the 8 orientations of an input pattern returns the correct output
- Test with actual input rules

**Test Data**:
```
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
```

**Expected Results**:
- Dictionary contains entries for all orientations
- Looking up any of the 8 orientations of input returns same output
- Example: `rules["../.#"]` and all its rotations/flips (like `"#./.."` which is 180° rotation) both return `"##./#../..."`
- Note: Horizontal flip of `"../.#"` is `"../#."`, vertical flip is `"#./.."`, and 180° rotation is also `"#./.."`

**Validation**:
- Parse rules
- Generate orientations of input pattern
- Look up each orientation and verify same output

### Test 3.2: Single Block Enhancement
**Function**: `enhance_block()`

**Test Cases**:
- Enhance `["..", ".#"]` with rule `../.# => ##./#../...`
- Expected: `["##.", "#..", "..."]`

**Expected Results**: Correct transformed pattern

**Validation**: Compare output with expected grid

### Test 3.3: Single Iteration
**Function**: `perform_iterations()` with num_iterations=1

**Test Cases**:
- Start with `[".#.", "..#", "###"]` (3×3)
- After 1 iteration with example rules, verify resulting 4×4 grid

**Expected Results**:
- Grid grows from 3×3 to 4×4
- Pattern matches expected transformation

**Validation**:
- Check grid size
- Manually verify against rules

### Test 3.4: Example Walkthrough
Use the example from problem statement:

**Input Rules**:
```
../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#
```

**Starting Grid**: `[".#.", "..#", "###"]`

**After 1 iteration**:
- Grid is 3×3, divide into one 3×3 block
- Match `.#./..#/###` → `#..#/..../..../#..#`
- Result: 4×4 grid

**After 2 iterations**:
- Grid is 4×4, divide into four 2×2 blocks
- Each block transforms according to rules
- Result: 6×6 grid with 12 '#' pixels

**Expected Results**: After 2 iterations, count = 12

**Validation**:
- Run full algorithm for 2 iterations
- Count '#' pixels
- Assert count == 12

## 4. Final Solution Validation

### Test 4.1: Full 5 Iterations with Actual Input
**Test Case**: Run complete solution with actual input rules from `input.md`

**Validation Steps**:
1. Verify grid size progression: 3 → 4 → 6 → 9 → 12 → 18
2. Print grid dimensions after each iteration
3. Ensure no errors during pattern matching (all patterns found - should not raise KeyError)
4. Verify final count is a positive integer

**Expected Behavior**:
- All iterations complete successfully
- Final grid is 18×18
- Result is reasonable (between 0 and 324)

### Test 4.2: Grid Size Verification
Track grid dimensions through iterations:
- Start: 3×3
- Iteration 1: 3 % 3 == 0, divide by 3, blocks become 4×4 → 4×4
- Iteration 2: 4 % 2 == 0, divide by 2, blocks become 3×3 → 6×6
- Iteration 3: 6 % 2 == 0, divide by 2, blocks become 3×3 → 9×9
- Iteration 4: 9 % 3 == 0, divide by 3, blocks become 4×4 → 12×12
- Iteration 5: 12 % 2 == 0, divide by 2, blocks become 3×3 → 18×18

**Validation**: Assert grid dimensions match expected values after each iteration

## 5. Edge Cases and Error Conditions

### Test 5.1: Pattern Matching Coverage
**Validation**:
- During actual run, verify all pattern lookups succeed
- No KeyError should occur (error handling will show helpful message if this fails)
- This validates that orientation generation is complete
- If a pattern is not found, the error message will show the exact pattern that failed to match

### Test 5.2: Symmetric Patterns
**Test Case**:
- Patterns that are symmetric under rotation/flip
- Example: `"##/##"` looks the same in multiple orientations
- Verify these still match correctly

**Expected Results**: Should find match even with fewer unique orientations

### Test 5.3: Grid Boundaries
**Test Case**: Verify grid division at boundaries
- Ensure all cells are included in some block
- Ensure no cells are counted twice
- Test with various grid sizes (4, 6, 9, 12, 18)

**Validation**:
- Sum of block cells should equal total grid cells
- Reassembly should preserve all data

## 6. Testing Execution Plan

### Phase 1: Component Testing
1. Test pattern/grid conversion functions
2. Test rotation and flip functions
3. Test orientation generation
4. Fix any issues found

### Phase 2: Grid Operation Testing
1. Test grid division
2. Test grid reassembly
3. Test round-trip preservation
4. Fix any issues found

### Phase 3: Integration Testing
1. Test rule parsing
2. Test single block enhancement
3. Test single iteration
4. Test example walkthrough (2 iterations, 12 pixels)
5. Fix any issues found

### Phase 4: Full Solution Testing
1. Run with actual input from `input.md` for 5 iterations
2. Verify grid size progression (3→4→6→9→12→18)
3. Verify no matching errors (KeyError with helpful message if any pattern fails)
4. Get final pixel count
5. Validate result is reasonable (positive integer, 0 < count ≤ 324)

## 7. Debugging Strategies

### If pattern matching fails:
- Print the pattern being looked up
- Print all available patterns in rules dictionary
- Verify orientation generation produces all 8 variations
- Check for string formatting issues (spaces, case sensitivity)

### If grid size is wrong:
- Print grid size after each iteration
- Verify division logic (% 2 vs % 3)
- Check block reassembly logic
- Ensure enhanced blocks are correct size

### If pixel count seems wrong:
- Print intermediate grids (at least after each iteration)
- Manually count pixels in smaller grids
- Verify counting function logic

## Success Criteria
- All unit tests pass
- Example test (2 iterations → 12 pixels) passes
- Full solution runs without errors
- Final answer is obtained for 5 iterations
- Grid size progression is correct (3→4→6→9→12→18)
