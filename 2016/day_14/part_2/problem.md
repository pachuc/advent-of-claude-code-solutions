# Problem Report: One-Time Pad Key Generation with Key Stretching (Part 2)

## Objective
Find the index that produces the 64th valid key for a one-time pad cryptographic system, now using key stretching to enhance security.

## Context
This is Part 2 of the puzzle. In Part 1, we generated keys using a salt string combined with incrementing integers, computing MD5 hashes and applying validation rules. Part 1 found the 64th key at index **15035** using salt `ihaygndm`.

In Part 2, we implement **key stretching** - a security enhancement that makes hash generation computationally more expensive by applying MD5 repeatedly.

## Input
- Salt string: `ihaygndm`

## Algorithm Changes from Part 1

### Key Stretching (NEW in Part 2)
Instead of using the MD5 hash directly, we must now apply key stretching:

1. Compute the MD5 hash of salt + index (as before)
2. Apply MD5 to that hash result
3. Apply MD5 to the new result
4. Repeat step 3 for a total of **2016 additional MD5 operations**
5. Total: **2017 MD5 computations** (1 original + 2016 additional)

**Example for index 0 with salt `abc`:**
- Initial: MD5(`abc0`) = `577571be4de9dcce85a041ba0410f29f`
- After 1 more: MD5(`577571be4de9dcce85a041ba0410f29f`) = `eec80a0c92dc8a0777c619d9bb51e910`
- After 2 more: MD5(`eec80a0c92dc8a0777c619d9bb51e910`) = `16062ce768787384c81fe17a7a60c7e3`
- ... (2014 more iterations) ...
- After 2016 more: Final stretched hash = `a107ff634856bb300138cac6568c0f24`

**Important:** Always use lowercase hexadecimal representations of hashes.

### Hash Generation (Updated)
1. Start with index = 0
2. Concatenate salt with the current index (e.g., `ihaygndm0`, `ihaygndm1`, etc.)
3. Compute the initial MD5 hash
4. **Apply 2016 additional MD5 hashing iterations** (key stretching)
5. Use the final stretched hash for validation

### Key Validation Rules (Same as Part 1)
A stretched hash qualifies as a valid key if BOTH conditions are met:

1. **Triplet Condition**: The stretched hash contains three consecutive identical characters (e.g., `777`, `aaa`, `222`)
   - Only consider the FIRST triplet found in the hash

2. **Quintuplet Confirmation**: Within the next 1000 stretched hashes (indices [current+1, current+1000]), at least one hash must contain the same character repeated five consecutive times (e.g., `77777`)

### Important Notes
- All indices in the stream must be checked sequentially
- Finding a quintuplet does NOT skip that index from being checked as a potential key itself
- Each hash is evaluated independently regardless of whether previous hashes were keys
- **Every hash at every index must be stretched using 2017 total MD5 operations**

## Expected Output
The index (integer) that produces the 64th valid key using key stretching.

## Example with Key Stretching
Using salt `abc` with key stretching:
- First triplet: `222` at index 5, but no `22222` in next 1000 hashes → NOT a key
- Second triplet: `eee` at index 10, and index 89 contains `eeeee` → KEY #1
- Index 22551: Produces the 64th key (triplet `fff` with matching `fffff` at index 22859)

With salt `abc` and key stretching, the answer is **22551** (compared to 22728 in Part 1).

## Output Format
A single integer representing the index value.
