# Problem Report: Instruction Pointer Simulation

## Overview
We need to simulate a CPU with 6 registers (numbered 0-5) that can bind the instruction pointer to one of these registers, allowing for flow control through jump operations. The program will execute a series of assembly-like instructions until it halts, and we need to determine the final value in register 0.

## Objective
**Find the value left in register 0 when the program halts.**

## Input Format

The input consists of:

1. **Declaration line**: `#ip N` where N is the register number (0-5) that the instruction pointer is bound to
2. **Instructions**: Multiple lines, each containing an operation with the format:
   - `opcode A B C`
   - Where `opcode` is the operation name, and A, B, C are integer parameters

### Available Opcodes

The opcodes from the previous device implementation include:
- **Addition**: `addr` (add register), `addi` (add immediate)
- **Multiplication**: `mulr` (multiply register), `muli` (multiply immediate)
- **Bitwise AND**: `banr` (AND register), `bani` (AND immediate)
- **Bitwise OR**: `borr` (OR register), `bori` (OR immediate)
- **Assignment**: `setr` (set register), `seti` (set immediate)
- **Comparison**: `gtir` (greater-than immediate/register), `gtri` (greater-than register/immediate), `gtrr` (greater-than register/register)
- **Equality**: `eqir` (equal immediate/register), `eqri` (equal register/immediate), `eqrr` (equal register/register)

Each opcode operates as: `opcode A B C` stores the result in register C.

## Execution Model

### Instruction Pointer Binding
When the instruction pointer (IP) is bound to a register (specified by `#ip N`):
1. **Before each instruction**: The current IP value is written to register N
2. **Execute instruction**: The instruction is executed normally
3. **After each instruction**: The value in register N is written back to the IP
4. **Increment**: The IP is incremented by 1 (even if the instruction modified register N)

### Program Flow
- IP starts at 0
- All registers start at 0
- Instructions are indexed starting from 0 (first instruction after `#ip` line)
- Program halts when IP points outside the instruction list (before or after valid indices)

### Jump Behavior
Because the IP is incremented after writing back from the bound register:
- Instructions must set the bound register to (target_instruction - 1) to jump to target_instruction
- `setr`/`seti` can function as absolute jumps
- `addr`/`addi` can function as relative jumps

## Expected Output

A single integer: **the value in register 0 when the program halts**.

## Example

Given program:
```
#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5
```

Execution trace:
- ip=0: [0, 0, 0, 0, 0, 0] → seti 5 0 1 → [0, 5, 0, 0, 0, 0]
- ip=1: [1, 5, 0, 0, 0, 0] → seti 6 0 2 → [1, 5, 6, 0, 0, 0]
- ip=2: [2, 5, 6, 0, 0, 0] → addi 0 1 0 → [3, 5, 6, 0, 0, 0] (jumps to ip=4)
- ip=4: [4, 5, 6, 0, 0, 0] → setr 1 0 0 → [5, 5, 6, 0, 0, 0] (jumps to ip=6)
- ip=6: [6, 5, 6, 0, 0, 0] → seti 9 0 5 → [6, 5, 6, 0, 0, 9]
- ip=7: Program halts (out of bounds)

**Result: register 0 = 6**

## Implementation Notes

1. Parse the `#ip` declaration to determine which register is bound to the IP
2. Parse all instructions into a list
3. Initialize 6 registers to 0 and IP to 0
4. Execute loop:
   - Check if IP is within valid instruction range (0 to len(instructions)-1)
   - Write IP value to the bound register
   - Execute the instruction at position IP
   - Read the bound register value back to IP
   - Increment IP by 1
5. When the program halts, return the value in register 0
