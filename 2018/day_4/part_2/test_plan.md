# Test Plan - Part 2: Guard Sleep Pattern Analysis

## Testing Objectives
1. Verify the solution correctly identifies the (guard, minute) pair with highest frequency
2. Ensure the algorithm handles the provided input correctly
3. Validate edge cases specific to Strategy 2
4. Confirm the solution differs from Part 1 results (different strategies should yield different answers)

## Test 1: Manual Example from Problem Statement

### Test Data
Use the example mentioned in the problem:
- Guard #10 was asleep at minute 24 twice
- Guard #99 was asleep at minute 45 **three times**
- Expected answer: 99 × 45 = 4455

Create a test file `test_example.txt` with the following content:
```
[1518-11-01 00:00] Guard #10 begins shift
[1518-11-01 00:05] falls asleep
[1518-11-01 00:25] wakes up
[1518-11-01 00:30] falls asleep
[1518-11-01 00:55] wakes up
[1518-11-02 00:40] falls asleep
[1518-11-02 00:50] wakes up
[1518-11-03 00:00] Guard #10 begins shift
[1518-11-03 00:24] falls asleep
[1518-11-03 00:29] wakes up
[1518-11-04 00:00] Guard #10 begins shift
[1518-11-04 00:36] falls asleep
[1518-11-04 00:46] wakes up
[1518-11-05 00:00] Guard #99 begins shift
[1518-11-05 00:45] falls asleep
[1518-11-05 00:55] wakes up
[1518-11-06 00:00] Guard #99 begins shift
[1518-11-06 00:40] falls asleep
[1518-11-06 00:50] wakes up
[1518-11-07 00:00] Guard #99 begins shift
[1518-11-07 00:45] falls asleep
[1518-11-07 00:57] wakes up
[1518-11-08 00:00] Guard #99 begins shift
[1518-11-08 00:44] falls asleep
[1518-11-08 00:48] wakes up
```

In this data:
- Guard #10: sleeps at minute 24 on days 3 and 4 (frequency = 2)
- Guard #99: sleeps at minute 45 on days 5, 7, and 8 (frequency = 3)

### Test Steps
1. Save the above data to `test_example.txt`
2. Run: `python solution.py test_example.txt` (or modify to accept filename parameter)
3. Verify output matches: Guard #99, minute 45, answer 4455

### Expected Result
```
Guard #99 was asleep most frequently at minute 45
Frequency: asleep 3 times at this minute
Answer: 99 × 45 = 4455
```

### Why This Test Matters
This validates the core logic difference between Strategy 1 and Strategy 2. Even if Guard #10 slept more total minutes, Guard #99 has a single minute with higher frequency.

## Test 2: Full Input Validation

### Test Steps
1. Run solution on `input.md` (the actual puzzle input)
2. Capture the guard ID, minute, and final answer
3. Verify the answer is different from Part 1 answer (48680)

### Expected Behavior
- Solution should complete in under 1 second
- Answer should be a positive integer
- Answer should NOT equal 48680 (since strategies differ)
- Should identify a specific guard and minute combination

### Validation Checks
- Guard ID is a positive integer
- Minute is between 0-59 (inclusive)
- Frequency is at least 1
- Output calculation: guard_id × minute = answer

## Test 3: Edge Case - Single Guard

### Test Data
Create input with only one guard who has multiple sleep/wake cycles:
```
[1518-01-01 00:00] Guard #100 begins shift
[1518-01-01 00:10] falls asleep
[1518-01-01 00:15] wakes up
[1518-01-01 00:20] falls asleep
[1518-01-01 00:25] wakes up
[1518-01-02 00:00] Guard #100 begins shift
[1518-01-02 00:10] falls asleep
[1518-01-02 00:15] wakes up
```

### Expected Behavior
- Guard #100 sleep pattern:
  - Day 1: minutes 10-14 (5 minutes) and 20-24 (5 minutes)
  - Day 2: minutes 10-14 (5 minutes)
- Minute frequencies: minutes 10-14 each appear 2 times (day 1 + day 2)
- Minute frequencies: minutes 20-24 each appear 1 time (day 1 only)
- Should identify one of minutes 10-14 (all tied with frequency 2)
- Answer: 100 × (identified minute, likely 10) = 1000

### Why This Test Matters
Tests that the algorithm works correctly with a single guard (no comparison needed).

## Test 4: Edge Case - Tie in Frequencies

### Test Scenario
What if multiple (guard, minute) pairs have the same maximum frequency?

### Test Data
Create input where:
- Guard #50 sleeps at minute 20 exactly 5 times
- Guard #60 sleeps at minute 30 exactly 5 times

### Expected Behavior
- Algorithm should pick one consistently (whichever is encountered first in iteration)
- Answer should be valid: either (50 × 20 = 1000) or (60 × 30 = 1800)

### Validation
The problem doesn't specify tie-breaking, so any consistent behavior is acceptable. We just need to verify the solution doesn't crash and picks one of the valid options.

## Test 5: Edge Case - Guards Who Never Sleep

### Test Data
Include guards who start shifts but never have sleep/wake events:
```
[1518-01-01 00:00] Guard #200 begins shift
[1518-01-02 00:00] Guard #300 begins shift
[1518-01-02 00:10] falls asleep
[1518-01-02 00:15] wakes up
```

### Expected Behavior
- Guard #200 should have all zeros in their sleep array
- Guard #300 should have frequencies for minutes 10-14
- Algorithm should still work and identify Guard #300

### Why This Test Matters
Ensures the algorithm handles guards with zero frequencies correctly and doesn't crash on edge cases.

## Test 6: Verify Strategy Difference

### Comparison Test
Run both Part 1 and Part 2 solutions on the same input and compare:

