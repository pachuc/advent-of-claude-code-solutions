# Test Plan: Reindeer Racing Point System

## Testing Strategy Overview

The testing approach will verify:
1. **Input parsing correctness**
2. **Position calculation accuracy**
3. **State transition logic**
4. **Leader detection and point awarding**
5. **End-to-end simulation results**

We focus on functional correctness and algorithm validation rather than production-level testing.

## Test Categories

### 1. Input Parsing Tests

#### Test 1.1: Parse Single Reindeer
**Purpose**: Verify regex correctly extracts reindeer attributes

**Input**:
```
Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds.
```

**Expected Output**:
```python
{
    'name': 'Dancer',
    'speed': 27,
    'fly_time': 5,
    'rest_time': 132
}
```

**Validation**:
- Check all fields are extracted
- Verify data types (integers for numeric values)

#### Test 1.2: Parse All Input Lines
**Purpose**: Verify all 9 reindeer are parsed correctly

**Input**: Full input.md file

**Expected Output**: List of 9 reindeer dictionaries

**Validation**:
- Count == 9
- No duplicate names
- All speeds, fly_times, rest_times > 0

### 2. Position Calculation Tests

#### Test 2.1: Single Cycle Movement
**Purpose**: Verify position updates during one complete fly-rest cycle

**Setup**:
- Dancer: speed=27, fly_time=5, rest_time=132

**Test Points**:
- Second 1: distance = 27 (flying during second 1)
- Second 2: distance = 54 (flying during second 2)
- Second 5: distance = 135 (flying during second 5, last fly second)
- Second 6: distance = 135 (resting during second 6, first rest second)
- Second 137: distance = 135 (resting during second 137, last rest second before cycle completes)
- Second 138: distance = 162 (flying again during second 138, new cycle begins)

**Timing Note**: These distances are measured AFTER the position update for each second completes.

**Validation**: Check distance equals expected value at each checkpoint

#### Test 2.2: Multiple Reindeer Positions
**Purpose**: Verify correct tracking of multiple reindeer simultaneously

**Setup**:
- Dancer: 27 km/s for 5s, rest 132s
- Comet: 18 km/s for 6s, rest 103s

**Test at Second 10**:
- Dancer: 5s flying (135 km) + 5s resting (0 km) = 135 km
- Comet: 6s flying (108 km) + 4s resting (0 km) = 108 km

**Validation**: Both reindeer have correct distances

#### Test 2.3: Long Duration Position
**Purpose**: Verify position calculation over extended time (1000 seconds)

**Setup**: Use example reindeer from problem

**Expected at 1000 seconds**:
- Dancer: 1120 km (from problem example)
- Comet: 1056 km (from problem example)

**Validation**:
- Calculate expected distance using independent verification formula:
  - Complete cycles = floor(time / (fly_time + rest_time))
  - Remaining time = time % (fly_time + rest_time)
  - Distance = (complete_cycles × fly_time × speed) + (min(remaining, fly_time) × speed)
- Compare simulation result with formula

**IMPORTANT**: This formula is ONLY for test validation to verify distance calculations. It cannot be used for the main solution since it doesn't track point awards second-by-second.

### 3. State Transition Tests

#### Test 3.1: Flying to Resting Transition
**Purpose**: Verify correct state change from flying to resting

**Setup**: Reindeer with fly_time=3

**Test**:
- Second 1-3: is_flying=True, distance increases
- Second 4: is_flying=False, distance stays constant
- Check time_in_state resets to 0 at transition

**Validation**: State flag and timer update correctly

#### Test 3.2: Resting to Flying Transition
**Purpose**: Verify correct state change from resting to flying

**Setup**: Reindeer with fly_time=2, rest_time=3

**Test**:
- Start at second 3 (end of first fly period)
- Second 3-5: is_flying=False
- Second 6: is_flying=True, distance increases again
- Check time_in_state resets to 0 at transition

**Validation**: Resumption of movement after rest period

#### Test 3.3: Multiple Cycle Transitions
**Purpose**: Verify state transitions across many cycles

**Setup**: Reindeer with short cycle (fly_time=2, rest_time=2)

**Test Duration**: 20 seconds (5 complete cycles)

