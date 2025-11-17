# Problem Report: AdventCoin Mining

## Objective
Find the lowest positive integer that, when appended to a secret key string, produces an MD5 hash that starts with at least five zeroes in hexadecimal representation.

## Context
This is a mining problem similar to cryptocurrency mining (like Bitcoin), where we need to find a specific hash pattern by trying different input values.

## Input
- A secret key string (provided in input.md): `ckczppom`
- The input should be treated as a string without leading/trailing whitespace

## Algorithm Requirements
1. Start with positive integers: 1, 2, 3, 4, ... (no leading zeroes in the number)
2. For each integer `n`:
   - Concatenate the secret key with the integer (e.g., `ckczppom1`, `ckczppom2`, etc.)
   - Calculate the MD5 hash of this concatenated string
   - Convert the MD5 hash to hexadecimal representation
   - Check if the hexadecimal hash starts with at least five zeroes (`00000...`)
3. Return the lowest integer that satisfies the condition

## Expected Output
- A single positive integer representing the answer
- This integer is the smallest number that, when appended to the secret key, produces an MD5 hash starting with five zeroes in hexadecimal

## Examples
- Secret key `abcdef` → Answer: `609043`
  - MD5 hash of `abcdef609043` starts with `000001dbbfa...`
- Secret key `pqrstuv` → Answer: `1048970`
  - MD5 hash of `pqrstuv1048970` starts with `000006136ef...`

## Success Criteria
The hash must start with at least five consecutive zero characters when represented in hexadecimal format.
