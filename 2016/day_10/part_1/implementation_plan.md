# Implementation Plan: Balance Bots - Bot Comparison Tracker

## Problem Analysis

We need to simulate a factory where bots pass microchips to each other and find which bot compares values 61 and 17.

**Key Observations:**
- This is a discrete event simulation problem
- Bots process chips when they have exactly 2 chips
- Processing cascades through the network
- We need to track which bot holds and compares values 61 and 17

**Input Characteristics:**
- ~230 instruction lines
- Mix of initial value assignments and bot behavior rules
- Bots numbered 0-209, outputs numbered 0-20
- We need to find: bot comparing 61 and 17 (both values present in input)

## Algorithm Approach

**Simulation Strategy:**
- Use a queue-based event simulation (BFS-like approach)
- Process bots as they receive their second chip
- Track chip holdings for each bot
- Check each bot when it gets 2 chips to see if it's comparing 61 and 17

**Time Complexity:** O(N) where N is the number of chips/bots
- Each chip is processed once
- Each bot processes at most once (when it has 2 chips)

**Space Complexity:** O(B) where B is the number of bots
- Storage for bot holdings, rules, and processing queue

## Step-by-Step Implementation Plan

### Step 1: Data Structure Design

Define the following data structures:

1. **Bot chip storage**: `dict[int, list[int]]`
   - Key: bot number
   - Value: list of chips (max 2)

2. **Bot rules**: `dict[int, tuple[destination_low, destination_high]]`
   - Key: bot number
   - Value: tuple of (low_dest, high_dest) where each dest is (type, number)
   - type: 'bot' or 'output'

3. **Output bins**: `dict[int, list[int]]`
   - Key: output bin number
   - Value: list of chips received

4. **Ready queue**: `deque[int]`
   - Queue of bot numbers that have 2 chips and are ready to process

### Step 2: Input Parsing

Create a parser that:

1. Read all lines from input file (input.md)
2. For each line, identify instruction type:
   - Pattern: `value X goes to bot Y` → assign chip X to bot Y
   - Pattern: `bot X gives low to [bot/output] Y and high to [bot/output] Z` → store rule
3. Use regex for robust parsing:
   - `value (\d+) goes to bot (\d+)`
   - `bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)`
4. Store initial chip assignments separately to process after all rules are loaded

**Function signature**: `parse_input(filename: str) -> tuple[dict, list]`
- Returns: (rules_dict, initial_assignments_list)
- rules_dict format: `{bot_num: ((low_type, low_num), (high_type, high_num))}`
- initial_assignments_list format: `[(chip_value, bot_num), ...]`

### Step 3: Initialization

1. Parse all bot rules first (to build complete rule set)
   - **Why this order matters**: Bots need their behavior rules defined before they can process chips. If we assign chips before parsing rules, a bot might receive 2 chips but have no rule for how to distribute them.
2. Then process initial value assignments:
   - Add chip to bot's chip list
   - If bot now has 2 chips, add to ready queue

### Step 4: Simulation Loop

Implement main simulation loop:

**Function signature**: `simulate(bots, outputs, rules, ready_queue) -> int`
- Returns: bot number that compares 61 and 17
- Modifies: bots, outputs, ready_queue (passed by reference)

```python
while ready_queue:
    bot_id = ready_queue.popleft()  # FIFO order for proper BFS
    chips = bots[bot_id]  # Should have exactly 2 chips

    # Basic assertion for debugging
    assert len(chips) == 2, f"Bot {bot_id} should have 2 chips, has {len(chips)}"

    # Check if this bot compares 61 and 17
    if set(chips) == {61, 17}:
        return bot_id  # Found the answer!

    # Process the bot
    low_chip = min(chips)
    high_chip = max(chips)

    low_dest_type, low_dest_num = rules[bot_id][0]
    high_dest_type, high_dest_num = rules[bot_id][1]

    # Give low chip to low destination
    give_chip(low_dest_type, low_dest_num, low_chip, bots, outputs, ready_queue)

    # Give high chip to high destination
    give_chip(high_dest_type, high_dest_num, high_chip, bots, outputs, ready_queue)

    # Clear this bot's chips to prevent double-processing
    bots[bot_id] = []

# If we exit loop without finding answer, the input doesn't have a solution
return None
```

### Step 5: Chip Distribution Helper

Create chip distribution helper function:

**Function signature**: `give_chip(dest_type, dest_num, chip_value, bots, outputs, ready_queue) -> None`

```python
def give_chip(dest_type, dest_num, chip_value, bots, outputs, ready_queue):
    if dest_type == 'output':
        # Add chip to output bin (terminal destination)
        outputs[dest_num].append(chip_value)
    elif dest_type == 'bot':
        # Add chip to bot's chip list
        bots[dest_num].append(chip_value)
        # If bot now has exactly 2 chips, it's ready to process
        if len(bots[dest_num]) == 2:
            ready_queue.append(dest_num)
```

### Step 6: Main Function Structure

**Required imports**:
```python
import re
from collections import defaultdict, deque
```

**Main function**:
```python
def main():
    # Parse input file
    rules, initial_assignments = parse_input('input.md')

    # Initialize data structures
    bots = defaultdict(list)  # bot_num -> list of chip values
    outputs = defaultdict(list)  # output_num -> list of chip values
    ready_queue = deque()  # queue of bot numbers ready to process

    # Process initial chip assignments
    # This must happen AFTER rules are parsed
    for chip_value, bot_num in initial_assignments:
        give_chip('bot', bot_num, chip_value, bots, outputs, ready_queue)

    # Run simulation to find which bot compares 61 and 17
    answer = simulate(bots, outputs, rules, ready_queue)

    # Validate answer before printing
    if answer is None:
        print("ERROR: No bot compared 61 and 17")
        return

    # Output result (single integer, followed by newline)
    print(answer)

if __name__ == '__main__':
    main()
```

### Step 7: Edge Cases to Handle

1. **Bot receives chips in any order**: Already handled by using min/max
2. **Multiple bots ready simultaneously**: Queue ensures all are processed
3. **Chips going to outputs**: Don't add to ready queue
4. **Bot already processed**: Clear chips after processing so they can't process twice

### Step 8: Answer Validation and Output

Before printing the answer:
1. Verify answer is not None (i.e., 61 and 17 were compared)
2. Verify answer is a valid bot number (0-209 range based on input)
3. Optional: Verify answer bot has a rule defined

Output format:
- Print the bot number as a single integer
- Followed by a newline
- No prefix text or additional formatting
- Example output: `2\n` (for bot 2)

## Code Organization

```
solution.py
├── Imports: re, defaultdict, deque
├── parse_input(filename: str) → tuple[dict, list]
│   Returns: (rules_dict, initial_assignments_list)
├── give_chip(dest_type, dest_num, chip_value, bots, outputs, ready_queue) → None
│   Distributes chip to destination and updates ready_queue if needed
├── simulate(bots, outputs, rules, ready_queue) → int | None
│   Returns: bot number that compares 61 and 17, or None if not found
└── main() → None
    Orchestrates parsing, initialization, simulation, and output
```

## Algorithm Efficiency

**Why this is efficient:**
- Single pass through all instructions: O(N) parsing
- Each bot processes exactly once: O(B) simulation
- Each chip moves at most once through the system: O(C) chip movements
- Total: O(N + B + C) ≈ O(N) for reasonable inputs

**Memory efficiency:**
- Only store current state, not history
- Chips removed from bots after processing
- Total space: O(B + O) for bots and outputs

This approach will handle the ~230 line input efficiently, completing in milliseconds.
