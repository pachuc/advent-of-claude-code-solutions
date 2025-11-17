# Implementation Plan for Part 2

## Overview
Part 2 requires running the same assembunny interpreter with register `a` initialized to 12 instead of 7. However, the problem explicitly hints at performance issues with the phrase "bunnies usually multiply" - suggesting the code performs multiplication using nested inc/dec loops, which becomes extremely slow for larger values.

## Key Insight: Performance Optimization Required
With `a=12`, the program computes factorial-like operations. The unoptimized version would execute approximately 12! = 479,001,600 increments of `a` (plus additional decrements, jumps, and loop overhead), resulting in billions of total instruction executions. This would take hours or days without optimization. We need to detect and optimize multiplication patterns in the assembunny code.

## Reusing Part 1 Code
The Part 1 solution (`part_1_solution.py`) provides a complete, working interpreter. We can adapt it with minimal changes:
- Change `initial_a=7` to `initial_a=12`
- Add optimization to detect and fast-forward through multiplication loops
- Part 1 completed successfully with a=7 (result: 11340), confirming the base interpreter is correct

## Step-by-Step Implementation Plan

### Step 1: Copy and Adapt Part 1 Solution
**Files to reference**: `part_1_solution.py`

- Copy the entire `AssembunnyInterpreter` class from Part 1
- The existing implementation already handles all instruction types correctly:
  - `cpy`, `inc`, `dec`, `jnz`, `tgl`
  - Invalid instruction skipping
  - Dynamic instruction modification

### Step 2: Add Multiplication Pattern Detection
**Optimization target**: Detect nested loops that implement multiplication

**Pattern to recognize**:
```
cpy b c          # Copy multiplier to counter
inc a            # Accumulator increment
dec c            # Decrement counter
jnz c -2         # Loop back if counter non-zero
dec d            # Outer counter
jnz d -5         # Outer loop
```

This pattern adds `b` to `a`, `d` times (i.e., `a += b * d`), then sets `c` and `d` to 0.

**Detection logic**:
- When executing a loop, check if the current PC is at the start of a known multiplication pattern
- Verify the pattern matches exactly (instruction sequence and jump offsets)
- Check that registers referenced exist and have valid values
- Account for instruction modifications via `tgl` (pattern may not always be valid)

**Implementation approach**:
```python
def detect_multiplication_pattern(self):
    """
    Detect if current instruction is start of multiplication loop.
    Pattern: inc register in loop controlled by another register.
    Returns: (is_pattern, multiplier_reg, counter_reg, result_reg, skip_instructions)
    """
    # Check for specific instruction sequences
    # Return None if not a multiplication pattern
    # Return tuple with optimization parameters if pattern detected
```

### Step 3: Implement Fast-Forward Optimization
**When pattern detected**:
1. Calculate the result directly: `registers[result] += registers[multiplier] * registers[counter]`
2. Set counter registers to 0 (as they would be after loop completion)
3. Jump PC forward past the entire loop
4. Continue execution normally

**Safety considerations**:
- Only optimize if instructions haven't been toggled (track modified instructions)
- Verify all registers in pattern exist and are valid
- Handle edge cases (zero values, negative values)

### Step 4: Modify Initialization
Change the interpreter initialization:
```python
interpreter = AssembunnyInterpreter(initial_a=12)  # Changed from 7
```

### Step 5: Add Optimization Flag (Optional)
For debugging and verification:
```python
def __init__(self, initial_a=12, optimize=True):
    self.registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    self.instructions = []
    self.pc = 0
    self.modified_instructions = set()  # Track toggled instructions
    self.optimize = optimize  # Default to True for performance
    # ... rest of initialization
```

This allows testing both optimized and unoptimized versions for correctness. **Default is True** to ensure the solution completes in reasonable time.

### Step 6: Handle Toggle Instruction Interaction
**Critical consideration**: The `tgl` instruction can modify the code, potentially breaking optimization patterns.

**Implementation**:
- Track which instructions have been toggled
- Before applying optimization, verify pattern is still intact
- If any instruction in the pattern was toggled, skip optimization and execute normally

