# Testing Plan: Circuit Emulation

## Testing Strategy

We need to verify that our circuit emulation correctly handles:
1. All operation types (AND, OR, NOT, LSHIFT, RSHIFT, direct assignment)
2. Dependency resolution (instructions in arbitrary order)
3. 16-bit arithmetic constraints
4. Numeric literals vs wire references
5. The actual problem input

## Test Execution Methodology

Tests will be executed **manually** using the following approach:

1. **Create test input strings** directly in a test script or inline
2. **Call `solve(input_text, target_wire='a')`** with each test input
   - Modify the `solve()` function to accept an optional `target_wire` parameter (defaults to 'a')
   - This allows testing any wire value, not just 'a'
3. **Compare actual output** against expected output
4. **Print results** for each test case with pass/fail status

**Example test structure**:
```python
def run_test(name, input_text, expected, target_wire='a'):
    result = solve(input_text, target_wire)
    status = "PASS" if result == expected else "FAIL"
    print(f"{name}: {status} (expected {expected}, got {result})")
    return result == expected

# Example test
test_input = "123 -> x\nx -> a"
run_test("Test 1.2: Direct Wire Assignment", test_input, 123)
```

**Rationale**: For a script-based solution (not production code), manual testing is simpler than setting up a full test framework. We can add a test section at the bottom of `solution.py` or create a separate `test_solution.py` file.

## Test Categories

### 1. Unit Tests for Individual Operations

#### Test 1.1: Direct Value Assignment
**Input**:
```
123 -> x
```
**Expected**: `x = 123`
**Purpose**: Verify simple numeric assignment

#### Test 1.2: Direct Wire Assignment
**Input**:
```
123 -> x
x -> y
y -> a
```
**Expected**: `a = 123`
**Purpose**: Verify wire-to-wire assignment and dependency resolution

#### Test 1.3: AND Operation with Two Wires
**Input**:
```
123 -> x
456 -> y
x AND y -> z
```
**Expected**: `z = 123 & 456 = 72`
**Purpose**: Verify bitwise AND operation
**Calculation**:
- 123 in binary: 0000000001111011
- 456 in binary: 0000000111001000
- AND result:    0000000001001000 = 72

#### Test 1.4: OR Operation
**Input**:
```
123 -> x
456 -> y
x OR y -> z
```
**Expected**: `z = 123 | 456 = 507`
**Purpose**: Verify bitwise OR operation

#### Test 1.5: LSHIFT Operation
**Input**:
```
123 -> x
x LSHIFT 2 -> y
```
**Expected**: `y = 123 << 2 = 492`
**Purpose**: Verify left shift operation

#### Test 1.6: RSHIFT Operation
**Input**:
```
456 -> x
x RSHIFT 2 -> y
```
**Expected**: `y = 456 >> 2 = 114`
**Purpose**: Verify right shift operation

#### Test 1.7: NOT Operation (Critical for 16-bit handling)
**Input**:
```
123 -> x
NOT x -> y
```
**Expected**: `y = ~123 & 0xFFFF = 65412`
**Purpose**: Verify bitwise NOT with 16-bit constraint
**Calculation**:
- 123 in 16-bit: 0000000001111011
- NOT result:     1111111110000100 = 65412
- **Critical**: Must use 16-bit mask, not Python's arbitrary precision NOT

### 2. Integration Tests

#### Test 2.1: Example from Problem Statement
**Input**:
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
**Expected Outputs**:
- d: 72
- e: 507
- f: 492
- g: 114
- h: 65412
- i: 65079
- x: 123
- y: 456

**Purpose**: Verify all operations work together with the provided example

**Method**: Test each wire individually using modified `solve()` function:
```python
test_input = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

run_test("d", test_input, 72, target_wire='d')
run_test("e", test_input, 507, target_wire='e')
run_test("f", test_input, 492, target_wire='f')
run_test("g", test_input, 114, target_wire='g')
run_test("h", test_input, 65412, target_wire='h')
run_test("i", test_input, 65079, target_wire='i')
run_test("x", test_input, 123, target_wire='x')
run_test("y", test_input, 456, target_wire='y')
```

#### Test 2.2: Out-of-Order Dependencies
**Input**:
```
y AND z -> a
456 -> z
123 -> y
```
**Expected**: `a = 123 & 456 = 72`
**Purpose**: Verify dependency resolution works regardless of instruction order
**Note**: Wire 'a' depends on y and z, which are defined after it

#### Test 2.3: Deep Dependency Chain
**Input**:
```
d -> a
c -> d
b -> c
123 -> b
```
**Expected**: `a = 123`
**Purpose**: Verify deep recursive dependency resolution
**Depth**: 4 levels of dependencies

#### Test 2.4: Numeric Literal as Operand
**Input**:
```
100 -> x
1 AND x -> a
```
**Expected**: `a = 1 & 100 = 0`
**Purpose**: Verify handling of numeric literals in operations (from actual input: "1 AND fi -> fj")

#### Test 2.5: AND with Numeric 1 (Bit Masking Pattern)
**Input**:
```
255 -> x
1 AND x -> a
```
**Expected**: `a = 1 & 255 = 1`
**Purpose**: Verify numeric literal in AND operation (common pattern for bit masking)

#### Test 2.6: Whitespace and Empty Line Handling
**Input**:
```
123  ->  x

  x   ->  y
y -> a
```
**Expected**: `a = 123`
**Purpose**: Verify parsing handles extra whitespace and empty lines robustly

### 3. Edge Cases

