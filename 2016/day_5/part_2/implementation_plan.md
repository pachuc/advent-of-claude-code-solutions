# Implementation Plan: Part 2 - Position-Based Password Generation

## Overview
Part 2 modifies the Part 1 algorithm to use position-based password generation instead of sequential character collection. The key difference is that the 6th character of valid hashes now indicates the **position** (0-7) where the 7th character should be placed, rather than being the character itself.

## Algorithm Comparison

### Part 1 Algorithm
- Find hashes starting with `00000`
- Extract 6th character (index 5) as the next password character
- Build password left-to-right in order of discovery

### Part 2 Algorithm (New)
- Find hashes starting with `00000`
- Extract 6th character (index 5) as the **position** (must be 0-7)
- Extract 7th character (index 6) as the **character** to place at that position
- Only use the first valid hash for each position
- Ignore invalid positions (>7 or non-numeric)
- Ignore duplicate positions (already filled)

## Code Reusability from Part 1

The Part 1 solution (`part_1_solution.py`) can be adapted with minimal changes:
- **Keep**: Input reading, MD5 hashing logic, five-zero checking, progress reporting
- **Modify**: Password building logic (from sequential list to position-based array)
- **Add**: Position validation, duplicate position checking

## Step-by-Step Implementation Plan

### Step 1: Initialize Data Structures
- Read Door ID from `input.md` and strip whitespace (this handles multi-line input)
- Initialize password as a **dictionary** with string keys (recommended)
  - Dictionary approach: `{}` - keys are position strings '0'-'7', values are characters
  - This matches the type returned by `hash_result[5]` which is already a string
- Initialize index counter at 0
- Initialize `found_hashes` list to store all discoveries for verification (like Part 1)
- Set up progress tracking variables

**Rationale**: Dictionary with string keys avoids type conversion and naturally tracks which positions are filled via `len(password) == 8`.

### Step 2: Set Up Position Tracking
- Create a set or use the password dictionary to track which positions are filled
- Need to check if a position is already filled before accepting a new hash
- When all 8 positions (0-7) are filled, algorithm completes

### Step 3: Main Hash Generation Loop
Reuse Part 1 structure with modifications:

```
while len(password) < 8:  # Continue until all 8 positions filled
    1. Create hash input: (door_id + str(index)).encode()
       IMPORTANT: Must encode to bytes for MD5 computation
    2. Compute MD5 hash: hashlib.md5(hash_input).hexdigest()
    3. Check if hash starts with '00000'
    4. If valid:
       a. Extract position from hash_result[5] (6th character) - this is a STRING
       b. Validate position is in '0'-'7' range
       c. Check if position is not already filled (position not in password)
       d. If valid and empty:
          - Extract character from hash_result[6] (7th character)
          - Store: password[position] = character (position is string key)
          - Store: found_hashes.append((index, hash_result, position, character))
          - Print progress: "Found position {position}: '{character}' at index {index}"
       e. Otherwise: skip this hash (optionally log rejection reason)
    5. Increment index
    6. Print progress every 1,000,000 iterations showing indices checked and positions filled
```

### Step 4: Position Validation Logic
- Check if `hash[5]` is in the set {'0', '1', '2', '3', '4', '5', '6', '7'}
- Alternative: use `hash[5].isdigit() and int(hash[5]) < 8`
- If invalid, skip and continue to next index

**Edge case**: Hash might be valid (starts with 00000) but position character could be 'a'-'f' (hexadecimal), which is invalid

### Step 5: Duplicate Position Handling
- Before storing a character, check if position is already in the password dictionary/filled in list
- Only accept the **first** occurrence for each position
- Subsequent hashes for the same position are ignored

### Step 6: Password Assembly
- Once all 8 positions are filled, construct the final password
- Using dictionary with string keys: `final_password = ''.join(password[str(i)] for i in range(8))`
- This ensures characters are assembled in position order (0→7)
- Output should be an 8-character string
- Verify all characters are valid hexadecimal (in range [0-9a-f])

