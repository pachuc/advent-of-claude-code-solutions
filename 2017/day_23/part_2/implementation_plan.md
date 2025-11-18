# Implementation Plan - Part 2: Coprocessor Optimization

## Problem Analysis

### What the Assembly Code Does

After analyzing the assembly code, the program implements a **composite number counter**:

1. **Initialization Phase (lines 1-8)**:
   - When `a=0` (Part 1): Sets `b=67`, `c=67`
   - When `a=1` (Part 2): Sets `b=106700`, `c=123700`

   The logic (traced step-by-step):
   - Line 1: `b = 67`
   - Line 2: `c = b = 67`
   - Line 3: `jnz a 2` → If `a != 0`, jump to line 5; else continue
   - Line 4: `jnz 1 5` → Jump to line 9 (skips transformation)
   - Line 5: `mul b 100` → `b = 67 * 100 = 6700`
   - Line 6: `sub b -100000` → `b = 6700 - (-100000) = 106700`
   - Line 7: `set c b` → `c = 106700`
   - Line 8: `sub c -17000` → `c = 106700 + 17000 = 123700`

2. **Main Algorithm (lines 9-32)**:
   - For each value of `b` from 106700 to 123700 (inclusive), stepping by 17:
     - Check if `b` is composite (non-prime)
     - Use nested loops with `d` (from 2 to `b`) and `e` (from 2 to `b`)
     - Check if `d * e == b` for any combination
     - If found, `b` is composite → increment `h`
     - Move to next value: `b += 17`

3. **What We Need to Calculate**:
   - Range: 106700 to 123700 (inclusive), step 17
   - Count: `(123700 - 106700) / 17 + 1 = 1001` numbers
   - Answer: How many of these 1001 numbers are composite?

### Why Direct Simulation Fails

The assembly code uses an extremely inefficient primality test with nested loops checking all combinations of `d` and `e`. For numbers around 100,000, this would require ~10^10 operations per number, making it computationally infeasible.

## Implementation Strategy

### Step 1: Keep It Simple
Rather than building a generic assembly optimizer, we'll solve this specific puzzle efficiently:

1. **Extract Initial Values**:
   - Hard-code the values visible from the input: `b=106700`, `c=123700`, `step=17`
   - Alternative: Simulate ONLY lines 1-8 with `a=1` to extract `b` and `c`
   - Either approach is valid since we're solving one puzzle, not building production code

2. **Implement Efficient Primality Test**:
   - Use trial division up to sqrt(n)
   - Only need to check divisibility, not find all factors
   - Function: `is_composite(n) -> bool`

3. **Count Composite Numbers**:
   - Iterate through range `[b, c]` with step 17
   - Count how many are composite
   - Return the count

### Why We DON'T Run Full Simulation
The original Part 1 `execute_program()` function will NOT work for Part 2:
- With `a=1`, the nested loops in the assembly run in O(n²) time
- For n≈100,000, this means ~10¹⁰ operations per value checked
- Checking 1001 values would take weeks/months to complete
- Instead, we optimize by understanding WHAT the code computes, not HOW it computes it

### Step 3: Algorithm Details

```python
def is_composite(n):
    """Check if n is composite (not prime)"""
    if n < 2:
        return True
    if n == 2:
        return False
    if n % 2 == 0:
        return True

    # Check odd divisors up to sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return True
        i += 2

    return False

def solve_optimized():
    """Calculate the answer directly"""
    b = 106700
    c = 123700
    step = 17

    h = 0
    current = b
    while current <= c:
        if is_composite(current):
            h += 1
        current += step

    return h
```

### Step 4: Parameter Extraction (Simple Approach)

Since this is a one-time puzzle, we have two simple options:

**Option A: Hard-code values (SIMPLEST)**
```python
b = 106700
c = 123700
step = 17
```

**Option B: Extract from assembly (SLIGHTLY MORE ROBUST)**
```python
def extract_initial_values(instructions):
    """Simulate only lines 1-8 to get b and c with a=1"""
    registers = {'a': 1, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
    # Manually simulate lines 1-8 (or run a mini-simulator)
    # ... execute lines 0-7 ...
    return registers['b'], registers['c']

# Step size is visible in line 31: "sub b -17"
step = 17
```

Both approaches are acceptable. Choose based on preference.

## Implementation Steps

### Step 1: Implement primality testing (10 minutes)
- Write `is_composite(n)` function
- Handle edge cases: 0, 1 (both composite), 2 (prime)
- Optimize with early return for even numbers
- Use trial division up to sqrt(n) for odd divisors

### Step 2: Implement optimized counting (10 minutes)
- Create `count_composites(b, c, step)` function
- Iterate through range with proper stepping
- Use `is_composite()` to count
- Ensure loop uses `current <= c` (inclusive upper bound)

### Step 3: Set up parameters (5 minutes)
- Choose approach: hard-code OR extract from assembly
- If hard-coding: `b=106700, c=123700, step=17`
- If extracting: simulate lines 1-8 with a=1

### Step 4: Main function (5 minutes)
- Call `count_composites(b, c, step)`
- Output result
- Keep it simple - no need for complex input parsing if hard-coding

### Step 5: Validation (10 minutes)
- Test primality function on known values
- Verify range produces exactly 1001 values
- Optional: Test with a=0 case (should give h=0 due to immediate loop exit)
- Cross-check answer using sympy or online prime checker

## Time Complexity Analysis

- **Assembly simulation**: O(n^2) per number, where n ≈ 100,000
  - Total: O(1001 * 10^10) = O(10^13) operations → **INFEASIBLE**

- **Optimized solution**: O(sqrt(n)) per number
  - Total: O(1001 * sqrt(106700)) ≈ O(1001 * 327) ≈ O(327,000) operations → **FEASIBLE**

- **Expected runtime**: < 1 second

## File Structure

```
solution.py
├─ is_composite(n)           # Core: efficient primality test
├─ count_composites(b,c,s)   # Core: optimized counting
└─ main()                    # Simple: call count_composites and output
```

Note: We don't need the Part 1 parsing infrastructure unless we choose to extract parameters from assembly. Hard-coding is perfectly acceptable for this puzzle.

## Key Insights

1. **Reverse engineering is essential**: Direct simulation won't work
2. **The algorithm is a composite counter**: Not immediately obvious from assembly
3. **Primality testing optimization**: Use sqrt(n) bound, not full range
4. **Mathematical optimization**: Replace nested loops with efficient algorithm
5. **Keep it simple**: Hard-coding puzzle-specific values is acceptable - we're solving one puzzle, not building production code
6. **Part 1 validation**: With a=0, the loop exits immediately (b=67, c=67) giving h=0, providing a quick sanity check

## Additional Notes

### Understanding the Part 1 Case (a=0)
When a=0:
- Initialization gives b=67, c=67
- Main loop starts, immediately checks if b==c
- Since b==c, loop exits without incrementing h
- Result: h=0
- This is NOT because 67 is prime, but because the termination condition is met immediately