**Complete implementation of modified tracking**:
```python
def __init__(self, initial_a=12, optimize=True):
    self.registers = {'a': initial_a, 'b': 0, 'c': 0, 'd': 0}
    self.instructions = []
    self.pc = 0
    self.modified_instructions = set()  # Track toggled instruction indices
    self.optimize = optimize

def execute_tgl(self, x):
    """Execute tgl x: toggle instruction at offset x."""
    offset = self.get_value(x)
    target = self.pc + offset

    # Check if target is within bounds
    if target < 0 or target >= len(self.instructions):
        self.pc += 1
        return

    # Mark instruction as modified BEFORE toggling
    self.modified_instructions.add(target)

    # Toggle the instruction
    instr = self.instructions[target]
    opcode = instr[0]

    # Check if it's a one-argument or two-argument instruction
    if instr[2] is None:
        # One-argument instruction
        if opcode == 'inc':
            self.instructions[target][0] = 'dec'
        else:
            # Any other one-arg instruction (including dec, tgl) becomes inc
            self.instructions[target][0] = 'inc'
    else:
        # Two-argument instruction
        if opcode == 'jnz':
            self.instructions[target][0] = 'cpy'
        else:
            # Any other two-arg instruction (including cpy) becomes jnz
            self.instructions[target][0] = 'jnz'

    self.pc += 1
```

### Step 7: Optimization Implementation Strategy

**Conservative approach** (Recommended for correctness):
- Only optimize the most common pattern (lines 5-10)
- Detect at runtime, not ahead of time
- Fall back to normal execution if any uncertainty

**Pattern detection location** (optimized to avoid overhead):
```python
def run(self):
    while 0 <= self.pc < len(self.instructions):
        instr = self.instructions[self.pc]

        # Only check for multiplication pattern when at a 'cpy' instruction
        # This avoids pattern-matching overhead on inc, dec, jnz, and tgl instructions
        if instr[0] == 'cpy' and self.try_optimize_multiplication():
            continue

        # Normal instruction execution
        opcode = instr[0]
        # ... existing execution logic
```

### Step 8: Specific Pattern for This Input

Analyzing the input instructions (lines 5-10 in input.md):
```
Line 5:  cpy b c
Line 6:  inc a
Line 7:  dec c
Line 8:  jnz c -2
Line 9:  dec d
Line 10: jnz d -5
```

**This is a classic `a += b * d` pattern**, setting c and d to 0.

**Mathematical proof of equivalence**:
```
Original pattern:
  cpy b c      # c = b
  [inner loop]
    inc a      # a += 1
    dec c      # c -= 1
    jnz c -2   # loop while c != 0
  [inner loop runs b times, adds b to a]
  dec d        # d -= 1
  jnz d -5     # outer loop while d != 0

Effect: Inner loop runs b times (adding b to a), outer loop runs d times
Total: a += (b * d), with c = 0 and d = 0 after completion

Optimization: a += b * d; c = 0; d = 0
✓ Semantically equivalent
```

**How the factorial is computed**: Lines 1-4 initialize: b=11, d=12, a=0. Then lines 5-10 compute a += 11*12 = 132. Lines 11-19 (particularly lines 11-17) decrement b and loop back to line 5, creating the factorial computation: 12 * 11 * 10 * ... * 1 = 12!

**Note on multiple patterns**: There's also a second multiplication pattern at lines 20-26 that computes `84 * 75 = 6,300` and adds it to `a`. This second pattern uses a different structure (it increments both `a` and `d` in the inner loop, with `jnz 75 d` for initialization). **Optimization strategy**: We only need to optimize the first pattern (lines 5-10) since:
1. It executes many times (during the factorial loop) making it the performance bottleneck
2. The second pattern only executes once, so optimizing it has minimal performance impact
3. Keeping optimization simple reduces implementation complexity and risk of bugs

**Optimization function**:
```python
def try_optimize_multiplication(self):
    """Detect and optimize a * b multiplication pattern at current PC."""
    pc = self.pc

    # Check if we have enough instructions ahead (need pc through pc+5, i.e., 6 instructions)
    if pc + 6 > len(self.instructions):
        return False

    # Check pattern hasn't been modified by tgl instruction
    # (Overhead of checking 6 set memberships is negligible compared to executing the loop)
    for i in range(pc, pc + 6):
        if i in self.modified_instructions:
            return False

    # Match the specific pattern (indices relative to pc)
    pattern = [
        ('cpy', 'b', 'c'),  # pc+0
        ('inc', 'a', None), # pc+1
        ('dec', 'c', None), # pc+2
        ('jnz', 'c', '-2'), # pc+3
        ('dec', 'd', None), # pc+4
        ('jnz', 'd', '-5')  # pc+5
    ]

    for i, (expected_op, expected_arg1, expected_arg2) in enumerate(pattern):
        instr = self.instructions[pc + i]
        if instr[0] != expected_op or instr[1] != expected_arg1:
            return False
        # String comparison: arguments are stored as strings during parsing (line 17-18 of Part 1)
        # so we need to compare as strings
        if expected_arg2 is not None and str(instr[2]) != str(expected_arg2):
            return False

    # Apply optimization
    b_val = self.registers['b']
    d_val = self.registers['d']
    self.registers['a'] += b_val * d_val
    self.registers['c'] = 0
    self.registers['d'] = 0
    self.pc += 6  # Skip entire pattern (next instruction will be at pc+6)

    return True
```

