# Testing Plan: Balance Bots - Bot Comparison Tracker

## Testing Strategy Overview

We need to verify that our simulation correctly:
1. Parses all input instructions
2. Simulates chip distribution accurately
3. Identifies the correct bot comparing values 61 and 17
4. Handles the cascade of chip transfers properly

**Testing Approach**: For this script, we'll use:
- Simple `assert` statements for unit tests
- Manual verification for the example
- Debug print statements for tracing (when needed)
- No formal testing framework needed (pytest/unittest)

**Integration with Implementation**: Tests will verify the following functions from solution.py:
- `parse_input(filename)` - input parsing
- `give_chip(...)` - chip distribution logic
- `simulate(...)` - main simulation loop
- `main()` - end-to-end execution

## Test Categories

### 1. Input Parsing Tests

**Test 1.1: Parse Value Assignment**
- Input: `"value 23 goes to bot 138"`
- Expected: Extract chip=23, bot=138
- Validates: Regex pattern matching for value assignments

**Test 1.2: Parse Bot Rule - Bot Destinations**
- Input: `"bot 2 gives low to bot 1 and high to bot 0"`
- Expected: bot=2, low=('bot', 1), high=('bot', 0)
- Validates: Rule parsing with bot destinations

**Test 1.3: Parse Bot Rule - Mixed Destinations**
- Input: `"bot 1 gives low to output 1 and high to bot 0"`
- Expected: bot=1, low=('output', 1), high=('bot', 0)
- Validates: Mixed bot/output destinations

**Test 1.4: Parse Bot Rule - Output Destinations**
- Input: `"bot 0 gives low to output 2 and high to output 0"`
- Expected: bot=0, low=('output', 2), high=('output', 0)
- Validates: Output-only destinations

**Test 1.5: Parse All Input Lines**
- Input: Full input.md file (232 lines)
- Expected: No parsing errors, all lines processed
- Validates: Robustness of parsing logic

**How to execute parsing tests**:
```python
# Test parse_input function directly
rules, assignments = parse_input('input.md')

# Verify we got reasonable outputs
assert len(rules) > 0, "Should have parsed some bot rules"
assert len(assignments) > 0, "Should have parsed some value assignments"

# Spot check a few known rules from input.md
assert 127 in rules, "Bot 127 should have a rule"
assert rules[127] == (('output', 1), ('bot', 180)), "Bot 127 rule should match"
```

### 2. Simulation Logic Tests

**Test 2.1: Example from Problem Statement** ⭐ CRITICAL TEST
- Input: The 6-line example from problem.md
- Expected: Bot 2 compares values 2 and 5
- Validates: Basic simulation correctness, end-to-end flow

**How to execute**:
1. Create a test file `example_input.txt` with:
```
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
```

2. Modify solution to accept filename parameter or create a test harness:
```python
# Test harness
from solution import parse_input, simulate, give_chip
from collections import defaultdict, deque

rules, assignments = parse_input('example_input.txt')
bots = defaultdict(list)
outputs = defaultdict(list)
ready_queue = deque()

for chip_value, bot_num in assignments:
    give_chip('bot', bot_num, chip_value, bots, outputs, ready_queue)

# Modify simulate to accept target values as parameters
# Or just run and look for bot comparing 2 and 5
answer = simulate(bots, outputs, rules, ready_queue, target_values={2, 5})
assert answer == 2, f"Expected bot 2, got {answer}"
print("✓ Example test passed")
```

3. Alternative: Add debug output to main simulation to print all comparisons:
```python
# In simulate(), before checking for {61, 17}:
print(f"Bot {bot_id} comparing {min(chips)} and {max(chips)}")
# Run with example input and verify output shows "Bot 2 comparing 2 and 5"
```

