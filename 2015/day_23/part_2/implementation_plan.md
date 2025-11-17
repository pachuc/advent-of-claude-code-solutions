# Implementation Plan: Computer Instruction Simulator (Part 2)

## Problem Analysis

This is a virtual machine simulator that executes a sequence of instructions on two registers (`a` and `b`). The key difference from Part 1 is that register `a` starts at `1` instead of `0`.

### Key Observations:
1. The instruction set is simple with 6 operations (hlf, tpl, inc, jmp, jie, jio)
2. The program has 48 instructions
3. There are loops in the code (negative jumps like `jmp -7`)
4. The initial value of `a=1` will affect control flow (particularly `jio a, +22` at line 1)
5. Register `b` is incremented at line 42, and the loop structure suggests it may be incremented multiple times
6. **Critical**: Jump offsets are relative to the current instruction position (if PC=5 and instruction is `jmp +3`, new PC = 5+3 = 8)

### Input Format:
- The file `input.md` contains plain text instructions, one per line
- No markdown formatting or code blocks to parse
- Lines can be read directly and parsed

### Algorithm Efficiency Considerations:
- The program contains loops, so we need to execute instruction-by-instruction
- Since this is a fixed program (48 instructions) with deterministic behavior, the runtime depends on how many iterations occur
- No optimization is needed beyond straightforward simulation
- The program will eventually terminate (no infinite loops given the structure)

## Implementation Steps

### Step 1: Parse Input Instructions
**Objective:** Read and parse the instruction file into a structured format

**Details:**
- Read all lines from input.md (plain text file, no markdown parsing needed)
- For each line, parse the instruction type and operands
- Store instructions in a list where index = instruction position
- Handle two instruction formats:
  - Single operand: `hlf r`, `tpl r`, `inc r`
  - Jump with offset: `jmp offset`
  - Two operands: `jie r, offset`, `jio r, offset`
- Strip whitespace and split on comma + space to separate operands
- Use `int()` to parse offsets (automatically handles '+' and '-' prefixes)

**Data Structure (using dictionaries for clarity):**
```python
instructions = [
    {"op": "jio", "reg": "a", "offset": 22},
    {"op": "inc", "reg": "a"},
    {"op": "jmp", "offset": 19},
    {"op": "tpl", "reg": "b"},
    ...
]
```

**Parsing Example:**
```python
def parse_instruction(line):
    parts = line.strip().replace(',', '').split()
    op = parts[0]

    if op in ['hlf', 'tpl', 'inc']:
        return {"op": op, "reg": parts[1]}
    elif op == 'jmp':
        return {"op": op, "offset": int(parts[1])}
    elif op in ['jie', 'jio']:
        return {"op": op, "reg": parts[1], "offset": int(parts[2])}
```

### Step 2: Initialize Registers and Program Counter
**Objective:** Set up the execution environment

**Details:**
- Create a dictionary for registers: `registers = {"a": 1, "b": 0}`
- Initialize program counter (PC): `pc = 0`
- PC tracks the current instruction index

### Step 3: Implement Instruction Execution Logic
**Objective:** Create functions to execute each instruction type

**Details:**

**CRITICAL**: The `execute_instruction` function must **return** the new PC value (not modify in place, since Python integers are immutable).

**3.1: Arithmetic Instructions** (all increment PC by 1)
- `hlf r`: `registers[r] //= 2`, then return `pc + 1`
- `tpl r`: `registers[r] *= 3`, then return `pc + 1`
- `inc r`: `registers[r] += 1`, then return `pc + 1`

**3.2: Jump Instructions**
- `jmp offset`: return `pc + offset` (unconditional relative jump)
- `jie r, offset`: If `registers[r] % 2 == 0`, return `pc + offset`, else return `pc + 1`
- `jio r, offset`: If `registers[r] == 1`, return `pc + offset`, else return `pc + 1`

**Jump Semantics:**
- All offsets are relative to the **current instruction**
- Example: At PC=10, `jmp +5` results in PC=15 (not 16)
- Example: At PC=10, `jie a, +3` with a=4 results in PC=13 (not 14)
- When jump condition is false, PC increments by 1 (normal progression)

**Implementation Approach:**
```python
def execute_instruction(inst, registers, pc):
    op = inst["op"]

    if op == "hlf":
        registers[inst["reg"]] //= 2
        return pc + 1
    elif op == "tpl":
        registers[inst["reg"]] *= 3
        return pc + 1
    elif op == "inc":
        registers[inst["reg"]] += 1
        return pc + 1
    elif op == "jmp":
        return pc + inst["offset"]
    elif op == "jie":
        if registers[inst["reg"]] % 2 == 0:
            return pc + inst["offset"]
        return pc + 1
    elif op == "jio":
        if registers[inst["reg"]] == 1:
            return pc + inst["offset"]
        return pc + 1
```

### Step 4: Main Execution Loop
**Objective:** Run the program until termination

**Details:**
```python
while 0 <= pc < len(instructions):
    instruction = instructions[pc]
    pc = execute_instruction(instruction, registers, pc)  # CRITICAL: Update pc with return value
```

**Termination Conditions:**
- `pc < 0`: Jumped before the first instruction (terminates)
- `pc >= len(instructions)`: Moved beyond the last instruction (terminates)
- For 48 instructions (indices 0-47), PC=48 or PC=-1 will terminate

**Loop Structure:**
- Check if PC is within bounds
- Fetch instruction at current PC
- Execute instruction (modifies registers, returns new PC)
- **Update PC with the returned value**
- Repeat until PC is out of bounds

