# Problem Report: Chronal Classification - Part 2

## Context from Part 1

In Part 1, we analyzed a device with a CPU that has 4 registers (numbered 0-3) and 16 different opcodes. The device's manual lists the opcode names but doesn't specify which opcode number (0-15) corresponds to which operation. We were given sample observations that showed the "Before" state, an instruction execution, and the "After" state of the registers.

Part 1 found that **590 samples** behaved like three or more opcodes, meaning multiple opcodes could have produced the observed transformation.

## The 16 Opcodes (Reference)

### Addition
- **addr**: register[C] = register[A] + register[B]
- **addi**: register[C] = register[A] + value B

### Multiplication
- **mulr**: register[C] = register[A] * register[B]
- **muli**: register[C] = register[A] * value B

### Bitwise AND
- **banr**: register[C] = register[A] & register[B]
- **bani**: register[C] = register[A] & value B

### Bitwise OR
- **borr**: register[C] = register[A] | register[B]
- **bori**: register[C] = register[A] | value B

### Assignment
- **setr**: register[C] = register[A] (B is ignored)
- **seti**: register[C] = value A (B is ignored)

### Greater-than Testing
- **gtir**: register[C] = 1 if value A > register[B], else 0
- **gtri**: register[C] = 1 if register[A] > value B, else 0
- **gtrr**: register[C] = 1 if register[A] > register[B], else 0

### Equality Testing
- **eqir**: register[C] = 1 if value A == register[B], else 0
- **eqri**: register[C] = 1 if register[A] == value B, else 0
- **eqrr**: register[C] = 1 if register[A] == register[B], else 0

## What We Are Trying to Solve in Part 2

We need to:
1. **Deduce the mapping** from opcode numbers (0-15) to opcode names using the sample observations from Part 1
2. **Execute a test program** using the deduced opcode mappings
3. **Return the value in register 0** after the test program completes

## Input Format

The input file has two sections separated by a double blank line:

### Section 1: Sample Observations (lines 1-3128)
Same format as Part 1:
```
Before: [r0, r1, r2, r3]
opcode A B C
After:  [r0, r1, r2, r3]
<blank line>
```

This section provides samples we can use to deduce which opcode number corresponds to which operation.

### Section 2: Test Program (lines 3130-4022)
After the double blank line, the rest of the input is the test program. Each line is a single instruction in the format:
```
opcode A B C
```

These are the instructions we need to execute after determining the opcode mappings.

## Task Details

### Phase 1: Deduce Opcode Mappings

For each sample in Section 1:
1. Check which of the 16 opcodes could produce the observed transformation
2. Track which opcode numbers are compatible with which opcode names

Use constraint satisfaction or deduction to determine the unique mapping from each opcode number (0-15) to its corresponding opcode name. Some samples will narrow down possibilities, and through iterative elimination, we should be able to determine all 16 mappings uniquely.

### Phase 2: Execute Test Program

1. Initialize all 4 registers to 0: `[0, 0, 0, 0]`
2. For each instruction in the test program:
   - Read the opcode number and parameters A, B, C
   - Look up the opcode name from our deduced mapping
   - Execute the corresponding operation on the registers
   - Update the register state
3. Continue until all instructions are executed

## Expected Output

A single integer: **the value contained in register 0** after executing the entire test program.

## Algorithm Strategy

1. Parse both sections of the input file
2. For each sample, determine which opcodes are compatible with that sample
3. Build a mapping of possible opcodes for each opcode number
4. Use constraint propagation or iterative elimination to uniquely determine all 16 mappings:
   - Find opcode numbers that can only be one opcode name
   - Remove that opcode name from all other opcode numbers' possibilities
   - Repeat until all mappings are unique
5. Execute the test program using the determined mappings
6. Return register[0]