### Step 7: Output and Verification (MANDATORY)
- Print the final password
- Print total indices checked
- **REQUIRED**: Verify all stored hashes (reuse Part 1's verification pattern):
  - Iterate through `found_hashes` list
  - For each entry: re-compute hash from `door_id + str(index)`
  - Confirm hash matches stored value
  - Confirm it starts with '00000'
  - Confirm position character (index 5) is correct
  - Confirm value character (index 6) is correct
  - Print verification success for each hash
- This verification step is critical for ensuring correctness

## Efficiency Considerations

### Time Complexity
- Expected O(n) where n is the number of indices checked
- Based on Part 1, we found 8 characters after checking ~20 million indices
- Part 2 may require checking more indices since:
  - Some hashes have invalid positions (8, 9, a-f)
  - Some hashes target already-filled positions
- Estimate: 25-35 million iterations worst case

### Space Complexity
- O(1) - only storing 8 characters maximum
- Dictionary/list of size 8
- Constant space for tracking

### Optimization Opportunities
1. **Early termination**: Stop immediately when all 8 positions filled
2. **Progress reporting**: Every 1M iterations to show it's working
3. **No need for optimization beyond Part 1**: The algorithm is already efficient
4. **Consider using a set for filled_positions**: O(1) lookup instead of checking dictionary/list

## Implementation Details

### Constants
```python
PASSWORD_LENGTH = 8
VALID_POSITIONS = set('01234567')
PROGRESS_INTERVAL = 1_000_000
```

### Key Data Structure Choice
**Recommended**: Use a dictionary
```python
password = {}  # {position: character}
```

**Advantages**:
- Easy to check if position is filled: `position in password`
- Natural mapping from position to character
- Simple final assembly: `''.join(password[str(i)] for i in range(8))`

### Variable Naming (Consistency with Part 1)
Maintain consistent variable names with Part 1 for readability:
- `hash_input` - the encoded string to hash
- `hash_result` - the hexadecimal hash output
- `found_hashes` - list of tuples tracking all discovered positions
- `index` - the incrementing counter
- `door_id` - the input string

This consistency makes the code easier to understand and maintain.

## Code Structure (Adapted from Part 1)

```
1. Import hashlib
2. Define constants (PASSWORD_LENGTH=8, VALID_POSITIONS, PROGRESS_INTERVAL)
3. Read input from input.md and strip whitespace
4. Validate input (not empty) - assert statement
5. Initialize:
   - password = {} (dictionary with string keys)
   - index = 0
   - found_hashes = [] (for verification)
6. Print header with door ID
7. Main loop (while len(password) < PASSWORD_LENGTH):
   - Create hash_input: (door_id + str(index)).encode()  # MUST ENCODE
   - Compute MD5: hash_result = hashlib.md5(hash_input).hexdigest()
   - Check if hash_result.startswith('00000')
   - If valid:
     * Extract position = hash_result[5]  # STRING '0'-'7'
     * Validate position in VALID_POSITIONS
     * Check position not in password
     * If valid and empty:
       - Extract character = hash_result[6]
       - password[position] = character
       - found_hashes.append((index, hash_result, position, character))
       - Print: "Found position X: 'Y' at index Z"
   - Increment index
   - Progress reporting every PROGRESS_INTERVAL
8. Assemble final password: ''.join(password[str(i)] for i in range(8))
9. Print result and total indices checked
10. MANDATORY verification step (reuse Part 1 pattern):
    - Iterate through found_hashes
    - Re-compute each hash
    - Verify correctness
    - Print verification status
```

## Testing Hooks
- Use example from problem statement (Door ID "abc" → password "05ace8e3")
- Test with actual input "ugkcyxxp"
- Validate intermediate hashes if needed

## Expected Runtime
- Part 1 took significant time (~20M iterations)
- Part 2 likely takes 1.5-2x longer due to rejections
- Still computable in reasonable time (minutes on modern hardware)
- No special optimizations needed beyond straightforward implementation
