# Test Plan - Part 2: Output Bin Product

## Testing Objective
Verify that the simulation correctly processes all chips and accurately calculates the product of values in output bins 0, 1, and 2.

## Test Strategy
Since this is a script to solve a specific puzzle input (not production code), we'll focus on:
1. Verifying the simulation completes successfully
2. Checking that outputs 0, 1, 2 all contain chips
3. Validating the final product calculation
4. Spot-checking a few intermediate states for correctness

## Test Cases

### Test 1: Basic Execution
**Purpose**: Verify the script runs without errors on the actual input

**Steps**:
1. Run `python solution.py` with the provided input
2. Verify it produces a single integer output
3. Verify no Python errors or exceptions occur

**Expected Result**:
- Script completes successfully
- Outputs a positive integer (the product)

### Test 2: Output Bins Population
**Purpose**: Verify that outputs 0, 1, and 2 are populated with exactly one chip each

**Steps**:
1. Add debug print statements before calculating the product:
   ```python
   print(f"Output 0: {outputs[0]}")
   print(f"Output 1: {outputs[1]}")
   print(f"Output 2: {outputs[2]}")
   print(f"Output 0 chip count: {len(outputs[0])}")
   print(f"Output 1 chip count: {len(outputs[1])}")
   print(f"Output 2 chip count: {len(outputs[2])}")
   ```
2. Run the script
3. Verify each output contains exactly one chip value

**Expected Result**:
- Output 0: [single positive integer]
- Output 1: [single positive integer]
- Output 2: [single positive integer]
- Each output has exactly 1 chip (based on problem statement)

### Test 3: Simulation Completeness
**Purpose**: Verify all chips are distributed (none stuck in bots)

**Steps**:
1. After simulation, add debug check:
   ```python
   # Count total chips in bots
   chips_in_bots = sum(len(chips) for chips in bots.values())
   print(f"Chips remaining in bots: {chips_in_bots}")

   # Count total chips in outputs
   chips_in_outputs = sum(len(chips) for chips in outputs.values())
   print(f"Chips in outputs: {chips_in_outputs}")
   ```
2. Verify that all chips have been distributed to outputs

**Expected Result**:
- Chips remaining in bots: 0 (all bots should be empty)
- Chips in outputs: equals total initial chip count (21 based on Part 1 input)

### Test 4: Product Calculation Correctness
**Purpose**: Verify the product calculation is correct

**Steps**:
1. Extract the values from outputs 0, 1, 2 (from debug output in Test 2)
2. Manually calculate the product
3. Compare with script output

**Expected Result**:
- Manual calculation matches script output

### Test 5: Consistency with Part 1
**Purpose**: Ensure Part 2 simulation is consistent with Part 1

**Steps**:
1. Verify that the simulation still processes bot 98 with values 61 and 17
2. Add a check in the simulate function:
   ```python
   if bot_id == 98 and set(chips) == {61, 17}:
       print("Bot 98 is comparing 61 and 17 (Part 1 answer)")
   ```
3. Run and verify this message appears

**Expected Result**:
- The debug message confirms bot 98 still compares 61 and 17
- This validates our simulation logic hasn't changed incorrectly

### Test 6: Specific Output Routing Check
**Purpose**: Trace specific outputs to verify correct routing

**Steps**:
1. Check the input for direct assignments to outputs 0, 1, 2:
   - Search for "output 0", "output 1", "output 2" in input.md
2. Identify which bots send to these outputs
3. Add debug logging to trace these specific transfers:
   ```python
   if dest_type == 'output' and dest_num in [0, 1, 2]:
       print(f"Bot {bot_id if 'bot_id' in locals() else 'init'} -> output {dest_num}: chip {chip_value}")
   ```

**Expected Result**:
- Trace output shows which bots sent which chips to outputs 0, 1, 2
- Manual verification that the routing follows the rules

### Test 7: Chip Count Validation
**Purpose**: Verify exactly one chip per output bin as expected

**Steps**:
1. After simulation, check chip count in outputs 0, 1, 2
2. Verify each has exactly 1 chip
3. Based on input analysis:
   - Line 61: `bot 18 gives low to output 0` (only source for output 0)
   - Line 1: `bot 127 gives low to output 1` (only source for output 1)
   - Line 32: `bot 180 gives low to output 2` (only source for output 2)
