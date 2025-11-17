# Testing Plan: Clock Signal Generator

## Overview
This is a pragmatic testing plan focused on verifying correctness for a one-off script. We'll focus on essential integration tests and manual verification rather than exhaustive unit testing.

## Testing Strategy

### Philosophy
- **Integration over unit testing**: Test the complete solution with real input
- **Manual verification**: Inspect actual outputs for correctness
- **Minimality testing**: Verify we found the LOWEST answer
- **Pattern consistency**: Ensure the pattern truly repeats

## Core Tests

### Test 1: Input Parsing Smoke Test

**Purpose:** Verify input file is read and parsed correctly

**Procedure:**
```python
instructions = parse_input('input.md')
print(f"Loaded {len(instructions)} instructions")
print(f"First instruction: {instructions[0]}")
print(f"Last instruction: {instructions[-1]}")
```

**Expected Results:**
- Should load 30 instructions
- First instruction: `['cpy', 'a', 'd']`
- Last instruction: `['jnz', '1', '-21']`
- No parsing errors

### Test 2: Simple Interpreter Test

**Purpose:** Verify interpreter can execute basic instruction sequences

**Test Program:**
```python
test_instructions = [
    ['cpy', '0', 'a'],
    ['out', 'a'],
    ['cpy', '1', 'b'],
    ['out', 'b'],
    ['out', 'a'],
    ['out', 'b']
]
```

**Procedure:**
```python
result = run_program(0, test_instructions, max_outputs=4)
print(f"Result: {result}")
```

**Expected Result:**
- Should return `True` (outputs 0, 1, 0, 1 match the alternating pattern)

**Test Early Termination:**
```python
bad_instructions = [
    ['cpy', '1', 'a'],  # First output will be 1 (should be 0)
    ['out', 'a']
]
result = run_program(0, bad_instructions, max_outputs=10)
print(f"Result: {result}")
```

**Expected Result:**
- Should return `False` immediately (pattern starts with 1 instead of 0)

### Test 3: Run Full Solution

**Purpose:** Find the answer and verify correctness

**Procedure:**
```python
# Run the complete solution
answer = find_clock_signal_input(instructions)
print(f"Answer: {answer}")
```

**Expected Results:**
- Should find an answer in range 1-10000
- Should complete in < 10 seconds
- Answer should be deterministic (same every run)

### Test 4: Verify Answer Correctness

**Purpose:** Manually verify the answer produces the correct pattern

**Procedure:**
```python
# Test the found answer with extended output
def run_program_verbose(initial_a, instructions, max_outputs=100):
    """Modified version that returns list of outputs for inspection"""
    registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    pc = 0
    outputs = []

    while 0 <= pc < len(instructions) and len(outputs) < max_outputs:
        # ... same execution logic ...
        # But store outputs instead of validating
        if cmd == 'out':
            value = get_value(inst[1], registers)
            outputs.append(value)
            pc += 1

    return outputs

# Verify the answer
outputs = run_program_verbose(answer, instructions, max_outputs=100)
print(f"First 20 outputs: {outputs[:20]}")
print(f"Total outputs generated: {len(outputs)}")

# Check pattern manually
is_valid = all(outputs[i] == i % 2 for i in range(len(outputs)))
print(f"Pattern is valid: {is_valid}")
```

**Expected Results:**
- First 20 outputs should be: `[0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]`
- Should generate 100 outputs
- Pattern should be perfectly valid

### Test 5: Verify Minimality

**Purpose:** Confirm answer is the LOWEST value that works

**Procedure:**
```python
# Test answer - 1
result_below = run_program(answer - 1, instructions, max_outputs=50)
print(f"Answer - 1 ({answer - 1}): {result_below}")

# Show where it fails
outputs_below = run_program_verbose(answer - 1, instructions, max_outputs=10)
print(f"First 10 outputs for answer-1: {outputs_below}")

# Optional: Test answer + 1 (might also work, but we want the minimum)
result_above = run_program(answer + 1, instructions, max_outputs=50)
print(f"Answer + 1 ({answer + 1}): {result_above}")
```