### Step 9: Main Function Update

```python
def main():
    """Main function to run the interpreter."""
    with open('input.md', 'r') as f:
        input_text = f.read()

    # Create interpreter with a=12 and optimization enabled
    interpreter = AssembunnyInterpreter(initial_a=12)
    interpreter.parse_instructions(input_text)
    result = interpreter.run()

    print(result)

if __name__ == '__main__':
    main()
```

## Algorithm Complexity Analysis

**Without optimization**:
- For a=12, the code computes 12! (factorial)
- The inner loop executes 12! = 479,001,600 times
- Each loop iteration executes multiple instructions (inc, dec, jnz)
- **Total instructions executed**: Several billion (approximately 3-5 times 12!)
- **Time complexity**: O(n!) where n is initial value of register a
- **Estimated runtime**: Hours to days (impractical)

**With optimization**:
- Each multiplication pattern detected and replaced with O(1) operation
- The factorial loop still runs 12 times (outer iterations), but inner multiplication is O(1)
- **Time complexity**: O(n + k) where n is initial value of a and k is number of instructions
- **Estimated runtime**: Sub-second (practical)

## Expected Answer

Based on analysis of the input:
- Lines 1-10 compute a factorial-like operation: after these lines, `a` will be approximately 12! = 479,001,600
- Lines 20-26 add 84 * 75 = 6,300 to register `a`
- **Expected final answer**: 479,001,600 + 6,300 = **479,007,900** (approximately)

This can be verified by running the optimized solution and checking the result is in this range.

## Edge Cases to Handle

1. **Empty multiplication**: If b or d is 0, result should be 0 added
2. **Negative values**: Unlikely in this problem, but handle gracefully
3. **Pattern at end of program**: Ensure bounds checking
4. **Toggled instructions**: Never optimize modified code
5. **Self-modifying code**: Pattern may appear/disappear during execution

## Code Structure

```
solution.py
├── AssembunnyInterpreter (class)
│   ├── __init__(initial_a=12)
│   ├── parse_instructions(input_text)
│   ├── is_register(value)
│   ├── get_value(arg)
│   ├── execute_cpy(x, y)
│   ├── execute_inc(x)
│   ├── execute_dec(x)
│   ├── execute_jnz(x, y)
│   ├── execute_tgl(x)
│   ├── try_optimize_multiplication()  [NEW]
│   └── run()  [MODIFIED]
└── main()  [MODIFIED]
```

## Testing Strategy Integration

The implementation should support:
- Running with optimization enabled (default)
- Running with optimization disabled (for verification with small inputs)
- Comparing results between optimized and non-optimized for a=7

## Summary

**Core changes from Part 1**:
1. Change `initial_a` from 7 to 12 in main()
2. Add `modified_instructions = set()` to `__init__()`
3. Update `execute_tgl()` to mark modified instructions
4. Add `try_optimize_multiplication()` method (30-35 lines)
5. Add optimization check in `run()` method (2 lines)

**Estimated lines of code**: +40-50 lines added to Part 1 solution

**Critical success factor**: Correct pattern detection and optimization that maintains semantic equivalence with the original loop behavior.

## Quick Start Guide

For rapid implementation, follow these 6 essential steps:

1. **Copy Part 1 solution** to new file
2. **Add to `__init__`**: `self.modified_instructions = set()`
3. **Update `execute_tgl`**: Add `self.modified_instructions.add(target)` before toggling
4. **Add `try_optimize_multiplication()` method** (copy code from Step 8)
5. **Update `run()` loop**: Add pattern check before normal execution (see Step 7)
6. **Change main()**: Set `initial_a=12` instead of 7

Test with a=7 first (should get 11340), then run with a=12 for final answer.
