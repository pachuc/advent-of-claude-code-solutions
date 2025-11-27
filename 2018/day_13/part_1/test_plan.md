# Testing Plan: Mine Cart Collision Detection

## Overview
Comprehensive testing strategy to verify the cart collision simulation works correctly.

## Testing Approach

### Philosophy
- Start with unit tests for individual components
- Progress to integration tests with small examples
- Validate with the actual input
- Focus on correctness over exhaustive edge cases (script-level testing)

## Test Categories

### 1. Unit Tests for Direction Logic

#### Test 1.1: Turn Left Function
**Objective**: Verify left turns work for all directions

**Test Cases**:
```
Input → Expected Output
UP → LEFT
LEFT → DOWN
DOWN → RIGHT
RIGHT → UP
```

**Validation Method**:
- Create simple assertions for each direction
- Print "PASS" or "FAIL" for each case

#### Test 1.2: Turn Right Function
**Objective**: Verify right turns work for all directions

**Test Cases**:
```
Input → Expected Output
UP → RIGHT
RIGHT → DOWN
DOWN → LEFT
LEFT → UP
```

#### Test 1.3: Curve Transformations
**Objective**: Verify direction changes on curves

**Test Cases for `/` curve**:
```
Direction → Expected New Direction
UP → RIGHT
RIGHT → UP
DOWN → LEFT
LEFT → DOWN
```

**Test Cases for `\` curve**:
```
Direction → Expected New Direction
UP → LEFT
LEFT → UP
DOWN → RIGHT
RIGHT → DOWN
```

**Validation Method**:
- Test each combination explicitly
- Verify bidirectional correctness (both ways through curve)

#### Test 1.4: Intersection Logic
**Objective**: Verify intersection turning pattern

**Test Cases** (for a cart moving UP):
```
Intersection Count → Action → New Direction
0 → LEFT → LEFT (from UP)
1 → STRAIGHT → UP (unchanged)
2 → RIGHT → RIGHT (from UP)
3 → LEFT → LEFT (pattern repeats)
```

**Validation Method**:
- Simulate cart going through 4+ intersections
- Verify pattern cycles correctly

### 2. Small Example Tests

#### Test 2.1: Simple Head-On Collision
**Objective**: Verify basic collision detection

**Input Map**:
```
|
v
|
|
^
|
```

**Expected Behavior**:
- Carts should collide after moving toward each other
- Should detect collision immediately when they occupy same position

**Expected Result**: Collision at position where they meet

**Validation Method**:
- Run simulation
- Verify collision is detected
- Verify position is correct

#### Test 2.2: Two Carts on Straight Track
**Objective**: Test horizontal collision

**Input Map**:
```
>--<
```

**Expected Result**: Collision at middle position

#### Test 2.3: Curve Following
**Objective**: Verify carts correctly follow curves

**Input Map**:
```
/--\
|  |
v  |
\--/
```

**Expected Behavior**:
- Cart should navigate around the loop
- Should maintain correct direction at each curve
- Cart starts moving down on left side
- At bottom-left: `\` turns it right
- At bottom-right: `/` turns it up
- At top-right: `\` turns it left
- At top-left: `/` turns it down (completing loop)

**Validation Method**:
- Track cart position for several ticks
- Verify direction changes at each curve
- Verify cart follows track correctly and completes the loop

#### Test 2.4: Intersection Without Collision
**Objective**: Verify intersection turning logic

**Input Map**:
```
  |
--+--
  |
  v
```

**Expected Behavior**:
- Cart entering from bottom should turn left (first intersection)
- Track cart through multiple passes if needed

**Validation Method**:
- Monitor cart direction after passing intersection
- Verify it turned left (first time through)

### 3. Cart Ordering Tests

#### Test 3.1: Multiple Carts - Correct Move Order
**Objective**: Verify carts move in top-to-bottom, left-to-right order

**Input Map**:
```
>  >
v  v
```

**Expected Move Order**:
1. Top-left cart (row 0, col 0)
2. Top-right cart (row 0, col 3)
3. Bottom-left cart (row 1, col 0)
4. Bottom-right cart (row 1, col 3)

**Validation Method**:
- Add debug prints showing move order
- Verify sequence matches expected

#### Test 3.2: Mid-Tick Collision Detection
**Objective**: Verify collision detected immediately, not at end of tick

**Input Map**:
```
>-<>-
```
(Note: All carts on connected track, but first two will collide before third cart moves)

**Expected Behavior**:
- Leftmost cart moves right
- Second cart (facing left) moves left
- They collide at position between them
- Collision should be detected immediately
- Fourth cart should not have moved yet when collision detected

**Validation Method**:
- Track collision position
- Verify collision happens mid-tick
- Ensure simulation stops at first collision

### 4. Track Parsing Tests

#### Test 4.1: Cart Character Replacement
**Objective**: Verify carts are replaced with correct track

**Test Cases**:
```
^ → | (vertical)
v → | (vertical)
< → - (horizontal)
> → - (horizontal)
```

**Validation Method**:
- Parse input
- Check track grid has correct characters
- Verify no cart characters remain in track

#### Test 4.2: Cart Position Extraction
**Objective**: Verify cart positions parsed correctly

**Input Map**:
```
--v--
  |
