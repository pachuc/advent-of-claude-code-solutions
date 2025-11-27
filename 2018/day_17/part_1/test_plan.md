# Test Plan: Water Flow Simulation

## Testing Objectives
1. Verify correct parsing of clay vein input
2. Validate water flow physics (down, spread, settle, overflow)
3. Confirm correct counting within y-range boundaries
4. Test edge cases and complex scenarios

## Test Categories

### 1. Input Parsing Tests

#### Test 1.1: Parse Horizontal Clay Veins
**Input**: `y=7, x=495..501`
**Expected**: Set containing {(495,7), (496,7), (497,7), (498,7), (499,7), (500,7), (501,7)}
**Verify**: All positions generated correctly

#### Test 1.2: Parse Vertical Clay Veins
**Input**: `x=495, y=2..7`
**Expected**: Set containing {(495,2), (495,3), (495,4), (495,5), (495,6), (495,7)}
**Verify**: All positions generated correctly

#### Test 1.3: Parse Single Position
**Input**: `x=500, y=10..10`
**Expected**: Set containing {(500,10)}
**Verify**: Single position handled correctly

#### Test 1.4: Y-Range Calculation
**Input**: Clay at y=5, y=10, y=7, y=100
**Expected**: min_y=5, max_y=100
**Verify**: Correct min/max extraction

### 2. Basic Water Flow Tests

#### Test 2.1: Simple Downward Flow
**Setup**:
```
+     (spring at 500, 0)
|
|
#     (clay at y=5)
```
**Expected**: Flowing water from y=0 to y=5 (if within valid range)
**Verify**: Water flows straight down until blocked

#### Test 2.2: Simple Container (Settling)
**Setup**:
```
  +       (spring)
  |
  |
 ###      (U-shaped container)
# | #
#####
```
**Expected**: Water settles in container, marked as settled (~)
**Verify**:
- Water flows down
- Spreads left and right
- Detects walls on both sides
- Converts to settled water

#### Test 2.3: Overflow (One-sided Barrier)
**Setup**:
```
  +       (spring)
  |
  |
  ####    (clay wall on right only)
  |
```
**Expected**: Water flows right, hits wall, overflows left, continues down
**Verify**: Water marked as flowing (|), not settled

### 3. Complex Flow Scenarios

#### Test 3.1: Stacked Containers
**Setup**:
```
  +
  |
 ###
# ~ #
#####
#   #
#####
```
**Expected**:
- Bottom container fills first
- Water then fills on top of settled water
- Both levels contain settled water
**Verify**: Multiple levels of settlement work correctly

#### Test 3.2: Nested Containers
**Setup**:
```
  +
 ###
# # #
# # #
#####
```
**Expected**:
- Water fills inner container first
- Then overflows and fills outer container
**Verify**: Overflow between containers handled correctly

#### Test 3.3: Side Overflow
**Setup**:
```
    +
   ###
  #   #
  #   #
  #####
 #
```
**Expected**:
- Water fills container
- Overflows at top
- Falls down the side
**Verify**: Water finds overflow path and continues flowing

#### Test 3.4: Multiple Streams
**Setup**: Container with divider
```
     +
    ###
   #   #
   #   #
   # # #
   #####
```
**Expected**: Water may split into multiple flowing streams
**Verify**: Separate flow paths tracked correctly

#### Test 3.5: Rim Overflow (CRITICAL)
**Setup**:
```
    +
  #####
 #     #
 #     #
 #######
```
**Expected**:
- Water flows down inside container
- Bottom rows (y where fully enclosed) have SETTLED water (~)
- Top rim row (y where water can escape) has FLOWING water (|)
- Water at the rim DOES NOT settle because it's not fully contained
**Verify**:
- Distinguish between settled water in container and flowing water at overflow level
- This is a common bug - water at rim must be flowing, not settled

#### Test 3.6: Spreading Over Settled Water
**Setup**:
```
     +
    ####
   #    #
   #    #
   ######
```
**Expected**:
- Container fills from bottom (settled water)
- Water continues to flow and spread on top of settled water
- New water can spread horizontally on top of settled water surface
**Verify**: Water correctly uses settled water as support for spreading

### 4. Boundary and Edge Cases

#### Test 4.1: Spring Outside Valid Range
**Setup**: Spring at y=0, min clay at y=10
**Expected**: Spring itself not counted, only water from y=10 onwards
**Verify**: Only count water within [min_y, max_y]

#### Test 4.2: Water Falls Beyond max_y
**Setup**: Open bottom, water falls past max_y
**Expected**: Flowing water past max_y not counted
**Verify**: Boundary check prevents over-counting

#### Test 4.3: Extremely Wide Spread
**Setup**: Water spreads 100+ units horizontally
**Expected**: All positions tracked correctly
**Verify**: No performance issues, all positions counted

#### Test 4.4: Deep Recursion
**Setup**: Very tall vertical drop (1000+ units)
**Expected**: Simulation completes without stack overflow
**Verify**: Recursion limit sufficient or iterative approach works

#### Test 4.5: Clay at Spring Position
**Setup**: Clay directly below spring at (500, 1)
**Expected**: Water spreads immediately from y=1
**Verify**: Handles immediate blockage correctly

### 5. Counting Verification Tests

#### Test 5.1: Settled vs Flowing Distinction
**Setup**: Mix of settled and flowing water
**Expected**: Both types counted in final answer
**Verify**:
- Settled water (~) counted
- Flowing water (|) counted
- Total is sum of both

