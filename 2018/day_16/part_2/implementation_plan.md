# Implementation Plan: Chronal Classification - Part 2

## Problem Overview
Part 2 builds directly on Part 1. We need to:
1. Deduce the mapping from opcode numbers (0-15) to opcode names using the sample observations
2. Execute a test program using the deduced opcode mappings
3. Return the value in register 0 after the test program completes

## Reusable Code from Part 1
The Part 1 solution (`part_1_solution.py`) already contains:
- ✅ All 16 opcode implementations in `execute_opcode()` function
- ✅ Parsing logic for registers and instructions
- ✅ Logic to test which opcodes match a given sample
- ✅ List of all opcode names in `ALL_OPCODES`

We will **reuse and extend** this code rather than rewriting from scratch.

## Algorithm Strategy

### Phase 1: Deduce Opcode Mappings (Constraint Satisfaction)
1. For each sample, determine which opcode names are compatible with the observed transformation
2. Build a mapping: `opcode_number -> set of possible opcode names`
3. Use iterative constraint propagation:
   - Find opcode numbers that have only one possible opcode name
   - Lock in that mapping
   - Remove that opcode name from all other opcode numbers' possibilities
   - Repeat until all 16 mappings are uniquely determined

### Phase 2: Execute Test Program
1. Parse the test program (after the double blank line in input)
2. Initialize registers to [0, 0, 0, 0]
3. For each instruction:
   - Use the deduced mapping to convert opcode number to opcode name
   - Execute the operation using the existing `execute_opcode()` function
   - Update the registers
4. Return the value in register 0

## Detailed Implementation Steps

### Step 1: Extend the parsing function
**File:** Modify `parse_input()` function
**What:** Update it to return both samples AND the test program
**How:**
- Parse samples as before (until double blank line detected)
- When we encounter two consecutive blank lines (lines i and i+1 are both blank):
  - Set `i = i + 2` to skip past the double blank line
  - All remaining non-blank lines are test program instructions
  - Parse each line using `parse_instruction()` to get [opcode, A, B, C]
- Return a tuple: `(samples, test_program)` where:
  - `samples` is a list of tuples: `[(before, instruction, after), ...]`
  - `test_program` is a list of lists: `[[opcode, A, B, C], ...]` (all integers)

**Complexity:** O(n) where n is the number of input lines (~4022)

### Step 2: Create function to find compatible opcodes for a sample
**File:** New function `get_compatible_opcodes(before, instruction, after)`
**What:** Given a sample's components, return the set of opcode names that could produce the transformation
**How:**
- Extract A, B, C from instruction (indices 1, 2, 3)
  - Note: instruction[0] is the opcode number, which we ignore here
- Initialize empty set: `compatible = set()`
- For each opcode name in ALL_OPCODES:
  - Execute: `result = execute_opcode(opcode_name, before, A, B, C)`
  - If result == after, add opcode name to compatible set
- Return the set of compatible opcode names

**Complexity:** O(16) = O(1) per sample (constant number of opcodes)

### Step 3: Build initial possibility mapping
**File:** New function `build_opcode_possibilities(samples)`
**What:** Build a dictionary mapping opcode numbers to sets of possible opcode names
**How:**
- Initialize: `possibilities = {i: set(ALL_OPCODES) for i in range(16)}`
- For each sample in the samples list:
  - Unpack: `before, instruction, after = sample`
  - Get the opcode number: `opcode_num = instruction[0]`
  - Get compatible opcodes: `compatible = get_compatible_opcodes(before, instruction, after)`
  - Narrow possibilities via intersection: `possibilities[opcode_num] &= compatible`
- Return the possibilities dictionary

**Complexity:** O(num_samples * 16) where num_samples ≈ 782
**Note:** Each sample narrows down the possibilities for one opcode number

