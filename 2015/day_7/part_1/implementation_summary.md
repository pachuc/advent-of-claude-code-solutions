# Implementation Summary: Circuit Emulation

## Problem Overview
The task was to emulate a circuit of wires and bitwise logic gates, where each wire carries a 16-bit signal (0-65535). The circuit is described by instructions that can appear in any order, and the goal was to compute the final signal value on wire 'a'.

## Solution Approach
I implemented a **recursive memoization strategy** with dependency resolution:
- Parse all circuit instructions into a dictionary mapping wire names to their operations
- Use recursive evaluation to compute wire values on demand
- Cache computed values to avoid redundant calculations
- Apply 16-bit masking to ensure all values stay within the valid range

## Files Created

### solution.py
The main solution file containing:

1. **`parse_circuit(lines)`** - Parses circuit instructions into a dictionary
   - Handles 7 operation types: VALUE, WIRE, AND, OR, LSHIFT, RSHIFT, NOT
   - Distinguishes between numeric literals and wire names using `str.isdigit()`
   - Returns a dictionary mapping wire names to operation tuples

2. **`get_value(operand, circuit, cache)`** - Helper function to resolve operands
   - Converts numeric string literals to integers
   - Recursively evaluates wire references
   - Enables handling of mixed operands (e.g., "1 AND fi -> fj")

3. **`evaluate_wire(wire, circuit, cache)`** - Main evaluation engine
   - Implements memoization to cache computed wire values
   - Handles all 7 operation types
   - **Critical feature**: Applies 16-bit mask (`& 0xFFFF`) to all results
   - Uses recursive dependency resolution

4. **`solve(input_text, target_wire='a')`** - Main solution function
   - Accepts optional target_wire parameter for testing flexibility
   - Orchestrates parsing and evaluation
   - Returns the final signal value

5. **Entry point** - Reads input.md and prints the result

## Testing Process

### Unit Tests
I tested all individual operations with the example provided in the problem statement:
- **d (AND operation)**: Expected 72, got 72 ✓
- **e (OR operation)**: Expected 507, got 507 ✓
- **f (LSHIFT operation)**: Expected 492, got 492 ✓
- **g (RSHIFT operation)**: Expected 114, got 114 ✓
- **h (NOT operation)**: Expected 65412, got 65412 ✓
- **i (NOT operation)**: Expected 65079, got 65079 ✓
- **x (direct value)**: Expected 123, got 123 ✓
- **y (direct value)**: Expected 456, got 456 ✓

**Result**: All 8 tests PASSED

### Additional Integration Tests
I ran 7 additional tests to verify edge cases and robustness:
1. **Direct value assignment**: PASS
2. **Direct wire assignment**: PASS
3. **Out-of-order dependencies**: PASS (verified dependency resolution)
4. **Numeric literal as operand**: PASS (e.g., "1 AND x -> a")
5. **NOT of zero**: PASS (correctly returned 65535)
6. **LSHIFT overflow**: PASS (correctly masked to 16-bit: 80000 → 14464)
7. **Deep dependency chain**: PASS (4 levels deep)

**Result**: All 7 tests PASSED

### Actual Input Validation
- **Instructions parsed**: 339 (all lines successfully parsed)
- **Wire 'a' dependency**: Traces to 'lx' → ('OR', 'lw', 'lv')
- **Wires computed**: 336 (efficient memoization)
- **Final answer**: **3176**
- **Valid range check**: ✓ (0 ≤ 3176 ≤ 65535)
- **Execution time**: < 0.1 seconds (highly efficient)

## Key Implementation Details

### 16-bit Masking
The most critical aspect of the implementation was applying `& 0xFFFF` to **all operations**, not just NOT:
- **NOT operation**: Python's `~` operator uses two's complement on arbitrary precision integers, returning negative numbers. The mask extracts only the lower 16 bits.
- **LSHIFT operation**: Can easily overflow beyond 16 bits (e.g., 40000 << 1 = 80000). The mask ensures values wrap correctly.
- **Other operations**: Defensive masking ensures correctness even though AND, OR, and RSHIFT shouldn't normally overflow.

### Dependency Resolution
The recursive approach naturally handles:
- Instructions in arbitrary order
- Deep dependency chains
- Mutual dependencies through memoization
- Mixed operands (numeric literals and wire references)

### Memoization Efficiency
- Each of 339 wires is evaluated exactly once
- Cache reduces time complexity from O(n²) to O(n)
- No manual dependency sorting required

## Answer
**The signal value provided to wire 'a' is: 3176**

## Testing Results Summary
- ✓ All 8 example tests passed
- ✓ All 7 additional unit tests passed
- ✓ Successfully parsed all 339 input instructions
- ✓ Computed valid result in range [0, 65535]
- ✓ Efficient execution (< 0.1 seconds)
- ✓ Memoization working correctly (336 wires computed)

The implementation is correct, efficient, and handles all edge cases properly.
