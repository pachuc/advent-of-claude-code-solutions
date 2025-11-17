# Problem: Balance Bots - Bot Comparison Tracker

## Objective
Determine which bot is responsible for comparing two specific microchip values (61 and 17).

## Context
A factory contains robots (bots) that pass microchips with numeric values to each other. Each bot:
- Only processes when it holds exactly 2 microchips
- When it has 2 chips, it gives the lower-value chip to one destination and the higher-value chip to another destination
- Destinations can be either other bots or numbered output bins

## Input Format
The input consists of two types of instructions:

1. **Initial value assignment**: `value X goes to bot Y`
   - Assigns a microchip with value X to bot Y

2. **Bot behavior rules**: `bot X gives low to [bot/output] Y and high to [bot/output] Z`
   - Defines what bot X does with its chips when it has 2
   - "low" = the lower-value chip goes to destination Y
   - "high" = the higher-value chip goes to destination Z
   - Destinations can be either `bot N` or `output N`

## Processing Rules
1. Bots receive microchips according to the initial value assignments
2. When a bot has exactly 2 microchips, it executes its behavior rule:
   - Compares the two values
   - Gives the lower value to its "low" destination
   - Gives the higher value to its "high" destination
3. This process cascades as bots receive chips and trigger their own behaviors
4. The system reaches equilibrium when all chips have been distributed

## Example
Given:
```
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
```

Execution:
- Bot 1 starts with chip value 3
- Bot 2 starts with chips value 2 and 5
- Bot 2 compares 2 and 5, gives 2 to bot 1 and 5 to bot 0
- Bot 1 now has 2 and 3, gives 2 to output 1 and 3 to bot 0
- Bot 0 now has 3 and 5, gives 3 to output 2 and 5 to output 0
- **Bot 2 compared values 2 and 5**

## Expected Output
**A single integer**: the number of the bot that compares microchip value 61 with microchip value 17.

Note: The bot that "compares" these values is the one that holds both chips at the same time and processes them according to its behavior rule.

## Answer Format
Return just the bot number as an integer (e.g., `2` for the example above).
