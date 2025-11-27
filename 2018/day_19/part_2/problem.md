# Problem Report: Instruction Pointer Simulation - Part 2

## Context from Part 1

In Part 1, we implemented a CPU simulator with 6 registers (numbered 0-5) that can bind the instruction pointer to one of these registers, allowing for flow control through jump operations. The program executes assembly-like instructions until it halts, and we needed to find the final value in register 0.

**Part 1 Result**: With all registers starting at 0, the program halted with register 0 containing the value **1056**.

## Part 2: What Changed

A new background process has started that appears identical to Part 1, but with one critical difference:

**Register 0 now starts with the value 1 (instead of 0)**.

All other registers (1-5) still start at 0.

## Objective

**Find the value left in register 0 when the program halts with register 0 initialized to 1.**

## Input Format

The input is identical to Part 1:

1. **Declaration line**: `#ip N` where N is the register number (0-5) that the instruction pointer is bound to
2. **Instructions**: Multiple lines, each containing an operation with the format:
   - `opcode A B C`
   - Where `opcode` is the operation name, and A, B, C are integer parameters

### Available Opcodes

Same as Part 1:
- **Addition**: `addr` (add register), `addi` (add immediate)
- **Multiplication**: `mulr` (multiply register), `muli` (multiply immediate)
- **Bitwise AND**: `banr` (AND register), `bani` (AND immediate)
- **Bitwise OR**: `borr` (OR register), `bori` (OR immediate)
- **Assignment**: `setr` (set register), `seti` (set immediate)
- **Comparison**: `gtir` (greater-than immediate/register), `gtri` (greater-than register/immediate), `gtrr` (greater-than register/register)
- **Equality**: `eqir` (equal immediate/register), `eqri` (equal register/immediate), `eqrr` (equal register/register)

Each opcode operates as: `opcode A B C` stores the result in register C.

## Execution Model

### Initial State (KEY DIFFERENCE)
- **Register 0**: starts at **1** (not 0!)
- **Registers 1-5**: start at 0
- **IP (instruction pointer)**: starts at 0

### Instruction Pointer Binding
When the instruction pointer (IP) is bound to a register (specified by `#ip N`):
1. **Before each instruction**: The current IP value is written to register N
2. **Execute instruction**: The instruction is executed normally
3. **After each instruction**: The value in register N is written back to the IP
4. **Increment**: The IP is incremented by 1 (even if the instruction modified register N)

### Program Flow
- IP starts at 0
- Program halts when IP points outside the instruction list (before or after valid indices)

### Jump Behavior
Because the IP is incremented after writing back from the bound register:
- Instructions must set the bound register to (target_instruction - 1) to jump to target_instruction
- `setr`/`seti` can function as absolute jumps
- `addr`/`addi` can function as relative jumps

## Expected Output

A single integer: **the value in register 0 when the program halts**.

## Important Notes

1. **Performance Consideration**: Since the initial value of register 0 has changed, the program's behavior may be significantly different. The program may:
   - Take much longer to execute
   - Follow different code paths
   - Produce a much larger result

2. **Optimization Opportunity**: If the program takes too long to simulate directly, consider analyzing what the program is actually computing (reverse engineering the assembly) and implementing the algorithm directly in a more efficient way.

3. **The actual input program** is the same as Part 1 (found in input.md), but the initial register state is different.

## Implementation Strategy

1. Use the same CPU simulator from Part 1
2. **Modify the initial state**: Set `registers[0] = 1` instead of 0
3. Execute the program
4. If execution is too slow, analyze the program to understand what it computes and optimize
