# Implementation Summary

## Overview
Successfully implemented an assembunny code interpreter that executes assembly-like instructions with dynamic instruction modification via the toggle (`tgl`) instruction. The interpreter processes a series of instructions and returns the final value in register `a`.

## Files Created
- **solution.py**: Main implementation file containing the `AssembunnyInterpreter` class and all necessary methods

## Implementation Details

### Architecture
The solution uses an object-oriented approach with a single `AssembunnyInterpreter` class that encapsulates:
- **Registers**: Dictionary storing values for registers a, b, c, d (initialized with a=7, others=0)
- **Instructions**: Mutable list of parsed instructions that can be modified by `tgl`
- **Program Counter (PC)**: Integer tracking the current instruction position

### Key Components

1. **Instruction Parsing** (`parse_instructions`):
   - Splits input text into individual instructions
   - Stores each instruction as a list: `[opcode, arg1, arg2]`
   - Arguments stored as strings for later type resolution

2. **Helper Functions**:
   - `is_register(value)`: Validates if a value is a register name (a, b, c, d)
   - `get_value(arg)`: Resolves argument value (returns register value or converts to integer)

3. **Instruction Execution**:
   - `execute_cpy(x, y)`: Copies value x to register y (validates destination is a register)
   - `execute_inc(x)`: Increments register x (validates x is a register)
   - `execute_dec(x)`: Decrements register x (validates x is a register)
   - `execute_jnz(x, y)`: Jumps y instructions if x is not zero (supports register/literal for both args)
   - `execute_tgl(x)`: Toggles instruction at offset x from current position

4. **Toggle Logic**:
   - One-argument instructions: `inc` ↔ `dec` (all others become `inc`)
   - Two-argument instructions: `jnz` ↔ `cpy` (all others become `jnz`)
   - Handles out-of-bounds toggles gracefully (no-op)
   - Modifies instruction opcode in-place, preserving arguments

5. **Main Execution Loop** (`run`):
   - Executes instructions sequentially while PC is within bounds
   - Dispatches to appropriate execution function based on opcode
   - Handles invalid instructions by skipping them
   - Returns final value of register a

## Testing Process

### Phase 1: Basic Instruction Tests
Tested all basic instructions individually:
- **Copy (cpy)**: Verified copying from literals and registers
- **Increment (inc)**: Verified register incrementation
- **Decrement (dec)**: Verified register decrementation
- **Jump (jnz)**: Verified conditional jumps (taken/not taken, forward/backward, with literals and registers)

**Result**: All basic instruction tests passed

### Phase 2: Toggle Instruction Tests
Tested toggle functionality comprehensively:
- **One-argument toggle**: Verified `inc` → `dec` transformation
- **Two-argument toggle**: Verified `jnz` → `cpy` transformation
- **Out-of-bounds toggle**: Verified graceful handling when target is outside program
- **Problem example**: Verified the exact example from problem statement (expected a=3)
- **Self-toggling**: Verified `tgl` can toggle itself
- **Multiple toggles**: Verified same instruction can be toggled multiple times

**Result**: All toggle tests passed, including the problem's example

### Phase 3: Advanced Tests
Tested complex scenarios:
- **Invalid instructions**: Verified `cpy` with non-register destination is skipped
- **Loops**: Verified basic loop functionality with backward jumps
- **Register as offset**: Verified using register values as jump offsets

**Result**: All advanced tests passed

### Phase 4: Actual Input Test
Ran the interpreter with the actual problem input:
- Initial state: `a=7, b=0, c=0, d=0`
- Execution completed without errors
- **Final result: 11340**
- Verified deterministic output (multiple runs produce same result)
- Execution time: < 1 second

**Result**: Solution produces consistent output of **11340**

## Key Design Decisions

1. **Mutable Instruction List**: Used a mutable list for instructions to allow `tgl` to modify opcodes in-place
2. **String Storage**: Stored all arguments as strings during parsing, resolving types during execution via `get_value()`
3. **Validation**: Added validation checks for register operations to handle invalid instructions gracefully
4. **In-place Modification**: Toggle modifies only the opcode (index 0) while preserving arguments
5. **Clean Separation**: Each instruction has its own execution function for clarity and maintainability

## Challenges Encountered

1. **Test Case Expectations**: Initial test cases had incorrect expectations for jump offsets. Resolved by carefully tracing through execution flow.
2. **Toggle Offset Calculation**: Ensured toggle offset is relative to current PC position (PC + offset)
3. **Invalid Instruction Handling**: Implemented proper validation to skip invalid instructions created by toggle operations

## Verification

The implementation successfully:
- Executes all 5 instruction types correctly
- Handles dynamic instruction modification via `tgl`
- Validates and skips invalid instructions
- Manages program counter and jumps correctly
- Returns the correct final value for register `a` (11340)
- Runs deterministically with consistent results
- Completes execution in reasonable time

## Conclusion

The assembunny code interpreter is fully functional and correctly solves the problem. All test cases pass, including the provided example and the actual puzzle input. The final answer is **11340**.
