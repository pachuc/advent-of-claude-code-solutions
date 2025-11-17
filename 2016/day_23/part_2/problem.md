# Problem Report: Assembunny Code Interpreter - Part 2

## Part 1 Context
In Part 1, we implemented an assembunny code interpreter with a special `tgl` (toggle) instruction that could modify other instructions during runtime. The interpreter simulates a keypad logic circuit for a safe.

We ran the program with register `a` initialized to `7` (representing the number of eggs counted in a painting) and found the answer **11340**.

## Part 2 Objective
The safe didn't open with the first answer. Upon re-examining the painting, we realize we undercounted the eggs - there are actually `12` colored eggs (not just 7).

We need to run the same assembunny interpreter with register `a` initialized to **12** instead of 7, and determine what value should be sent to the safe.

## Key Change from Part 1
- **Initial register state**: Register `a` now starts with the value `12` (instead of 7)
- All other registers (`b`, `c`, `d`) still start at `0`
- The program instructions remain exactly the same

## Input
The same assembunny instructions from Part 1, including:
- `cpy x y` - copies value `x` into register `y`
- `inc x` - increments register `x` by 1
- `dec x` - decrements register `x` by 1
- `jnz x y` - jumps `y` instructions if `x` is not zero
- `tgl x` - toggles the instruction at offset `x` from the current instruction

## Instruction Set (Same as Part 1)

### Standard Instructions
- `cpy x y`: Copy value from `x` to register `y` (`x` can be a number or register)
- `inc x`: Increment register `x`
- `dec x`: Decrement register `x`
- `jnz x y`: Jump `y` instructions if `x` is not zero (`x` and `y` can be numbers or registers)

### Toggle Instruction (`tgl x`)
The `tgl x` instruction modifies the instruction located `x` positions away:
- **For one-argument instructions**:
  - `inc` becomes `dec`
  - Any other one-argument instruction becomes `inc`
- **For two-argument instructions**:
  - `jnz` becomes `cpy`
  - Any other two-argument instruction becomes `jnz`

### Toggle Rules
1. Arguments of toggled instructions remain unchanged
2. If toggle targets an instruction outside program bounds, nothing happens
3. Invalid instructions (e.g., `cpy 1 2`) are skipped during execution
4. If `tgl` toggles itself, the resulting instruction executes on the next iteration

## Expected Output
A single integer value: the final value in register `a` after all instructions have been executed.

## Performance Note
The puzzle hints that the program may take a long time to execute with the larger input value (12 vs 7), and mentions that "bunnies usually multiply" - suggesting there may be optimization opportunities in how the assembunny code implements multiplication using only increment/decrement operations.

**Potential approaches if the naive interpreter is too slow:**
1. Run the interpreter as-is and wait (may take several minutes)
2. Analyze the instruction patterns to detect multiplication loops (e.g., nested loops that implement `a = a + b*c`) and replace them with optimized operations
3. Reverse-engineer what the entire program computes mathematically and calculate the result directly

## Implementation Requirements
1. Initialize registers: `a=12`, `b=0`, `c=0`, `d=0`
2. Parse and execute each instruction sequentially (same interpreter as Part 1)
3. Handle dynamic instruction modification via `tgl`
4. Skip invalid instructions
5. Return the final value of register `a`

**Note**: The existing Part 1 solution can be reused by simply changing the initial value of register `a` from 7 to 12.
