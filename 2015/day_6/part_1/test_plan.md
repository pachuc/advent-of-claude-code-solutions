# Testing Plan: Light Grid Control System

## Testing Strategy Overview
Since this is a script to solve a specific problem (not production code), we'll focus on:
1. **Coordinate system validation** to ensure correct interpretation
2. **Correctness verification** using the provided examples
3. **Edge case validation** for boundary conditions
4. **Component testing** for parsing and grid operations
5. **Integration testing** with sample instruction sequences
6. **Final validation** with the actual input

## Coordinate System Convention
**CRITICAL**: All tests must verify correct coordinate interpretation:
- First coordinate = column (horizontal, x-axis)
- Second coordinate = row (vertical, y-axis)
- Grid indexing: `row * 1000 + column` (row-major order)
- Example: "5,10 through 7,12" affects columns 5-7, rows 10-12 (9 lights: 3 wide × 3 tall)

## Test Categories

### 1. Unit Tests: Instruction Parsing

#### Test 1.1: Parse "turn on" instruction
**Input**: `"turn on 887,9 through 959,629"`
**Expected Output**: `('on', 887, 9, 959, 629)` where 887=col1, 9=row1, 959=col2, 629=row2
**Purpose**: Verify correct extraction of "turn on" command and coordinates

#### Test 1.2: Parse "turn off" instruction
**Input**: `"turn off 499,499 through 500,500"`
**Expected Output**: `('off', 499, 499, 500, 500)`
**Purpose**: Verify correct extraction of "turn off" command and coordinates

#### Test 1.3: Parse "toggle" instruction
**Input**: `"toggle 0,0 through 999,0"`
**Expected Output**: `('toggle', 0, 0, 999, 0)` - columns 0-999, row 0 (a horizontal line)
**Purpose**: Verify correct extraction of "toggle" command and coordinates

#### Test 1.4: Parse with various coordinate ranges
**Inputs**:
- `"turn on 0,0 through 0,0"` → Single light at origin (col 0, row 0)
- `"toggle 999,999 through 999,999"` → Single light at far corner
- `"turn off 0,0 through 999,999"` → Entire grid

**Purpose**: Verify parsing handles min/max coordinates correctly

### 2. Unit Tests: Grid Operations

#### Test 2.0: **CRITICAL - Coordinate Interpretation Test**
**Purpose**: Verify grid indexing matches coordinate system (catches transposition bugs)
**Setup**: Empty grid
**Action**: `apply_instruction(grid, 'on', 5, 10, 7, 12)`
  - This is columns 5-7, rows 10-12 → 3 wide × 3 tall = 9 lights
**Verification**:
- `sum(grid)` should be `9`
- Verify specific indices are True using `row * 1000 + col`:
  - grid[10*1000 + 5] = True (row 10, col 5)
  - grid[10*1000 + 6] = True (row 10, col 6)
  - grid[10*1000 + 7] = True (row 10, col 7)
  - grid[12*1000 + 5] = True (row 12, col 5)
  - grid[12*1000 + 7] = True (row 12, col 7)

#### Test 2.1: Asymmetric rectangle (catches transposition)
**Setup**: Empty grid
**Action**: `apply_instruction(grid, 'on', 100, 200, 102, 210)`
  - 3 columns wide (100-102), 11 rows tall (200-210) → 3 × 11 = 33 lights
**Verification**: `sum(grid)` should be `33`
**Purpose**: Catch coordinate transposition bugs (would give 11 × 3 = 33 by coincidence, but wrong positions)

#### Test 2.2: Turn on single light
**Setup**: Empty grid (all False)
**Action**: `apply_instruction(grid, 'on', 0, 0, 0, 0)`
**Verification**:
- `grid[0]` should be `True`
- `sum(grid)` should be `1`
**Purpose**: Verify basic "turn on" functionality

#### Test 2.3: Turn on rectangular region
**Setup**: Empty grid
**Action**: `apply_instruction(grid, 'on', 0, 0, 2, 2)`
**Verification**:
- All 9 lights in 3×3 region should be `True`
- `sum(grid)` should be `9`
- Check corners: grid[0*1000+0], grid[0*1000+2], grid[2*1000+0], grid[2*1000+2]
**Purpose**: Verify inclusive rectangular range

#### Test 2.4: Turn off lights
**Setup**: Grid with some lights ON
**Action**: `apply_instruction(grid, 'off', 1, 1, 1, 1)`
**Verification**: Specific light is OFF, others unchanged
**Purpose**: Verify "turn off" functionality

#### Test 2.5: Toggle lights
**Setup**: Grid with mix of ON and OFF lights
**Action**: `apply_instruction(grid, 'toggle', col1, row1, col2, row2)` on a region
**Verification**:
- ON lights become OFF
- OFF lights become ON
**Purpose**: Verify toggle flips state correctly