**Test 2.2: Bot Receives Chips in Different Orders**
- Scenario: Bot gets chip A, then chip B vs. chip B, then chip A
- Expected: Same comparison result (order shouldn't matter)
- Validates: min/max logic works regardless of chip arrival order

**Test case**:
```python
# Create minimal test
from collections import defaultdict, deque

# Test 1: Receive chips in order 3, 5
bots1 = defaultdict(list)
ready_queue1 = deque()
bots1[0].append(3)
bots1[0].append(5)
assert min(bots1[0]) == 3 and max(bots1[0]) == 5

# Test 2: Receive chips in order 5, 3
bots2 = defaultdict(list)
bots2[0].append(5)
bots2[0].append(3)
assert min(bots2[0]) == 3 and max(bots2[0]) == 5

print("✓ Order independence verified")
```

**Test 2.3: Chain Reaction**
- Scenario: Bot A → Bot B → Bot C cascade
- Expected: All bots process in correct sequence
- Validates: Queue-based processing, cascading transfers

**Test case**:
```
value 3 goes to bot 0
value 5 goes to bot 0
bot 0 gives low to bot 1 and high to bot 2
value 7 goes to bot 1
bot 1 gives low to output 0 and high to output 1
value 9 goes to bot 2
bot 2 gives low to output 2 and high to output 3
```

Expected sequence:
1. Bot 0 gets 3 and 5, sends 3→bot 1, 5→bot 2
2. Bot 1 now has 3 and 7, sends 3→output 0, 7→output 1
3. Bot 2 now has 5 and 9, sends 5→output 2, 9→output 3

Verify: All four outputs should have one chip each

**Test 2.4: Multiple Bots Ready Simultaneously**
- Scenario: Initial state has 2+ bots with 2 chips each
- Expected: All bots process (order may vary but all must complete)
- Validates: Queue handles multiple ready bots

**Test 2.5: Output Bins Don't Trigger Processing**
- Scenario: Chip sent to output bin
- Expected: Chip stored, no further processing triggered
- Validates: Outputs are terminal destinations

### 3. Edge Cases

**Test 3.1: Bot with Only One Chip**
- Scenario: Bot receives 1 chip but never gets a second
- Expected: Bot never processes (stays in pending state)
- Validates: Two-chip requirement enforced

**Test case**:
```
value 42 goes to bot 0
bot 0 gives low to output 0 and high to output 1
```

Expected:
- Bot 0 has 1 chip in its list
- Bot 0 is NOT in ready_queue
- Outputs 0 and 1 remain empty
- Simulation completes without processing bot 0

**Test 3.2: Same Value Chips**
- Scenario: Bot receives chips with same value (e.g., 5 and 5)
- Expected: min=5, max=5, both sent correctly
- Validates: min/max works with duplicates

**Test 3.3: Large Value Numbers**
- Scenario: Chip values like 73, 67, 61
- Expected: Correct comparison and routing
- Validates: No integer overflow or comparison issues

**Test 3.4: High Bot Numbers**
- Scenario: Bot 209 (highest in input)
- Expected: Processes correctly
- Validates: No indexing issues with high bot numbers

### 4. Target Values Detection

**Test 4.1: Find Bot Comparing 61 and 17**
- Input: Full input.md
- Expected: Returns a valid bot number (0-209)
- Validates: Core requirement - finding the answer

**Test 4.2: Verify 61 and 17 Arrive at Same Bot**
- Check: Both values 61 and 17 are in input
- Check: They eventually meet at the same bot
- Validates: Problem has a solution in the input

**Test 4.3: The Specific Comparison of {61, 17} Happens Exactly Once**
- Monitor: How many times the set {61, 17} is compared
- Expected: Exactly one bot should compare these specific values
- Validates: No duplicate processing of the target comparison

**How to verify**:
```python
# Add counter in simulate()
comparisons_61_17 = 0
while ready_queue:
    bot_id = ready_queue.popleft()
    chips = bots[bot_id]

    if set(chips) == {61, 17}:
        comparisons_61_17 += 1
        answer = bot_id
    # ... rest of simulation

assert comparisons_61_17 == 1, f"Expected exactly 1 comparison, got {comparisons_61_17}"
```

### 5. State Consistency Tests

**Test 5.1: Chips Don't Disappear (Conservation Check)**
- Count: Total chips in initial assignments
- Count: Total chips in system after simulation
- Expected: Equal (conservation of chips)
- Validates: No chips lost or duplicated

**Implementation**:
```python
# After simulation completes:
initial_chip_count = len(assignments)

# Count chips in all locations
final_chip_count = 0
for bot_chips in bots.values():
    final_chip_count += len(bot_chips)
for output_chips in outputs.values():
    final_chip_count += len(output_chips)

assert initial_chip_count == final_chip_count, \
    f"Chip count mismatch: started with {initial_chip_count}, ended with {final_chip_count}"
print(f"✓ Conservation verified: {initial_chip_count} chips")
```

**Test 5.2: Bots Process At Most Once**
- Monitor: Each bot's processing count
- Expected: 0 or 1 (never more than once)
- Validates: Bots don't re-process after clearing chips

**Implementation**:
```python
# Track which bots have processed
processed_bots = set()

# In simulate() loop, after popping from queue:
if bot_id in processed_bots:
    raise ValueError(f"Bot {bot_id} processing twice!")
processed_bots.add(bot_id)
# ... continue with processing

print(f"✓ Processed {len(processed_bots)} bots, no duplicates")
```

**Test 5.3: All Initial Chips Distributed**
- Check: All initial value assignments trigger transfers
- Expected: No chips stuck in initial state
- Validates: Initialization works correctly

## Manual Verification Steps

### Step 1: Trace Example
Run the provided example and manually trace:
- Bot 2: receives 5 and 2 → compares → sends 2 to bot 1, 5 to bot 0
- Bot 1: has 3, receives 2 → compares → sends 2 to output 1, 3 to bot 0
- Bot 0: receives 5 and 3 → compares → sends 3 to output 2, 5 to output 0
- Verify output: Bot 2

### Step 2: Check Target Values in Input
Verify that both target values exist in the input:
```bash
grep "value 61" input.md  # Should find: value 61 goes to bot 187
grep "value 17" input.md  # Should find: value 17 goes to bot 155
```

**Manual trace** (optional, for verification):
To manually trace where chips 61 and 17 meet:
1. Start at bot 187 (has chip 61) and bot 155 (has chip 17)
2. Look up each bot's rule to see where it sends its chips
3. Follow the chain until both chips arrive at the same bot
4. This is tedious but possible for verification

**Easier approach**: Add debug logging to simulation:
```python
# Track specific chips
if 61 in chips or 17 in chips:
    print(f"Bot {bot_id} has chip(s): {chips}")
```
Run simulation and look for the bot that prints both 61 and 17

### Step 3: Validate Final Answer
Run solution with full input and verify:
```python
answer = main()  # Or capture from simulate()

# Validation checks:
assert answer is not None, "No solution found"
assert isinstance(answer, int), f"Answer should be int, got {type(answer)}"
assert 0 <= answer <= 209, f"Answer {answer} out of valid range"
assert answer in rules, f"Bot {answer} has no rules defined"

print(f"✓ Answer validated: Bot {answer}")
```

### Step 4: Sanity Check Outputs
After simulation:
- Check some output bins have chips
- Verify no bots still holding 2 chips (all should be processed or have 0-1 chips)

## Debugging Aids

If answer is incorrect, add these debug outputs:

1. **Comparison Logger**: Print every bot comparison
   - Format: "Bot X comparing Y and Z"
   - Look for when 61 and 17 appear

2. **State Snapshot**: Print system state at key points
   - After initialization
   - After each bot processes
   - At completion

3. **Queue Monitor**: Print queue contents
   - Shows processing order
   - Helps identify if bots aren't getting queued

## Success Criteria

The solution is correct if:

✅ **Parsing**: All 232 input lines parsed without errors
✅ **Example test**: Passes the provided example (returns bot 2 for values {2, 5})
✅ **Output format**: Returns a single integer for the full input
✅ **Simulation completes**: Queue empties, no infinite loops
✅ **Determinism**: Answer is consistent across multiple runs (same answer every time)
✅ **Conservation**: All initial chips are accounted for in final state
✅ **Valid answer**: Answer is a valid bot number (0-209) with defined rules

**Minimum required test**: The example test (Test 2.1) MUST pass before running on full input.

## Testing Execution Order

**Phase 1: Unit Tests** (Quick validation)
1. Test `parse_input()` with a few sample lines
2. Test `give_chip()` logic with simple scenarios
3. Test order independence (Test 2.2)

**Phase 2: Integration Test** (CRITICAL)
4. **Test the example from problem statement (Test 2.1)** ⭐
   - This is the most important test
   - Must pass before proceeding to full input
   - Validates end-to-end correctness

**Phase 3: Full Input** (Production run)
5. Run solution on input.md
6. Validate answer format and range
7. Optional: Run state consistency checks (Tests 5.1, 5.2)

**Phase 4: Verification** (If needed)
8. Manual trace of chips 61 and 17 (Step 2)
9. Debug logging to verify comparison sequence

**If example test fails**:
- Add debug output to show all bot comparisons
- Manually trace through the example step-by-step
- Check queue ordering (FIFO vs LIFO)
- Verify chips are being cleared after processing

This testing approach ensures correctness without over-testing trivial cases, focusing on the aspects that matter for solving this specific problem.

## Quick Test Script Template

For rapid testing, create `test_solution.py`:
```python
from solution import *

def test_example():
    """Test the example from problem statement"""
    rules, assignments = parse_input('example_input.txt')
    bots = defaultdict(list)
    outputs = defaultdict(list)
    ready_queue = deque()

    for chip_value, bot_num in assignments:
        give_chip('bot', bot_num, chip_value, bots, outputs, ready_queue)

    # Modify simulate to accept target parameter or check manually
    # For now, add print statements to see all comparisons
    result = simulate(bots, outputs, rules, ready_queue)
    assert result == 2, f"Expected bot 2, got {result}"
    print("✓ Example test passed!")

if __name__ == '__main__':
    test_example()
    print("All tests passed!")
```
