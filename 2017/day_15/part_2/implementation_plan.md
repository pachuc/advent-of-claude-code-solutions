# Implementation Plan: Dueling Generators Part 2

## Overview
Part 2 builds directly on Part 1 by adding filtering logic to the generators. The core algorithm remains the same, but now each generator must skip values that don't meet specific criteria before presenting them to the judge.

## Key Differences from Part 1
- Generator A now only yields values where `value % 4 == 0`
- Generator B now only yields values where `value % 8 == 0`
- Number of comparisons reduced from 40 million to 5 million
- Generators operate independently (one may generate many internal values before finding a valid one)
- Part 1 found 592 matches in 40M pairs; Part 2's result is not directly comparable due to different filtering and pair count

## Algorithm Analysis

### Time Complexity
- Each generator produces values in O(1) time per value
- On average, Generator A will keep 1/4 of its values (multiples of 4)
- On average, Generator B will keep 1/8 of its values (multiples of 8)
- Expected internal iterations for 5M pairs: ~20M for A, ~40M for B
- Overall: O(n) where n = 5 million pairs
- Estimated runtime: 5-15 seconds on typical hardware (based on similar computational complexity to Part 1)

### Space Complexity
- O(1) - we only store current values and counters, no arrays needed

## Step-by-Step Implementation Plan

### Step 1: Reuse Part 1 Infrastructure
**Files to reference:** `part_1_solution.py`

**Actions:**
1. Copy the entire Part 1 solution as a starting point to minimize errors
2. Reuse the `parse_input()` function unchanged - it works identically
3. Keep the same constants (FACTOR_A, FACTOR_B, MODULO, MASK_16_BIT)
4. Reuse the main structure

**Rationale:** The input parsing and basic setup are identical to Part 1. Starting from a working solution reduces risk of introducing bugs.

### Step 2: Modify the Generator Function
**Current approach (Part 1):**
```python
def generate_values(start, factor, modulo):
    current = start
    while True:
        current = (current * factor) % modulo
        yield current
```

**New approach (Part 2) - Replace the existing function:**
```python
def generate_values_filtered(start, factor, modulo, filter_divisor):
    current = start
    while True:
        current = (current * factor) % modulo
        if current % filter_divisor == 0:
            yield current
```

**Decision:** Replace the Part 1 `generate_values()` function entirely with `generate_values_filtered()`. Part 2 doesn't need the unfiltered version.

**Changes:**
- Add a `filter_divisor` parameter (4 for A, 8 for B)
- Add filtering logic: only yield values that are divisible by `filter_divisor`
- Internal loop continues until a valid value is found
- Generator is still infinite, but yields less frequently

**Key considerations:**
- The generator continues to produce ALL internal values in sequence
- It only YIELDS values that pass the filter
- This ensures both generators maintain their correct internal state

**CRITICAL: Common Pitfall to Avoid**
Do NOT check the filter before generation:
```python
# WRONG - this breaks the sequence!
def generate_values_filtered_WRONG(start, factor, modulo, filter_divisor):
    current = start
    while True:
        if current % filter_divisor == 0:  # ❌ Checking BEFORE generation
            yield current
        current = (current * factor) % modulo
```

Always generate FIRST, then check the filter. The filter applies to the newly generated value, not the starting/previous value.

### Step 3: Update the Count Matches Function
**Modifications needed:**
1. Change default `pairs` parameter from 40,000,000 to 5,000,000
2. Create two filtered generators:
   - `gen_a = generate_values_filtered(start_a, FACTOR_A, MODULO, 4)`
   - `gen_b = generate_values_filtered(start_b, FACTOR_B, MODULO, 8)`
3. Keep the comparison logic identical (use `next()` and compare lowest 16 bits)

**Why this works:**
- The filtered generators handle all the skipping internally
- The main loop can remain simple: just call `next()` on each generator
- Each `next()` call automatically gets the next VALID value from that generator

### Step 4: Update Main Function
**Changes:**
- Update the `count_matches()` call to use 5,000,000 pairs instead of 40,000,000
- Everything else remains the same

### Step 5: Code Organization
**Final structure:**
```
1. parse_input() - unchanged from Part 1
2. generate_values_filtered() - new function with filtering
3. count_matches() - modified to use filtered generators and 5M pairs
4. main() - updated to call count_matches with correct pair count
```

**Alternative approach (optional optimization):**
- Could keep the old `generate_values()` and create a wrapper, but the modified version is clearer

## Implementation Details

### Constants
For consistency with Part 1 style, define constants inside the `count_matches()` function:
```python
def count_matches(start_a, start_b, pairs=5_000_000):
    FACTOR_A = 16807
    FACTOR_B = 48271
    MODULO = 2147483647
    MASK_16_BIT = 0xFFFF
    FILTER_A = 4  # Generator A keeps multiples of 4
    FILTER_B = 8  # Generator B keeps multiples of 8
    # ... rest of function
```

**Rationale:** This matches Part 1's coding style where constants are defined within the function scope.

### Expected Input
- File: `input.txt`
- Format: Two lines with starting values for A and B
- Values: A=277, B=349

### Expected Output
- Single integer: count of matching pairs in lowest 16 bits
- Printed to stdout (same as Part 1)
- Note: Result is not directly comparable to Part 1's 592 (different filtering and pair count make comparison meaningless)

## Performance Considerations

### Why This is Efficient
1. **Generator pattern:** Memory-efficient, only stores current state
2. **Bitwise operations:** Using `& MASK_16_BIT` is faster than modulo for extracting lowest 16 bits
3. **No unnecessary storage:** We don't store the sequence, just compare on-the-fly
4. **Early filtering:** Check divisibility immediately after generation

### Estimated Runtime
- Part 1 did 40M pairs (80M total generator calls)
- Part 2 will do ~20M internal iterations for A + ~40M for B = ~60M total generator calls
- Only 5M comparisons (fewer than Part 1)
- Expected runtime: 5-15 seconds on typical hardware (comparable to Part 1, potentially faster due to fewer comparisons)

### Potential Bottlenecks
- None significant for this input size
- The modulo operation in value generation is the main computation
- Python's native integer arithmetic handles this efficiently

## Edge Cases Handled

1. **First values might not match filter:** The generator will skip them automatically
2. **Different skip rates:** A and B skip at different rates, but this is handled by independent generators
3. **Integer overflow:** Not an issue - Python handles arbitrary precision integers, and the modulo keeps values bounded
4. **Zero values:** Won't occur since starting values are positive and modulo operation preserves positivity

## Testing Integration Points

1. **Parsing:** Verify starting values are 277 and 349
2. **Generator filtering:** Test that A only yields multiples of 4, B only multiples of 8
3. **Sequence correctness:** Verify first few filtered values match example
4. **Final count:** Should match expected answer for the given input

## Summary

This is a straightforward modification of Part 1:
- Start by copying the entire Part 1 solution
- Main change: add filtering to the generator function (with filter parameter)
- Update pair count from 40M to 5M
- All other logic remains identical
- No error handling needed (appropriate for puzzle solution)
- Output via print to stdout (same as Part 1)

The solution maintains O(1) space complexity and O(n) time complexity, making it efficient for the given input size.

## Key Reminders
1. Filter AFTER generation, not before
2. Replace the old generator function entirely
3. Use 5 million pairs, not 40 million
4. Expected runtime: 5-15 seconds
5. Don't compare result to Part 1's answer (not meaningful)