**Validation**:
- Count total cycles completed = 5
- Verify state alternates correctly
- Distance = 5 cycles × 2 seconds flying × speed

### 4. Leader Detection Tests

#### Test 4.1: Single Leader
**Purpose**: Verify correct identification when one reindeer is ahead

**Setup**:
- Reindeer A: distance=100
- Reindeer B: distance=90
- Reindeer C: distance=85

**Expected**: Leaders = [Reindeer A]

**Validation**: Only the reindeer with max distance is returned

#### Test 4.2: Multiple Leaders (Tie)
**Purpose**: Verify all tied reindeer are identified as leaders

**Setup**:
- Reindeer A: distance=100
- Reindeer B: distance=100
- Reindeer C: distance=95

**Expected**: Leaders = [Reindeer A, Reindeer B]

**Validation**: Both tied reindeer are returned

#### Test 4.3: All Tied
**Purpose**: Edge case where all reindeer have same distance

**Setup**: All reindeer at distance=0 (initial state)

**Expected**: Leaders = [all reindeer]

**Validation**: All reindeer receive points

### 5. Point Awarding Tests

#### Test 5.1: Points Accumulate Correctly
**Purpose**: Verify points increment for leaders each second

**Setup**: Single reindeer leading for 10 seconds

**Expected**: Reindeer has 10 points after 10 seconds

**Validation**: Points = seconds as leader

#### Test 5.2: Points with Leadership Changes
**Purpose**: Verify points awarded correctly when lead changes

**Scenario**:
- Second 1-5: Reindeer A leads
- Second 6-10: Reindeer B leads

**Expected**:
- Reindeer A: 5 points
- Reindeer B: 5 points

**Validation**: Points reflect time spent in lead

#### Test 5.3: Points with Ties
**Purpose**: Verify both tied reindeer get points

**Scenario**: Reindeer A and B tied for 10 seconds

**Expected**:
- Reindeer A: 10 points
- Reindeer B: 10 points

**Validation**: All leaders receive points simultaneously

### 6. Example Validation Test

#### Test 6.1: 1000-Second Example
**Purpose**: Validate against problem example

**Setup**:
- Dancer: 27 km/s for 5s, rest 132s
- Comet: 18 km/s for 6s, rest 103s
- Duration: 1000 seconds

**Expected**:
- Dancer: 689 points
- Comet: 312 points
- Winner: Dancer

**Validation**:
- Run simulation for 1000 seconds
- Check Dancer has 689 points (exact match)
- Check Comet has 312 points (exact match)
- Verify Dancer is winner

**Importance**: This is the reference example from the problem statement

### 7. Full Simulation Test

#### Test 7.1: Complete 2503-Second Race
**Purpose**: Verify full simulation with actual input

**Setup**: All 9 reindeer from input.md, 2503 seconds

