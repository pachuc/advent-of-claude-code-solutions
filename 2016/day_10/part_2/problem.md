# Problem: Balance Bots Part 2 - Output Bin Product

## Context from Part 1

In Part 1, we simulated a factory with robots (bots) that pass microchips with numeric values to each other. Each bot:
- Only processes when it holds exactly 2 microchips
- When it has 2 chips, it gives the lower-value chip to one destination and the higher-value chip to another destination
- Destinations can be either other bots or numbered output bins

We successfully simulated the entire system and found that **bot 98** was responsible for comparing microchip values 61 and 17.

## Part 2 Objective

After the simulation completes, multiply together the values of one chip in each of output bins 0, 1, and 2.

## Input Format

The input is the same as Part 1, containing two types of instructions:

1. **Initial value assignment**: `value X goes to bot Y`
   - Assigns a microchip with value X to bot Y

2. **Bot behavior rules**: `bot X gives low to [bot/output] Y and high to [bot/output] Z`
   - Defines what bot X does with its chips when it has 2
   - "low" = the lower-value chip goes to destination Y
   - "high" = the higher-value chip goes to destination Z
   - Destinations can be either `bot N` or `output N`

## Processing

1. Run the complete simulation (same as Part 1) until all chips have been distributed to their final destinations
2. Track which microchip values end up in which output bins
3. After the simulation completes, retrieve the values stored in output bins 0, 1, and 2
4. Multiply these three values together

## Important Notes

- Output bins can contain multiple chips (unlike bots which only hold 2 at a time before processing)
- The problem states "one chip in each of outputs 0, 1, and 2" - this implies each of these output bins will contain at least one chip
- If an output bin contains multiple chips, we should use the value of one of them (likely there will be exactly one chip per output bin)

## Expected Output

**A single integer**: the product of (value in output 0) × (value in output 1) × (value in output 2)

## Example

If the simulation results in:
- Output bin 0 contains chip with value 5
- Output bin 1 contains chip with value 2
- Output bin 2 contains chip with value 3

The answer would be: 5 × 2 × 3 = **30**

## Answer Format

Return just the product as an integer (e.g., `30` for the example above).

## Implementation Strategy

Reuse the simulation code from Part 1, but:
1. Continue tracking output bins throughout the simulation
2. After the simulation completes, extract the values from outputs 0, 1, and 2
3. Multiply these values together to get the final answer
