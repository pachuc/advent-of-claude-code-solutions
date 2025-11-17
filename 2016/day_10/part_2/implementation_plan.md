# Implementation Plan - Part 2: Output Bin Product

## Overview
Part 2 requires us to reuse the Part 1 simulation with a minor modification: instead of returning when we find the bot that compares values 61 and 17, we need to run the complete simulation and then extract and multiply the values from output bins 0, 1, and 2.

## Key Observations
1. **The Part 1 solution already tracks outputs** - `outputs = defaultdict(list)` is already populated during simulation
2. **We need to run the full simulation** - Part 1's simulation returns early when it finds the target bot, but Part 2 needs the complete simulation to finish
3. **Simple calculation at the end** - Just extract values from outputs 0, 1, 2 and multiply them

## Algorithm Efficiency
- **Time Complexity**: O(N) where N is the number of instructions/chip transfers
- **Space Complexity**: O(B + O) where B is the number of bots and O is the number of outputs
- This is optimal since we need to process each chip transfer once
- The input size is reasonable (~230 lines), so no optimization needed beyond the existing approach

## Step-by-Step Implementation

### Step 1: Copy and Adapt Part 1 Code Structure
- Copy the entire `part_1_solution.py` as the base
- Reuse functions: `parse_input()`, `give_chip()`
- The parsing logic is identical - same input file format

### Step 2: Modify the `simulate()` Function
- **Current behavior**: Returns the bot number when target values (61, 17) are found
- **New behavior**: Run the complete simulation without early return
- **Changes needed**:
  - Remove the `target_values` parameter (not needed for Part 2)
  - Remove the check `if set(chips) == target_values: return bot_id`
  - Continue simulation until `ready_queue` is empty
  - Return nothing (the outputs dict is already being populated)

### Step 3: Modify the `main()` Function
- Keep the same initialization: parse input, create bots/outputs/ready_queue
- Process initial chip assignments the same way
- Call the modified `simulate()` function
- **After simulation completes**:
  - Extract values from `outputs[0]`, `outputs[1]`, and `outputs[2]`
  - According to problem statement (problem.md:39), we expect exactly one chip per output bin
  - Based on the input analysis, only 3 bots send directly to outputs 0, 1, 2:
    - Bot 18 → output 0 (low chip)
    - Bot 127 → output 1 (low chip)
    - Bot 180 → output 2 (low chip)
  - Therefore, each output should have exactly 1 chip
  - Calculate product: `outputs[0][0] * outputs[1][0] * outputs[2][0]`
  - Print the product

### Step 4: Handle Edge Cases and Validation
- Verify that outputs 0, 1, and 2 all exist and contain chips
- Check that each has exactly one chip (as expected from problem)
- Verify the product is positive and non-zero (sanity check)
- If any validation fails, print a clear error message

## Code Structure
```python
# Reuse from Part 1:
# - parse_input() [no changes]
# - give_chip() [no changes]

# Modified function:
def simulate(bots, outputs, rules, ready_queue):
    """Run complete simulation without early return"""
    while ready_queue:
        bot_id = ready_queue.popleft()
        chips = bots[bot_id]

        # Process bot: distribute low and high chips
        low_chip = min(chips)
        high_chip = max(chips)

        # Give chips to destinations
        # ... (same logic as Part 1)

        # Clear bot's chips
        bots[bot_id] = []

    # No return value needed

def main():
    # Parse and initialize (same as Part 1)
    rules, initial_assignments = parse_input('input.md')
    bots = defaultdict(list)
    outputs = defaultdict(list)
    ready_queue = deque()

    # Process initial assignments (same as Part 1)
    for chip_value, bot_num in initial_assignments:
        give_chip('bot', bot_num, chip_value, bots, outputs, ready_queue)

    # Run complete simulation
    simulate(bots, outputs, rules, ready_queue)

    # Extract and multiply values from outputs 0, 1, 2
    # Validation: Check each output exists and has chips
    for output_num in [0, 1, 2]:
        if output_num not in outputs or not outputs[output_num]:
            print(f"ERROR: Output {output_num} is empty")
            return
        if len(outputs[output_num]) != 1:
            print(f"WARNING: Output {output_num} has {len(outputs[output_num])} chips (expected 1)")

    # Calculate product
    value_0 = outputs[0][0]
    value_1 = outputs[1][0]
    value_2 = outputs[2][0]
    product = value_0 * value_1 * value_2

    # Sanity check
    if product <= 0:
        print(f"ERROR: Invalid product {product} from values {value_0}, {value_1}, {value_2}")
        return

    print(product)
```

## Implementation Notes
- The simulation is deterministic - each bot processes exactly once when it has 2 chips
- No race conditions since we process bots sequentially from the queue
- The output bins accumulate chips throughout the simulation
- Input file is 'input.md' (verified from part_1_solution.py:96)
- Based on input analysis:
  - Only bot 18 sends to output 0 (line 61 of input.md)
  - Only bot 127 sends to output 1 (line 1 of input.md)
  - Only bot 180 sends to output 2 (line 32 of input.md)
  - Therefore, each output will have exactly 1 chip
- Keep the assertion from Part 1 (part_1_solution.py:69) to catch bugs during simulation
