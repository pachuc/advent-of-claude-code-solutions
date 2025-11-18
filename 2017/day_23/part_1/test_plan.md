# Test Plan: Coprocessor Instruction Counter

## Testing Strategy
Since this is a script to solve a specific problem, we focus on:
1. Verifying correct parsing and execution logic
2. Testing individual instruction behavior
3. Validating the full program execution
4. Checking edge cases relevant to the problem

## Test Categories

### 1. Unit Tests - Individual Instructions

#### Test 1.1: `set` Instruction
**Purpose**: Verify `set` correctly assigns values to registers

**Test Cases**:
```python
# Test setting from literal
instructions = [("set", "a", "42")]
# Expected: registers['a'] == 42

# Test setting from another register
instructions = [("set", "a", "10"), ("set", "b", "a")]
# Expected: registers['b'] == 10

# Test setting negative value
instructions = [("set", "a", "-5")]
# Expected: registers['a'] == -5
```

**Verification**: Check register values after execution

#### Test 1.2: `sub` Instruction
**Purpose**: Verify `sub` correctly performs subtraction

**Test Cases**:
```python
# Test subtracting literal
instructions = [("set", "a", "10"), ("sub", "a", "3")]
# Expected: registers['a'] == 7

# Test subtracting register value
instructions = [("set", "a", "10"), ("set", "b", "3"), ("sub", "a", "b")]
# Expected: registers['a'] == 7

# Test subtracting negative (adds)
instructions = [("set", "a", "10"), ("sub", "a", "-5")]
# Expected: registers['a'] == 15

# Test result going negative
instructions = [("set", "a", "5"), ("sub", "a", "10")]
# Expected: registers['a'] == -5
```

**Verification**: Check register values after execution

#### Test 1.3: `mul` Instruction
**Purpose**: Verify `mul` correctly multiplies AND increments counter

**Test Cases**:
```python
# Test multiplying by literal
instructions = [("set", "a", "5"), ("mul", "a", "3")]
# Expected: registers['a'] == 15, mul_count == 1

# Test multiplying by register
instructions = [("set", "a", "5"), ("set", "b", "3"), ("mul", "a", "b")]
# Expected: registers['a'] == 15, mul_count == 1

# Test multiplying by zero
instructions = [("set", "a", "5"), ("mul", "a", "0")]
# Expected: registers['a'] == 0, mul_count == 1

# Test multiple mul instructions
instructions = [("set", "a", "2"), ("mul", "a", "3"), ("mul", "a", "2")]
# Expected: registers['a'] == 12, mul_count == 2

# Test multiplying negative numbers
instructions = [("set", "a", "-5"), ("mul", "a", "3")]
# Expected: registers['a'] == -15, mul_count == 1
```

**Verification**: Check both register values AND mul_count

#### Test 1.4: `jnz` Instruction
**Purpose**: Verify `jnz` correctly jumps conditionally

**Test Cases**:
```python
# Test jump when condition is true (non-zero)
instructions = [
    ("set", "a", "5"),
    ("jnz", "a", "2"),    # Should jump
    ("set", "b", "1"),    # Should be skipped
    ("set", "c", "1")     # Should execute
]
# Expected: registers['b'] == 0, registers['c'] == 1

# Test no jump when condition is false (zero)
instructions = [
    ("set", "a", "0"),
    ("jnz", "a", "2"),    # Should NOT jump
    ("set", "b", "1"),    # Should execute
    ("set", "c", "1")     # Should execute
]
# Expected: registers['b'] == 1, registers['c'] == 1

# Test jump with literal (always jumps)
instructions = [
    ("jnz", "1", "2"),    # Should jump (1 is non-zero)
    ("set", "a", "1"),    # Should be skipped
    ("set", "b", "1")     # Should execute
]
# Expected: registers['a'] == 0, registers['b'] == 1

# Test backward jump with proper termination
instructions = [
    ("set", "a", "3"),     # ip=0, loop counter
    ("set", "b", "0"),     # ip=1, accumulator
    ("sub", "a", "1"),     # ip=2, decrement counter
    ("sub", "b", "-1"),    # ip=3, increment b (subtract negative)
    ("jnz", "a", "-2")     # ip=4, jump back to ip=2 if a != 0
]
# Expected: registers['a'] == 0, registers['b'] == 3
# Loop executes 3 times, incrementing b each time

# Test jump out of bounds (terminates program)
instructions = [
    ("set", "a", "1"),
    ("jnz", "1", "10")     # Jumps beyond program
]
# Expected: Program terminates, only first instruction executes
```

