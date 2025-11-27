# Problem Report: Intcode Computer Simulator

## Objective
Implement an Intcode computer simulator that processes a list of integers according to specific opcodes, then report the value at position 0 after the program halts.

## Input Format
- A single line containing comma-separated integers
- Example: `1,0,0,3,1,1,2,3,1,3,4,3,...`

## Intcode Computer Specification

### Memory Model
- The program is a list of integers stored at sequential positions (0-indexed)
- Positions can be both instructions and data
- Values at positions can be modified during execution

### Instruction Format
- Instructions are processed in groups of 4 integers: `opcode, param1, param2, param3`
- After processing each instruction, advance the instruction pointer by 4 positions

### Opcodes

| Opcode | Operation | Description |
|--------|-----------|-------------|
| 1 | ADD | Read values from positions `param1` and `param2`, add them, store result at position `param3` |
| 2 | MULTIPLY | Read values from positions `param1` and `param2`, multiply them, store result at position `param3` |
| 99 | HALT | Stop execution immediately |

### Execution Flow
1. Start at position 0
2. Read the opcode at the current position
3. If opcode is 99, halt
4. If opcode is 1 or 2, read the next 3 values as position references
5. Perform the operation using values AT those positions (not the position numbers themselves)
6. Store the result at the position specified by param3
7. Advance instruction pointer by 4
8. Repeat from step 2

## Pre-Processing Requirement
**IMPORTANT**: Before running the program, modify the input:
- Set position 1 to value `12`
- Set position 2 to value `2`

## Expected Output
- A single integer: the value at position 0 after the program halts

## Examples

| Initial State | Final State | Explanation |
|---------------|-------------|-------------|
| `1,0,0,0,99` | `2,0,0,0,99` | mem[0] + mem[0] = 1+1 = 2, stored at pos 0 |
| `2,3,0,3,99` | `2,3,0,6,99` | mem[3] * mem[0] = 3*2 = 6, stored at pos 3 |
| `2,4,4,5,99,0` | `2,4,4,5,99,9801` | mem[4] * mem[4] = 99*99 = 9801, stored at pos 5 |
| `1,1,1,4,99,5,6,0,99` | `30,1,1,4,2,5,6,0,99` | Multiple operations |

## Walkthrough Example
Given: `1,9,10,3,2,3,11,0,99,30,40,50`

1. Position 0: opcode 1 (ADD)
   - Read positions 9 and 10 → values 30 and 40
   - 30 + 40 = 70
   - Store 70 at position 3
   - Memory: `1,9,10,70,2,3,11,0,99,30,40,50`

2. Position 4: opcode 2 (MULTIPLY)
   - Read positions 3 and 11 → values 70 and 50
   - 70 * 50 = 3500
   - Store 3500 at position 0
   - Memory: `3500,9,10,70,2,3,11,0,99,30,40,50`

3. Position 8: opcode 99 (HALT)
   - Stop execution
   - Final answer: 3500 (value at position 0)
