# Test Plan: Assembunny Code Interpreter - Part 2

## Testing Strategy
Since the Part 1 solution is fully working and tested, Part 2 testing focuses on:
1. Verifying the single change (register `c` initialized to `1`)
2. Confirming the program produces a different result
3. Basic sanity checks (no infinite loops, reasonable execution time)

## Primary Tests

### Test 1: Regression Test - Part 1 Still Works
**Purpose**: Verify no accidental changes broke Part 1 functionality
**Program**: Full input from `input.md`
**Initial State**: `{'a': 0, 'b': 0, 'c': 0, 'd': 0}` (Part 1 configuration)
**Expected**: `registers['a'] == 318077`
**Note**: This confirms the interpreter logic wasn't broken

### Test 2: Example Program Validation
**Purpose**: Verify the example from Part 1 problem statement still works
**Program**:
```
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
```
**Initial State**: All registers `0`
**Expected**: `registers['a'] == 42`
**Note**: Quick sanity check of basic instruction execution

### Test 3: Part 2 Specific Tests

#### Test 3.1: Register `c` Initial Value
**Before execution**: Verify `registers['c'] == 1` (not `0`)
**Purpose**: Confirm the key difference from Part 1

#### Test 3.2: Full Program Execution with `c=1`
**Input**: The 23-line program from `input.md`
**Initial State**: `{'a': 0, 'b': 0, 'c': 1, 'd': 0}`
**Verification Steps**:
1. Program completes without infinite loop
2. Final `a` value is different from Part 1 answer (318077)
3. Final `a` value is a positive integer
4. Execution completes in reasonable time (< 2 seconds)

#### Test 3.3: Output Format
**Expected**: Single integer printed to stdout
**Purpose**: Confirm output matches expected format

## Optional Verification Steps

### Manual Trace (If Needed)
If the output seems incorrect, manually trace the first few instructions:
- Line 1: `cpy 1 a` → `a=1`
- Line 2: `cpy 1 b` → `b=1`
- Line 3: `cpy 26 d` → `d=26`
- Line 4: `jnz c 2` → Since `c=1`, jump to line 6 (skip line 5)
- Continue from line 6...

This helps verify the conditional logic executes correctly with `c=1`.

## Success Criteria
1. ✅ Part 1 regression test passes (output = 318077 with `c=0`)
2. ✅ Example program produces correct output (42)
3. ✅ Full program with `c=1` executes without errors
4. ✅ Part 2 result is different from Part 1 (not 318077)
5. ✅ Part 2 result is a positive integer
6. ✅ Execution completes in under 2 seconds
7. ✅ Output is a single integer value

## Test Execution Order
1. Run example program test (quick validation)
2. Run Part 1 regression test (verify `c=0` still produces 318077)
3. Run Part 2 full program with `c=1`
4. Verify output differs from Part 1 and is formatted correctly
5. Perform manual trace only if results seem incorrect