4. Confirm no other bots send to these outputs

**Expected Result**:
- Each of outputs 0, 1, 2 contains exactly 1 chip
- If any has ≠ 1 chip, this indicates a bug in the simulation

### Test 8: Product Reasonableness
**Purpose**: Sanity check that the final answer is reasonable

**Steps**:
1. Check that the product is positive
2. Check that the product is non-zero
3. Verify it's the product of three positive integers
4. Based on input values (range appears to be 2-73), product should be < 73^3 = 389,017

**Expected Result**:
- Product is a positive integer
- Product is in a reasonable range (likely 4-6 digits)

## Input-Specific Validations

From the input file, we can identify the ONLY sources for outputs 0, 1, 2:
- Line 61: `bot 18 gives low to output 0 and high to bot 202`
- Line 1: `bot 127 gives low to output 1 and high to bot 180`
- Line 32: `bot 180 gives low to output 2 and high to bot 125`

**Validation Steps**:
1. Verify that bot 18 sends its low chip to output 0 (and only bot 18 does this)
2. Verify that bot 127 sends its low chip to output 1 (and only bot 127 does this)
3. Verify that bot 180 sends its low chip to output 2 (and only bot 180 does this)
4. Confirm no other bots in the input send to outputs 0, 1, or 2 (can verify with grep/search)
5. This guarantees each output receives exactly one chip

### Test 9: Input File Verification
**Purpose**: Confirm we're reading the correct input file

**Steps**:
1. Verify the file 'input.md' exists in the working directory
2. Check it has ~230 lines (consistent with the input shown)
3. Verify it contains both "value X goes to bot Y" and "bot X gives..." instructions
4. Check for the specific lines identified above (bot 18, 127, 180 outputs)

**Expected Result**:
- File exists and is readable
- Contains the expected format and content
- Input filename matches what's used in part_1_solution.py:96

## Success Criteria

The solution is correct if ALL of the following are true:
1. ✅ Script executes without errors or exceptions
2. ✅ All chips are distributed (no chips remain in bots after simulation)
3. ✅ Outputs 0, 1, and 2 each contain exactly one chip
4. ✅ The product is calculated correctly (value0 × value1 × value2)
5. ✅ The simulation is consistent with Part 1 (bot 98 still compares 61 and 17 at some point)
6. ✅ Output is a single positive integer
7. ✅ Product value is reasonable (positive, non-zero, < 400,000)
8. ✅ Running multiple times produces identical output (deterministic)

## Debugging Strategy

If the answer is incorrect:
1. Enable all debug prints to see the simulation flow
2. Verify which bots send to outputs 0, 1, 2
3. Trace back through the simulation to see which chips end up in these bots
4. Verify the initial chip assignments are parsed correctly
5. Check for any off-by-one errors in indexing

## Performance Validation

**Expected Runtime**: < 1 second
- The simulation is O(N) where N is the number of chip transfers
- With ~230 instructions, this should be nearly instantaneous
- If runtime > 1 second, investigate potential infinite loops

## Final Verification Checklist

Before submitting the answer, verify ALL of the following:

### Correctness Checks
- [ ] Script runs without errors on the actual input
- [ ] Output is a single integer (no extra text, whitespace, or formatting)
- [ ] Running multiple times produces the same answer (deterministic)
- [ ] Product value is positive and reasonable (< 400,000 based on input range)

### Logic Verification
- [ ] Each of outputs 0, 1, 2 has exactly 1 chip
- [ ] All chips from initial assignments are accounted for in outputs
- [ ] No chips remain stuck in bots after simulation
- [ ] Simulation processes bot 98 with values 61 and 17 (Part 1 consistency)

### Code Quality
- [ ] No hardcoded values specific to test data
- [ ] Input file 'input.md' is correctly referenced
- [ ] Error messages are clear if validation fails
- [ ] Code follows the same structure as Part 1 for easy comparison

### Manual Verification
- [ ] Manually trace the path for at least one output bin (e.g., output 0)
- [ ] Verify the product calculation by manually multiplying the three values
- [ ] Check that values are extracted from outputs[0][0], outputs[1][0], outputs[2][0]
