# Implementation Plan: Circuit Emulation

## Problem Analysis

We need to simulate a circuit of wires and bitwise logic gates where:
- Each wire carries a 16-bit signal (0-65535)
- Wires can receive signals from gates, other wires, or direct values
- Instructions can appear in any order (dependency resolution required)
- We need to find the final signal value on wire `a`

## Algorithm Approach

**Strategy**: Recursive memoization with dependency resolution
- **Why**: Instructions can appear in any order, so we can't process linearly
- **How**: Parse all instructions, then recursively evaluate wire `a`, computing dependencies as needed
- **Efficiency**: O(n) time with memoization where n is the number of wires (each wire computed once)
- **Space**: O(n) for storing wire computations in cache

## Step-by-Step Implementation

### Step 1: Input Parsing
**File**: `solution.py`

Create a function to parse the input file and build a circuit representation:

```python
def parse_circuit(lines):
    """
    Parse circuit instructions into a dictionary mapping wire names to their operations.

    Returns:
        dict: {wire_name: (operation_type, operands)}
    """
```

**Data Structure**: Dictionary where:
- Key: wire name (string)
- Value: tuple containing operation type (string) and operands (tuple)

**Operation Types to Handle**:
1. `'VALUE'`: `('VALUE', value)` - e.g., "123 -> x"
2. `'WIRE'`: `('WIRE', source_wire)` - e.g., "lx -> a"
3. `'AND'`: `('AND', input1, input2)` - e.g., "x AND y -> z"
4. `'OR'`: `('OR', input1, input2)` - e.g., "x OR y -> e"
5. `'LSHIFT'`: `('LSHIFT', input, shift_amount)` - e.g., "x LSHIFT 2 -> f"
6. `'RSHIFT'`: `('RSHIFT', input, shift_amount)` - e.g., "y RSHIFT 2 -> g"
7. `'NOT'`: `('NOT', input)` - e.g., "NOT x -> h"

**Note**: Shift amounts (for LSHIFT/RSHIFT) are always numeric literals in the input, never wire references.

**Detailed Parsing Logic**:
```python
for line in lines:
    line = line.strip()
    if not line:  # Skip empty lines
        continue

    # Split by " -> " to get operation and output wire
    left_side, output_wire = line.split(' -> ')
    parts = left_side.split()

    if len(parts) == 1:
        # Direct assignment: could be "123 -> x" or "lx -> a"
        if parts[0].isdigit():
            circuit[output_wire] = ('VALUE', int(parts[0]))
        else:
            circuit[output_wire] = ('WIRE', parts[0])

    elif len(parts) == 2:
        # NOT operation: "NOT x -> h"
        circuit[output_wire] = ('NOT', parts[1])

    elif len(parts) == 3:
        # Binary operations: AND, OR, LSHIFT, RSHIFT
        operation = parts[1]  # AND, OR, LSHIFT, RSHIFT
        # Note: parts[0] and parts[2] stay as strings
        # They will be resolved later (could be wire names or numeric literals)
        circuit[output_wire] = (operation, parts[0], parts[2])
```

**Key Points**:
- Use `str.isdigit()` to distinguish numeric literals from wire names
- Keep operands as strings initially; resolution happens during evaluation
- Handle extra whitespace with `strip()`
- Skip empty lines

### Step 2: Value Resolution Helper
Create a helper function to resolve a value (could be a wire name or numeric literal):

```python
def get_value(operand, circuit, cache):
    """
    Resolve an operand to its numeric value.
    If it's a number, return it directly.
    If it's a wire, evaluate that wire recursively.

    Note: This function and evaluate_wire() are mutually recursive.
    This is intentional and handles nested wire dependencies.
    """
    if operand.isdigit():
        return int(operand)
    else:
        # It's a wire name - recursively evaluate it
        return evaluate_wire(operand, circuit, cache)
```

**Logic**:
- If operand is numeric string: convert to int and return
- If operand is wire name: call `evaluate_wire()` to recursively evaluate that wire
- The mutual recursion between `get_value()` and `evaluate_wire()` naturally handles dependency chains

### Step 3: Wire Evaluation with Memoization
Create the main evaluation function using recursive memoization:

```python
def evaluate_wire(wire, circuit, cache):
    """
    Recursively evaluate a wire's signal value.
    Uses memoization to cache results.

    Returns:
        int: The 16-bit signal value (0-65535)
    """
```

