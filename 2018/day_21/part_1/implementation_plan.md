# Implementation Plan: Chronal Conversion - Part 1

## Problem Analysis

This problem requires us to:
1. Parse and execute a custom assembly-like language with 6 registers
2. Find the lowest non-negative integer for register 0 that causes the program to halt in the fewest instructions
3. The program binds one register to the instruction pointer (IP)
4. The program halts when the IP goes out of bounds

### Key Insights

1. **Program Structure**: The input has 31 instructions (indices 0-30). Instruction 29 is `eqrr 5 0 3` - this compares register 5 with register 0 (our input). This is the **only instruction that reads from register 0**.

2. **Halting Condition**: The program will only halt when it jumps out of bounds. At instruction 29, r5 is compared with r0:
   - If r5 == r0, then r3 = 1
   - At instruction 30 (`addr 3 2 2`), the IP register (r2) becomes r3 + 30
   - If r3 = 1: r2 = 31, which after increment becomes 32 (out of bounds → halt)
   - If r3 = 0: r2 = 30, which after increment becomes 31 (continues to instruction 31)

3. **Optimal Strategy**: To halt in the fewest instructions, we want the program to reach instruction 29 on its **first iteration**, with register 5 containing a specific value:
   - Simulate the program execution with r0 = 0 (or any value)
   - Monitor when it **first** reaches instruction 29
   - Capture the value in register 5 at that moment
   - That value is what we should set register 0 to for immediate halting
   - **Justification**: Since instruction 29 is the only place r0 is checked, and we want minimum instructions, we must capture the first occurrence. Any later occurrence would require more instructions to execute.

4. **Validation Loop**: Instructions 0-4 implement a validation check (123 & 456 == 72), which should pass and jump to instruction 6, skipping the infinite loop at instruction 5.

## Implementation Steps

### Step 1: Define the Instruction Set

Create a class or dictionary to handle all 16 opcodes:
- **Addition**: `addr`, `addi`
- **Multiplication**: `mulr`, `muli`
- **Bitwise AND**: `banr`, `bani`
- **Bitwise OR**: `borr`, `bori`
- **Assignment**: `setr`, `seti`
- **Greater-than**: `gtir`, `gtri`, `gtrr`
- **Equality**: `eqir`, `eqri`, `eqrr`

Each instruction takes 4 parameters: `opcode inputA inputB outputC`

### Step 2: Parse the Input

1. Read the first line to extract the IP register binding (e.g., `#ip 2` → IP bound to register 2)
2. Parse each subsequent instruction line into:
   - Opcode string
   - Three integer parameters (A, B, C)
3. Store instructions in a list indexed by their line number

### Step 3: Implement the VM Execution Engine

Create a function to execute the program:
```
registers = [0, 0, 0, 0, 0, 0]  # 6 registers initialized to 0
ip = 0  # instruction pointer
ip_register = <parsed from input>
instructions = <parsed from input>

while 0 <= ip < len(instructions):
    # Write IP to bound register
    registers[ip_register] = ip

    # Execute instruction at IP
    opcode, a, b, c = instructions[ip]
    execute_instruction(opcode, a, b, c, registers)

    # Read IP from bound register
    ip = registers[ip_register]

    # Increment IP
    ip += 1
```

### Step 4: Monitor for First Comparison with Register 0

Instead of setting register 0 initially, we:
1. Leave register 0 at 0 (or any value)
2. Monitor when the IP reaches instruction 29 (the `eqrr 5 0 3` instruction)
3. When we reach instruction 29 for the first time:
   - Record the value currently in register 5
   - This is our answer (the value to put in register 0 to halt quickly)
4. Return this value

### Step 5: Optimization Considerations

**Runtime Analysis**: The program contains loops (instructions 19-27 form a loop). The program might:
- Execute thousands or millions of instructions before reaching instruction 30
- Need efficient register operations (simple array access)

**Key Optimization**: We don't need to run the program to completion. We only need to:
1. Run until we first hit instruction 29
2. Capture register 5's value at that moment
3. Exit

This should be reasonably fast since we're looking for the first occurrence.

**Optional Debug Logging**: Consider adding a flag to enable trace logging:
- Print IP, current instruction, and register state after each instruction
- This helps verify the execution path and debug any issues
- Can be disabled for production run

### Step 6: Implementation Structure

```python
def parse_input(filename):
    """Parse the instruction file and return ip_register and instructions list"""
    pass

def execute_instruction(opcode, a, b, c, registers):
    """Execute a single instruction on the registers"""
    pass

def find_halting_value(ip_register, instructions):
    """
    Simulate program execution and find the value in register 5
    when instruction 29 is first reached
    """
    registers = [0, 0, 0, 0, 0, 0]
    ip = 0

    while 0 <= ip < len(instructions):
        # Check if we're at instruction 29 (the eqrr 5 0 3)
        if ip == 29:
            return registers[5]

        registers[ip_register] = ip
        opcode, a, b, c = instructions[ip]
        execute_instruction(opcode, a, b, c, registers)
        ip = registers[ip_register]
        ip += 1

    return None

def main():
    ip_register, instructions = parse_input('input.md')
    result = find_halting_value(ip_register, instructions)
    print(result)
```

## Algorithm Efficiency

- **Time Complexity**: O(n) where n is the number of instructions executed before reaching instruction 29 the first time. This could be large (potentially millions) but is bounded by the program's logic.
- **Space Complexity**: O(m) where m is the number of instructions (31 in our case). We need 6 registers (constant) plus the instruction list.

## Edge Cases to Handle

1. **IP Register Binding**: Ensure we correctly read/write the IP to the bound register before/after each instruction
2. **Instruction 29 Check**: Must check IP **before** executing the instruction, not after
3. **Immediate vs Register Values**: Different opcodes interpret parameters differently (some use immediate values, some use register indices)
4. **Integer Size**: Python handles arbitrary precision integers, but bitwise operations should work correctly with the masking values used (e.g., `bani 5 16777215 5`)