### Test Steps
1. Run Part 1 solution → get answer A1, guard G1, minute M1
2. Run Part 2 solution → get answer A2, guard G2, minute M2
3. Compare results

### Expected Observations
- **If G1 ≠ G2**: Different guards identified (confirms different strategies)
- **If G1 = G2 but M1 ≠ M2**: Same guard, different minute (possible but less likely)
- **A1 ≠ A2**: Final answers should differ (different strategies)

### Why This Test Matters
Validates that we've implemented a genuinely different strategy, not accidentally repeated Part 1.

## Test 7: Data Integrity Validation

### Validation Checks During Execution
1. **Record count**: Verify all ~935 lines are parsed
2. **Sort verification**: Confirm records are in chronological order after sorting
3. **Guard count**: Count unique guards in the dataset (should be 10-20 guards)
4. **Frequency sanity**: Maximum frequency should be reasonable (probably 5-20 for the most common minute)

### Test Steps
Add debug output or assertions to verify:
```python
print(f"Total records parsed: {len(records)}")
print(f"Unique guards: {len(guard_sleep_minutes)}")
print(f"Maximum frequency found: {max_frequency}")
```

### Expected Ranges
- Records: ~935
- Unique guards: 10-20
- Max frequency: 5-20 (a guard sleeping at the same minute 15 times would be very consistent)

## Test 8: Algorithm Correctness - Manual Verification

### Test Steps
1. Run the solution and identify the winning (guard, minute) pair
2. Manually grep the input for that guard's records
3. Manually count how many times that guard slept at that specific minute
4. Verify the frequency matches the algorithm's output

### Detailed Manual Verification Procedure
If solution says Guard #G at minute M with frequency F:

```bash
# Step 1: Extract all records for Guard #G
grep "Guard #G" input.md > guard_records.txt
grep "falls asleep\|wakes up" input.md >> guard_records.txt
sort guard_records.txt > guard_sorted.txt

# Step 2: Parse and trace through each sleep/wake cycle
# For each "falls asleep" at minute A followed by "wakes up" at minute B:
#   - Check if M is in range [A, B) (inclusive A, exclusive B)
#   - If yes, increment counter
#
# Step 3: Verify counter equals F
```

### Manual Counting Example
If Guard #2789 sleeps at:
- [1518-04-05 00:40] falls asleep → [1518-04-05 00:50] wakes up (includes minute 42)
- [1518-04-07 00:35] falls asleep → [1518-04-07 00:45] wakes up (includes minute 42)
- [1518-04-10 00:42] falls asleep → [1518-04-10 00:55] wakes up (includes minute 42)

Then minute 42 has frequency 3 for Guard #2789.

### Why This Test Matters
Provides high confidence in correctness by manual verification of a subset.

## Test 9: Performance Validation

### Test Steps
1. Time the solution execution: `time python solution.py`
2. Verify it completes in under 1 second

### Expected Performance
- **Parsing + Sorting**: < 100ms
- **Sleep tracking**: < 50ms
- **Finding max frequency**: < 10ms
- **Total**: < 200ms

### Why This Test Matters
Confirms the O(N log N) algorithm is efficient enough for the input size.

## Test 10: Output Format Verification

### Validation Checks
Verify the output includes:
1. Guard ID clearly identified
2. Minute clearly identified
3. Frequency count clearly stated
4. Final answer calculation shown
5. Answer is a positive integer

### Expected Format
```
Guard #<ID> was asleep most frequently at minute <MINUTE>
Frequency: asleep <COUNT> times at this minute
Answer: <ID> × <MINUTE> = <RESULT>
```

## Test 11: Quick Smoke Test

### Test Data
Minimal test case to verify basic functionality:
```
[1518-01-01 00:00] Guard #1 begins shift
[1518-01-01 00:10] falls asleep
[1518-01-01 00:15] wakes up
```

### Expected Behavior
- Guard #1 sleeps at minutes 10, 11, 12, 13, 14 (each with frequency 1)
- Should return Guard #1 at minute 10 (first one encountered)
- Answer: 1 × 10 = 10

### Why This Test Matters
Quick sanity check that basic parsing and analysis works before running more complex tests.

## Critical Test Cases Summary

### Must Pass
1. ✓ Example from problem statement (Guard #99, minute 45)
2. ✓ Full input produces valid answer different from Part 1
3. ✓ Manual verification of the winning guard-minute pair

### Should Pass
4. ✓ Single guard scenario
5. ✓ Guards with zero sleep
6. ✓ Performance under 1 second

### Nice to Have
7. ✓ Tie-breaking behavior (consistent but arbitrary)
8. ✓ Data integrity checks

## Testing Sequence

### Recommended Order
1. **First**: Quick smoke test (Test 11) - verify basic functionality
2. **Second**: Run on full input to get answer
3. **Third**: Compare with Part 1 answer (48680) to confirm different strategies
4. **Fourth**: Manual verification (Test 8) of the identified guard-minute pair
5. **Fifth**: Example test case (Test 1) to verify correctness
6. **Sixth**: Performance check (Test 9)
7. **Optional**: Edge case tests (Tests 3-5) if time permits

## Success Criteria

### The solution is correct if:
1. It produces a valid answer (positive integer) for the full input
2. The answer differs from Part 1 (48680)
3. Manual verification confirms the frequency count is accurate
4. The example case (if tested) produces answer 4455
5. Execution completes in under 1 second

### Red Flags to Watch For
- Answer equals Part 1 answer (48680) → likely implemented wrong strategy
- Frequency of 1 → suspiciously low, probably wrong
- Execution takes > 1 second → algorithm issue
- Crash or exception → edge case not handled