**Optional Safety:**
- Add iteration counter to detect infinite loops during testing
- Set max iterations (e.g., 1,000,000) and raise error if exceeded
- Remove this check once verified the program terminates

### Step 5: Extract and Return Result
**Objective:** Get the final value of register `b`

**Details:**
- After the execution loop terminates, read `registers["b"]`
- Print or return this value as the answer

## Implementation Structure

```python
def parse_instructions(filename):
    """Parse input file into list of instruction dictionaries"""
    instructions = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:  # Skip empty lines
                parts = line.replace(',', '').split()
                op = parts[0]

                if op in ['hlf', 'tpl', 'inc']:
                    instructions.append({"op": op, "reg": parts[1]})
                elif op == 'jmp':
                    instructions.append({"op": op, "offset": int(parts[1])})
                elif op in ['jie', 'jio']:
                    instructions.append({"op": op, "reg": parts[1], "offset": int(parts[2])})

    return instructions

def execute_instruction(inst, registers, pc):
    """Execute a single instruction and return new PC value"""
    op = inst["op"]

    if op == "hlf":
        registers[inst["reg"]] //= 2
        return pc + 1
    elif op == "tpl":
        registers[inst["reg"]] *= 3
        return pc + 1
    elif op == "inc":
        registers[inst["reg"]] += 1
        return pc + 1
    elif op == "jmp":
        return pc + inst["offset"]
    elif op == "jie":
        if registers[inst["reg"]] % 2 == 0:
            return pc + inst["offset"]
        return pc + 1
    elif op == "jio":
        if registers[inst["reg"]] == 1:
            return pc + inst["offset"]
        return pc + 1

    # Should never reach here with valid input
    raise ValueError(f"Unknown instruction: {op}")

def simulate(instructions, initial_a=1, initial_b=0, verbose=False, max_iterations=1_000_000):
    """Run the simulation and return final register values"""
    registers = {"a": initial_a, "b": initial_b}
    pc = 0
    iterations = 0

    while 0 <= pc < len(instructions):
        if verbose:
            print(f"[{iterations}] PC={pc} | a={registers['a']}, b={registers['b']} | {instructions[pc]}")

        pc = execute_instruction(instructions[pc], registers, pc)
        iterations += 1

        if iterations > max_iterations:
            raise RuntimeError(f"Exceeded max iterations ({max_iterations}). Possible infinite loop.")

    if verbose:
        print(f"Program terminated at PC={pc} after {iterations} iterations")

    return registers

def main():
    """Main entry point"""
    instructions = parse_instructions("input.md")
    registers = simulate(instructions, initial_a=1, initial_b=0)
    print(registers["b"])

if __name__ == "__main__":
    main()
```

## Edge Cases to Handle

1. **Jump offsets**: Ensure positive and negative offsets work correctly
   - Test `jmp +5` and `jmp -3` both work
   - Verify offset is relative to current instruction, not next instruction

2. **Register parsing**: Split on comma and whitespace correctly
   - Input like `jio a, +22` should parse to reg="a", offset=22
   - The comma is a separator, not part of the register name

3. **Offset parsing**: Use `int()` which handles '+' and '-' automatically
   - `int("+22")` returns 22
   - `int("-7")` returns -7

4. **PC updates**: Ensure PC is captured from return value
   - CRITICAL: `pc = execute_instruction(...)` not just calling the function

5. **Input validation**: (Not required for AoC with known-good input)
   - Could add checks for invalid register names or malformed instructions
   - Skip for this script to keep it simple

## Performance Considerations

- **Time Complexity**: O(n) where n is the number of instructions executed (not just in the program, but total executions including loops)
- **Space Complexity**: O(m) where m is the number of instructions in the program (for storage)
- Given the program size (48 instructions) and likely iteration counts, performance should be excellent
- No optimization or memoization needed for this problem size

## Expected Execution Flow Analysis

Looking at the input:
1. **Line 1** (PC=0): `jio a, +22` - Since `a=1`, this WILL jump to PC=22 (instruction at index 22)
2. **Lines 2-22** (PC=1-21): Skipped due to initial jump
3. **Line 23** (PC=22): `jmp +19` - Jumps to PC=41
4. **Line 42** (PC=41): `jio a, +8` - If a=1, jump to PC=49 (terminate). Otherwise, continue.
5. **Line 43** (PC=42): `inc b` - Increments b
6. **Line 44** (PC=43): `jie a, +4` - If a is even, jump to PC=47, otherwise continue
7. **Line 45-46** (PC=44-45): `tpl a`, `inc a` - Executed if a is odd
8. **Line 47** (PC=46): `jmp +2` - Skip hlf instruction
9. **Line 48** (PC=47): `hlf a` - Executed if a is even
10. **Line 49** (PC=48): `jmp -7` - Jump back to PC=41, creating a loop

**Loop Analysis:**
- The loop (PC=41 to PC=48) repeats until `a == 1`
- Each iteration increments `b` once
- Register `a` is manipulated each iteration:
  - If a is odd: a = (a * 3) + 1
  - If a is even: a = a / 2
- This is similar to the Collatz sequence!
- Loop terminates when a reaches 1, at which point `jio a, +8` at PC=41 jumps to PC=49 (program end)

**Note:** The initial value of `a` determines the initial jump. With `a=1` (Part 2), we skip the first section. With `a=0` (Part 1), we would execute lines 2-22 first, building up a different initial value before entering the loop.
