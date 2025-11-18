# Test Plan: Stream Processing

## Problem Context
This tests the solution for **Advent of Code 2017, Day 9, Part 1**. Full problem description in `problem.md`.

## Testing Strategy
Use a combination of unit tests with known examples from the problem statement, edge case testing, and validation with the actual input to ensure correctness.

**Note on Test Framework**: We're using a simple custom test runner rather than pytest/unittest. This is appropriate for a one-off Advent of Code script and keeps dependencies minimal.

## Test Categories

### 1. Basic Functionality Tests

#### 1.1 Single Group Tests
Test the simplest cases to verify basic scoring logic:

| Input | Expected Score | Description |
|-------|----------------|-------------|
| `{}` | 1 | Single empty group at depth 1 |
| `{{{}}}` | 6 | Three nested groups: 1+2+3 = 6 |

**Validation**: Ensure depth tracking and score accumulation work correctly.

#### 1.2 Multiple Groups at Same Level
Test comma-separated groups:

| Input | Expected Score | Description |
|-------|----------------|-------------|
| `{{},{}}` | 5 | Parent group (1) + two children (2+2) = 5 |
| `{{{},{},{{}}}}` | 16 | Complex nesting: 1+2+3+3+3+4 = 16 |

**Validation**: Ensure depth properly decrements and increments as groups close and open.

### 2. Garbage Handling Tests

#### 2.1 Basic Garbage
Test that garbage doesn't affect group counting:

| Input | Expected Score | Description |
|-------|----------------|-------------|
| `{<>}` | 1 | Group with empty garbage |
| `{<random characters>}` | 1 | Group with garbage content |
| `{<<<<>}` | 1 | Extra `<` inside garbage are ignored |
| `{<a>,<a>,<a>,<a>}` | 1 | Multiple garbage sections |

**Validation**: Verify that characters inside garbage (including `{` and `}`) don't affect scoring.

#### 2.2 Garbage with Group Characters
Test that group delimiters inside garbage are ignored:

| Input | Expected Score | Description |
|-------|----------------|-------------|
| `{<{},{},{{}}>}` | 1 | Garbage contains what looks like groups |
| `{{<a>},{<a>},{<a>},{<a>}}` | 9 | 1+2+2+2+2 = 9 |

**Validation**: Ensure `{` and `}` inside garbage don't affect depth tracking.

### 3. Cancellation Tests

#### 3.1 Basic Cancellation
Test that `!` properly cancels the next character:

| Input | Expected Score | Description |
|-------|----------------|-------------|
| `{<{!>}>}` | 1 | First `>` is canceled, garbage ends at second `>` |
| `{<!!>}` | 1 | Second `!` is canceled, `>` ends garbage |
| `{<!!!>>}` | 1 | Second `!` canceled, first `>` canceled, second `>` ends |

**Validation**: Verify cancellation properly skips the next character.

#### 3.2 Complex Cancellation
Test multiple and nested cancellations:

| Input | Expected Score | Description |
|-------|----------------|-------------|
| `{<{o"i!a,<{i<a>}` | 1 | Garbage ends at the `>` |
| `{{<!>},{<!>},{<!>},{<a>}}` | 3 | Cancellations prevent `>` from closing: 1+2 = 3 |
| `{{<!!>},{<!!>},{<!!>},{<!!>}}` | 9 | Each `!!` cancels second `!`: 1+2+2+2+2 = 9 |
| `{{<a!>},{<a!>},{<a!>},{<ab>}}` | 3 | Multiple canceled `>`: 1+2 = 3 |

**Detailed trace for** `{<{o"i!a,<{i<a>}`:
```
{ - open group (depth=1, score=1)
< - start garbage
{o"i!a,<{i<a - all garbage content (including the ! which cancels next char 'a')
> - end garbage
} - close group (depth=0)
Final score: 1
```

**Validation**: Ensure complex cancellation scenarios are handled correctly.

### 4. Edge Cases

#### 4.1 Empty and Minimal Inputs
| Input | Expected Score | Description |
|-------|----------------|-------------|
| `` | 0 | Empty string |
| `<>` | 0 | Only garbage, no groups |
| `<random>` | 0 | Only garbage with content |

**Validation**: Handle cases with no groups gracefully.

#### 4.2 Deep Nesting
Test with deeply nested groups to ensure no stack overflow or incorrect depth tracking:

```python
# Generate test: 10 levels deep
input_str = '{' * 10 + '}' * 10
expected = sum(range(1, 11))  # 1+2+3+...+10 = 55
```

**Validation**: Ensure arbitrary nesting depth works correctly.

#### 4.3 Long Garbage Sequences
Test that long garbage doesn't cause issues:

```python
input_str = '{<' + 'a' * 10000 + '>}'
expected = 1
```

**Validation**: Ensure performance with large garbage sections.

#### 4.4 Many Groups
Test with many sequential groups:

```python
input_str = '{}' * 1000
expected = 1000
```

**Validation**: Ensure correct handling of many groups at depth 1.

### 5. Validation Tests

#### 5.1 All Provided Examples
Run all examples from the problem statement:

```python
test_cases = [
    ('{}', 1),
    ('{{{}}}', 6),
    ('{{},{}}', 5),
    ('{{{},{},{{}}}}', 16),
    ('{<a>,<a>,<a>,<a>}', 1),
    ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9),
    ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9),
    ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3),
]
```

