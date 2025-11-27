# Implementation Plan: Fuel Requirement Calculator (Part 2 - Recursive Fuel)

## Overview

Part 2 extends Part 1 by requiring recursive fuel calculation. Fuel itself has mass and requires additional fuel to carry it. We must calculate the total fuel including all the recursively-needed fuel until the fuel requirement drops to zero or negative.

## Key Difference from Part 1

- **Part 1**: Simple calculation: `fuel = floor(mass / 3) - 2` for each module, sum all.
- **Part 2**: For each module, repeatedly apply the fuel formula to the fuel amount itself until the result is zero or negative. Sum all intermediate positive fuel values.

## Algorithm Analysis

### Time Complexity
- For each module mass M, we iterate until the fuel becomes ≤ 0
- Each iteration divides the current value by ~3, so the number of iterations per module is O(log₃(M))
- With N modules, total time complexity is O(N * log(max_mass))
- For 100 modules with masses ~150,000, this is extremely efficient (roughly 100 * 11 = ~1100 iterations max)

### Space Complexity
- O(N) to store the input masses
- O(1) additional space for calculations
- Very efficient for the given input size

### Convergence Guarantee
The algorithm is guaranteed to terminate because:
1. Each iteration computes `fuel = current // 3 - 2`
2. For any positive `current`, the new fuel is strictly less than `current` (since `current // 3 - 2 < current` for all `current >= 0`)
3. Eventually, the fuel becomes ≤ 0, terminating the loop

## Reusing Part 1 Code

The Part 1 solution (`part_1_solution.py`) provides excellent building blocks:

1. **`calculate_fuel(mass)`**: This function remains unchanged and will be reused as-is.
2. **`read_masses(filename)`**: This function remains unchanged and will be reused as-is.
3. **`calculate_total_fuel(masses)`**: This needs modification to use recursive fuel calculation.

**Note on code organization**: For a self-contained puzzle solution, we will copy the functions directly into `solution.py` rather than importing from `part_1_solution.py`. This keeps the solution simple and avoids import path complications. Either approach is valid.

## Edge Case Handling

Before implementation, let's document how the algorithm handles edge cases:

| Mass Range | Initial Fuel | Behavior | Total Fuel |
|------------|--------------|----------|------------|
| 0 | -2 | Loop never executes (fuel ≤ 0) | 0 |
| 1-5 | -2 to -1 | Loop never executes | 0 |
| 6-8 | 0 | Loop never executes | 0 |
| 9-11 | 1 | One iteration, then fuel = -2 | 1 |
| 12-14 | 2 | One iteration, then fuel = -2 | 2 |
| 27-32 | 7-8 | One iteration, then fuel = 0 | 7-8 |
| 33+ | 9+ | Multiple iterations | > initial fuel |

## Implementation Steps

### Step 1: Keep the base `calculate_fuel` function
```python
def calculate_fuel(mass):
    """Calculate fuel required for a given mass.
    Formula: floor(mass / 3) - 2
    Uses integer division for floor behavior.
    """
    return mass // 3 - 2
```
No changes needed.

### Step 2: Keep the `read_masses` function
```python
def read_masses(filename):
    """Read module masses from input file."""
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]
```
No changes needed.

### Step 3: Create a new `calculate_recursive_fuel` function
This is the key new function for Part 2:

```python
def calculate_recursive_fuel(mass):
    """Calculate total fuel for a module including fuel for the fuel.

    For a given module mass, repeatedly calculate fuel needed and add it
    to the total. The fuel itself has mass, so we calculate fuel for the
    fuel, and so on until the calculated fuel is zero or negative.

    Args:
        mass: The module mass (non-negative integer)

    Returns:
        Total fuel needed including recursive fuel requirements (always >= 0)
    """
    total_fuel = 0
    fuel = calculate_fuel(mass)

    while fuel > 0:
        total_fuel += fuel
        fuel = calculate_fuel(fuel)

    return total_fuel
```

**Logic explanation:**
1. Calculate the initial fuel needed for the module mass
2. While fuel is positive:
   - Add it to the running total
   - Calculate fuel needed for that fuel amount (fuel becomes the new "mass")
3. When fuel becomes zero or negative, stop and return the total

**Handling edge cases:**
- If `mass` is small (≤ 8), initial `fuel` is ≤ 0, loop never executes, returns 0
- If `mass` is 0, `fuel = -2`, loop never executes, returns 0
- For masses 9+, at least one iteration occurs

### Step 4: Modify `calculate_total_fuel` to use recursive calculation
```python
def calculate_total_fuel(masses):
    """Calculate total fuel for all masses including recursive fuel."""
    return sum(calculate_recursive_fuel(mass) for mass in masses)
```

### Step 5: Update the `main` function with optional validation
```python
def main():
    # Read input
    masses = read_masses('input.md')

    # Calculate total fuel
    total_fuel = calculate_total_fuel(masses)

    # Output result
    print(total_fuel)


if __name__ == '__main__':
    main()
```

## Complete Solution Structure

```python
def calculate_fuel(mass):
    """Calculate fuel required for a given mass."""
    return mass // 3 - 2


def calculate_recursive_fuel(mass):
    """Calculate total fuel including fuel for the fuel itself."""
    total_fuel = 0
    fuel = calculate_fuel(mass)

    while fuel > 0:
        total_fuel += fuel
        fuel = calculate_fuel(fuel)

    return total_fuel


def read_masses(filename):
    """Read module masses from input file."""
    with open(filename, 'r') as f:
        return [int(line.strip()) for line in f if line.strip()]


def calculate_total_fuel(masses):
    """Calculate total fuel for all masses including recursive fuel."""
    return sum(calculate_recursive_fuel(mass) for mass in masses)


def main():
    masses = read_masses('input.md')
    total_fuel = calculate_total_fuel(masses)
    print(total_fuel)


if __name__ == '__main__':
    main()
```

## Alternative Implementation Approaches

### Approach 1: Iterative (Recommended - shown above)
- Uses a while loop
- Clear and readable
- Efficient memory usage (no stack overhead)

### Approach 2: True Recursion
```python
def calculate_recursive_fuel(mass):
    fuel = calculate_fuel(mass)
    if fuel <= 0:
        return 0
    return fuel + calculate_recursive_fuel(fuel)
```
- More elegant but has function call overhead
- Could hit recursion limit for extremely large masses (not a concern for this input)
- Maximum recursion depth ~11 for masses up to 150,000

**Recommendation**: Use the iterative approach for clarity and efficiency.

## Verification Against Examples

Before running on full input, verify against provided examples:

1. **Mass 14**: Expected total = 2
   - Fuel: floor(14/3) - 2 = 2
   - Fuel for 2: floor(2/3) - 2 = -2 (stop)
   - Total: 2 ✓

2. **Mass 1969**: Expected total = 966
   - 654 + 216 + 70 + 21 + 5 = 966 ✓

3. **Mass 100756**: Expected total = 50346
   - 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = 50346 ✓

## Expected Output

The answer will be greater than Part 1's answer (3267638) since we're now adding fuel for the fuel itself. The exact answer needs to be computed by running the solution.

**Expected bounds:**
- Lower bound: > 3,267,638 (Part 1 answer)
- Upper bound: < 6,535,276 (approximately 2× Part 1; fuel-for-fuel won't double the total)
- Realistic estimate: ~1.4x to 1.6x Part 1 answer

## Files to Create/Modify

- **Create**: `solution.py` - The complete Part 2 solution
- **Reference**: `part_1_solution.py` - Reuse `calculate_fuel` and `read_masses` functions
- **Input**: `input.md` - Same input file as Part 1
