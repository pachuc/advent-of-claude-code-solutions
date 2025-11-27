# Test Plan: Guard Sleep Pattern Analysis

## Testing Strategy
This test plan focuses on verifying correctness of the solution through:
1. Example data validation (known answer)
2. Unit tests for individual components
3. Integration test with the provided input
4. Edge case validation
5. Manual verification of intermediate results

## Test 0: Example Data Validation
**Objective**: Verify solution produces correct answer on provided example
**Priority**: CRITICAL - Must pass before proceeding to actual input

**Example Scenario** (from problem description):
```
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-01 23:58] Guard #99 begins shift
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:05] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:02] Guard #99 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:03] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
```

**Expected Results**:
- Guard #10: 50 total minutes asleep (20 + 25 + 5)
- Guard #99: 30 total minutes asleep (10 + 10 + 10)
- Sleepiest guard: #10
- Most frequent minute for Guard #10: minute 24 (asleep 2 times)
- **Expected Answer: 10 × 24 = 240**

**Test Steps**:
1. Create test file with example data (may need to be sorted first)
2. Run solution on example data
3. Verify sleepiest guard is #10
4. Verify best minute is 24
5. Verify answer is 240

**Pass Criteria**: Answer must equal 240

## Test 1: Input Parsing
**Objective**: Verify records are correctly parsed from input file

**Test Steps**:
1. Read input.md
2. Parse all records
3. Verify record count matches expected (~900+ records)
4. Spot check several parsed records

**Validation**:
- Check first record is parsed correctly
- Check last record is parsed correctly
- Verify timestamp format is correct
- Verify event text is extracted properly

**Sample Checks**:
```
Input: "[1518-07-04 00:01] falls asleep"
Expected: (datetime(1518, 7, 4, 0, 1), "falls asleep")

Input: "[1518-06-07 00:03] Guard #2789 begins shift"
Expected: (datetime(1518, 6, 7, 0, 3), "Guard #2789 begins shift")
```

**Pass Criteria**: All records parsed without errors

## Test 2: Record Sorting
**Objective**: Verify chronological sorting works correctly

**Test Steps**:
1. Take parsed records
2. Sort by timestamp
3. Verify order is chronological

**Validation**:
- First record should be earliest timestamp (1518-03-31)
- Last record should be latest timestamp (1518-11-22 or similar)
- Iterate through sorted list and verify each timestamp >= previous

**Edge Cases**:
- Multiple events at same minute (should maintain relative order or be handled correctly)
- Events spanning midnight hour
- Guards starting shifts before midnight (23:XX timestamps)

**Pass Criteria**: Records are in strictly non-decreasing chronological order

## Test 3: Event Type Recognition
**Objective**: Verify all three event types are correctly identified

**Test Cases**:
1. "Guard #2789 begins shift" → Extract guard ID: 2789
2. "Guard #101 begins shift" → Extract guard ID: 101
3. "falls asleep" → Recognize as sleep event
4. "wakes up" → Recognize as wake event

**Validation**:
- Guard ID extraction regex captures all guard IDs correctly
- Different guard ID formats work (1-4 digit IDs)
- Sleep and wake events don't extract guard IDs (use current guard)

**Pass Criteria**: All event types correctly identified across input

## Test 4: Sleep Tracking State Machine
**Objective**: Verify state transitions work correctly

**Test Scenario**:
```
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
```

**Expected State Transitions**:
1. Guard #10 starts shift → current_guard = 10, sleep_start = None
2. Falls asleep at minute 5 → sleep_start = 5
3. Wakes at minute 25 → Mark minutes [5, 25) as asleep, sleep_start = None
4. Falls asleep at minute 30 → sleep_start = 30
5. Wakes at minute 55 → Mark minutes [30, 55) as asleep, sleep_start = None

**Expected Sleep Minutes**: Guard #10 asleep for: (25-5) + (55-30) = 20 + 25 = 45 minutes
**Affected Minutes**: 5-24 (count=1 each), 30-54 (count=1 each)

