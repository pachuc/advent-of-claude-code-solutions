# Test Plan: Circuit Signal Simulation (Part 2)

## Testing Strategy

Test the solution through a combination of:
1. **Unit tests** for individual components (parsing, evaluation functions)
2. **Simple example** to verify basic circuit logic
3. **Full input test** with the actual puzzle input
4. **Edge case verification** for bitwise operations

## Test Cases

### Test 1: Parsing Instructions
**Objective:** Verify that input parsing correctly identifies all operation types

**Test Data:**
```
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
```

**Expected Results:**
- 8 instructions in dictionary
- Correct operation types identified
- Correct operands extracted
- Wire names mapped correctly

**Verification:**
```python
instructions = parse_instructions(test_lines)
assert 'x' in instructions
assert instructions['x']['op'] == 'VALUE'
assert instructions['d']['op'] == 'AND'
assert instructions['h']['op'] == 'NOT'
```

### Test 2: Simple Circuit Evaluation (Part 1 Example)
**Objective:** Verify basic circuit evaluation works correctly

**Test Data:**
```
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
```

**Expected Wire Values:**
- `x`: 123
- `y`: 456
- `d`: 123 AND 456 = 72
- `e`: 123 OR 456 = 507
- `f`: 123 << 2 = 492
- `g`: 456 >> 2 = 114
- `h`: NOT 123 = 65412
- `i`: NOT 456 = 65079

**Verification:**
```python
memo = {}
assert evaluate_wire('x', instructions, memo) == 123
assert evaluate_wire('y', instructions, memo) == 456
assert evaluate_wire('d', instructions, memo) == 72
assert evaluate_wire('e', instructions, memo) == 507
assert evaluate_wire('f', instructions, memo) == 492
assert evaluate_wire('g', instructions, memo) == 114
assert evaluate_wire('h', instructions, memo) == 65412
assert evaluate_wire('i', instructions, memo) == 65079
```

### Test 3: 16-bit Overflow Handling
**Objective:** Verify that left shift operations properly handle 16-bit overflow

**Test Data:**
```
65535 -> x
x LSHIFT 1 -> y
x LSHIFT 8 -> z
```

**Expected Results:**
- `x`: 65535
- `y`: (65535 << 1) & 0xFFFF = 65534
- `z`: (65535 << 8) & 0xFFFF = 65280

**Verification:**
```python
assert evaluate_wire('x', instructions, memo) == 65535
assert evaluate_wire('y', instructions, memo) == 65534
assert evaluate_wire('z', instructions, memo) == 65280
```

### Test 4: NOT Operation (16-bit Complement)
**Objective:** Verify NOT operation works correctly for 16-bit values

**Test Data:**
```
0 -> x
65535 -> y
1 -> z
NOT x -> a
NOT y -> b
NOT z -> c
```

**Expected Results:**
- NOT 0 = 65535
- NOT 65535 = 0
- NOT 1 = 65534

**Verification:**
```python
assert evaluate_wire('a', instructions, memo) == 65535
assert evaluate_wire('b', instructions, memo) == 0
assert evaluate_wire('c', instructions, memo) == 65534
```

### Test 5: Mixed Literal and Wire Operands
**Objective:** Verify operations handle both wire references and numeric literals

**Test Data:**
```
123 -> x
1 AND x -> y
x AND 456 -> z
```

**Expected Results:**
- `y`: 1 AND 123 = 1
- `z`: 123 AND 456 = 72

**Verification:**
```python
assert evaluate_wire('y', instructions, memo) == 1
assert evaluate_wire('z', instructions, memo) == 72
```

### Test 6: Dependency Chain
**Objective:** Verify recursive evaluation handles deep dependency chains

**Test Data:**
```
1 -> a
a -> b
b -> c
c -> d
d -> e
```

**Expected Results:**
- All wires should evaluate to 1
- Memoization should prevent redundant calculations

**Verification:**
```python
memo = {}
assert evaluate_wire('e', instructions, memo) == 1
# Check memoization worked
assert len(memo) == 5  # All intermediate values cached
assert 'a' in memo and memo['a'] == 1
```

