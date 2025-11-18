# Implementation Plan - Part 2: Firewall Packet Scanner

## Overview
Find the minimum delay (in picoseconds) needed before starting the packet's journey so that it can traverse all firewall layers without being caught by any scanner.

## Key Differences from Part 1
- **Part 1**: Calculated severity when immediately entering (delay=0)
- **Part 2**: Find minimum delay where packet is NOT caught at ANY layer
- **Core Logic Reusable**: Scanner position calculation and period logic from Part 1 can be adapted

## Algorithm Strategy

### Approach: Brute Force with Early Termination
Given that the delay could be large, we'll use a simple iteration strategy with optimizations:
1. Start with delay = 0 and increment
2. For each delay, check if packet is caught at any layer
3. Use early termination: as soon as we detect a catch, skip to next delay
4. Return the first delay where packet passes through all layers safely

### Time Complexity Analysis
- Input size: ~44 layers (based on input.md)
- For each delay d, we check O(n) layers where n = number of layers
- Expected worst case: We may need to check many delays, but with Chinese Remainder Theorem insights, the answer typically appears within reasonable bounds
- Practical complexity: O(d * n) where d = answer and n = number of layers
- Given the small number of layers (44), even if d is in the millions, this should run in seconds

## Implementation Steps

### Step 1: Reuse Part 1 Parsing Logic
**Action**: Copy the `parse_input()` function from part_1_solution.py
- Already handles the "depth: range" format correctly
- Returns list of (depth, range) tuples
- No changes needed

### Step 2: Adapt the Caught Detection Logic
**Action**: Modify the `is_caught()` function to accept a delay parameter

**Note on approach**: The Part 1 function had signature `is_caught(depth, range_val)`. For Part 2, we'll modify it to add a `delay` parameter with default value 0 for backward compatibility, though since we're writing a fresh solution for Part 2, we can simply use the new signature.

**Changes needed**:
```python
def is_caught(depth, range_val, delay):
    """
    Determine if packet is caught at given layer with a specific delay.

    Args:
        depth: Layer depth (0-indexed position)
        range_val: Height of the layer (scanner range)
        delay: Number of picoseconds to wait before starting

    Returns:
        True if caught, False if safe
    """
    # Edge case: range=1 means scanner always at position 0
    if range_val == 1:
        return True  # Always caught regardless of delay

    # Calculate period of scanner oscillation
    period = 2 * (range_val - 1)

    # Packet enters this layer at time = delay + depth
    # Scanner is at position 0 if (delay + depth) % period == 0
    time_at_layer = delay + depth
    return time_at_layer % period == 0
```

**Key modification**: The time when packet enters a layer is now `delay + depth` instead of just `depth`

### Step 3: Implement Delay Search Function
**Action**: Create a new function to find minimum safe delay

```python
def find_minimum_delay(layers):
    """
    Find the minimum delay needed to pass through firewall without being caught.

    Args:
        layers: List of (depth, range) tuples

    Returns:
        Integer representing minimum delay in picoseconds
    """
    delay = 0

    while True:
        # Check if this delay allows safe passage through all layers
        caught = False

        for depth, range_val in layers:
            if is_caught(depth, range_val, delay):
                caught = True
                break  # Early termination: skip to next delay

        if not caught:
            # Found a safe delay!
            return delay

        delay += 1
```

**Optimization notes**:
- Early termination: Break out of layer loop as soon as we detect a catch
- This avoids checking remaining layers for delays we know won't work
- Could add additional optimizations (see Step 5) if needed

**Progress monitoring**:
- For potentially long-running searches, add progress output
- Print current delay being checked every 10,000 iterations
- This provides feedback and helps estimate completion time
- Example: `if delay % 10000 == 0: print(f"Checking delay {delay}...")`

### Step 4: Update Main Function
**Action**: Modify the main() function to call the new delay search

```python
def main():
    # Parse input (reuse from Part 1)
    layers = parse_input('input.md')

    # Find minimum delay
    min_delay = find_minimum_delay(layers)

    # Output result
    print(min_delay)
```

**Note on input file**: Verify that the input file is named `input.md` - if it's named differently (e.g., `input.txt`), update the filename accordingly.

### Step 5: Optional Optimizations (If Needed)

**Decision criteria**: Run the basic solution first. Only implement optimizations if:
- Runtime exceeds 1 minute, OR
- Progress monitoring shows the answer will take unreasonably long (> 5-10 minutes)

If optimization is needed, consider these approaches:

#### Optimization A: Step Size Intelligence
- Most scanners have even periods
- Could try incrementing by 2 or other factors
- Risk: May miss the answer, needs careful implementation

#### Optimization B: Chinese Remainder Theorem (CRT)
- The problem is essentially finding the smallest d such that:
  - `(d + depth₁) % period₁ ≠ 0`
  - `(d + depth₂) % period₂ ≠ 0`
  - ... for all layers
- This is a system of modular inequalities
- More complex to implement, likely overkill for this input size

#### Optimization C: Pre-filter Impossible Layers
- If range=1 at any depth, NO delay will work
- Check this upfront and handle as special case or error

**Recommendation**: Start with the simple brute force approach with progress monitoring. It should be fast enough for this input.

## File Structure
```python
# solution.py

def parse_input(filename):
    # [Reuse from Part 1 - no changes]
    pass

def is_caught(depth, range_val, delay):
    # [Modified from Part 1 - add delay parameter]
    pass

def find_minimum_delay(layers):
    # [New function for Part 2]
    # Include optional progress monitoring
    pass

def verify_delay(layers, delay):
    # [Optional verification function]
    # Returns True if delay allows safe passage through all layers
    pass

def main():
    # [Modified from Part 1 - call find_minimum_delay instead of calculate_severity]
    # Optionally verify the answer before printing
    pass

if __name__ == '__main__':
    main()
```

## Edge Cases to Handle

1. **range = 1**: Scanner always at position 0
   - If ANY layer has range=1, there is NO valid delay (impossible to pass)
   - Check if input has any such layers (looking at input.md, none visible)

2. **depth = 0**: First layer
   - Time at layer = delay + 0 = delay
   - Need: delay % period ≠ 0

3. **Large delays**:
   - Algorithm may need to check thousands or millions of delays
   - Monitor performance during testing

4. **Empty input**:
   - If no layers, delay = 0 works (but unlikely given puzzle context)

## Expected Behavior
- Input: List of "depth: range" pairs from input.md
- Output: Single integer (minimum delay in picoseconds)
- Performance: Should complete in reasonable time (< 1 minute preferred; if > 5 minutes, consider optimizations)
- Progress: Optional progress output every 10,000 iterations to monitor execution

## Optional Verification Step
After finding the minimum delay, optionally verify:
1. The found delay allows safe passage through all layers
2. The previous delay (answer - 1) would result in at least one catch
This confirms both correctness and minimality of the answer.

## Testing Integration
The implementation will be tested using the test plan (test_plan.md) which includes:
- Small example from problem description
- Edge cases
- Full input validation
