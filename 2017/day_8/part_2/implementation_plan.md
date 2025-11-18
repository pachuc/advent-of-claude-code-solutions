# Implementation Plan - Part 2: Maximum Value During Execution

## Overview
Part 2 requires finding the **highest value held in any register at any point during execution**, not just the final state. This is a simple modification to the Part 1 solution that requires tracking a running maximum.

**Key Difference from Part 1**:
- **Part 1**: Returns maximum value in final register state (after all instructions complete)
- **Part 2**: Returns maximum value ever seen across all intermediate states during execution
- **Example**: If a register goes to 10 then drops to -10, Part 1 returns -10 (or max of other registers), Part 2 returns 10

**Expected Relationship**: Part 2 answer ≥ Part 1 answer (since the final state is one of the intermediate states)

## Core Algorithm
The algorithm remains identical to Part 1 with one addition:
- **Time Complexity**: O(n) where n is the number of instructions
- **Space Complexity**: O(r) where r is the number of unique registers
- **Key Change**: Add a single variable to track the global maximum across all execution states

## Implementation Steps

### 1. Reuse Part 1 Infrastructure
**Files to leverage**: `part_1_solution.py`

Reuse the following components without modification:
- `parse_instruction_line()` - parsing logic is identical
- `parse_input()` - input reading is identical
- `get_comparator()` - condition evaluation is identical

### 2. Modify the Core Processing Function
**Function**: `process_instructions()`

**Changes Required**:
```python
def process_instructions(instructions, verbose=False):
    """Execute all instructions and track maximum value during execution

    Args:
        instructions: List of instruction dictionaries
        verbose: If True, print register state after each modification

    Returns:
        tuple: (dict, int) where dict is {register_name: value} and int is max_value_ever
    """
    registers = {}
    max_value_ever = 0  # NEW: Track maximum value across all states
                        # Start at 0 since all registers implicitly begin at 0
                        # If no register ever exceeds 0, the answer is 0

    for i, instr in enumerate(instructions):
        # [Existing condition evaluation code - unchanged]
        cond_reg_value = registers.get(instr['cond_reg'], 0)
        comparator = get_comparator(instr['comparator'])

        if comparator(cond_reg_value, instr['cond_val']):
            # [Existing operation code - unchanged]
            current_value = registers.get(instr['target_reg'], 0)

            if instr['operation'] == 'inc':
                registers[instr['target_reg']] = current_value + instr['amount']
            elif instr['operation'] == 'dec':
                registers[instr['target_reg']] = current_value - instr['amount']

            # NEW: Update maximum after each modification
            max_value_ever = max(max_value_ever, registers[instr['target_reg']])

            if verbose:
                print(f"After instruction {i+1}: {instr['target_reg']} = {registers[instr['target_reg']]}, max_ever = {max_value_ever}")

    return registers, max_value_ever
```

**Key Changes**:
1. Initialize `max_value_ever = 0` before loop
2. After each register modification (inside the `if` block), update: `max_value_ever = max(max_value_ever, registers[instr['target_reg']])`
3. Return both `registers` and `max_value_ever` as a tuple

**Critical Placement**: The maximum check must happen AFTER the register is modified but ONLY if the condition was true (inside the `if comparator(...)` block).

### 3. Update Main Function
**Function**: `main()`

**Changes Required**:
```python
def main():
    """Main execution function"""
    try:
        instructions = parse_input('input.md')
    except FileNotFoundError:
        print("Error: input.md not found")
        return
    except Exception as e:
        print(f"Error reading input: {e}")
        return

    # Process all instructions - now returns tuple
    registers, max_during_execution = process_instructions(instructions, verbose=False)

    # Print the maximum value during execution (Part 2 answer)
    print(max_during_execution)
```

**Key Changes**:
1. Unpack tuple from `process_instructions()`: `registers, max_during_execution = ...`
2. Print `max_during_execution` instead of `find_max_register_value(registers)`

### 4. Optional: Keep Helper Function for Clarity
The `find_max_register_value()` function can remain in the code for potential debugging or verification, but is not needed for the Part 2 answer.

## File Structure
```
part_2_solution.py
├── parse_instruction_line()     [UNCHANGED from Part 1]
├── parse_input()                [UNCHANGED from Part 1]
├── get_comparator()             [UNCHANGED from Part 1]
├── process_instructions()       [MODIFIED: track max_value_ever]
├── find_max_register_value()    [OPTIONAL: keep for debugging/verification]
└── main()                       [MODIFIED: print max_during_execution]
```

**Implementation Approach**: Copy `part_1_solution.py` as the starting point, then apply the modifications listed above. This approach is preferred over importing/referencing because it keeps the solution self-contained.

## Edge Cases Handled

1. **No instructions**: `max_value_ever` starts at 0, returns 0
2. **No conditions trigger**: `max_value_ever` remains 0 (correct - all registers stay at 0)
3. **All values negative**: Works correctly - we initialize to 0, which is greater than any negative value
4. **Maximum occurs early then decreases**: Correctly tracks peak value
5. **Ties**: No special handling needed - any maximum is valid

## Efficiency Considerations

**Input Size**: 1000 instructions (based on input.md)
- Single pass: O(1000) = O(n)
- Constant time maximum check per modified register
- No additional data structures needed
- **Total Runtime**: Linear in number of instructions - extremely efficient

**Why This is Optimal**:
- We must process every instruction anyway (sequential dependencies)
- Checking maximum after each update is O(1)
- No way to avoid processing all instructions
- Therefore, O(n) is optimal

## Testing Strategy Reference
The implementation should support:
- Small example from problem statement (should return 10)
- Full input processing
- Verbose mode for debugging
- Comparison with Part 1 answer (Part 2 answer ≥ Part 1 answer always)

## Implementation Checklist
- [ ] Copy Part 1 solution as starting point
- [ ] Add `max_value_ever = 0` initialization in `process_instructions()` with clarifying comment
- [ ] Add maximum tracking after register modifications
- [ ] **CRITICAL**: Verify maximum check is inside the conditional block (only when modifications occur)
- [ ] **CRITICAL**: Verify maximum check happens after register update (not before)
- [ ] Update return statement to return tuple
- [ ] Update `main()` to unpack tuple correctly
- [ ] **CRITICAL**: Verify printing the correct value (max_during_execution, not find_max_register_value)
- [ ] Test with example (expected output: 10, NOT 1)
- [ ] Test with full input
- [ ] Verify answer ≥ 5221 (Part 1 answer)

## Summary

This implementation plan leverages the existing Part 1 solution with minimal modifications:

1. **What stays the same**: All parsing, input reading, and condition evaluation logic (75% of code)
2. **What changes**: Adding 3 lines of code to track maximum values during execution
3. **Complexity**: Still O(n) time, O(r) space - optimal
4. **Risk**: Very low - changes are minimal and well-defined
5. **Verification**: Easy to test with provided example (should output 10, not 1)

The key insight is that Part 2 is almost identical to Part 1, just tracking an additional piece of state as we go. This makes implementation straightforward and low-risk.