--^--
```

**Expected Carts**:
- Cart 1: x=2, y=0, direction=DOWN
- Cart 2: x=2, y=2, direction=UP

**Validation Method**:
- Print parsed cart positions
- Compare with expected values

### 5. Integration Tests

#### Test 5.1: Provided Example (if any)
**Objective**: Verify against any examples in problem statement

**Method**:
- Check problem.md for any worked examples with complete input and expected output
- Note: problem.md shows output format example ("7,3") but no complete track example
- If no complete example is provided, skip this test and proceed to actual input validation

#### Test 5.2: Actual Input Validation
**Objective**: Verify solution works on actual input

**Method**:
1. Run simulation on actual input
2. Verify:
   - Simulation completes without errors
   - Result is in correct format (X,Y)
   - Coordinates are within grid bounds
3. Check result makes sense:
   - Position should be on track (not empty space)
   - Should be `+`, `/`, `\`, `|`, or `-` character

### 6. Edge Case Tests

#### Test 6.1: Carts Starting Adjacent
**Objective**: Handle carts very close together

**Input Map**:
```
>>
```

**Expected**: Should handle without immediate collision (unless they overlap)

#### Test 6.2: Complex Intersection Sequence
**Objective**: Cart hits multiple intersections

**Input Map**: Track with multiple `+` symbols in sequence

**Expected**: Cart correctly cycles through left/straight/right pattern

#### Test 6.3: All Four Directions Present
**Objective**: Verify all cart types work

**Input Map**: Include `^`, `v`, `<`, `>` all in separate locations

**Expected**: All carts move correctly

#### Test 6.4: Per-Cart Intersection State
**Objective**: Verify intersection counter is per-cart, not per-intersection-location

**Input Map**: Two carts that hit the same intersection at different times

**Setup**:
- Cart A hits intersection X for its first time (should turn left)
- Cart B later hits the same intersection X for its second time (should go straight)
- Both actions should happen correctly despite being the same physical intersection

**Expected Behavior**:
- Each cart independently cycles through left/straight/right
- The intersection state is tracked per-cart, not per-location
- Cart A's action at intersection X doesn't affect Cart B's action at the same intersection

**Validation Method**:
- Track each cart's intersection counter separately
- Verify they take different actions at the same physical intersection
- This catches the common mistake of tracking state per-intersection instead of per-cart

### 7. Output Format Tests

#### Test 7.1: Coordinate Format
**Objective**: Verify output format is exactly "X,Y"

**Validation**:
- Check result matches regex: `^\d+,\d+$`
- Verify X comes before Y
- No spaces, brackets, or other characters

#### Test 7.2: Coordinate System
**Objective**: Verify X=column, Y=row (not reversed)

**Method**:
- Use known collision point
- Verify X coordinate increases going right
- Verify Y coordinate increases going down

## Testing Execution Plan

### Phase 1: Component Testing (Unit Tests)
1. Test direction functions (turn_left, turn_right)
2. Test curve logic
3. Test intersection logic
4. Fix any issues found

### Phase 2: Small Examples
1. Create 3-5 minimal test cases
2. Hand-calculate expected results
3. Run and verify
4. Debug any discrepancies

### Phase 3: Integration Testing
1. Test cart ordering
2. Test parsing
3. Test full simulation on small inputs
4. Verify collision detection timing

### Phase 4: Full Input Validation
1. Run on actual input
2. Verify output format
3. Check result reasonableness:
   - Coordinates within bounds
   - Position is on valid track

### Phase 5: Manual Verification (if needed)
1. If result seems wrong:
   - Print first N ticks of simulation
   - Visualize cart positions
   - Trace movement manually
2. Check for common issues:
   - Wrong coordinate system (X/Y reversed)
   - Wrong turn directions on curves
   - Intersection pattern incorrect

## Debugging Strategies

### If Tests Fail:

#### Direction Logic Issues
- Print direction before/after each transformation
- Verify against manual calculation
- Check curve character interpretation

#### Collision Not Detected
- Print all cart positions each tick
- Check if positions actually overlap
- Verify collision detection runs after each cart move

#### Wrong Collision Location
- Print collision tick number
- Visualize final positions
- Check coordinate output format

#### Infinite Loop (No Collision)
- Add tick counter with maximum limit
- Print cart positions periodically
- Check if carts are actually moving

### Visualization Helper
Create optional debug function to print current state:
```
Tick 42:
--v--
  |
--^--

Carts: [(2,0,DOWN), (2,2,UP)]
```

## Success Criteria

### Minimum Requirements
1. All unit tests pass
2. At least 2 small examples work correctly
3. Actual input produces valid output (X,Y format)
4. No runtime errors or infinite loops

### Verification Checklist
- [ ] Direction transformations correct
- [ ] Intersection pattern cycles properly
- [ ] Carts move in correct order
- [ ] Collision detected immediately (mid-tick)
- [ ] Output format is exactly "X,Y"
- [ ] X and Y coordinates not reversed
- [ ] Result is on valid track location

## Test Documentation

For each test, record results in a simple format:

**Template**:
```
Test: [Test Name]
Input: [Input description or data]
Expected: [Expected output]
Actual: [Actual output]
Status: PASS/FAIL
Notes: [Any observations]
---
```

**Example**:
```
Test: Turn Left Function - UP direction
Input: UP
Expected: LEFT
Actual: LEFT
Status: PASS
---

Test: Simple Head-On Collision
Input: Two carts moving toward each other on vertical track
Expected: Collision at position where they meet
Actual: 0,2
Status: PASS
Notes: Collision occurred on tick 2 as expected
---
```

This creates a simple test trail without needing a full test framework.