**Algorithm**:
1. Check if wire value already in cache → return cached value
2. Get operation for this wire from circuit dictionary
3. Based on operation type, compute the result:
   - **'VALUE'**: `result = value`
   - **'WIRE'**: `result = get_value(source_wire, circuit, cache)`
   - **'AND'**: `result = get_value(input1, circuit, cache) & get_value(input2, circuit, cache)`
   - **'OR'**: `result = get_value(input1, circuit, cache) | get_value(input2, circuit, cache)`
   - **'LSHIFT'**: `result = get_value(input, circuit, cache) << shift_amount`
   - **'RSHIFT'**: `result = get_value(input, circuit, cache) >> shift_amount`
   - **'NOT'**: `result = ~get_value(input, circuit, cache)`
4. **CRITICAL**: Apply 16-bit mask to result: `result = result & 0xFFFF`
   - This must be done for ALL operations, not just NOT
   - LSHIFT can overflow beyond 16 bits
   - Defensive masking ensures correctness
5. Cache the result: `cache[wire] = result`
6. Return the result

**Important Notes**:
- **16-bit masking is universal**: Apply `& 0xFFFF` after every operation
- **NOT operation**: Python's `~` operator works on arbitrary precision integers with two's complement, so `~123` gives a negative number. The `& 0xFFFF` mask extracts only the lower 16 bits.
- **LSHIFT overflow**: Left shifting can easily exceed 16 bits (e.g., `40000 << 1 = 80000`), so masking is essential
- All operations return values in range [0, 65535]

### Step 4: Main Solution Function
Create the main function that ties everything together:

```python
def solve(input_text):
    """
    Main solution function.

    Args:
        input_text: String containing all circuit instructions

    Returns:
        int: Signal value on wire 'a'
    """
```

**Steps**:
1. Split input into lines and remove empty lines
2. Parse all instructions into circuit dictionary
3. Initialize empty cache dictionary
4. Evaluate wire 'a' using recursive memoization
5. Return the result

### Step 5: Entry Point
Create the main execution block:

```python
if __name__ == "__main__":
    with open('input.md', 'r') as f:
        input_text = f.read()

    result = solve(input_text)
    print(result)
```

## Data Structures Summary

1. **Circuit Dictionary**: `{wire_name: (operation_type, operands)}`
   - Stores the parsed instructions
   - O(1) lookup for any wire's operation

2. **Cache Dictionary**: `{wire_name: computed_value}`
   - Memoization to avoid recomputation
   - O(1) lookup and storage

## Complexity Analysis

**Time Complexity**: O(n) where n is the number of wires
- Each wire is evaluated exactly once due to memoization
- Each evaluation performs constant time operations

**Space Complexity**: O(n)
- Circuit dictionary: O(n)
- Cache dictionary: O(n)
- Recursion stack: O(d) where d is maximum dependency depth

**Expected Performance**:
- Input has 339 instructions
- With memoization, should complete in milliseconds
- No optimization beyond memoization needed for this input size

## Edge Cases to Handle

1. **Numeric literals as operands**: e.g., "1 AND fi -> fj"
   - Check if operand is digit before treating as wire
   - Handled by `get_value()` function

2. **16-bit overflow**: All operations must stay within 0-65535
   - Apply `& 0xFFFF` mask universally after ALL operations
   - Especially critical for LSHIFT and NOT

3. **NOT operation**: Must handle 16-bit complement correctly
   - Use `~value & 0xFFFF`, not just `~value`
   - Python's `~` gives negative numbers due to two's complement

4. **Direct value vs direct wire assignment**:
   - "123 -> x" (numeric literal)
   - "lx -> a" (wire reference)
   - Parse differently based on whether left side is numeric (use `str.isdigit()`)

5. **Whitespace handling**:
   - Use `strip()` to handle leading/trailing whitespace
   - Skip empty lines

6. **Shift amounts**: Always numeric literals, never wire references
   - No need to call `get_value()` on shift amounts
   - Can directly use `int(parts[2])` for LSHIFT/RSHIFT

## Assumptions

- **Well-formed input**: The input is assumed to be syntactically correct with no malformed instructions
- **No circular dependencies**: The circuit has no circular wire dependencies
- **No undefined wires**: All referenced wires are defined somewhere in the input
- **Recursion depth**: Dependency depth is assumed to be < 1000 (Python's default recursion limit)
  - If `RecursionError` occurs, can increase limit with `sys.setrecursionlimit(10000)`

## Python Environment

- **Python version**: Python 3.6 or higher
- **Dependencies**: None (uses only standard library)
- **Standard library imports needed**: None (all operations are built-in)

## Implementation Order

1. Parse circuit instructions (Step 1)
2. Implement value resolution helper (Step 2)
3. Implement wire evaluation with memoization (Step 3)
4. Create main solution function (Step 4)
5. Add entry point (Step 5)
6. Test with example from problem statement
7. Run on actual input
