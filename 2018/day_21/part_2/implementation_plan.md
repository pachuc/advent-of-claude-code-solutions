# Implementation Plan: Chronal Conversion Part 2

## Problem Summary
Find the lowest non-negative integer value for register 0 that causes the program to halt after executing the **most** instructions (while still actually halting). The program generates a sequence of values in register 5 at instruction 29 (`eqrr 5 0 3`), and eventually this sequence repeats. We need to find the last unique value before the cycle repeats.

## Code Reuse from Part 1
The Part 1 solution (`part_1_solution.py`) provides excellent foundation code that we can reuse:
- `parse_input()` - Already handles parsing the instruction file (reuse as-is)
- `execute_instruction()` - Already implements all opcodes (reuse as-is)
- The simulation loop logic (adapt for Part 2 requirements)

## Algorithm Overview
Instead of stopping at the first value in register 5 at instruction 29, we need to:
1. Track all unique values that appear in register 5 when instruction 29 is reached
2. Detect when a value repeats (indicating the sequence has cycled)
3. Return the last unique value seen before the cycle

## Step-by-Step Implementation

### Step 1: Reuse Parsing and Execution Functions
- Copy `parse_input()` function from Part 1 solution (no changes needed)
- Copy `execute_instruction()` function from Part 1 solution (no changes needed)

### Step 2: Implement Cycle Detection Function
Create a new function `find_last_halting_value()` that:

**Input**: `ip_register`, `instructions`

**Algorithm**:
1. Initialize registers to `[0, 0, 0, 0, 0, 0]`
2. Initialize `ip = 0` and `instruction_count = 0`
3. Create a **set** `seen_values` to track unique values in register 5
4. Create a **list** `value_sequence` to maintain the order of values (for finding the last one)

5. Main simulation loop:
   ```
   while 0 <= ip < len(instructions):
       if ip == 29:
           current_value = registers[5]

           if current_value in seen_values:
               # We've seen this value before - the cycle has completed
               # value_sequence[-1] is the last unique value (current_value is not in the list yet)
               # This is the value that will cause maximum instruction execution
               if len(value_sequence) == 0:
                   return (None, None, 0)  # Edge case: immediate repeat
               return (value_sequence[-1], value_sequence[0], len(value_sequence))
           else:
               # New unique value
               seen_values.add(current_value)
               value_sequence.append(current_value)

       # Standard execution steps
       registers[ip_register] = ip
       opcode, a, b, c = instructions[ip]
       execute_instruction(opcode, a, b, c, registers)
       ip = registers[ip_register]
       ip += 1
       instruction_count += 1

       # Progress indicator for long-running simulations
       if instruction_count % 10_000_000 == 0:
           print(f"Progress: {instruction_count:,} instructions executed, {len(value_sequence)} unique values found")
   ```

6. If loop exits without finding a cycle (unlikely), return `(None, None, 0)`

**Return value**: Tuple of `(last_unique_value, first_value, sequence_length)` for validation purposes

**Why this works**:
- The program generates values in register 5 in a deterministic sequence
- Eventually, the same value will appear again, indicating the start of a cycle
- The last unique value before the cycle is the answer
- Setting register 0 to this value will make the program execute all iterations through the sequence before halting

### Step 3: Optional Verification Function (NOT RECOMMENDED)
**Decision**: Skip full verification function for Part 2

**Rationale**:
- Full verification would take an extremely long time (potentially hours)
- The answer maximizes instruction count, so it would execute through the entire sequence
- The logic is sound: the last unique value before cycling is guaranteed to be correct
- We can validate correctness through other means (see Step 4)

**Alternative Validation** (if desired):
- Partial verification: Run for limited instructions (e.g., 10 million) and confirm no early halt
- Check that the answer exists in our tracked sequence
- Validate that first value matches Part 1 answer (15615244)

### Step 4: Main Function
```python
def main():
    # Parse input
    ip_register, instructions = parse_input('input.md')
    print(f"Parsed {len(instructions)} instructions with IP bound to register {ip_register}")

    # Find the last halting value
    print("\nFinding cycle in register 5 values...")
    result, first_value, sequence_length = find_last_halting_value(ip_register, instructions)

    if result is not None:
        # Validation: First value should match Part 1 answer
        PART_1_ANSWER = 15615244
        if first_value == PART_1_ANSWER:
            print(f"✓ Validation: First value matches Part 1 answer ({PART_1_ANSWER})")
        else:
            print(f"⚠ Warning: First value {first_value} doesn't match Part 1 answer {PART_1_ANSWER}")

        print(f"Total unique values in sequence: {sequence_length}")
        print(f"\nAnswer: {result}")
    else:
        print("Failed to find halting value")
```

**Note**: The function should return a tuple `(last_value, first_value, sequence_length)` for validation purposes.

## Performance Considerations

### Expected Runtime
- The program will need to cycle through all unique values in the sequence
- Based on the Part 1 result (15615244 after a few thousand instructions), the sequence likely has thousands to potentially millions of unique values
- **Estimated runtime**: 30 seconds to 5 minutes depending on cycle length
- This is acceptable for a one-time puzzle solution

### Optimization Notes
- We use a **set** for O(1) membership checking (`seen_values`)
- We use a **list** to maintain order (`value_sequence`)
- No need to optimize further - the bottleneck is the simulation itself, not our data structures
- We could potentially reverse-engineer the assembly to compute values directly, but that's complex and unnecessary for this problem size

### Memory Considerations
- Each unique value is stored once (4-8 bytes)
- If there are 1 million unique values, that's ~8 MB maximum
- Completely acceptable for this problem

## Algorithm Efficiency Analysis
- **Time Complexity**: O(N) where N is the number of instructions executed until cycle detection
- **Space Complexity**: O(U) where U is the number of unique values (typically << N)
- This is optimal - we must simulate to find the sequence, and we need to track values to detect cycles

## Edge Cases to Handle
1. **Immediate cycle**: If the first value repeats immediately, `value_sequence` would be empty. Add check: `if not value_sequence: return None`
2. **No instruction 29**: Program structure guarantees this exists based on problem statement
3. **Program halts before cycle**: Main loop condition `0 <= ip < len(instructions)` handles this - would return None
4. **Empty value sequence**: Check `len(value_sequence) > 0` before returning `value_sequence[-1]`

**Implementation**: Add safety check before returning:
```python
if current_value in seen_values:
    if len(value_sequence) == 0:
        # Edge case: first value seen is a repeat (shouldn't happen)
        return None
    return value_sequence[-1]
```

## File Structure
```
solution.py
├── parse_input()           # From Part 1 (no changes)
├── execute_instruction()   # From Part 1 (no changes)
├── find_last_halting_value()  # New - main algorithm, returns (last_value, first_value, count)
└── main()                  # Entry point with validation
```

## Expected Output Format
Single integer printed to stdout: the value for register 0 that maximizes instruction count while still halting.