#### Test 2.6: Idempotent operations
**Setup**: Empty grid
**Actions**:
1. `apply_instruction(grid, 'on', 5, 5, 10, 10)`
2. `apply_instruction(grid, 'on', 5, 5, 10, 10)` (again)
**Verification**: Count remains same (36 lights: 6×6)
**Purpose**: Verify turning on already-ON lights doesn't cause issues

**Setup**: Grid with lights ON
**Actions**:
1. `apply_instruction(grid, 'off', 5, 5, 10, 10)`
2. `apply_instruction(grid, 'off', 5, 5, 10, 10)` (again)
**Verification**: Lights remain OFF
**Purpose**: Verify turning off already-OFF lights doesn't cause issues

### 3. Integration Tests: Example Cases from Problem

#### Test 3.1: Example 1 - Turn on entire grid
**Instructions**: `"turn on 0,0 through 999,999"`
**Expected Result**: `1,000,000` lights ON
**Purpose**: Verify maximum case works correctly

#### Test 3.2: Example 2 - Toggle top row
**Instructions**:
1. `"turn on 0,0 through 999,999"` (all ON)
2. `"toggle 0,0 through 999,0"` (toggle columns 0-999, row 0 = top row = 1000 lights)
**Expected Result**: `999,000` lights ON (1M - 1000)
**Purpose**: Verify toggle works on ON lights
**Note**: This toggles the TOP ROW (row 0, all columns) - a horizontal line

#### Test 3.3: Example 3 - Turn off middle 4 lights
**Instructions**:
1. `"turn on 0,0 through 999,999"` (all ON)
2. `"turn off 499,499 through 500,500"` (turn off 2×2 in middle)
**Expected Result**: `999,996` lights ON (1M - 4)
**Purpose**: Verify small rectangular turn-off works

### 4. Edge Case Tests

#### Test 4.1: Empty instruction set
**Instructions**: Empty file or no instructions
**Expected Result**: `0` lights ON
**Purpose**: Verify initial state is all OFF

#### Test 4.2: Single light operations
**Instructions**:
1. `"turn on 500,500 through 500,500"`
**Expected Result**: `1` light ON
**Purpose**: Verify minimum rectangle size (1×1)

#### Test 4.3: Boundary coordinates
**Test coordinates at grid boundaries**:
- Top-left corner: (0, 0)
- Top-right corner: (0, 999)
- Bottom-left corner: (999, 0)
- Bottom-right corner: (999, 999)

**Purpose**: Ensure no off-by-one errors at boundaries

#### Test 4.4: Overlapping instructions
**Instructions**:
1. `"turn on 0,0 through 10,10"` → 121 lights ON
2. `"turn off 5,5 through 15,15"` → Should turn off overlap
**Expected Result**: Calculate exact count based on non-overlapping region
**Purpose**: Verify later instructions correctly override earlier ones

#### Test 4.5: Toggle twice returns to original state
**Instructions**:
1. `"turn on 100,100 through 200,200"` → 101×101 = 10,201 lights ON
2. `"toggle 100,100 through 200,200"` → 0 lights ON
3. `"toggle 100,100 through 200,200"` → 10,201 lights ON
**Expected Result**: `10,201` lights ON
**Purpose**: Verify toggle is truly reversible
**Calculation**: (200-100+1) × (200-100+1) = 101 × 101 = 10,201

#### Test 4.6: Full row and column operations
**Instructions**:
1. `"turn on 0,0 through 999,0"` → Full row (1,000 lights)
2. `"turn on 0,0 through 0,999"` → Full column (adds 999 more, since (0,0) already ON)
**Expected Result**: `1,999` lights ON
**Purpose**: Verify row/column spanning works correctly

### 5. Stress Tests

#### Test 5.1: Many overlapping regions
**Instructions**: Create 100 overlapping "turn on" operations on same region
**Expected Result**: Consistent final count
**Purpose**: Verify no accumulation bugs

#### Test 5.2: Alternating toggle operations
**Instructions**: Toggle same region 1000 times
**Expected Result**: All lights OFF if started with lights ON (even number of toggles)
**Purpose**: Verify toggle state management is correct

### 6. Final Validation Tests

#### Test 6.1: Sample subset of actual input
**Instructions**: Take first 10 instructions from input.md
**Method**:
1. Process manually or with verified logic
2. Compare against implementation output
**Purpose**: Validate on real data subset

#### Test 6.2: Full input processing
**Instructions**: Process all 300 instructions from input.md
**Method**:
1. Run the complete solution
2. Verify output is a reasonable number (0 ≤ result ≤ 1,000,000)
3. Check runtime is acceptable (< 60 seconds)
**Purpose**: Ensure solution works on complete problem