### Step 4: Deduce unique mappings via constraint propagation
**File:** New function `deduce_opcode_mapping(possibilities)`
**What:** Reduce the possibilities to unique 1-to-1 mappings
**How:**
- Create `opcode_map = {}` (final mapping: number -> name)
- Make a working copy: `remaining = possibilities.copy()` (since we'll modify it)
- While `len(opcode_map) < 16`:
  - Find an opcode number with exactly 1 possibility:
    ```python
    found = None
    for opcode_num, possible_names in remaining.items():
        if len(possible_names) == 1:
            found = opcode_num
            break
    ```
  - If none found, try opcodes with minimum possibilities (more robust):
    ```python
    if found is None:
        # Fall back to trying minimum possibilities
        min_count = min(len(v) for v in remaining.values())
        # This shouldn't happen with valid Advent of Code input,
        # but could add backtracking here if needed
        raise ValueError("Unable to uniquely determine opcode mapping")
    ```
  - Lock in the mapping: `opcode_map[found] = list(remaining[found])[0]`
  - Remove that opcode name from all other possibilities:
    ```python
    locked_name = opcode_map[found]
    for opcode_num in remaining:
        remaining[opcode_num].discard(locked_name)
    ```
  - Remove the locked opcode from remaining: `del remaining[found]`
- Return opcode_map

**Complexity:** O(16²) = O(256) worst case (16 iterations, each scanning up to 16 opcodes)
**Optimization:** Most iterations will resolve quickly since constraint propagation cascades

### Step 5: Parse the test program
**File:** Already handled in Step 1 (extended `parse_input()`)
**What:** Extract test program instructions from input
**Result:** List of instructions (each is [opcode, A, B, C])

### Step 6: Execute the test program
**File:** New function `execute_program(test_program, opcode_map)`
**What:** Run all test program instructions and return final register state
**How:**
- Initialize: `registers = [0, 0, 0, 0]`
- For each instruction in test_program:
  - Parse: `opcode_num, A, B, C = instruction`
  - Get opcode name: `opcode_name = opcode_map[opcode_num]`
  - Execute: `registers = execute_opcode(opcode_name, registers, A, B, C)`
  - (Optional assertion for debugging: `assert opcode_num in opcode_map`)
- Return registers[0]

**Complexity:** O(num_instructions) where num_instructions = 893
- All opcodes execute in O(1) time
- Total: O(893) linear in test program length

**Note:** No error handling needed for valid input, but assertions can help during development

### Step 7: Update main solve function
**File:** Modify `solve()` function
**What:** Orchestrate the entire solution
**How:**
```python
def solve(filename):
    # Parse input
    samples, test_program = parse_input(filename)

    # Phase 1: Deduce opcode mappings
    possibilities = build_opcode_possibilities(samples)
    opcode_map = deduce_opcode_mapping(possibilities)

    # Phase 2: Execute test program
    result = execute_program(test_program, opcode_map)

    return result
```

**Complexity:** Dominated by O(num_samples) from step 3

## Overall Complexity Analysis

### Time Complexity
- Parsing: O(n) where n is total input lines (4022)
- Building possibilities: O(samples * 16) ≈ O(782 * 16) ≈ 12,512 operations
- Deducing mappings: O(16²) ≈ 256 operations worst case
- Executing program: O(893) for 893 instructions
- **Total: O(n) linear in input size** - very efficient
- **Actual operations:** ~13,700 total (dominated by sample processing)

### Space Complexity
- Samples storage: O(samples) ≈ 782 samples × 3 lists of 4 integers
- Test program storage: O(instructions) ≈ 893 instructions × 4 integers
- Possibilities dict: O(16 × 16) = 256 entries worst case before constraint propagation
- Opcode map: O(16) for final mapping
- **Total: O(n)** - linear in input size, approximately 10KB of data

## Edge Cases & Considerations

1. **Constraint satisfaction convergence:** The iterative constraint propagation should yield exactly one unique solution. The algorithm handles cases where multiple opcodes have 1 possibility simultaneously (resolves all in same iteration). If no opcode has exactly 1 possibility, we raise an error.

2. **Empty possibilities:** If any opcode number ends up with zero possibilities after building the mapping, the input is contradictory. This shouldn't happen with valid Advent of Code input.

3. **Register bounds:** All register indices (A, B, C) should be 0-3. The existing `execute_opcode()` assumes valid indices. No bounds checking needed for the given input, but assertions can be added during development.

4. **Invalid opcode numbers:** Test program should only contain opcode numbers 0-15. No validation needed for given input.

5. **Integer overflow:** Python handles arbitrarily large integers natively, so no overflow concerns.

6. **Double blank line detection:** The parsing logic correctly detects two consecutive blank lines at lines 3128 and 3129, then resumes parsing at line 3130 for the test program (893 instructions from line 3130 to 4022).

## Code Reuse Summary

**From Part 1 (reuse as-is):**
- `ALL_OPCODES` list
- `parse_registers()` function
- `parse_instruction()` function
- `execute_opcode()` function

**From Part 1 (modify):**
- `parse_input()` - extend to also parse test program
- `solve()` - completely rewrite for Part 2 logic

**New functions needed:**
- `get_compatible_opcodes(before, instruction, after)` - find which opcodes match a sample
- `build_opcode_possibilities(samples)` - build initial constraint mapping
- `deduce_opcode_mapping(possibilities)` - solve constraints to get unique mapping
- `execute_program(test_program, opcode_map)` - run test program with deduced mappings

## Implementation Order

1. Copy Part 1 solution as starting point
2. Modify `parse_input()` to return both sections
3. Add `get_compatible_opcodes()` function
4. Add `build_opcode_possibilities()` function
5. Add `deduce_opcode_mapping()` function
6. Add `execute_program()` function
7. Rewrite `solve()` to orchestrate Part 2 logic
8. Test with the input file

## Changes Based on Critique

The following improvements were made to the implementation plan based on the critique:

1. **Clarified parsing logic:** Step 1 now explicitly describes how to handle the double blank line at lines 3128-3129 and resume parsing at line 3130. The return type is clearly specified as `(samples, test_program)` where test_program is a `list[list[int]]`.

2. **Fixed function signatures:** All function signatures now include parameter names for clarity:
   - `get_compatible_opcodes(before, instruction, after)`
   - `build_opcode_possibilities(samples)`
   - `deduce_opcode_mapping(possibilities)`
   - `execute_program(test_program, opcode_map)`

3. **Clarified instruction parameter extraction:** Step 2 explicitly notes that A, B, C are extracted from `instruction[1:4]`, not including the opcode number at `instruction[0]`.

4. **Improved constraint propagation robustness:** Step 4 now includes error handling for the case where no opcode has exactly 1 possibility, with a clear error message. This makes the algorithm more robust even though it's unlikely to be needed.

5. **Added optional assertions:** Step 6 notes that optional assertions can be added during development to catch bugs early, while acknowledging they're not strictly necessary for valid input.

6. **Improved complexity analysis:** Fixed the notation to properly distinguish between O(n) complexity and actual operation counts. Added concrete numbers for better understanding.

7. **Added edge case for double blank line:** Edge case #6 explicitly mentions the verified line positions (3128-3129 for double blank, 3130-4022 for test program).

These changes make the implementation plan more precise, robust, and easier to follow while addressing all critical issues from the critique.
