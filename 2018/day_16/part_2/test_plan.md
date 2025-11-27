# Test Plan: Chronal Classification - Part 2

## Testing Objectives

1. Verify the opcode mapping deduction is correct
2. Ensure the test program executes properly
3. Confirm the final answer is accurate
4. Validate edge cases in constraint satisfaction

## Test Strategy

Since this is an Advent of Code puzzle with a single specific input, our testing will focus on:
- Validating intermediate results
- Checking algorithm correctness
- Verifying the final answer matches expected output

## Phase 1: Parsing Validation

### Test 1.1: Verify Input Parsing
**Objective:** Ensure the input is correctly split into samples and test program

**Method:**
```python
samples, test_program = parse_input("input.md")
```

**Validation:**
- Input file has 4022 total lines
- Double blank line occurs at lines 3128-3129
- Samples section should end before the double blank line
- Test program should start at line 3130 and continue to end of file
- Each sample should have valid before/after states (lists of 4 integers)
- Each instruction should have 4 integers

**Expected Results:**
- `len(samples)` should be approximately 782 (verify by counting samples, not hardcoding)
- `len(test_program) == 893` (lines 3130-4022 = 893 lines)
- All samples have proper structure: `(before, instruction, after)`
- All test program instructions are lists of 4 integers: `[opcode, A, B, C]`
- All values in instructions are non-negative integers

**Edge Cases:**
- Double blank line separator at lines 3128-3129 is properly detected
- No samples or instructions are dropped during parsing
- Line parsing handles whitespace correctly (strips leading/trailing whitespace)
- The parsing resumes correctly after the double blank line at line 3130

### Test 1.2: Verify Opcode Execution (Inherited from Part 1)
**Objective:** Ensure all 16 opcodes execute correctly

**Method:** Use example from problem statement:
```python
before = [3, 2, 1, 1]  # Initial register state
A, B, C = 2, 1, 2      # Instruction parameters

# Test specific opcodes
# mulr: before[2]=1, before[1]=2, so reg[2] = 1 * 2 = 2
assert execute_opcode('mulr', before, A, B, C) == [3, 2, 2, 1]

# addi: before[2]=1, B=1, so reg[2] = 1 + 1 = 2
assert execute_opcode('addi', before, A, B, C) == [3, 2, 2, 1]

# seti: A=2, so reg[2] = 2
assert execute_opcode('seti', before, A, B, C) == [3, 2, 2, 1]
```

**Expected Results:**
- All three opcodes produce the expected output [3, 2, 2, 1]
- This confirms the execute_opcode function works correctly (already tested in Part 1)

## Phase 2: Opcode Mapping Deduction

### Test 2.1: Get Compatible Opcodes for a Sample
**Objective:** Verify `get_compatible_opcodes()` correctly identifies matching opcodes

**Method:** Test with the example from problem statement:
```python
before = [3, 2, 1, 1]
instruction = [9, 2, 1, 2]  # opcode 9, A=2, B=1, C=2
after = [3, 2, 2, 1]

# Function signature: get_compatible_opcodes(before, instruction, after)
compatible = get_compatible_opcodes(before, instruction, after)
```

**Expected Results:**
- Compatible set should contain exactly: {'mulr', 'addi', 'seti'}
- Should NOT contain other 13 opcodes
- `len(compatible) == 3`
- `compatible == {'mulr', 'addi', 'seti'}`

**Edge Cases:**
- Samples with only 1 compatible opcode (helps narrow mapping quickly)
- Samples with many compatible opcodes (10+, less informative)
- Verify function extracts A, B, C from instruction[1:4], not instruction[0:3]

### Test 2.2: Build Possibility Mapping
**Objective:** Verify `build_opcode_possibilities()` correctly narrows possibilities

**Method:**
```python
possibilities = build_opcode_possibilities(samples)
```

**Validation Checks:**
- All 16 opcode numbers (0-15) should be keys in the dictionary
- Each value should be a set of opcode names (strings)
- No possibility set should be empty (if any is empty, input is invalid)
- At least some opcode numbers should already be narrowed down (fewer than 16 possibilities)