**Verification**: Check instruction pointer behavior and register states

### 2. Integration Tests - Small Programs

#### Test 2.1: Simple Counter Loop
**Purpose**: Verify loops work correctly
```python
# Count from 0 to 3
instructions = [
    ("set", "a", "0"),     # ip=0
    ("set", "b", "3"),     # ip=1
    ("sub", "b", "1"),     # ip=2
    ("sub", "a", "-1"),    # ip=3 (increment a)
    ("jnz", "b", "-2")     # ip=4 (loop back if b != 0)
]
# Expected: registers['a'] == 3, registers['b'] == 0
```

#### Test 2.2: Multiplication Loop
**Purpose**: Verify mul counting in loops
```python
instructions = [
    ("set", "a", "2"),     # Counter
    ("set", "b", "1"),     # Accumulator
    ("mul", "b", "2"),     # Multiply
    ("sub", "a", "1"),     # Decrement counter
    ("jnz", "a", "-2")     # Loop
]
# Expected: mul_count == 2 (loop executes twice)
```

#### Test 2.3: Nested Loops with Mul
**Purpose**: Verify mul counting in nested loops
```python
# Note: This is a simplified nested loop test
# A full nested loop would require resetting the inner counter
instructions = [
    ("set", "a", "2"),     # Outer counter
    ("set", "c", "3"),     # Inner counter (using c, not b)
    ("mul", "c", "1"),     # Mul in inner loop (ip=2)
    ("sub", "c", "1"),     # Decrement inner (ip=3)
    ("jnz", "c", "-2"),    # Inner loop back to ip=2 (ip=4)
    ("sub", "a", "1"),     # Decrement outer (ip=5)
    ("set", "c", "3"),     # Reset inner counter (ip=6)
    ("jnz", "a", "-5")     # Outer loop back to ip=2 (ip=7)
]
# Expected: mul_count == 6 (2 iterations * 3 muls each)
# First outer iteration: c=3, mul executes 3 times
# c is reset to 3
# Second outer iteration: c=3, mul executes 3 times
# Total: 6 mul executions
```

**Alternative simpler test**:
```python
# Simpler test without proper reset (demonstrates why reset matters)
instructions = [
    ("set", "a", "3"),     # Counter
    ("mul", "a", "1"),     # Multiply by 1 (no-op for value)
    ("sub", "a", "1"),     # Decrement
    ("jnz", "a", "-2")     # Loop
]
# Expected: mul_count == 3 (loop executes 3 times)
```

### 3. Full Input Test

#### Test 3.1: Actual Problem Input
**Purpose**: Verify solution on the actual input

