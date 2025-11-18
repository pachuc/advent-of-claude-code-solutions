# Test Plan - Part 2: Garbage Character Count

## Testing Strategy

### Objective
Verify that the solution correctly counts non-canceled characters inside garbage sections while handling all edge cases from the problem specification.

### Test Levels
1. **Unit Tests**: Test core algorithm with example cases
2. **Integration Test**: Run against actual input file
3. **Edge Case Tests**: Verify boundary conditions

## Unit Test Cases

### 1. Basic Garbage Tests

#### Test 1.1: Empty Garbage
```
Input:  <>
Expected: 0
Reason: No characters between < and >
```

#### Test 1.2: Simple Content
```
Input:  <random characters>
Expected: 17
Reason: Count all 17 characters (including spaces)
```

#### Test 1.3: Special Characters Inside
```
Input:  <<<<>
Expected: 3
Reason: Three < characters before closing >
```

### 2. Cancellation Tests

#### Test 2.1: Cancel Closing Bracket
```
Input:  <{!>}>
Expected: 2
Reason: { counts (1), } counts (2), !> cancels the >, final > closes
```

#### Test 2.2: Cancel Exclamation
```
Input:  <!!>
Expected: 0
Reason: First ! cancels second !, then > closes garbage
```

#### Test 2.3: Double Cancellation
```
Input:  <!!!>>
Expected: 0
Reason: 1st ! cancels 2nd !, 3rd ! cancels 1st >, 2nd > closes
```

#### Test 2.4: Complex Cancellation
```
Input:  <{o"i!a,<{i<a>
Expected: 10
Reason: Count { o " i , < { i < a (the !a means ! cancels a, neither counts)
Breakdown:
  < - starts garbage (don't count)
  { - counts (1)
  o - counts (2)
  " - counts (3)
  i - counts (4)
  ! - cancels next
  a - canceled (don't count !)
  , - counts (5)
  < - counts (6)
  { - counts (7)
  i - counts (8)
  < - counts (9)
  a - counts (10)
  > - closes (don't count)
```

### 3. Multiple Garbage Sections

#### Test 3.1: Multiple Garbage with Groups
```
Input:  {<a>,<a>,<a>,<a>}
Expected: 4
Reason: Four garbage sections each with one 'a'
```

#### Test 3.2: Nested-Looking Groups in Garbage
```
Input:  {{<a>},{<a>},{<a>},{<ab>}}
Expected: 5
Reason: Four garbage sections:
  <a>  → 1 character
  <a>  → 1 character
  <a>  → 1 character
  <ab> → 2 characters
  Total: 1+1+1+2 = 5
```

### 4. Edge Cases

#### Test 4.1: No Garbage
```
Input:  {{{}}}
Expected: 0
Reason: Only groups, no garbage sections
```

#### Test 4.2: Only Garbage
```
Input:  <abcdef>
Expected: 6
Reason: Six characters in garbage
```

#### Test 4.3: Empty String
```
Input:  ""
Expected: 0
Reason: No input means no garbage
```

#### Test 4.4: Garbage at Start
```
Input:  <test>{<data>}
Expected: 8
Reason: "test" (4) + "data" (4) = 8
```

#### Test 4.5: Consecutive Cancellations
```
Input:  <!!!!!!!!>
Expected: 0
Reason: 1st ! cancels 2nd, 3rd cancels 4th, 5th cancels 6th, 7th cancels 8th, 9th closes
```

#### Test 4.6: Consecutive Empty Garbage
```
Input:  <><>
Expected: 0
Reason: Two consecutive empty garbage sections
```

## Integration Tests

### Test 5: Actual Input File

#### Test 5.1: File Reading
```
Action: Read input.md
Verify: File exists and contains data
Expected: Non-empty string
```

#### Test 5.2: Full Processing
```
Action: Run count_garbage_characters() on actual input
Verify: Returns integer result
Expected: Non-negative integer (exact value unknown, but should be consistent)
```

#### Test 5.3: Consistency
```
Action: Run solution twice on same input
Verify: Same result both times
Expected: Deterministic output
```

## Verification Strategy

### Automated Testing

The test suite should use the same approach as Part 1: collect all test results and report them together rather than halting on the first failure with assertions. This provides better visibility into which tests pass and which fail.