**Expected Results:**
- `len(possibilities) == 16`
- All values are non-empty sets
- `all(isinstance(v, set) for v in possibilities.values())`
- Some opcodes have fewer possibilities due to constraint intersection

**Debug Output:**
```python
for opcode_num in sorted(possibilities.keys()):
    print(f"Opcode {opcode_num}: {len(possibilities[opcode_num])} possibilities")
```

### Test 2.3: Deduce Unique Mapping
**Objective:** Verify `deduce_opcode_mapping()` produces a unique 1-to-1 mapping

**Method:**
```python
possibilities = build_opcode_possibilities(samples)
opcode_map = deduce_opcode_mapping(possibilities)
```

**Validation Checks:**
- Mapping should contain all 16 opcode numbers
- Mapping should contain all 16 unique opcode names
- No duplicates in values
- All values are valid opcode names from ALL_OPCODES

**Expected Results:**
- `len(opcode_map) == 16`
- `set(opcode_map.keys()) == set(range(16))`
- `set(opcode_map.values()) == set(ALL_OPCODES)`
- `len(set(opcode_map.values())) == 16` (all unique)

**Edge Cases:**
- Algorithm should converge to unique solution
- Should not require backtracking (if it does, may need algorithm enhancement)

**Debug Output:**
```python
for opcode_num in sorted(opcode_map.keys()):
    print(f"Opcode {opcode_num} -> {opcode_map[opcode_num]}")
```

This output will help verify the mapping makes logical sense.

### Test 2.4: Constraint Satisfaction Termination
**Objective:** Ensure the algorithm terminates and doesn't get stuck

**Method:**
- Add iteration counter to `deduce_opcode_mapping()` (optional, for debugging)
- Verify it completes in reasonable iterations

**Expected Results:**
- Algorithm should complete in at most 16 iterations (one per opcode)
- However, it may complete faster if multiple opcodes are resolved per iteration
- Each iteration should resolve at least one opcode when using constraint propagation
- No infinite loops or deadlocks

## Phase 3: Test Program Execution

### Test 3.1: Execute Simple Test Case
**Objective:** Verify `execute_program()` correctly executes instructions

**Method:** Create a minimal test program:
```python
# Test with known operations
opcode_map_test = {0: 'seti', 1: 'addi'}
test_program_simple = [
    [0, 5, 0, 0],  # seti 5 -> reg[0] = 5
    [1, 0, 3, 1],  # addi reg[0] + 3 -> reg[1] = 8
]
registers = [0, 0, 0, 0]

# Execute manually
result = execute_program(test_program_simple, opcode_map_test)
```

**Expected Results:**
- After first instruction: registers = [5, 0, 0, 0]
- After second instruction: registers = [5, 8, 0, 0]
- Return value should be 5 (register 0)

### Test 3.2: Execute Full Test Program
**Objective:** Run the actual test program with deduced mappings

**Method:**
```python
samples, test_program = parse_input("input.md")
possibilities = build_opcode_possibilities(samples)
opcode_map = deduce_opcode_mapping(possibilities)
result = execute_program(test_program, opcode_map)
```

**Validation Checks:**
- Program executes without errors
- All 893 instructions are executed
- Result is a non-negative integer
- No index out of bounds errors
- No invalid opcode lookups

**Expected Results:**
- Function returns an integer (value of register 0)
- No exceptions raised
- Execution completes in reasonable time (<1 second)

## Phase 4: Integration Testing

### Test 4.1: Full End-to-End Solution
**Objective:** Verify the complete solution works correctly

**Method:**
```python
result = solve("input.md")
print(f"Answer: {result}")
```

**Validation:**
- Solution runs without errors
- Returns a single integer (non-negative)
- Answer should be consistent on multiple runs
- Execution time should be reasonable (<2 seconds)

**Correctness Verification:**
- The correct answer can only be verified by submitting to Advent of Code
- If the expected answer is known beforehand, add: `assert result == EXPECTED_ANSWER`
- If answer is incorrect, use the debugging strategy below to trace the issue

### Test 4.2: Consistency Check
**Objective:** Ensure solution is deterministic