**Approach**:
1. Run the program with the actual input from `input.md`
2. Record the mul_count result
3. Verify the program terminates (doesn't hang)
4. Check that execution time is reasonable (< 10 seconds)

**Manual Verification**:
- Trace through first few instructions manually to verify parsing
- Check that register `a` starts at 0 (debug mode)
- Verify that lines 5-8 are skipped due to the `jnz 1 5` at line 4
- Confirm the main loop structure executes

**Expected Behavior**:
- Program should terminate naturally
- mul_count should be > 0 and < 1,000,000 (sanity check)
- No infinite loops (program terminates)
- Execution completes in < 10 seconds

**Result Validation**:
- The exact expected value is initially unknown
- Run the implementation and record the result
- Verify determinism: run multiple times, should get same result
- If from Advent of Code, submit answer for verification
- Manually trace a few iterations to build confidence in correctness

**Performance Fallback**:
- If execution takes > 10 seconds, add iteration counter for debugging
- Add progress indicator to show execution hasn't hung
- Profile to identify bottlenecks (though shouldn't be needed for debug mode)

### 4. Edge Case Tests

#### Test 4.1: Empty Program
```python
instructions = []
# Expected: mul_count == 0, terminates immediately
```

#### Test 4.2: Single Instruction
```python
instructions = [("mul", "a", "5")]
# Expected: mul_count == 1
```

#### Test 4.3: No Mul Instructions
```python
instructions = [
    ("set", "a", "10"),
    ("sub", "a", "5"),
    ("jnz", "a", "1")
]
# Expected: mul_count == 0
```

#### Test 4.4: Jump to Program End
```python
instructions = [
    ("jnz", "1", "5"),     # Jump beyond end
    ("mul", "a", "1"),     # Never executed
]
# Expected: mul_count == 0
```

#### Test 4.5: All Registers Used
```python
# Test that all 8 registers (a-h) can be used
instructions = [
    ("set", "a", "1"),
    ("set", "b", "2"),
    ("set", "c", "3"),
    ("set", "d", "4"),
    ("set", "e", "5"),
    ("set", "f", "6"),
    ("set", "g", "7"),
    ("set", "h", "8"),
]
# Expected: All registers set correctly
```

### 5. Parsing Tests

#### Test 5.1: Input with Empty Lines
**Purpose**: Verify parsing handles empty lines correctly

```python
input_text = """set a 5

mul a 2
"""
lines = input_text.split('\n')
parsed = parse_instructions(lines)

# Expected parsed structure:
# [("set", "a", "5"), ("mul", "a", "2")]
# len(parsed) == 2

# Also verify execution works:
result = execute_program(parsed)
# Expected: mul_count == 1, registers['a'] == 10
```

#### Test 5.2: Negative Numbers
```python
input_text = """
set a -10
sub a -5
mul a -2
"""
# Expected: Parse negative numbers correctly
```

### 6. Validation Tests

#### Test 6.1: Value Resolution Helper
**Purpose**: Test the get_value helper function

```python
registers = {'a': 10, 'b': 20, 'c': 0, 'd': -5}

# Test register resolution
assert get_value('a', registers) == 10
assert get_value('b', registers) == 20
assert get_value('c', registers) == 0
assert get_value('d', registers) == -5

# Test literal resolution
assert get_value('5', registers) == 5
assert get_value('-3', registers) == -3
assert get_value('100', registers) == 100
assert get_value('0', registers) == 0
assert get_value('-100', registers) == -100

# Test multi-digit numbers
assert get_value('12345', registers) == 12345
assert get_value('-9999', registers) == -9999
```

## Test Execution Plan

### Phase 1: Component Testing
1. Test helper functions (get_value)
2. Test instruction parsing (verify data structure)
3. Test each instruction type individually

**Test Isolation**: Each test should create fresh state:
```python
# Each test starts with:
registers = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0}
ip = 0
mul_count = 0
```
This ensures tests don't interfere with each other.

### Phase 2: Integration Testing
1. Test simple programs (2-3 instructions)
2. Test loops with proper termination
3. Test nested structures (if needed)

### Phase 3: Full Solution Testing
1. Run on actual input
2. Verify termination and performance
3. Record result
4. Run multiple times to verify determinism
5. Validate result (submit to AoC if applicable)

### Phase 4: Edge Case Validation
1. Test boundary conditions
2. Test empty/minimal inputs
3. Verify no crashes or hangs

## Acceptance Criteria

The solution is correct if:
1. ✓ All unit tests pass (100% pass rate - at least 15+ individual test cases)
2. ✓ Integration tests produce exact expected values as specified
3. ✓ Full input executes without errors or exceptions
4. ✓ Execution completes in < 10 seconds
5. ✓ mul_count is accurately tracked (increments only on `mul` instructions)
6. ✓ Program terminates naturally when ip goes out of bounds
7. ✓ All 4 instruction types (set, sub, mul, jnz) work as specified
8. ✓ All 8 registers (a-h) can be used correctly
9. ✓ Multiple runs produce identical results (deterministic execution)
10. ✓ Result can be validated (e.g., via Advent of Code submission)

## Debugging Strategy

If tests fail:
1. **Wrong mul_count**:
   - Add debug print before each instruction execution
   - Print ip, instruction, and registers
   - Verify mul counter increments only on mul instruction

2. **Infinite loop**:
   - Add iteration counter with max limit
   - Print ip each iteration
   - Check jump logic in jnz

3. **Wrong register values**:
   - Print registers after each instruction
   - Verify get_value function works correctly
   - Check operation logic

4. **Parsing errors**:
   - Print parsed instructions
   - Check for whitespace issues
   - Verify operand splitting

## Manual Verification Checklist

Before considering the solution complete:
- [ ] Run on actual input and get a numeric result
- [ ] Verify program terminates
- [ ] Spot-check first 5-10 instructions manually
- [ ] Confirm mul_count increments only on mul instructions
- [ ] Check that jnz logic handles both jump and no-jump cases
- [ ] Verify all 4 instruction types are implemented
- [ ] Confirm register initialization (all start at 0)
- [ ] Test with at least one simple custom example