**Validation**: All examples must pass with exact expected scores.

#### 5.2 Actual Input
Test with the provided input file to get the final answer:

```python
with open('input.md', 'r') as f:
    actual_input = f.read().strip()
result = calculate_stream_score(actual_input)
print(f"Final answer: {result}")
```

**Purpose**: This test is for **getting the final answer** to submit to Advent of Code, not for validation (we don't know the expected value).

**Validation**:
- Result should be a positive integer
- No runtime errors or exceptions
- Execution completes successfully

### 6. State Transition Tests

#### 6.1 Verify State Correctness
Test that internal state is correct after processing:

```python
# After processing, we should be:
# - Not in garbage (in_garbage = False)
# - At depth 0 (depth = 0)
# - All groups properly closed
```

**Test approach**: Modify the function temporarily to return state for validation, or add assertions within the function during testing:

```python
def calculate_stream_score_with_state(stream: str) -> tuple[int, bool, int]:
    """Version that returns (score, in_garbage, depth) for testing."""
    # ... implementation ...
    return total_score, in_garbage, depth

# In tests:
score, in_garbage, depth = calculate_stream_score_with_state('{{},{}}')
assert score == 5
assert in_garbage == False
assert depth == 0
```

For the simple script version, this validation is optional - if all test cases pass, the state is implicitly correct.

### 7. Manual Verification Strategy

#### 7.1 Small Examples - Manual Calculation
For small test cases, manually trace through the algorithm:
1. Write out each character
2. Track state at each step (depth, in_garbage, score)
3. Verify final score matches expected

Example trace for `{{},{}}`:
```
Char | In Garbage | Depth | Score | Action
-----|------------|-------|-------|--------
{    | False      | 1     | 1     | Open group, add 1
{    | False      | 2     | 3     | Open group, add 2
}    | False      | 1     | 3     | Close group
,    | False      | 1     | 3     | Separator, ignore
{    | False      | 2     | 5     | Open group, add 2
}    | False      | 1     | 5     | Close group
}    | False      | 0     | 5     | Close group
```

#### 7.2 Debugging Failed Tests
If any test fails:
1. Add debug print statements showing character-by-character processing
2. Compare actual vs expected state at each step
3. Identify the first point where they diverge
4. Fix the logic error

### 8. Performance Validation

#### 8.1 Basic Performance Check
For this Advent of Code problem, strict performance testing is not critical. A simple check is sufficient:

```python
import time

# Test with actual input
start = time.time()
result = calculate_stream_score(actual_input)
elapsed = time.time() - start

print(f"Processed in {elapsed:.4f} seconds")
# Should be very fast (< 0.1s), but no hard assertion needed
```

**Note**: Given the input size (~20KB) and O(n) algorithm, performance will not be an issue. This check is just to confirm reasonable execution time.

#### 8.2 Memory Usage
Basic expectation (no formal testing needed):
- Should not create any new strings or lists
- Only use primitive variables (int, bool)
- No memory profiling required for this simple script

### 9. Test Implementation Approach

```python
def run_tests():
    """Run all test cases and report results."""

    # Test suite
    test_cases = [
        # Basic tests
        ('{}', 1, 'single group'),
        ('{{{}}}', 6, 'nested groups'),
        ('{{},{}}', 5, 'sibling groups'),
        ('{{{},{},{{}}}}', 16, 'complex nesting'),

        # Garbage tests
        ('{<a>,<a>,<a>,<a>}', 1, 'multiple garbage'),
        ('{{<ab>},{<ab>},{<ab>},{<ab>}}', 9, 'garbage in nested groups'),
        ('{<{},{},{{}}>}', 1, 'garbage with group chars'),

        # Cancellation tests
        ('{<{!>}>}', 1, 'canceled >'),
        ('{<!!>}', 1, 'canceled !'),
        ('{<!!!>>}', 1, 'double canceled'),
        ('{{<!!>},{<!!>},{<!!>},{<!!>}}', 9, 'multiple !!'),
        ('{{<a!>},{<a!>},{<a!>},{<ab>}}', 3, 'multiple canceled >'),

        # Edge cases
        ('', 0, 'empty string'),
        ('<>', 0, 'only garbage'),
    ]

    passed = 0
    failed = 0

    for input_str, expected, description in test_cases:
        result = calculate_stream_score(input_str)
        if result == expected:
            print(f"PASS - {description}: {result}")
            passed += 1
        else:
            print(f"FAIL - {description}: expected {expected}, got {result}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")

    return failed == 0
```

### 10. Acceptance Criteria

The solution is considered correct if:
1. All provided examples pass with exact expected scores
2. Edge cases (empty, only garbage, deep nesting) work correctly
3. Cancellation logic works for all test cases
4. Actual input produces a valid integer result
5. Execution completes successfully without errors
6. No runtime errors or exceptions
7. Result can be submitted to Advent of Code

## Test Execution Order

1. **Run basic functionality tests first** - Ensure core logic works
2. **Run garbage tests** - Verify garbage handling
3. **Run cancellation tests** - Verify cancellation logic
4. **Run edge cases** - Verify robustness
5. **Run performance test** - Verify efficiency
6. **Run actual input** - Get final answer

If any test fails, debug before proceeding to the next category.