**Expected Results:**
- `answer - 1` should return `False` (does NOT produce correct pattern)
- This confirms we found the minimum value
- `answer + 1` might return `True` or `False` (doesn't matter, we want the minimum)

### Test 6: Pattern Consistency Verification

**Purpose:** Ensure the pattern repeats consistently for different verification lengths

**Procedure:**
```python
# Test with different verification lengths
for length in [20, 50, 100]:
    result = run_program(answer, instructions, max_outputs=length)
    print(f"Verification length {length}: {result}")
```

**Expected Results:**
- All verification lengths should return `True`
- This confirms the pattern truly repeats indefinitely (not just for first few outputs)

### Test 7: Explore First Few Candidates (Optional)

**Purpose:** Understand why the first few values fail (debugging/educational)

**Procedure:**
```python
print("Testing first 5 candidates:")
for candidate in range(1, 6):
    outputs = run_program_verbose(candidate, instructions, max_outputs=10)
    print(f"a={candidate}: {outputs}")
```

**Expected Results:**
- Shows the actual output patterns for candidates before the answer
- Helps understand what makes the correct answer special
- Useful for debugging if the answer seems wrong

## Test Execution Sequence

Run tests in this order:

1. **Test 1**: Input parsing smoke test
2. **Test 2**: Simple interpreter test
3. **Test 3**: Run full solution to find answer
4. **Test 4**: Verify answer correctness with 100 outputs
5. **Test 5**: Verify minimality (answer-1 fails)
6. **Test 6**: Pattern consistency across different lengths
7. **Test 7** (optional): Explore first few candidates

## Success Criteria

The solution is correct if:
- ✓ Answer is a positive integer in range 1-10000
- ✓ Answer produces exactly `0, 1, 0, 1, 0, 1...` for 100+ outputs
- ✓ `answer - 1` does NOT produce the correct pattern
- ✓ Different verification lengths (20, 50, 100) all validate successfully
- ✓ Solution completes in < 10 seconds

## Debugging Strategies

### If no answer is found:
1. Check that early termination logic is correct (expected = output_count % 2)
2. Verify PC updates correctly (especially for JNZ)
3. Test with smaller verification length (e.g., 10) to see if answer appears
4. Add debug output to see what patterns are being generated

### If wrong answer is found:
1. Manually run `run_program_verbose(answer, instructions, 20)` and inspect outputs
2. Check if answer-1 actually fails
3. Verify that we're starting from candidate=1, not candidate=0
4. Check for off-by-one errors in pattern validation

### If pattern breaks unexpectedly:
1. Increase verification length to see if it's a consistent pattern
2. Print register states at each output to understand the program logic
3. Check for bugs in instruction execution (especially JNZ and CPY)

### If solution is too slow:
1. Verify early termination is working (should fail on first wrong output)
2. Check that we're not storing all outputs (just validating)
3. Consider reducing upper bound if answer should be smaller
4. Add counter to see how many candidates are tested

## Quick Validation Script

Use this script to run all essential tests:

```python
def validate_solution():
    print("=" * 50)
    print("VALIDATION TESTS")
    print("=" * 50)

    # Test 1: Parse input
    print("\n[Test 1] Parsing input...")
    instructions = parse_input('input.md')
    print(f"✓ Loaded {len(instructions)} instructions")

    # Test 3: Find answer
    print("\n[Test 3] Finding answer...")
    import time
    start = time.time()
    answer = find_clock_signal_input(instructions)
    elapsed = time.time() - start
    print(f"✓ Answer: {answer} (found in {elapsed:.2f}s)")

    # Test 4: Verify correctness
    print("\n[Test 4] Verifying correctness...")
    outputs = run_program_verbose(answer, instructions, 100)
    is_valid = all(outputs[i] == i % 2 for i in range(len(outputs)))
    print(f"✓ Generated {len(outputs)} outputs")
    print(f"✓ Pattern valid: {is_valid}")
    print(f"  First 20: {outputs[:20]}")

    # Test 5: Verify minimality
    print("\n[Test 5] Verifying minimality...")
    result_below = run_program(answer - 1, instructions, 50)
    print(f"✓ Answer-1 result: {result_below} (should be False)")

    # Test 6: Pattern consistency
    print("\n[Test 6] Pattern consistency...")
    for length in [20, 50, 100]:
        result = run_program(answer, instructions, length)
        print(f"✓ Length {length}: {result}")

    print("\n" + "=" * 50)
    print(f"FINAL ANSWER: {answer}")
    print("=" * 50)

if __name__ == "__main__":
    validate_solution()
```

## Expected Output from Validation

```
==================================================
VALIDATION TESTS
==================================================

[Test 1] Parsing input...
✓ Loaded 30 instructions

[Test 3] Finding answer...
✓ Answer: XXX (found in X.XXs)

[Test 4] Verifying correctness...
✓ Generated 100 outputs
✓ Pattern valid: True
  First 20: [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]

[Test 5] Verifying minimality...
✓ Answer-1 result: False (should be False)

[Test 6] Pattern consistency...
✓ Length 20: True
✓ Length 50: True
✓ Length 100: True

==================================================
FINAL ANSWER: XXX
==================================================
```