**Validation Method**:
- Create unit test with assertions:
  - `assert guard_sleep_minutes[10][5] == 1`
  - `assert guard_sleep_minutes[10][24] == 1`
  - `assert guard_sleep_minutes[10][25] == 0`  # Not asleep at wake minute
  - `assert guard_sleep_minutes[10][30] == 1`
  - `assert guard_sleep_minutes[10][54] == 1`
  - `assert sum(guard_sleep_minutes[10]) == 45`

**Pass Criteria**: All assertions pass, sleep tracking accurately captures all sleep periods

## Test 5: Sleep Range Boundaries
**Objective**: Verify inclusive/exclusive boundaries are correct

**Critical Test**:
```
Falls asleep: minute 23
Wakes up: minute 27
```

**Expected**:
- Minute 23: asleep ✓ (inclusive start)
- Minute 24: asleep ✓
- Minute 25: asleep ✓
- Minute 26: asleep ✓
- Minute 27: awake ✓ (exclusive end)

**Pass Criteria**:
- 4 minutes marked (23, 24, 25, 26)
- Minute 27 NOT marked as asleep

## Test 6: Multiple Sleep Sessions Per Guard
**Objective**: Verify frequency counting across multiple days

**Test Scenario**:
```
Day 1: Guard #10 asleep minutes 10-15, 20-25
Day 2: Guard #10 asleep minutes 12-18, 24-30
```

