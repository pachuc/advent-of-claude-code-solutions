# Problem Report: Finding the Lowest House Number with Sufficient Presents

## Objective
Find the lowest house number that receives at least a specified number of presents.

## Problem Context
Elves are delivering presents to an infinite street of houses numbered sequentially (1, 2, 3, 4, ...). Each elf has a number and delivers presents to houses based on a specific pattern.

## Delivery Rules

1. **Elf Assignment Pattern**: Elf number `N` delivers presents to every `N`-th house
   - Elf 1 delivers to houses: 1, 2, 3, 4, 5, ... (every house)
   - Elf 2 delivers to houses: 2, 4, 6, 8, 10, ... (every 2nd house)
   - Elf 3 delivers to houses: 3, 6, 9, 12, 15, ... (every 3rd house)
   - In general: Elf N delivers to houses N, 2N, 3N, 4N, ...

2. **Present Calculation**: Each elf delivers presents equal to **10 times their elf number**
   - Elf 1 delivers 10 presents to each house they visit
   - Elf 2 delivers 20 presents to each house they visit
   - Elf N delivers (N × 10) presents to each house they visit

3. **Total Presents per House**: A house receives the sum of presents from all elves that visit it
   - House number H is visited by all elves whose number is a divisor of H
   - Total presents at house H = 10 × (sum of all divisors of H)

## Examples

- House 1: Visited by Elf 1 → 10 presents
- House 2: Visited by Elves 1, 2 → 10 + 20 = 30 presents
- House 3: Visited by Elves 1, 3 → 10 + 30 = 40 presents
- House 4: Visited by Elves 1, 2, 4 → 10 + 20 + 40 = 70 presents
- House 6: Visited by Elves 1, 2, 3, 6 → 10 + 20 + 30 + 60 = 120 presents

## Input
A single integer representing the minimum number of presents required.

**Input value**: `34000000`

## Expected Output
A single integer: the lowest house number that receives at least the input number of presents.

## Algorithm Notes
- This is essentially finding the smallest positive integer H where the sum of its divisors multiplied by 10 is at least the target value
- Mathematically: Find minimum H where 10 × σ(H) ≥ target, where σ(H) is the sum of divisors function
- The search space starts at house 1 and continues sequentially until a solution is found