#### Test 5.2: Duplicate Position Prevention
**Setup**: Complex flow that might revisit positions
**Expected**: Each position counted only once
**Verify**: Use sets to prevent double-counting

#### Test 5.3: Y-Range Filtering
**Setup**: Water from y=0 to y=100, valid range y=10 to y=50
**Expected**: Only positions in [10, 50] counted
**Verify**: Boundary filtering works correctly

#### Test 5.4: Flowing to Settled State Transition (CRITICAL)
**Setup**: Container where water initially flows through, then settles
```
   +
  ####
 #    #
 #    #
 ######
```
**Expected**:
- Initially, water flows straight down → positions marked as flowing
- When water hits bottom and spreads, container fills
- Positions transition from flowing → settled
- Final count should include all water, with correct state
**Verify**:
- Positions can be in flowing set first, then moved to settled set
- No position should be in both sets simultaneously
- Counting includes positions that changed state

### 6. Example Test Case

#### Test 6.1: Problem Example
**Input**: (from Advent of Code problem description)
```
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=10..13
x=506, y=1..2
y=13, x=498..504
```
**Expected**: 57 tiles of water (both flowing and settled)

**Important**: The example in the problem description shows the expected grid state.

**Verify**:
- Parse all clay correctly
- Simulate water flow
- Count exactly 57 positions

**Debugging for this test**:
- Print grid visualization to verify correctness
- Check settled vs flowing distribution
- Verify overflow points
- Compare visual output with problem example diagram

### 7. Visual Debugging Tests (REQUIRED IMPLEMENTATION)

#### Test 7.1: Grid Visualization (MUST IMPLEMENT FIRST)
**Purpose**: Create a print function to visualize the grid - this is REQUIRED, not optional
**Implementation**:
```python
def print_grid(clay, flowing, settled, min_x, max_x, min_y, max_y):
    # Print grid with:
    # # for clay
    # | for flowing water
    # ~ for settled water
    # + for spring at (500, 0)
    # . for empty space
    # Include y-coordinate labels for debugging
```
**Use**: Debug ALL scenarios visually - implement this before flow logic

**Why required**: Without visualization, debugging water flow is nearly impossible. This should be the first or second function you implement.

#### Test 7.2: Step-by-Step Simulation (Optional)
**Purpose**: Print grid state after each major operation
**Use**: Understand how water propagates through complex structures
**Note**: This is optional for advanced debugging, but 7.1 is mandatory

### 8. Performance Tests

#### Test 8.1: Large Input
**Setup**: Actual puzzle input (~1800 clay lines)
**Expected**: Completes in < 5 seconds
**Verify**: Algorithm efficiency sufficient for problem size

#### Test 8.2: Pathological Case
**Setup**: Very wide container (500+ units wide)
**Expected**: Handles horizontal spread efficiently
**Verify**: No timeout or memory issues

## Test Execution Strategy

### Phase 1: Unit Tests
1. Test parsing functions independently
2. Test y-range calculation
3. Test individual helper functions

### Phase 2: Integration Tests
1. Simple flow scenarios (2.1, 2.2, 2.3)
2. Complex scenarios (3.1, 3.2, 3.3, 3.4)
3. Example test case (6.1)

### Phase 3: Edge Case Validation
1. All boundary tests (4.x)
2. Counting verification (5.x)

### Phase 4: Full Problem
1. Run with actual puzzle input
2. Time the execution (should complete in under 5 seconds)
3. Verify the answer is accepted by the problem checker

## Success Criteria

✅ All basic flow tests pass
✅ Example produces exactly 57 tiles
✅ Settled water correctly identified
✅ Flowing water correctly identified
✅ Y-range filtering works
✅ No double-counting of positions
✅ Completes actual input in reasonable time
✅ Algorithm handles all edge cases

## Debugging Checklist

If tests fail:
- [ ] **FIRST**: Print grid visualization to see actual vs expected
- [ ] Check if water is settling when it shouldn't (rim overflow test 3.5)
- [ ] Check if water is flowing when it should settle (container test)
- [ ] Verify overflow detection logic (horizontal spread function)
- [ ] Check boundary conditions (min_y, max_y filtering)
- [ ] Ensure sets are used (no duplicate counting)
- [ ] Verify recursion depth is sufficient (increase sys.setrecursionlimit)
- [ ] Check that water spreads correctly on top of settled water (test 3.6)
- [ ] Verify state transitions from flowing → settled (test 5.4)
- [ ] Add debug prints showing:
  - When water settles vs flows at each level
  - The return values from flow_down() calls
  - Whether horizontal spread finds walls or overflow points
- [ ] Verify memoization is working (positions not processed multiple times)
- [ ] Check for off-by-one errors in spread bounds

### Specific Debug Prints to Add

When debugging, add these prints to your flow_down function:
```python
print(f"flow_down({x}, {y})")
print(f"  has_support_below: {has_support_below}")
print(f"  is_contained: {is_contained}")
print(f"  returning: {return_value}")
```

When debugging, add these prints to your spread_horizontal function:
```python
print(f"spread_horizontal({x}, {y})")
print(f"  left_wall: {left_wall}, left_bound: {left_bound}")
print(f"  right_wall: {right_wall}, right_bound: {right_bound}")
print(f"  is_contained: {is_contained}")
```