```python
def run_tests():
    test_cases = [
        ('<>', 0, 'empty garbage'),
        ('<random characters>', 17, 'simple content'),
        ('<<<<>', 3, 'special chars inside'),
        ('<{!>}>', 2, 'cancel closing bracket'),
        ('<!!>', 0, 'cancel exclamation'),
        ('<!!!>>', 0, 'double cancellation'),
        ('<{o"i!a,<{i<a>', 10, 'complex cancellation'),
        ('{{{}}}', 0, 'no garbage'),
        ('<abcdef>', 6, 'only garbage'),
        ('', 0, 'empty string'),
        ('<><>', 0, 'consecutive empty garbage'),
    ]

    passed = 0
    failed = 0

    for input_str, expected, description in test_cases:
        result = count_garbage_characters(input_str)
        if result == expected:
            print(f"✓ PASS - {description}: {result}")
            passed += 1
        else:
            print(f"✗ FAIL - {description}: expected {expected}, got {result}")
            failed += 1

    return failed == 0
```

### Manual Verification

#### Step 1: Trace Through Example
Pick `<{!>}>` and manually trace:
```
i=0: char='<', in_garbage=False → set in_garbage=True, i=1
i=1: char='{', in_garbage=True → garbage_count=1, i=2
i=2: char='!', in_garbage=True → skip to i=4
i=4: char='}', in_garbage=True → garbage_count=2, i=5
i=5: char='>', in_garbage=True → set in_garbage=False, i=6
Result: garbage_count=2 ✓
```

#### Step 2: Compare with Part 1
```
Action: Run both Part 1 and Part 2 on input
Verify: Part 1 gives 23588 (groups score)
Verify: Part 2 gives different number (garbage count)
Expected: Both should complete without errors
```

## Test Execution Order

1. **Run unit tests first** - Fast, catches algorithmic errors
2. **If all pass**: Run integration test on actual input
3. **If any fail**: Debug specific test case before proceeding

## Success Criteria

### All Tests Must Pass
- ✓ All 10 unit tests return expected values
- ✓ File reading works correctly
- ✓ Solution runs in < 100ms
- ✓ Result is a positive integer

### Expected Behavior
- No crashes or exceptions
- Deterministic output (same input → same output)
- Handles all cancellation patterns correctly
- Correctly identifies garbage boundaries

## Common Pitfalls to Avoid

### Pitfall 1: Counting Delimiters
❌ **Wrong**: Counting `<` or `>` in garbage_count
✓ **Correct**: Only count characters between them

### Pitfall 2: Incorrect Cancellation
❌ **Wrong**: Only skipping one character after `!`
✓ **Correct**: Skip both `!` and the next character

### Pitfall 3: Nested Garbage
❌ **Wrong**: Treating `<` inside garbage as starting new garbage
✓ **Correct**: Inside garbage, `<` is just another character to count

### Pitfall 4: Off-by-One in Index
❌ **Wrong**: `i += 1` after `i += 2` for cancellation
✓ **Correct**: `continue` after `i += 2` to skip the loop increment

## Performance Testing

### Test 6: Large Input Performance

This test validates the O(n) time complexity claim from the implementation plan:

```python
# Generate large test input
large_input = '<' + 'a' * 100000 + '>'
start_time = time.time()
result = count_garbage_characters(large_input)
elapsed = time.time() - start_time

assert result == 100000
assert elapsed < 0.1  # Should be much faster than 100ms
print(f"Performance test: processed {len(large_input)} chars in {elapsed:.4f}s")
```

This should be part of the standard test suite to verify performance characteristics.

## Debug Output

For debugging failing tests, implement verbose mode from the start:

```python
def count_garbage_characters(stream: str, verbose=False) -> int:
    # ... existing code ...
    if verbose:
        print(f"i={i}, char={char!r}, in_garbage={in_garbage}, count={garbage_count}")
```

This helps trace through complex cases like `<{o"i!a,<{i<a>`. Use it when debugging any failing test cases.

## Final Validation

Before submitting:
1. ✓ All example tests pass
2. ✓ Solution runs on actual input without errors
3. ✓ Result is reasonable (positive integer, likely 5,000-15,000)
4. ✓ Code is clean and follows same structure as Part 1
