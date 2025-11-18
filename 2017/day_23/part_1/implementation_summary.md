# Implementation Summary

## Problem Overview
The task was to build a coprocessor simulator that executes a simple assembly-like language and counts how many times the `mul` (multiply) instruction is invoked during program execution.

## Solution Approach
I implemented a straightforward interpreter following the implementation plan:

1. **Instruction Parser**: Parses input lines into tuples of (operation, arg1, arg2)
2. **Value Resolver**: Helper function to resolve operands (either register values or integer literals)
3. **Instruction Executor**: Main loop that executes instructions and tracks state
4. **Mul Counter**: Tracks each time a `mul` instruction executes

## Files Created

### solution.py
The main solution file containing:
- `parse_instructions(lines)`: Parses input into instruction tuples
- `get_value(operand, registers)`: Resolves operands to actual values (handles both register names and integer literals)
- `execute_program(instructions)`: Main interpreter loop that executes the program and returns mul_count
- `main()`: Entry point that reads input, executes program, and prints result

### test_solution.py
Comprehensive test suite with 9 test functions covering:
- Helper function (get_value)
- Individual instructions (set, sub, mul, jnz)
- Simple loops
- Edge cases (empty program, no mul instructions)
- Parsing logic

## Implementation Details

The interpreter maintains:
- 8 registers (a-h) initialized to 0
- Instruction pointer (ip) starting at 0
- Multiplication counter (mul_count) starting at 0

The execution loop runs while `0 <= ip < len(instructions)`:
- **set X Y**: Sets register X to value of Y
- **sub X Y**: Subtracts Y from register X
- **mul X Y**: Multiplies register X by Y, increments mul_count
- **jnz X Y**: Jumps by offset Y if X is not zero

Key implementation detail: The `jnz` instruction handles the instruction pointer itself (either jumps or increments), while all other instructions execute and then increment ip by 1. This prevents double-incrementing.

## Testing Process

### Unit Tests (test_solution.py)
All 9 test functions passed successfully:
- ✓ get_value tests (register and literal resolution)
- ✓ set instruction tests
- ✓ sub instruction tests
- ✓ mul instruction tests (including counter verification)
- ✓ jnz instruction tests (jump and no-jump cases)
- ✓ loop test (verifies mul counting in loops)
- ✓ no mul test (programs without mul instructions)
- ✓ empty program test
- ✓ parsing test (handles empty lines correctly)

### Integration Test
Ran the solution on the actual input from `input.md`:
- **Result**: 4225
- **Execution time**: < 1 second
- **Determinism**: Verified by running 3 times, all produced 4225

### Test Coverage
The test suite validates:
1. All 4 instruction types work correctly
2. Register state management
3. Instruction pointer handling (including jumps)
4. Mul counter accuracy (only increments on mul instructions)
5. Loop execution and termination
6. Parsing handles empty lines
7. Negative number handling
8. Edge cases (empty program, no mul instructions)

## Results

- **Final Answer**: 4225
- **All tests passed**: 9/9 test functions
- **Execution verified**: Deterministic behavior confirmed
- **Performance**: Excellent (< 1 second execution time)

## Verification

The solution meets all acceptance criteria:
- ✓ Correctly parses and executes all 4 instruction types
- ✓ Accurately tracks mul instruction invocations
- ✓ Handles jumps and loops correctly
- ✓ Terminates when instruction pointer goes out of bounds
- ✓ All unit tests pass
- ✓ Deterministic execution (same result on multiple runs)
- ✓ Fast execution (< 1 second)
- ✓ Clean, simple implementation following the plan

The implementation successfully solves the problem with a clear, well-tested solution.
