# Implementation Plan: MD5 Password Generation

## Overview
Build a Python script that generates an 8-character password by finding MD5 hashes starting with five zeros and extracting the 6th character from each valid hash.

## Algorithm Analysis

### Complexity Considerations
- **Search Space**: Need to find 8 valid hashes where probability of a hash starting with `00000` is approximately 1 in 16^5 = 1,048,576
- **Expected Iterations**: Roughly 8-10 million iterations to find 8 valid hashes
- **Optimization Strategy**: Use efficient MD5 implementation, minimize string operations, avoid unnecessary conversions

### Performance Requirements
- Input size: Millions of hash computations required
- Bottleneck: MD5 computation speed
- Strategy: Use Python's built-in `hashlib` (C-based implementation) for maximum speed

## Step-by-Step Implementation

### Step 1: Import Required Libraries
```python
import hashlib
```
- Use `hashlib.md5()` for MD5 hash computation (fast C implementation)
- No additional dependencies needed

### Step 2: Read Input
- Read the door ID from `input.md`
- Strip all whitespace/newlines to get clean door ID string
- Verify the door ID is non-empty
- Store as a string variable

### Step 3: Initialize Variables
- `PASSWORD_LENGTH`: Constant set to 8
- `index`: Start at 0, will increment through millions of values
- `password`: Empty list to accumulate found characters
- Progress tracking variables (optional but recommended for user feedback)

### Step 4: Main Search Loop
Iterate until 8 valid characters are found:

**Pseudocode:**
```
while len(password) < PASSWORD_LENGTH:
    1. Create input string: door_id + str(index)
    2. Compute MD5 hash of input string
    3. Get hexadecimal digest
    4. Check if first 5 characters are '00000'
    5. If valid:
        - Extract 6th character (index 5)
        - Append to password
        - Print progress (character number and index)
    6. Increment index
    7. Optional: Print periodic progress every 1M iterations
```

### Step 5: Optimization Details

**String Encoding:**
- MD5 requires bytes input: encode string as UTF-8
- Use `.encode()` or `.encode('utf-8')`

**Hash Computation:**
- Create new MD5 object for each hash: `hashlib.md5()`
- Convert to hex: `.hexdigest()` returns lowercase hex string

**Efficiency Tips:**
- Avoid redundant string conversions
- Use string concatenation efficiently (f-strings or + operator are similar speed for small strings)
- Keep the inner loop tight - minimize operations inside the main loop

**Progress Tracking (Recommended):**
- Print when each valid character is found (shows 8 progress updates)
- Print every 1,000,000 iterations to show script is actively running
- Helps verify script is working during long computation (~60-90 seconds)

### Step 6: Output Result
- Print the final 8-character password to stdout
- Format: `Password: <password>` (labeled output for clarity)
- Validate all characters are valid hex digits (0-9, a-f) before output

## Code Structure

```python
import hashlib

# Constants
PASSWORD_LENGTH = 8
PROGRESS_INTERVAL = 1_000_000

# Read input
with open('input.md', 'r') as f:
    door_id = f.read().strip()

# Validate input
assert door_id, "Door ID cannot be empty"

# Initialize
index = 0
password = []

# Main loop
while len(password) < PASSWORD_LENGTH:
    # Periodic progress output
    if index > 0 and index % PROGRESS_INTERVAL == 0:
        print(f"Checked {index:,} hashes, found {len(password)}/{PASSWORD_LENGTH} characters...")

    # Create hash input
    hash_input = (door_id + str(index)).encode()

    # Compute MD5
    hash_result = hashlib.md5(hash_input).hexdigest()

    # Check for five leading zeros
    if hash_result.startswith('00000'):
        # Extract 6th character
        char = hash_result[5]
        password.append(char)
        print(f"Found character {len(password)}/{PASSWORD_LENGTH}: '{char}' at index {index}")

    index += 1

# Validate and output result
final_password = ''.join(password)
assert all(c in '0123456789abcdef' for c in final_password), "Invalid characters in password"
print(f"\nPassword: {final_password}")
```

## Implementation Notes

### Data Types
- Door ID: string
- Index: integer (can grow to 10+ million)
- Hash result: string (32-character hex)
- Password: list of characters, joined to string at end

### Edge Cases Handled
1. **Input parsing**: Strip all whitespace from door ID and validate non-empty
2. **Character extraction**: Use index [5] for 6th character (0-indexed)
3. **Hash format**: Use lowercase hex (`.hexdigest()` returns lowercase)
4. **Output validation**: Verify all characters are valid hex digits before output

### Not Handled (Out of Scope)
- Invalid input file (assume exists and contains valid door ID)
- Memory constraints (minimal memory usage anyway)
- Multi-threading (adds complexity, single-thread sufficient)
- Early termination (let loop complete naturally)

## Expected Runtime
- **Estimate**: 60-90 seconds on modern hardware (typical single-core performance)
- **Factors**:
  - Python interpreter overhead
  - MD5 computation speed (~1-2 million hashes/second typical)
  - Need ~8-10 million iterations on average
- **Progress updates**: Every 1M iterations to show active progress

## Files to Create
- `solution.py`: Main script implementing the algorithm above
- Reads from: `input.md` (contains door ID: `ugkcyxxp`)
- Outputs to: stdout with format `Password: <8-character password>`
