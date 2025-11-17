# Problem Report: One-Time Pad Key Generation

## Objective
Find the index that produces the 64th valid key for a one-time pad cryptographic system.

## Context
We need to generate cryptographic keys using a specific algorithm that combines a salt string with incrementing integers and applies validation rules to determine which hashes qualify as valid keys.

## Input
- A salt string: `ihaygndm`

## Algorithm

### Hash Generation
1. Start with index = 0
2. Concatenate the salt with the current index (e.g., `ihaygndm0`, `ihaygndm1`, etc.)
3. Compute the MD5 hash of this string
4. Represent the hash as a lowercase hexadecimal string

### Key Validation Rules
A hash qualifies as a valid key if BOTH conditions are met:

1. **Triplet Condition**: The hash contains three consecutive identical characters (e.g., `777`, `aaa`, `ccc`)
   - Only consider the FIRST triplet found in the hash

2. **Quintuplet Confirmation**: Within the next 1000 hashes (indices [current+1, current+1000]), at least one hash must contain the same character repeated five consecutive times (e.g., `77777`)

### Important Notes
- All indices in the stream must be checked sequentially
- Finding a quintuplet does NOT skip that index from being checked as a potential key itself
- Each hash is evaluated independently regardless of whether previous hashes were keys

## Expected Output
The index (integer) that produces the 64th valid key.

## Example
Using salt `abc`:
- Index 18: Contains triplet `888` in hash `...cc38887a5...`, but no hash in range [19-1018] contains `88888` → NOT a key
- Index 39: Contains triplet `eee`, and index 816 contains `eeeee` → KEY #1
- Index 92: Contains triplet `999`, and index 200 contains `99999` → KEY (after 6 non-qualifying triples)
- Index 22728: Produces the 64th key

With salt `abc`, the answer is `22728`.

## Output Format
A single integer representing the index value.
