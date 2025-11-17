# Implementation Plan: Assembunny Code Interpreter with Toggle

## Problem Analysis

We need to build an interpreter for assembunny assembly-like code that:
- Executes 5 instruction types: `cpy`, `inc`, `dec`, `jnz`, `tgl`
- Handles dynamic instruction modification via `tgl` during runtime
- Manages 4 registers (a, b, c, d) with initial values: a=7, b=0, c=0, d=0
- Returns the final value in register `a`

### Key Challenges
1. **Dynamic Code Modification**: The `tgl` instruction can change other instructions during execution
2. **Invalid Instructions**: After toggling, some instructions may become invalid (e.g., `cpy 1 2`)
3. **Nested Loops**: The input contains nested loops that could be inefficient if not optimized
4. **Complex Jump Logic**: `jnz` can use both registers and literals for both arguments

### Algorithm Efficiency Considerations
Looking at the input:
- Lines 5-8: A loop multiplying b and c, adding to a (multiplication operation)
- Lines 12-16: Another loop (copying/incrementing pattern)
- Lines 20-26: Nested loops adding c*d to a (84*75 = 6300 additions)

The algorithm is O(n*m) where n and m are values in registers, which could be very large after initial computations. However, since this is an interpreter simulation, we cannot optimize the logic itself - we must execute instruction by instruction.

## Implementation Steps

### Step 1: Data Structure Setup
**File: solution.py**

1. Create a class `AssembunnyInterpreter`:
   - `registers`: Dictionary to store register values `{'a': 7, 'b': 0, 'c': 0, 'd': 0}`
   - `instructions`: List of parsed instructions (mutable for toggle)
   - `pc`: Program counter (instruction pointer), starts at 0

2. Define instruction representation:
   - Each instruction stored as a list: `[opcode, arg1, arg2]`
   - Example: `['cpy', 'a', 'b']` or `['inc', 'a', None]`

### Step 2: Input Parsing
**Function: `parse_instructions(input_text)`**

1. Split input text by newlines
2. For each line:
   - Strip whitespace
   - Skip empty lines
   - Split by spaces to get opcode and arguments
   - Store as list: `[opcode, arg1, arg2]` (arg2 is None for one-arg instructions)
   - **Important**: Store all arguments as strings (e.g., `['cpy', '5', 'a']`). The `get_value()` function will handle type conversion during execution.
3. Return list of parsed instructions

### Step 3: Helper Functions

**Function: `is_register(value)`**
- Check if value is one of: 'a', 'b', 'c', 'd'
- Return boolean

**Function: `get_value(arg)`**
- If `arg` is a register name, return register value
- Otherwise, convert to integer and return
- This handles both literal values and register references

### Step 4: Instruction Execution Functions

**Function: `execute_cpy(x, y)`**
1. Check if `y` is a valid register (not a number)
2. If invalid, skip (do nothing)
3. Otherwise: `registers[y] = get_value(x)`
4. Increment PC by 1

**Function: `execute_inc(x)`**
1. Check if `x` is a valid register
2. If invalid, skip
3. Otherwise: `registers[x] += 1`
4. Increment PC by 1

**Function: `execute_dec(x)`**
1. Check if `x` is a valid register
2. If invalid, skip
3. Otherwise: `registers[x] -= 1`
4. Increment PC by 1

**Function: `execute_jnz(x, y)`**
1. Get the value of `x` using `get_value(x)`
2. If value is not zero:
   - Get jump offset using `get_value(y)`
   - `pc += offset`
3. Otherwise:
   - `pc += 1`

**Function: `execute_tgl(x)`**
1. Get offset value using `get_value(x)`
2. Calculate target instruction index: `target = pc + offset`
3. If target is out of bounds (< 0 or >= len(instructions)), skip
4. Otherwise, toggle the instruction at `target`:
   - Get the instruction: `instr = instructions[target]`
   - Count arguments (check if arg2 is None)
   - If one-argument instruction (arg2 is None):
     - If opcode is 'inc', change to 'dec': `instructions[target][0] = 'dec'`
     - Otherwise (including 'dec' and 'tgl'), change to 'inc': `instructions[target][0] = 'inc'`
   - If two-argument instruction (arg2 is not None):
     - If opcode is 'jnz', change to 'cpy': `instructions[target][0] = 'cpy'`
     - Otherwise (including 'cpy'), change to 'jnz': `instructions[target][0] = 'jnz'`
   - **Note**: Modify only the opcode (index 0) in-place; keep arguments unchanged
5. Increment PC by 1

### Step 5: Main Execution Loop

**Function: `run()`**
1. While `pc` is within bounds (0 <= pc < len(instructions)):
   - Get current instruction: `instr = instructions[pc]`
   - Extract opcode and arguments
   - Match opcode and call corresponding execute function:
     - 'cpy': `execute_cpy(arg1, arg2)`
     - 'inc': `execute_inc(arg1)`
     - 'dec': `execute_dec(arg1)`
     - 'jnz': `execute_jnz(arg1, arg2)`
     - 'tgl': `execute_tgl(arg1)`
   - **Note**: Given the toggle rules, only the 5 known opcodes can exist in the instructions list. If an unknown opcode somehow appears, treat it as a no-op and increment PC by 1.
2. Return `registers['a']`

### Step 6: Main Function

**Function: `main()`**
1. Read input from file 'input.md'
2. Create interpreter instance with initial register values
3. Parse instructions
4. Run the interpreter
5. Print the final value of register `a`

## Code Structure

```
solution.py
├── class AssembunnyInterpreter
│   ├── __init__(self, initial_a=7)
│   ├── parse_instructions(self, input_text)
│   ├── is_register(self, value)
│   ├── get_value(self, arg)
│   ├── execute_cpy(self, x, y)
│   ├── execute_inc(self, x)
│   ├── execute_dec(self, x)
│   ├── execute_jnz(self, x, y)
│   ├── execute_tgl(self, x)
│   └── run(self)
└── main()
```

## Implementation Notes

1. **Mutability**: Instructions list must be mutable since `tgl` modifies it
2. **Argument Storage**: Store all arguments as strings during parsing; use `get_value()` for type conversion during execution
3. **Instruction Mutation**: When toggling, modify only the opcode (index 0) in-place: `instructions[target][0] = new_opcode`
4. **Validation**: Always validate register names before modifying
5. **Value Resolution**: Use `get_value()` consistently to handle both literals and registers
6. **PC Management**: Each execute function is responsible for updating PC
7. **Bounds Checking**: Always check PC and toggle targets are within valid range

## Expected Runtime

The input contains nested loops that will execute many iterations. The actual runtime depends on the register values calculated during execution. While the input has only 27 instructions, the number of instructions executed can be much larger due to loops. The solution should complete within a reasonable time (under a minute) for the given input size.

**Note**: The time complexity is O(instructions executed), which can be much larger than O(input size) due to loops, potentially reaching millions of iterations for nested loops with large register values.

## Optimization Opportunities (Not Implemented)

While we could recognize patterns like multiplication loops and optimize them, for this problem we'll execute instruction-by-instruction as specified. The straightforward interpretation approach is sufficient for the input size.
