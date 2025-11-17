# Implementation Plan: Part 2 - Room Name Decryption

## Updates from Critique (Version 2)

This plan has been updated based on feedback to address the following improvements:

1. **More Precise Search Logic**: Changed from `"north" in name and "pole" in name` to `"north pole" in name or "northpole" in name` to avoid false positives like "northeastern polynomial"
2. **Better Error Handling**: Changed `return None` to `raise ValueError()` when no North Pole room is found, for clearer error reporting
3. **Comprehensive Validation**: Expanded validation function to include multiple test cases (zero shift, wraparound, large IDs, modulo boundaries, Part 1 integration)
4. **Added Import Documentation**: Explicitly documented imports in the file structure
5. **Modulo 26 Boundary Tests**: Added test cases for sector_id = 25 and 27 to verify boundary behavior
6. **Clarified Part 1 Reuse**: Added note that Part 1 functions are pre-validated

## Overview
Part 2 builds directly on Part 1's validation logic. We need to decrypt the names of real rooms using a Caesar cipher and find the room storing "North Pole objects".

## Code Reuse Strategy
We can reuse almost all of Part 1's code:
- `parse_room_entry()` - extract encrypted name, sector ID, checksum
- `generate_expected_checksum()` - calculate checksum from letter frequencies
- `is_real_room()` - validate room authenticity
- File reading and parsing logic

**New functionality needed:** Decryption function and search logic.

## Algorithm Analysis

### Runtime Complexity
- **Input size:** 947 room entries
- **Per room operations:**
  - Parsing: O(n) where n = line length (~50 chars avg)
  - Checksum validation: O(m) where m = encrypted name length (~30 chars avg)
  - Decryption: O(m) for character shifting
  - Search: O(k) where k = decrypted name length
- **Overall:** O(N × M) where N = 947 rooms, M = avg name length
- **Expected runtime:** < 1 second (very efficient)

### Space Complexity
- O(N) to store valid rooms if needed
- O(M) for decrypted strings
- Overall: O(N × M) ≈ 947 × 30 = ~28KB (negligible)

## Step-by-Step Implementation Plan

### Step 1: Copy and Adapt Part 1 Code
**File:** `solution.py`

Copy the following functions from `part_1_solution.py`:
- `parse_room_entry(line: str) -> tuple[str, int, str]`
- `generate_expected_checksum(encrypted_name: str) -> str`
- `is_real_room(encrypted_name: str, checksum: str) -> bool`

These functions are perfect as-is and require no modifications.

### Step 2: Implement Caesar Cipher Decryption
**Function:** `decrypt_room_name(encrypted_name: str, sector_id: int) -> str`

**Algorithm:**
1. Calculate effective shift: `shift = sector_id % 26`
   - Optimization: Since alphabet has 26 letters, shifts repeat every 26 positions
2. For each character in encrypted_name:
   - If dash (`-`): convert to space (` `)
   - If letter:
     - Convert to 0-based index: `ord(char) - ord('a')` (0-25)
     - Apply shift: `(index + shift) % 26`
     - Convert back to character: `chr(new_index + ord('a'))`
3. Return decrypted string

**Implementation details:**
```python
def decrypt_room_name(encrypted_name: str, sector_id: int) -> str:
    """Decrypt room name using Caesar cipher with given sector ID shift."""
    shift = sector_id % 26  # Optimize: modulo 26 since alphabet repeats
    decrypted = []

    for char in encrypted_name:
        if char == '-':
            decrypted.append(' ')
        else:
            # Shift letter by sector_id positions
            char_index = ord(char) - ord('a')  # Convert to 0-25
            new_index = (char_index + shift) % 26  # Apply shift with wraparound
            decrypted.append(chr(new_index + ord('a')))  # Convert back to char

    return ''.join(decrypted)
```

**Edge cases handled:**
- Large sector IDs (e.g., 1000+): modulo 26 optimization
- Wraparound (z → a): modulo operator handles this
- Dashes: explicitly converted to spaces

### Step 3: Implement Search Logic
**Function:** `find_north_pole_storage(filename: str) -> int`

**Algorithm:**
1. Read input file and parse all lines
2. For each line:
   - Parse room entry
   - Validate it's a real room (checksum matches)
   - If real: decrypt the room name
   - Check if decrypted name contains "north" and "pole"
3. Return sector ID of matching room

**Search strategy:**
- Convert decrypted name to lowercase (already lowercase, but safe)
- Search for keywords: "north pole" (most likely) or "northpole"
- Use precise matching to avoid false positives: `"north pole" in decrypted or "northpole" in decrypted`
- This avoids matching unrelated words like "northeastern polynomial"