**Expected Frequencies** (for Guard #10):
- Minute 10: 1
- Minute 11: 1
- Minute 12: 2 (both days)
- Minute 13: 2 (both days)
- Minute 14: 2 (both days)
- Minute 15: 1
- Minute 20: 1
- Minute 24: 2 (both days)
- Minute 25: 1
- Others: 0

**Validation Method**:
- Unit test with specific assertions:
  - `assert guard_sleep_minutes[10][12] == 2`
  - `assert guard_sleep_minutes[10][13] == 2`
  - `assert guard_sleep_minutes[10][14] == 2`
  - `assert guard_sleep_minutes[10][24] == 2`
  - `assert guard_sleep_minutes[10][0] == 0`

**Pass Criteria**: All assertions pass, frequency counts accumulate correctly across multiple shifts

## Test 7: Total Sleep Calculation
**Objective**: Verify total sleep minutes are summed correctly

**Method**:
1. For each guard, sum all 60 minutes in their sleep array
2. Verify totals make sense
3. Cross-check: total should equal sum of all sleep ranges

**Validation**:
- If guard sleeps minutes [5, 10) and [20, 25), total = 5 + 5 = 10
- If a minute has count=3, it contributes 3 to total
- Total sleep minutes should be reasonable (not negative, not > 60 × number of shifts)

**Pass Criteria**: Total sleep calculation matches expected sum

## Test 8: Finding Sleepiest Guard
**Objective**: Verify correct guard is identified

**Test Method**:
1. Calculate total sleep for all guards
2. Identify guard with maximum total
3. Print top 5 sleepiest guards for manual verification

**Validation**:
- Manually check calculation for top 2-3 guards
- Verify the selected guard truly has the highest total
- Handle ties appropriately (take first if any)

**Expected Output Format**:
```
Guard #XXXX: YYY total minutes
Guard #XXXX: YYY total minutes
...
Sleepiest Guard: #XXXX
```

**Pass Criteria**: Correct guard identified with correct total

## Test 9: Finding Best Minute
**Objective**: Verify most frequent sleep minute is found

**Test Method**:
1. For the sleepiest guard, examine their 60-minute frequency array
2. Find minute with highest frequency
3. Print top 5 minutes for manual verification

**Validation**:
- Manually verify the selected minute has highest frequency
- Check surrounding minutes to ensure max is correct
- Handle ties (take lowest minute number if tied)

**Expected Output Format**:
```
Guard #XXXX sleep frequency by minute:
  Minute 24: 10 times
  Minute 25: 8 times
  Minute 12: 7 times
  ...
Best minute: 24
```

**Pass Criteria**: Correct minute identified with correct frequency

## Test 10: Complete Solution Integration
**Objective**: Verify end-to-end solution produces correct answer on actual input

**Test Steps**:
1. Run complete solution on provided input.md
2. Calculate answer: Guard ID × Minute
3. Verify answer is reasonable
4. Submit answer to Advent of Code to verify correctness

**Validation Checks**:
- Answer is a positive integer
- Guard ID exists in the input data
- Minute is in range [0, 59]
- Print intermediate values for traceability:
  - Sleepiest guard ID
  - Their total sleep minutes
  - The best minute
  - The frequency at that minute
  - Final answer

**Expected Output Format**:
```
Sleepiest Guard: #XXXX (YYY total minutes asleep)
Most frequent sleep minute: ZZ (asleep AA times at this minute)
Answer: XXXX × ZZ = NNNNNN
```

**Final Verification**:
- If Advent of Code expected answer is known, compare against it
- Otherwise, submit answer to Advent of Code portal and verify it's accepted
- Document the correct answer for future reference

**Pass Criteria**:
- Solution completes successfully with valid answer
- Answer is accepted by Advent of Code (or matches known correct answer)

## Test 11: Data Integrity Checks
**Objective**: Verify data follows expected state machine rules
**Priority**: HIGH - Should run early to catch data issues

**Checks to Perform**:
1. No sleep event without prior guard shift start
2. No wake event without prior sleep event
3. No double sleep (sleep, sleep without wake)
4. No double wake (wake, wake without sleep)
5. All minutes in range [0, 59]

**Implementation**:
- Add assertions during state tracking
- `assert current_guard is not None` before processing sleep/wake
- `assert sleep_start is not None` before processing wake
- `assert sleep_start is None` before processing sleep

**Expected for Valid Input**: Clean execution with no assertion failures

**Pass Criteria**: All state transitions are valid, no data integrity violations

## Test 12: Edge Cases

### Edge Case 12.1: Guard Never Sleeps
**Scenario**: A guard appears in shifts but never has sleep/wake events

**Expected**:
- Guard entry in data structure with all zeros
- Total sleep = 0
- Not selected as sleepiest guard (unless all guards have 0)

### Edge Case 12.2: Shift Starting Before Midnight
**Scenario**: `[1518-07-12 23:56] Guard #613 begins shift`

**Expected**:
- Guard is on duty for any sleep/wake events after this timestamp
- Events after midnight on next day belong to this guard
- Correctly tracks that guard started shift on previous calendar day

### Edge Case 12.3: Very Short Sleep Period
**Scenario**: Falls asleep minute 15, wakes minute 16

**Expected**:
- Only minute 15 is marked (1 minute of sleep)
- Minute 16 is NOT marked
- Total = 1 minute

### Edge Case 12.4: Sleep Until End of Hour
**Scenario**: Falls asleep minute 45, wakes minute 59

**Expected**:
- Minutes 45-58 marked (14 minutes total)
- Minute 59 NOT marked
- No overflow issues

### Edge Case 12.5: Tie in Total Sleep
**Scenario**: Two guards have same total sleep minutes

**Expected**:
- Take first encountered or guard with lower ID (define consistent behavior)
- Document tie-breaking rule

### Edge Case 12.6: Tie in Best Minute
**Scenario**: Guard has same frequency for multiple minutes

**Test Case**:
```
Guard #10 sleep pattern:
- Minutes 20-22: count = 3 each
- Minutes 45-47: count = 3 each
```

**Expected**:
- Take lowest minute number (minute 20, first occurrence)
- Consistent with Python's `max(range(60), ...)` behavior

**Validation**:
- `assert best_minute == 20`
- Document that tie-breaking favors lower minute numbers

### Edge Case 12.7: Tie-Breaking Test for Guards
**Scenario**: Two guards with identical total sleep

**Test Case**:
```
Guard #10: 45 total minutes
Guard #20: 45 total minutes
```

**Expected**:
- Deterministic behavior (first in iteration order)
- Document which guard is selected

**Validation**: Verify consistent tie-breaking behavior

**Pass Criteria**: All edge cases handled gracefully and deterministically

## Test 13: Negative Test Cases
**Objective**: Verify graceful handling of invalid/malformed input

**Test Cases**:

### 13.1: Empty Input File
**Scenario**: input.md is empty or contains only whitespace
**Expected**: Handle gracefully (empty result or appropriate error)

### 13.2: Malformed Timestamp
**Scenario**: Line with invalid timestamp format
**Expected**: Skip line with warning (if implemented) or ignore

### 13.3: Missing Guard ID
**Scenario**: Sleep/wake event before any guard shift starts
**Expected**: Assertion failure or appropriate error (acceptable for Advent of Code)

### 13.4: Orphaned Sleep Event
**Scenario**: File ends with guard asleep (no wake event)
**Expected**: Handle gracefully (sleep never counted, or counted to end of hour)

**Note**: For Advent of Code, input is guaranteed valid, so extensive error handling is not required. These tests are optional and primarily for robustness.

**Pass Criteria**: Solution doesn't crash unexpectedly on malformed input

## Test 14: Performance Verification

**Objective**: Ensure solution runs efficiently on provided input

**Test Method**:
- Run solution and observe execution time
- Use `time python solution.py` or similar
- No formal benchmarking required for this problem size

**Expected Performance**:
- Execution time should be < 1 second for ~1000 records
- Memory usage should be reasonable (< 10 MB)
- No infinite loops or hangs

**Pass Criteria**: Solution completes quickly without resource issues (observed, not measured formally)

## Test Execution Order

**Recommended order to run tests**:
1. Test 0: Example data validation (MUST PASS FIRST)
2. Test 1: Input parsing
3. Test 2: Record sorting
4. Test 11: Data integrity checks
5. Test 3: Event type recognition
6. Test 4: Sleep tracking state machine
7. Test 5: Sleep range boundaries
8. Test 6: Multiple sleep sessions
9. Test 7: Total sleep calculation
10. Test 8: Finding sleepiest guard
11. Test 9: Finding best minute
12. Test 12: Edge cases
13. Test 13: Negative cases (optional)
14. Test 14: Performance verification
15. Test 10: Complete solution integration (FINAL)

**Note**: Data integrity checks should run early to catch issues before complex tests fail.

## Manual Verification Checklist

**When to perform**: After all automated tests pass, before final submission

Before considering solution complete, manually verify:

- [ ] Test 0 passes with answer = 240 on example data
- [ ] Input file is read completely
- [ ] Record count matches expected (~900+)
- [ ] Records are sorted chronologically
- [ ] All guard IDs are extracted correctly
- [ ] Sleep/wake pairs are matched correctly
- [ ] Sleep minute ranges are correct (inclusive start, exclusive end)
- [ ] Frequency counts accumulate across multiple days
- [ ] Total sleep calculations are accurate
- [ ] Sleepiest guard identification is correct
- [ ] Best minute identification is correct
- [ ] Final answer calculation is correct
- [ ] Answer is printed clearly

## Debugging Output Recommendations

Include optional verbose output showing:
1. Number of records parsed
2. Date range of records (first to last)
3. Number of unique guards
4. Top 5 sleepiest guards with totals
5. For sleepiest guard: sleep pattern visualization (which minutes they're typically asleep)
6. Step-by-step calculation of final answer

## Success Criteria

The solution is considered correct if:
1. **Test 0 passes**: Example data produces answer = 240 (CRITICAL)
2. All unit tests pass
3. All edge cases are handled appropriately
4. Data integrity checks pass (no state violations)
5. Integration test produces valid answer on actual input
6. **Answer is accepted by Advent of Code** (or matches known correct answer)
7. Manual verification confirms intermediate calculations are reasonable
8. No runtime errors or exceptions on valid input
9. Performance is acceptable (completes quickly)
10. Code is readable and maintainable

**Primary Success Indicator**: Answer accepted by Advent of Code submission system