#### Test 6.3: Verify grid state makes sense
**After processing full input**:
- Count should be between 0 and 1,000,000
- No negative values
- No values > 1,000,000
**Purpose**: Sanity check on final answer

## Testing Implementation Approach

### Manual Testing Strategy
Since this is a script (not production code), implement simple assertion-based tests:

```python
def test_parsing():
    # Test parsing extracts coordinates correctly (col, row format)
    assert parse_instruction("turn on 0,0 through 999,999") == ('on', 0, 0, 999, 999)
    assert parse_instruction("turn off 499,499 through 500,500") == ('off', 499, 499, 500, 500)
    assert parse_instruction("toggle 0,0 through 999,0") == ('toggle', 0, 0, 999, 0)
    print("✓ Parsing tests passed")

def test_coordinate_system():
    """CRITICAL: Verify correct coordinate interpretation (col, row) -> grid[row*1000+col]"""
    grid = [False] * 1000000

    # Test: 3 columns (5-7) × 3 rows (10-12) = 9 lights
    apply_instruction(grid, 'on', 5, 10, 7, 12)
    assert sum(grid) == 9, f"Expected 9 lights, got {sum(grid)}"

    # Verify specific positions
    assert grid[10*1000 + 5] == True, "Position (col=5, row=10) should be ON"
    assert grid[12*1000 + 7] == True, "Position (col=7, row=12) should be ON"
    assert grid[10*1000 + 8] == False, "Position (col=8, row=10) should be OFF"

    print("✓ Coordinate system tests passed")

def test_grid_operations():
    # Test turn on single light
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 0, 0, 0, 0)
    assert sum(grid) == 1
    assert grid[0] == True

    # Test rectangular region
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 0, 0, 2, 2)
    assert sum(grid) == 9

    # Test asymmetric rectangle (3 wide × 11 tall = 33)
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 100, 200, 102, 210)
    assert sum(grid) == 33, f"Expected 33 lights (3×11), got {sum(grid)}"

    # Test toggle
    grid = [False] * 1000000
    apply_instruction(grid, 'toggle', 0, 0, 0, 0)
    assert grid[0] == True
    apply_instruction(grid, 'toggle', 0, 0, 0, 0)
    assert grid[0] == False

    print("✓ Grid operation tests passed")

def test_examples():
    # Example 1: Turn on all lights
    grid = [False] * 1000000
    apply_instruction(grid, 'on', 0, 0, 999, 999)
    assert sum(grid) == 1000000

    # Example 2: Toggle top row (row 0, all columns) after turning all on
    grid = [True] * 1000000
    apply_instruction(grid, 'toggle', 0, 0, 999, 0)
    assert sum(grid) == 999000

    # Example 3: Turn off middle 4 lights (2×2)
    grid = [True] * 1000000
    apply_instruction(grid, 'off', 499, 499, 500, 500)
    assert sum(grid) == 999996

    print("✓ Example tests passed")
```

### Test Execution Order
1. Run parsing tests first (fail fast if parsing is broken)
2. **Run coordinate system tests** (CRITICAL - catches transposition bugs)
3. Run grid operation tests (verify core functionality)
4. Run example tests (verify against known results)
5. Run edge case tests (verify boundary conditions)
6. Run full input (final validation)

## Verification Checklist

- [ ] **Coordinate system correctly interprets (col, row) format**
- [ ] **Grid indexing uses row-major order: row * 1000 + col**
- [ ] **Asymmetric rectangles test passes (catches transposition bugs)**
- [ ] Parsing correctly extracts all three command types
- [ ] Parsing correctly handles all coordinate ranges
- [ ] Grid operations work for single lights
- [ ] Grid operations work for rectangular regions
- [ ] Inclusive ranges are handled correctly (col1 to col2 includes both endpoints)
- [ ] Toggle correctly flips state
- [ ] Turn on/off are idempotent
- [ ] All example cases pass
- [ ] Boundary coordinates (0, 999) work correctly
- [ ] Overlapping instructions are processed sequentially
- [ ] Full input processes without errors
- [ ] Final count is within valid range [0, 1,000,000]
- [ ] Runtime is acceptable (30-60 seconds expected)

## Success Criteria
The implementation is considered correct if:
1. **Coordinate system test passes** (verifies correct col/row interpretation)
2. **Asymmetric rectangle tests pass** (catches transposition bugs)
3. All unit tests pass
4. All three examples from the problem statement produce correct results
5. Full input processes successfully
6. Output is a single integer in range [0, 1,000,000]
7. No runtime errors or exceptions occur
8. Runtime is acceptable (under 2 minutes)

## Notes on Final Validation
- The actual expected answer for the full input is unknown until solved
- Test 6.2 provides only sanity checking (valid range, no crashes)
- Correctness depends on passing all unit and example tests first
