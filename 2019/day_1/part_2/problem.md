# Problem Report: Fuel Requirement Calculator (Part 2 - Recursive Fuel)

## Objective
Calculate the **total fuel requirement** for all spacecraft modules, including the additional fuel required to carry the fuel itself.

## Background (from Part 1)
In Part 1, fuel for a module was calculated using:
- **Formula:** `fuel = floor(mass / 3) - 2`

Part 1's answer was **3267638** (sum of fuel for all modules without accounting for fuel mass).

## Part 2 - New Requirement
Fuel also has mass, and therefore requires additional fuel to carry it. The calculation must be applied recursively:

1. Calculate fuel for the module's mass
2. Calculate fuel for that fuel's mass
3. Continue until the calculated fuel is zero or negative
4. Sum all the fuel amounts

**Key rule:** Any mass that would require **negative fuel** should be treated as requiring **zero fuel** (stop the recursion).

## Fuel Calculation Formula (Unchanged)
`fuel = floor(mass / 3) - 2`

## Recursive Process
For each module:
1. Calculate initial fuel from module mass
2. If fuel > 0, calculate fuel required for that fuel amount
3. Repeat step 2 until fuel calculation yields 0 or less
4. Sum all positive fuel values

## Examples

### Example 1: Mass of 14
- Module fuel: floor(14/3) - 2 = 4 - 2 = **2**
- Fuel for fuel: floor(2/3) - 2 = 0 - 2 = **-2** (negative, treated as 0)
- **Total: 2**

### Example 2: Mass of 1969
| Step | Input Mass | Fuel Calculated |
|------|------------|-----------------|
| 1    | 1969       | 654             |
| 2    | 654        | 216             |
| 3    | 216        | 70              |
| 4    | 70         | 21              |
| 5    | 21         | 5               |
| 6    | 5          | -1 (stop)       |
- **Total: 654 + 216 + 70 + 21 + 5 = 966**

### Example 3: Mass of 100756
- Fuel sequence: 33583 + 11192 + 3728 + 1240 + 411 + 135 + 43 + 12 + 2 = **50346**

## Input Format
- A text file containing one integer per line
- Each integer represents the mass of a single module
- The input contains 100 module masses
- Same input as Part 1

## Expected Output
- A single integer representing the **total sum of all fuel requirements** for every module
- This includes all recursively calculated fuel for the fuel itself

## Algorithm Steps
1. Read all module masses from the input file
2. For each module mass:
   a. Initialize total_fuel_for_module = 0
   b. Calculate fuel = floor(mass / 3) - 2
   c. While fuel > 0:
      - Add fuel to total_fuel_for_module
      - Set mass = fuel (fuel becomes the new mass to calculate)
      - Recalculate fuel = floor(mass / 3) - 2
3. Sum all total_fuel_for_module values across all modules
4. Output the final total