#### Test 3.1: Maximum 16-bit Value
**Input**:
```
65535 -> x
x -> a
```
**Expected**: `a = 65535`
**Purpose**: Verify maximum value handling

#### Test 3.2: Zero Value
**Input**:
```
0 -> x
x -> a
```
**Expected**: `a = 0`
**Purpose**: Verify zero handling (from actual input: "0 -> c")

#### Test 3.3: NOT of Zero
**Input**:
```
0 -> x
NOT x -> a
```
**Expected**: `a = 65535`
**Purpose**: Verify NOT operation on edge value

#### Test 3.4: NOT of Maximum
**Input**:
```
65535 -> x
NOT x -> a
```
**Expected**: `a = 0`
**Purpose**: Verify NOT operation wraps correctly

#### Test 3.5: Left Shift Overflow
**Input**:
```
40000 -> x
x LSHIFT 1 -> a
```
**Expected**: `a = (40000 << 1) & 0xFFFF = 14464`
**Purpose**: Verify left shift overflow is handled with 16-bit mask
**Calculation**: 80000 & 0xFFFF = 14464

#### Test 3.6: Chained Operations
**Input**:
```
123 -> x
NOT x -> y
NOT y -> a
```
**Expected**: `a = 123`
**Purpose**: Verify double NOT returns original value

### 4. Actual Input Validation

#### Test 4.1: Input File Format
**Purpose**: Verify the input file can be parsed correctly
**Checks**:
- All 339 lines are read
- No parsing errors occur
- All instruction types are recognized

#### Test 4.2: Dependency Chain Validation
**Purpose**: Verify that wire 'a' has a valid dependency chain with no circular references
**From input**: Line 96 shows `lx -> a`
**Method**:
- Solution should complete without `RecursionError` or infinite loop
- If solution returns a value, dependency chain is valid
**Pass Criteria**: Solution completes and returns a value in range [0, 65535]

#### Test 4.3: Final Answer Validation
**Purpose**: Verify the answer is within valid range
**Checks**:
- Result is an integer
- Result is between 0 and 65535
- Result is deterministic (running multiple times gives same answer)

### 5. Performance Tests

#### Test 5.1: Memoization Effectiveness
**Purpose**: Verify each wire is computed only once
**Method**:
- Add a counter variable: `evaluation_count = 0` (could be global or passed through)
- Increment in `evaluate_wire()` before checking cache
- After solving, verify: `evaluation_count == len(circuit)` (number of unique wires)
**Expected**: Each wire evaluated exactly once (total evaluations ≈ 339 or number of wires in circuit)
**Implementation**:
```python
def evaluate_wire(wire, circuit, cache, stats=None):
    if stats is not None:
        stats['evaluations'] = stats.get('evaluations', 0) + 1

    if wire in cache:
        return cache[wire]
    # ... rest of evaluation
```

#### Test 5.2: Execution Time
**Purpose**: Verify solution completes in reasonable time
**Expected**: < 1 second for 339 instructions
**Method**: Time the execution

## Testing Execution Order

1. **Start with Unit Tests (1.1-1.8)**:
   - Create small test circuits
   - Verify each operation type individually
   - Focus especially on NOT operation (16-bit critical)
   - Include whitespace handling test

2. **Run Integration Tests (2.1-2.6)**:
   - Test the provided example first (most important validation - Test 2.1)
   - Test dependency resolution (Tests 2.2, 2.3)
   - Test numeric literals as operands (Tests 2.4, 2.5)
   - Test input robustness (Test 2.6)

3. **Validate Edge Cases (3.1-3.6)**:
   - Test boundary values (Tests 3.1, 3.2)
   - Test NOT with edge values (Tests 3.3, 3.4)
   - Test overflow conditions (Test 3.5)
   - Test operation chaining (Test 3.6)

4. **Run Against Actual Input (4.1-4.3)**:
   - Parse the full input
   - Compute wire 'a'
   - Validate result is reasonable

5. **Performance Validation (5.1-5.2)**:
   - Verify memoization works
   - Check execution time

## Modified solve() Function for Testing

To support testing multiple wires, modify the `solve()` function signature:

```python
def solve(input_text, target_wire='a'):
    """
    Main solution function.

    Args:
        input_text: String containing all circuit instructions
        target_wire: The wire to evaluate (default: 'a')

    Returns:
        int: Signal value on the target wire
    """
    lines = input_text.strip().split('\n')
    circuit = parse_circuit(lines)
    cache = {}
    return evaluate_wire(target_wire, circuit, cache)
```

This allows testing any wire by calling `solve(test_input, target_wire='x')`

## Success Criteria

✓ All individual operations produce correct results
✓ Example from problem statement matches all expected outputs
✓ Dependency resolution works in any order
✓ 16-bit constraint is properly enforced (especially for NOT)
✓ Actual input produces a value between 0 and 65535
✓ Solution completes in under 1 second

## Known Critical Points

1. **NOT Operation**: Most likely source of errors
   - Must use `~value & 0xFFFF`, not just `~value`
   - Test extensively with example values

2. **Numeric Literals**: Easy to miss
   - Some operations use numbers directly: "1 AND fi -> fj"
   - Parser must distinguish between "123" (number) and "abc" (wire)

3. **16-bit Overflow**: All operations must be masked
   - LSHIFT can easily overflow
   - AND, OR should be safe but mask anyway

## Debugging Strategy

If tests fail:
1. Print intermediate wire values during evaluation
2. Add logging to show which wires are being evaluated
3. Compare bit-by-bit for operations (print in binary)
4. Check cache to ensure memoization is working
5. Trace dependency chain for wire 'a' manually
