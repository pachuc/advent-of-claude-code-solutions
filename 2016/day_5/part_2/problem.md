# Problem Report: Position-Based Password Generation via MD5 Hash

## Objective
Generate an 8-character password using a position-based method where MD5 hashes indicate both the position and the character to place at that position.

## Context from Part 1
In Part 1, we generated a password by finding MD5 hashes that started with five zeroes and extracting the 6th character in order. This gave us the password `d4cd2ee1` for Door ID `ugkcyxxp`.

Part 2 uses a more sophisticated approach where the password is not filled left-to-right in order, but rather each valid hash indicates which position in the password to fill.

## Input
- **Door ID**: A string value (given in input.md as `ugkcyxxp`)
- **Starting index**: `0` (integer that increments)
- **Password length**: 8 characters (positions 0-7)

## Algorithm Requirements

### Hash Generation
1. Concatenate the Door ID with an increasing integer index (starting at 0)
2. Compute the MD5 hash of this concatenated string
3. Convert the hash to hexadecimal representation

### NEW: Character Selection Criteria (Part 2)
A hash is valid for password generation if:
- Its hexadecimal representation starts with **five zeroes** (`00000`)
- The **6th character** (index 5) represents the **position** in the password (must be `0`-`7`)
- The **7th character** (index 6) is the **character to place** at that position

### Important Rules
- Use only the **first result** for each position (positions 0-7)
- **Ignore invalid positions**: If the 6th character is not in the range `0`-`7`, skip this hash
- **Ignore duplicate positions**: If a position is already filled, skip any subsequent hashes for that position
- Continue until all 8 positions (0-7) are filled

### Process
1. Start with index = 0
2. Initialize an 8-character password array (all positions empty)
3. Compute MD5 hash of `Door_ID + index`
4. Check if hash starts with five zeroes in hexadecimal
5. If yes:
   - Extract the 6th character as the position
   - Check if position is valid (`0`-`7`) and not yet filled
   - If valid and empty: extract 7th character and place it at that position
   - If invalid or already filled: skip this hash
6. If no: increment index and repeat
7. Continue until all 8 positions are filled

## Expected Output
- An 8-character string representing the password
- Characters are placed at positions indicated by their corresponding hashes
- Only the first valid hash for each position is used

## Example
Given Door ID = `abc`:
- Index `3231929`: hash `0000015...` → position `1`, character `5` → password: `_5______`
- Index `5017308`: hash `000008f...` → position `8` (INVALID, out of range 0-7) → SKIP
- Index `5357525`: hash `000004e...` → position `4`, character `e` → password: `_5__e___`
- After finding all 8 positions, the complete password is: `05ace8e3`

## Input Value
The Door ID for this puzzle is: `ugkcyxxp`

## Task
Find the 8-character password for Door ID `ugkcyxxp` using the position-based method.
