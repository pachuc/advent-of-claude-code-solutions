# Problem Report: Password Generation via MD5 Hash

## Objective
Generate an 8-character password by finding MD5 hashes that meet specific criteria.

## Context
We need to crack a security door that generates its password character-by-character using MD5 hashing. The password is built by iterating through integer indices and checking the resulting hash values.

## Input
- **Door ID**: A string value (given in input.md as `ugkcyxxp`)
- **Starting index**: `0` (integer that increments)

## Algorithm Requirements

### Hash Generation
1. Concatenate the Door ID with an increasing integer index (starting at 0)
2. Compute the MD5 hash of this concatenated string
3. Convert the hash to hexadecimal representation

### Character Selection Criteria
A hash is valid for password generation if:
- Its hexadecimal representation starts with **five zeroes** (`00000`)
- When valid, the **6th character** (index 5) of the hexadecimal hash becomes the next character in the password

### Process
1. Start with index = 0
2. Compute MD5 hash of `Door_ID + index`
3. Check if hash starts with five zeroes in hexadecimal
4. If yes: extract the 6th character and add it to the password
5. If no: increment index and repeat
6. Continue until 8 characters have been found

## Expected Output
- An 8-character string representing the password
- Characters are derived from valid MD5 hashes in the order they are discovered

## Example
Given Door ID = `abc`:
- Index `3231929`: hash of `abc3231929` starts with `00000`, 6th character is `1` → password: `1`
- Index `5017308`: hash of `abc5017308` starts with `000008f82...`, 6th character is `8` → password: `18`
- Index `5278568`: hash of `abc5278568` starts with `00000`, 6th character is `f` → password: `18f`
- After finding 8 valid hashes, the complete password is: `18f47a30`

## Input Value
The Door ID for this puzzle is: `ugkcyxxp`

## Task
Find the 8-character password for Door ID `ugkcyxxp`.