**Validation Steps**:
1. **Sanity Checks**:
   - All reindeer have distances > 0
   - All reindeer have points ≥ 0
   - Sum of all points ≥ 2503 (equals 2503 if no ties, >2503 if ties occur)
   - Max points ≤ 2503 (one reindeer can't lead more than every second)

2. **Internal Consistency**:
   - Verify no reindeer has negative distance or points
   - Check all reindeer completed reasonable number of cycles

3. **Distance Validation**:
   - Calculate theoretical maximum distance for each reindeer
   - Verify actual distance ≤ theoretical max

4. **Result Range**:
   - Winning points should be in reasonable range (likely 1000-2500)
   - Winner should be one of the faster reindeer (Donner or Dancer)

### 8. Edge Case Tests

#### Test 8.1: First Second Behavior
**Purpose**: Explicitly validate behavior at the very first second

**Setup**: All 9 reindeer from input

**Expected After Second 1**:
- All reindeer have moved (distance equals their speed)
- All reindeer are tied for the lead
- All reindeer have exactly 1 point
- All reindeer are in flying state

**Validation**:
- Verify each reindeer: distance == speed
- Verify each reindeer: points == 1
- Verify sum of all points == 9

#### Test 8.2: Very Short Duration
**Purpose**: Test simulation with duration=1 second (similar to 8.1 but focused on final state)

**Expected**: All reindeer at distance=speed, all have 1 point (tie)

**Validation**: Handles minimal duration correctly

#### Test 8.3: Reindeer Never Rests
**Purpose**: Edge case with rest_time approaching 0 (if possible)

**Note**: Not applicable with given input, but algorithm should handle it

#### Test 8.4: Reindeer Barely Flies
**Purpose**: Edge case with fly_time=1, long rest_time

**Setup**: Custom reindeer with fly_time=1, rest_time=1000

**Validation**: Correctly handles heavily resting reindeer

### 9. Algorithm Correctness Tests

#### Test 9.1: Mathematical Verification
**Purpose**: Verify simulation matches mathematical calculations

**Method**:
```python
def calculate_distance_at_time(speed, fly_time, rest_time, total_time):
    cycle_time = fly_time + rest_time
    complete_cycles = total_time // cycle_time
    remainder = total_time % cycle_time

    distance = complete_cycles * fly_time * speed
    distance += min(remainder, fly_time) * speed

    return distance
```

**Test**: For each reindeer at various time points (100, 500, 1000, 2503), compare simulation distance with calculated distance

**Validation**: Distances match exactly

#### Test 9.2: Points Sum Consistency
**Purpose**: Verify total points awarded makes sense

**Formula**: Total points awarded = (sum of all reindeer points)

**Expected**:
- If no ties: total = 2503 exactly
- If ties occur: total > 2503 (multiple reindeer get points per second)

**Validation**:
- Minimum: Total points ≥ 2503
- Maximum: Total points ≤ 2503 × 9 = 22,527 (theoretical max if all tied every second)
- Reasonable upper bound

## Test Execution Plan

### Phase 1a: Basic Parsing and Setup
1. Run parsing tests (Test 1.x)
2. Verify all 9 reindeer are extracted correctly

### Phase 1b: Critical Early Validation
1. **Run example validation (Test 6.1) - HIGHEST PRIORITY**
2. This validates the 1000-second example (Dancer: 689 points)
3. If this fails, debug before proceeding further

### Phase 2: Detailed Unit Tests
1. Run position calculation tests (Test 2.x)
2. Run state transition tests (Test 3.x)
3. Run leader detection tests (Test 4.x)
4. Run point awarding tests (Test 5.x)
5. Run first second test (Test 8.1)

### Phase 3: Algorithm Verification
1. Run mathematical verification tests (Test 9.x)
2. Ensure simulation matches independent calculations

### Phase 4: Full System Test
1. Run complete 2503-second simulation (Test 7.1)
2. Verify answer is reasonable
3. Check against expected patterns
4. Run edge case tests (Test 8.x)

**Rationale for Reordering**: Running Test 6.1 early provides immediate validation that the core algorithm is correct before investing time in detailed unit tests.

## Validation Criteria for Correct Solution

### Must Pass:
1. ✅ 1000-second example produces exactly 689 points for Dancer
2. ✅ All reindeer parsed correctly (9 total)
3. ✅ Distance calculations match mathematical formula
4. ✅ Final answer is a positive integer
5. ✅ Winning points ≤ 2503

### Should Pass:
1. ✅ Total points awarded ≥ 2503
2. ✅ Winner is likely Dancer or Donner (fastest reindeer)
3. ✅ All intermediate states are consistent

## Debugging Strategies

### If Results Don't Match Example:
1. Print second-by-second state for first 20 seconds
2. Check if Dancer's position at second 137 is 135 km (after first cycle)
3. Verify state transitions happen at correct times
4. Check point awarding logic with manual calculation

### If Final Answer Seems Wrong:
1. Print final positions and points for all reindeer
2. Identify winner and verify they led most often
3. Calculate theoretical maximum points (2503 if always leading)
4. Check for off-by-one errors in loop bounds

## Test Implementation Notes

- Use assertions for automated validation
- Print intermediate results for manual verification
- Create helper functions for common validation patterns
- Log key checkpoints (seconds 100, 500, 1000, 2503)

## Expected Test Output

When all tests pass:
```
✓ Parsing: 9 reindeer extracted
✓ Position at 1000s: Dancer=1120km, Comet=1056km
✓ Example validation: Dancer=689 points, Comet=312 points
✓ Final simulation: Winner has XXXX points
✓ All validation checks passed

Final Answer: XXXX
```