**Method:**
```python
result1 = solve("input.md")
result2 = solve("input.md")
assert result1 == result2, "Solution is non-deterministic!"
```

**Expected Results:**
- Multiple runs produce identical results
- No randomness in algorithm

## Phase 5: Edge Cases and Robustness Considerations

**Note:** These are considerations for development rather than formal automated tests, since we're solving a specific puzzle with known valid input.

### Test 5.1: Constraint Satisfaction Edge Cases
**Objective:** Verify algorithm handles edge cases in constraint solving

**Considerations During Development:**
- Opcodes with only 1 possibility from the start (should be resolved immediately)
- Opcodes with many (10+) possibilities initially (narrowed down over iterations)
- Verify all opcodes eventually reduce to exactly 1 possibility
- Handle case where no opcode has exactly 1 possibility (raise informative error)

**Optional Assertions in `deduce_opcode_mapping()`:**
```python
# Before each iteration
assert all(len(v) > 0 for v in remaining.values()), "Empty possibility set detected"

# After completion
assert len(opcode_map) == 16, "Not all opcodes mapped"
assert len(set(opcode_map.values())) == 16, "Duplicate opcode names"
```

### Test 5.2: Register State Integrity
**Objective:** Ensure registers maintain valid state throughout execution

**Considerations During Development:**
- All register values remain integers throughout execution
- Register array always has length 4
- Register indices (A, B, C) are always in range [0, 3]

**Optional Validation (for debugging):**
```python
# In execute_program(), optionally add:
assert all(isinstance(r, int) for r in registers), "Non-integer register value"
assert len(registers) == 4, "Invalid register array length"
```

**Expected Behavior:**
- No corruption of register state with valid input
- All values remain valid throughout execution

## Test Execution Order

1. **Phase 1 (Parsing):** Verify input parsing works correctly
2. **Phase 2.1-2.2 (Compatibility):** Test opcode matching and possibility building
3. **Phase 2.3-2.4 (Deduction):** Verify constraint satisfaction produces unique mapping
4. **Phase 3.1 (Simple Execution):** Test program execution with known mappings
5. **Phase 3.2 (Full Execution):** Run actual test program
6. **Phase 4 (Integration):** Complete end-to-end test
7. **Phase 5 (Edge Cases):** Verify robustness

## Debugging Strategy

If the final answer is incorrect:

1. **Check opcode mapping:** Print the deduced mapping and verify it makes sense
2. **Sample validation:** Pick a few samples and manually verify compatible opcodes
3. **Trace execution:** Add logging to see how registers change during test program
4. **Compare with Part 1:** Ensure opcode implementations are identical and correct
5. **Boundary checks:** Verify no register indices are out of bounds

## Success Criteria

- All parsing tests pass (correct counts and structure)
- Opcode mapping produces exactly 16 unique 1-to-1 mappings
- Test program executes all 893 instructions without errors
- Final answer is a valid integer
- Solution runs in under 2 seconds
- Answer is accepted by Advent of Code submission system

## Changes Based on Critique

The following improvements were made to the test plan based on the critique:

1. **Fixed hardcoded line counts:** Changed Test 1.1 to verify parsing dynamically rather than assuming exact counts. Specified that the double blank line is at lines 3128-3129, and test program runs from line 3130 to 4022 (893 lines).

2. **Clarified function signatures:** Updated Test 2.1 to show the correct function signature `get_compatible_opcodes(before, instruction, after)` matching the implementation plan.

3. **Improved test comments:** Added clearer explanations in Test 1.2 showing the before state and calculations for each opcode test.

4. **Relaxed iteration count expectation:** Updated Test 2.4 to note that the algorithm may complete in fewer than 16 iterations if multiple opcodes are resolved simultaneously.

5. **Added correctness verification note:** Updated Test 4.1 to explicitly state that correctness must be verified via Advent of Code submission, or by comparing against a known expected answer.

6. **Converted Phase 5 to development considerations:** Renamed and restructured Phase 5 to clarify these are development considerations rather than formal automated tests, since we're solving a specific puzzle with known valid input.

These changes make the test plan more accurate, flexible, and aligned with the implementation plan while maintaining focus on solving the specific puzzle at hand.
