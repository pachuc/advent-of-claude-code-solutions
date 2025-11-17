# Problem Report: AdventCoin Mining (Part 2)

## Objective
Find the lowest positive integer that, when appended to a secret key string, produces an MD5 hash that starts with at least **six zeroes** in hexadecimal representation.

## Context
This is a continuation of the AdventCoin mining problem. In Part 1, we found hashes starting with five zeroes. Now we need to increase the difficulty by finding hashes that start with six zeroes, which is similar to how cryptocurrency mining difficulty increases over time.

## Input
- A secret key string (provided in input.md): `ckczppom`
- The input should be treated as a string without leading/trailing whitespace

## Algorithm Requirements
1. Start with positive integers: 1, 2, 3, 4, ... (no leading zeroes in the number)
2. For each integer `n`:
   - Concatenate the secret key with the integer (e.g., `ckczppom1`, `ckczppom2`, etc.)
   - Calculate the MD5 hash of this concatenated string
   - Convert the MD5 hash to hexadecimal representation
   - Check if the hexadecimal hash starts with at least **six zeroes** (`000000...`)
3. Return the lowest integer that satisfies the condition

## Expected Output
- A single positive integer representing the answer
- This integer is the smallest number that, when appended to the secret key, produces an MD5 hash starting with six zeroes in hexadecimal

## Success Criteria
The hash must start with at least six consecutive zero characters when represented in hexadecimal format.

## Notes
- The answer will be larger than the Part 1 answer (which required five zeroes)
- This is computationally more intensive than Part 1 due to the increased difficulty