### Test 7: Part 2 Logic - Two Simulation Runs
**Objective:** Verify the two-stage simulation process works correctly, especially when wire `a` depends on wire `b`

**Test Data (demonstrates value actually changes):**
```
NOT b -> a
100 -> b
```

**First Run:**
- `b` = 100
- `a` = NOT 100 = 65435

**After Override:**
- Set `b` = 65435 (value from first run's `a`)

**Second Run:**
- `b` = 65435
- `a` = NOT 65435 = 100

**Verification:**
```python
# First run
instructions = parse_instructions(test_lines)
memo1 = {}
original_a = evaluate_wire('a', instructions, memo1)
assert original_a == 65435

# Override b
instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a)]}

# Second run with FRESH memo
memo2 = {}
final_a = evaluate_wire('a', instructions, memo2)
assert final_a == 100

# Verify the values changed
assert original_a != final_a
```

**Alternative simpler test:**
```
b OR 1 -> a
5 -> b
```
- First run: `a` = 5 OR 1 = 5
- Override `b` = 5
- Second run: `a` = 5 OR 1 = 5 (same, but still validates logic)

### Test 8: Full Input Simulation (Primary Test)
**Objective:** Run the actual puzzle input and verify it produces a valid result

**Test Data:** Full 340-line input from input.md

**Verification Steps:**
1. Parse all 340 instructions successfully
2. First simulation completes without errors
3. Wire `a` has a valid 16-bit value (0-65535)
4. Second simulation with overridden `b` completes
5. Final wire `a` value is different from first run
6. Final value is in valid range (0-65535)
7. **If expected answer is known:** verify final_a matches expected value

**Code:**
```python
# Read full input
with open('input.md', 'r') as f:
    lines = f.readlines()

# Parse
instructions = parse_instructions(lines)
assert len(instructions) == 340

# First run
memo = {}
original_a = evaluate_wire('a', instructions, memo)
assert 0 <= original_a <= 65535
print(f"First run - wire a: {original_a}")

# Override b
instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a)]}

# Second run with FRESH memo
memo = {}
final_a = evaluate_wire('a', instructions, memo)
assert 0 <= final_a <= 65535
print(f"Second run - wire a: {final_a}")

# The two values should be different
assert original_a != final_a

# IMPORTANT: If you know the expected answer from Advent of Code submission,
# add assertion here:
# EXPECTED_ANSWER = <value from AoC>  # Replace with actual expected value
# assert final_a == EXPECTED_ANSWER, f"Expected {EXPECTED_ANSWER}, got {final_a}"

# If expected answer unknown, submit final_a to Advent of Code for verification
```

**Note:** The ultimate verification is submitting the answer to Advent of Code and confirming it's correct. The tests above ensure the code runs correctly but can't guarantee correctness without the known expected result.

### Test 9: Memoization Correctness
**Objective:** Verify memoization cache is cleared between runs

**Test Data:**
```
5 -> b
b -> a
```

**Process:**
- First run: a = 5, memo = {'b': 5, 'a': 5}
- Override b to 10
- Second run: Should recalculate, a = 10
- If memo not cleared, might incorrectly use cached value

**Verification:**
```python
# First run
memo1 = {}
result1 = evaluate_wire('a', instructions, memo1)
assert result1 == 5

# Override and second run with NEW memo
instructions['b'] = {'op': 'VALUE', 'args': [10]}
memo2 = {}  # MUST be fresh
result2 = evaluate_wire('a', instructions, memo2)
assert result2 == 10

# Verify different memo objects
assert memo1 is not memo2
```

### Test 10: Wire 'b' Override Verification
**Objective:** Ensure wire `b` is correctly overridden with first run's wire `a` value

**Test Data:** Actual input (line 4: `44430 -> b` - note this is input-specific)

**Verification:**
```python
# Parse input
instructions = parse_instructions(lines)

# Check initial b value (44430 is specific to this input file)
memo = {}
initial_b = evaluate_wire('b', instructions, memo)
assert initial_b == 44430  # Input-specific value

# First run
memo = {}
original_a = evaluate_wire('a', instructions, memo)

# Override b
instructions['b'] = {'op': 'SIGNAL', 'args': [str(original_a)]}

# Verify b is now different (with fresh memo)
memo = {}
new_b = evaluate_wire('b', instructions, memo)
assert new_b == original_a
assert new_b != 44430  # Should be different from original

# Also verify the instruction was actually modified
assert instructions['b']['op'] == 'SIGNAL'
assert instructions['b']['args'][0] == str(original_a)
```

## Edge Cases to Consider

### 1. Bitwise Operation Edge Cases
- **AND with 0:** Any value AND 0 = 0
- **OR with 65535:** Any value OR 65535 = 65535
- **LSHIFT overflow:** Large values shifted left must wrap to 16 bits
- **RSHIFT to 0:** Any value >> 16 or more = 0
- **NOT twice:** NOT(NOT x) = x

### 2. Operand Type Edge Cases
- Single digit literals: "0", "1"
- Maximum value: "65535"
- Wire names that could look like numbers (none in this input)

### 3. Circuit Structure Edge Cases
- Direct assignment: `lx -> a` (wire a gets value from wire lx)
- Constant assignment: `0 -> c`
- Long dependency chains
- Wide dependency trees (many wires feeding into one)

## Manual Verification Approach

### Step-by-Step Manual Check
For a small subset of the circuit, manually trace evaluation:

**Example: Verify wire 'a' gets value from 'lx'**
1. Instruction for `a`: `lx -> a` (line 96)
2. Find instruction for `lx`: `lw OR lv -> lx` (line 128)
3. Find instructions for `lw` and `lv`: ...
4. Continue tracing back until reaching literal values
5. Calculate forward to verify

**This is impractical for full circuit but useful for debugging**

## Success Criteria

The solution is correct if:
1. ✅ All parsing tests pass
2. ✅ Simple circuit example produces correct values
3. ✅ Bitwise operation edge cases handled correctly
4. ✅ First simulation produces valid wire `a` value
5. ✅ Wire `b` successfully overridden with first `a` value
6. ✅ Second simulation produces different, valid wire `a` value
7. ✅ Memoization cache properly cleared between runs
8. ✅ Final answer is a 16-bit unsigned integer

## Performance Verification

**Expected Performance:**
- Parsing: < 10ms
- Each simulation run: < 50ms
- Total runtime: < 200ms for the entire solution

**Measurement:**
```python
import time

start = time.time()
# Run full solution (parse + simulate + override + simulate)
end = time.time()

runtime_ms = (end - start) * 1000
print(f"Runtime: {runtime_ms:.2f}ms")
assert (end - start) < 0.5  # Should complete in under 500ms
```

**Note:** The assertion checks < 0.5 seconds (500ms) as a reasonable upper bound for a script, which is more realistic than the stricter sub-100ms target but still ensures reasonable performance.

## Debugging Strategy

If tests fail:
1. **Check parsing:** Print parsed instructions, verify format
2. **Check individual operations:** Test each operation type in isolation
3. **Trace evaluation:** Add debug prints in evaluate_wire to see call stack
4. **Check memoization:** Print memo contents to verify caching
5. **Verify 16-bit masking:** Check all results are in [0, 65535]
6. **Check wire b override:** Print instructions['b'] before and after override
7. **Verify memo clearing:** Ensure different memo objects between runs (use `id(memo)`)

**Sample Debug Output:**
```python
def evaluate_wire(wire_name, instructions, memo, depth=0):
    indent = "  " * depth
    print(f"{indent}Evaluating: {wire_name}")

    if wire_name in memo:
        print(f"{indent}  -> Cached: {memo[wire_name]}")
        return memo[wire_name]

    # ... evaluation logic ...

    print(f"{indent}  -> Computed: {result}")
    memo[wire_name] = result
    return result
```

This will show the dependency traversal and help identify issues.

## Test Execution Order

1. Run parsing test first (Test 1)
2. Run basic circuit test (Test 2)
3. Run edge case tests (Tests 3-5)
4. Run dependency test (Test 6)
5. Run Part 2 logic test (Test 7)
6. Run memoization test (Test 9)
7. Run override verification test (Test 10)
8. Finally, run full input test (Test 8)

This order ensures basic functionality works before testing complex scenarios.
