# Implementation Plan - Part 2: Garbage Character Count

## Overview
Part 2 changes the objective from scoring groups to counting non-canceled characters inside garbage sections. The parsing logic remains similar to Part 1, but instead of tracking depth/score, we track garbage character count.

## Key Insight: Reuse Part 1 Logic
The Part 1 solution (`part_1_solution.py`) already handles:
- State tracking (inside/outside garbage)
- Cancellation logic (`!` skips next character)
- Proper garbage boundaries (`<` and `>`)

We can **directly adapt** the Part 1 solution by changing what we track.

## Implementation Steps

### Step 1: Adapt the Core Function
**File:** `solution.py`

**Changes from Part 1:**
- Remove: `depth` and `total_score` variables
- Add: `garbage_count` variable initialized to 0
- Remove: Group tracking logic (lines 37-47 in Part 1)
- Modify: Inside garbage section to count characters

**New Logic:**
```python
def count_garbage_characters(stream: str) -> int:
    in_garbage = False
    garbage_count = 0
    i = 0

    while i < len(stream):
        char = stream[i]

        # Handle cancellation (only inside garbage)
        if in_garbage and char == '!':
            i += 2  # Skip both ! and next character (don't count either)
            continue

        # Handle garbage start (don't count the <)
        if not in_garbage and char == '<':
            in_garbage = True
            i += 1
            continue

        # Handle garbage end (don't count the >)
        if in_garbage and char == '>':
            in_garbage = False
            i += 1
            continue

        # Count all other characters inside garbage
        if in_garbage:
            garbage_count += 1

        i += 1

    return garbage_count
```

### Step 2: Reuse Input Reading Function
**Action:** Copy the `read_input()` function directly from Part 1 - no changes needed.

### Step 3: Create Test Suite
**Action:** Implement the test suite as specified in `test_plan.md`, including:
- Basic garbage tests (empty, simple content, special characters)
- Cancellation tests (various patterns)
- Multiple garbage sections
- Edge cases (no garbage, empty input, consecutive empty garbage)

### Step 4: Main Execution Flow
**Action:** Create main block that:
1. Runs tests first
2. If tests pass, read input from `input.md`
3. Calculate garbage count
4. Print result

## Algorithm Analysis

### Time Complexity: O(n)
- Single pass through the stream
- Each character processed once (or skipped once for cancellation)
- No nested loops or recursive calls

### Space Complexity: O(1)
- Only a few variables: `in_garbage`, `garbage_count`, `i`
- No data structures that grow with input size
- Input string is already in memory (unavoidable)

### Efficiency for Large Inputs
The algorithm is **optimal** for this problem:
- Must read every character at least once → O(n) is lower bound
- Our solution is O(n) → matches lower bound
- No optimization opportunities exist

**Expected Performance:**
- Input size: ~10,000 characters (typical Advent of Code)
- Processing time: < 1ms (Python can process millions of characters per second)
- Memory: Negligible (few integer variables)

## File Structure
```
solution.py          # Main solution file
├── count_garbage_characters()  # Core algorithm
├── read_input()                # Input file reader
├── run_tests()                 # Test suite
└── __main__                    # Execution entry point
```

## Differences from Part 1
| Aspect | Part 1 | Part 2 |
|--------|--------|--------|
| **Goal** | Score groups by depth | Count garbage characters |
| **Track** | `depth`, `total_score` | `garbage_count` |
| **Group logic** | Essential | Ignored |
| **Garbage logic** | Skip entirely | Count characters |
| **Complexity** | O(n) time, O(1) space | O(n) time, O(1) space |

## Edge Cases Handled
1. **Empty garbage** `<>` → 0 characters
2. **Nested-looking garbage** `<<<<>` → Each `<` inside counts
3. **Cancellation chains** `<!!>`, `<!!!>>` → Proper skip logic
4. **Mixed content** `<{o"i!a,<{i<a>` → All non-canceled chars count
5. **Empty input** → 0 characters
6. **No garbage** `{{{}}}` → 0 characters
7. **Consecutive empty garbage** `<><>` → 0 characters
8. **Cancellation outside garbage** → Assumption: Input is well-formed; `!` only appears inside garbage
9. **Stream ending with `!` inside garbage** → Assumption: Won't occur in valid input (input is well-formed)

## Dependencies
- Python 3.x (any version with f-strings)
- No external libraries required
- Only standard library: `open()` for file I/O

## Input Assumptions
- **Well-formed input**: All garbage sections are properly closed (every `<` has a matching `>`)
- **Cancellation placement**: The `!` character only appears inside garbage sections
- **Whitespace handling**: The `read_input()` function strips trailing whitespace from the input file

## Expected Runtime
< 10ms for typical Advent of Code input size