**Implementation details:**
```python
def find_north_pole_storage(filename='input.md') -> int:
    """Find sector ID of room storing North Pole objects."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    for line in lines:
        parsed = parse_room_entry(line)
        if parsed:
            encrypted_name, sector_id, checksum = parsed

            # Only process real rooms
            if is_real_room(encrypted_name, checksum):
                decrypted_name = decrypt_room_name(encrypted_name, sector_id)

                # Search for North Pole objects (precise matching)
                if 'north pole' in decrypted_name or 'northpole' in decrypted_name:
                    return sector_id

    # If no match found, raise an error for clarity
    raise ValueError("No room containing 'North Pole' found in input")
```

### Step 4: Create Main Function
**Function:** `solve(filename='input.md') -> int`

Simple wrapper that calls `find_north_pole_storage()`:
```python
def solve(filename='input.md'):
    """Main solving function."""
    return find_north_pole_storage(filename)
```

### Step 5: Add Validation Function
**Function:** `validate_solution()`

Test the decryption function comprehensively with multiple test cases:
- Example from problem: `qzmt-zixmtkozy-ivhz-343` → `very encrypted name`
- Zero shift edge case
- Wraparound edge case
- Large sector IDs
- Part 1 integration

```python
def validate_solution():
    """Run comprehensive validation tests."""
    print("Running validation tests...")

    # Test 1.1: Example verification
    result = decrypt_room_name("qzmt-zixmtkozy-ivhz", 343)
    assert result == "very encrypted name", f"Test 1.1 failed: {result}"
    print("✓ Test 1.1: Example verification passed")

    # Test 1.2: Zero shift
    assert decrypt_room_name("abc-xyz", 0) == "abc xyz"
    assert decrypt_room_name("abc-xyz", 26) == "abc xyz"
    print("✓ Test 1.2: Zero shift passed")

    # Test 1.3: Full rotation with wraparound
    assert decrypt_room_name("zabc", 1) == "abcd"
    assert decrypt_room_name("xyz", 3) == "abc"
    print("✓ Test 1.3: Alphabet wraparound passed")

    # Test 1.4: Large sector IDs
    assert decrypt_room_name("abc", 1000) == "mno"
    print("✓ Test 1.4: Large sector IDs passed")

    # Test 1.5: Modulo 26 boundary cases
    assert decrypt_room_name("abc", 25) == "zab"
    assert decrypt_room_name("abc", 27) == "bcd"  # 27 % 26 = 1
    print("✓ Test 1.5: Modulo 26 boundaries passed")

    # Test 2.1: Part 1 logic integration
    encrypted, sid, checksum = parse_room_entry("aaaaa-bbb-z-y-x-123[abxyz]")
    assert sid == 123
    assert is_real_room(encrypted, checksum) == True
    print("✓ Test 2.1: Part 1 integration passed")

    print("All validation tests passed!")
```

**Note:** Part 1 functions (`parse_room_entry`, `generate_expected_checksum`, `is_real_room`) are assumed to be already validated from Part 1's solution and testing.

### Step 6: Create Entry Point
```python
if __name__ == "__main__":
    validate_solution()
    result = solve()
    print(result)
```

## File Structure
```
solution.py
├── Imports
│   ├── import re                        # For regex parsing (from Part 1)
│   └── from collections import Counter # For checksum generation (from Part 1)
├── parse_room_entry()          # From Part 1
├── generate_expected_checksum() # From Part 1
├── is_real_room()              # From Part 1
├── decrypt_room_name()         # NEW
├── find_north_pole_storage()   # NEW
├── solve()                     # NEW (simple wrapper)
├── validate_solution()         # NEW
└── __main__                    # Entry point
```

## Optimization Considerations

### Why This is Efficient Enough
1. **Linear scan:** O(N) where N = 947 - unavoidable, must check all rooms
2. **String operations:** Python string operations are highly optimized in C
3. **Early termination:** Returns immediately upon finding match
4. **Modulo optimization:** `sector_id % 26` prevents redundant rotations

### Why We Don't Need Further Optimization
- Input size is small (947 rooms)
- Each operation is O(1) or O(M) where M < 50
- Total operations: ~50,000 character operations
- Modern CPU: billions of operations per second
- **Expected runtime:** ~10-50 milliseconds

### What We're NOT Doing (Intentionally)
- No caching/memoization: not needed for single-pass algorithm
- No parallel processing: overhead would exceed benefit
- No complex data structures: simple iteration is fastest for this size
- No pre-filtering: validation is already fast enough

## Dependencies
```python
import re                 # For regex parsing (from Part 1)
from collections import Counter  # For checksum generation (from Part 1)
```

## Expected Behavior
- Should find exactly one room matching "North Pole objects"
- Return its sector ID as an integer
- Print validation confirmation before solving
- Total runtime: well under 1 second
