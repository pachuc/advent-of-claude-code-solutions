# Implementation Plan: Room Validation and Sector ID Summation

## Updates Based on Critique
This plan has been updated to address the following items from the critique:
1. **Regex Pattern Clarified**: Changed from `^(.+)-(\d+)\[([a-z]{5})\]$` to `^([a-z-]+)-(\d+)\[([a-z]{5})\]$` to explicitly match letters and dashes
2. **Function Organization**: Clarified that letter frequency calculation is handled internally within `generate_expected_checksum()`, not as a separate public function
3. **Edge Case Documentation**: Explicitly documented handling of <5 unique letters case (uses `[:5]` slice)
4. **Validation Integration**: Added `validate_solution()` function to test examples before running on actual input
5. **Complete Code Structure**: Provided full implementation with all functions, including validation

## Overview
We need to parse encrypted room entries, validate them using checksum verification, and sum the sector IDs of valid rooms. The input contains ~947 room entries.

## Algorithm Complexity Analysis
- **Input Size**: ~947 rooms
- **Per-room Processing**: O(n) where n is the length of the encrypted name (typically <50 characters)
- **Overall Complexity**: O(R * N) where R is number of rooms (~947) and N is average name length
- **Expected Runtime**: Very fast (< 1 second) - the input size is small enough that optimization is not critical

## Step-by-Step Implementation

### Step 1: Input Reading
**Goal**: Read and store all room entries from input.md

**Implementation**:
- Open and read `input.md` file
- Read all lines into a list
- Strip whitespace from each line
- Filter out any empty lines

**Data Structure**: List of strings

### Step 2: Room Entry Parsing
**Goal**: Extract encrypted name, sector ID, and checksum from each room entry

**Implementation**:
- Use regex pattern to parse the format: `(letters-and-dashes)-(number)[checksum]`
- Pattern: `^([a-z-]+)-(\d+)\[([a-z]{5})\]$`
  - Group 1: encrypted name with dashes (explicitly matches letters and dashes)
  - Group 2: sector ID (digits)
  - Group 3: checksum (exactly 5 lowercase letters)
- The pattern `[a-z-]+` will match all letters and dashes up to the last dash before the sector ID
- Use `re.match()` to parse each line

**Function Signature**:
```python
def parse_room_entry(line: str) -> tuple[str, int, str]:
    """
    Parses a room entry line and extracts components.
    Returns: (encrypted_name, sector_id, checksum)
    Example: "abc-def-123[abcde]" -> ("abc-def", 123, "abcde")
    """
```

**Edge Cases**:
- Assume all input lines are well-formed per problem specification
- If a line doesn't match (unlikely), the regex match will return None

### Step 3: Letter Frequency Calculation (Internal Helper)
**Goal**: Count how many times each letter appears in the encrypted name

**Implementation**:
- This is handled internally within `generate_expected_checksum()`
- Remove all dashes from the encrypted name
- Use `collections.Counter` to count letter frequencies
- This gives us a dictionary mapping letter -> count

**Note**: This is not a separate function in the final implementation, but an internal step within `generate_expected_checksum()`. If needed for testing purposes, it can be extracted as a helper function.

**Complexity**: O(N) where N is length of encrypted name

### Step 4: Generate Expected Checksum
**Goal**: Create the expected checksum based on the five most common letters

**Implementation**:
- Remove dashes from encrypted name to get only letters
- Count letter frequencies using `collections.Counter`
- Sort letters by two criteria (in order of priority):
  1. Frequency (descending) - most common first
  2. Alphabetical order (ascending) - for ties
- Take the first 5 letters from the sorted result (or fewer if < 5 unique letters exist)
- Join them into a string

**Sorting Strategy**:
```python
letters_only = encrypted_name.replace('-', '')
frequency_dict = Counter(letters_only)
sorted_letters = sorted(
    frequency_dict.items(),
    key=lambda x: (-x[1], x[0])  # -x[1] for descending freq, x[0] for ascending alpha
)
expected_checksum = ''.join([letter for letter, count in sorted_letters[:5]])
```

**Function Signature**:
```python
def generate_expected_checksum(encrypted_name: str) -> str:
    """
    Generates expected checksum from encrypted name.
    Takes the 5 most common letters, sorted by frequency (desc) then alphabetically.
    Returns: checksum string (up to 5 characters)
    Example: "aaaaa-bbb-z-y-x" -> "abxyz"
    Note: If fewer than 5 unique letters exist, returns all available letters.
    """
```

**Complexity**: O(N log N) where N is number of unique letters (max 26)

**Note on Edge Case**: While all problem examples have 5+ unique letters, the algorithm naturally handles fewer by taking `min(5, available_letters)` via the slice `[:5]`

### Step 5: Room Validation
**Goal**: Determine if a room is real by comparing checksums

**Implementation**:
- Generate expected checksum from encrypted name
- Compare with provided checksum (simple string equality)
- Return True if match, False otherwise

**Function Signature**:
```python
def is_real_room(encrypted_name: str, checksum: str) -> bool:
    """
    Returns: True if room is real, False if decoy
    """
```

### Step 6: Main Processing Loop
**Goal**: Process all rooms and accumulate sector IDs of real rooms

**Implementation**:
```python
def solve():
    # Read input
    with open('input.md', 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total_sector_id_sum = 0

    for line in lines:
        # Parse entry
        encrypted_name, sector_id, checksum = parse_room_entry(line)

        # Validate room
        if is_real_room(encrypted_name, checksum):
            total_sector_id_sum += sector_id

    return total_sector_id_sum
```

### Step 7: Validation and Output
**Goal**: Validate solution with examples, then output the final sum

**Implementation**:
- First, run validation tests on the provided examples to ensure correctness
- The example sum should equal 1514
- If validation passes, run on actual input.md
- Print only the final integer sum to stdout (no debug output in final version)

**Validation Check**:
```python
# Validate with examples before running on real input
def validate_solution():
    test_input = [
        "aaaaa-bbb-z-y-x-123[abxyz]",
        "a-b-c-d-e-f-g-h-987[abcde]",
        "not-a-real-room-404[oarel]",
        "totally-real-room-200[decoy]"
    ]
    # Should return 1514 (123 + 987 + 404)
```

## Complete Code Structure

```python
import re
from collections import Counter

def parse_room_entry(line: str) -> tuple[str, int, str]:
    """Parse room entry and extract components."""
    pattern = r'^([a-z-]+)-(\d+)\[([a-z]{5})\]$'
    match = re.match(pattern, line)
    if match:
        encrypted_name = match.group(1)
        sector_id = int(match.group(2))
        checksum = match.group(3)
        return encrypted_name, sector_id, checksum
    return None

def generate_expected_checksum(encrypted_name: str) -> str:
    """Generate expected checksum from encrypted name."""
    # Remove dashes and count letter frequencies
    letters_only = encrypted_name.replace('-', '')
    frequency_dict = Counter(letters_only)

    # Sort by frequency (descending) then alphabetically (ascending)
    sorted_letters = sorted(
        frequency_dict.items(),
        key=lambda x: (-x[1], x[0])
    )

    # Take first 5 letters (or all if fewer than 5 unique letters)
    return ''.join([letter for letter, count in sorted_letters[:5]])

def is_real_room(encrypted_name: str, checksum: str) -> bool:
    """Validate room by comparing checksums."""
    expected = generate_expected_checksum(encrypted_name)
    return expected == checksum

def solve(filename='input.md'):
    """Main processing function."""
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    total_sector_id_sum = 0

    for line in lines:
        parsed = parse_room_entry(line)
        if parsed:
            encrypted_name, sector_id, checksum = parsed
            if is_real_room(encrypted_name, checksum):
                total_sector_id_sum += sector_id

    return total_sector_id_sum

def validate_solution():
    """Run validation tests on provided examples."""
    test_cases = [
        ("aaaaa-bbb-z-y-x-123[abxyz]", True, 123),
        ("a-b-c-d-e-f-g-h-987[abcde]", True, 987),
        ("not-a-real-room-404[oarel]", True, 404),
        ("totally-real-room-200[decoy]", False, 200)
    ]

    total = 0
    for line, should_be_real, sector_id in test_cases:
        encrypted_name, sid, checksum = parse_room_entry(line)
        is_real = is_real_room(encrypted_name, checksum)
        assert is_real == should_be_real, f"Failed on {line}"
        if is_real:
            total += sector_id

    assert total == 1514, f"Expected 1514, got {total}"
    print("All validation tests passed!")

if __name__ == "__main__":
    validate_solution()
    result = solve()
    print(result)
```

## Optimization Considerations

### Current Approach Efficiency
- The input size (~947 rooms) is small enough that optimization is unnecessary
- Simple, readable code is preferred over micro-optimizations
- Expected runtime: < 0.1 seconds

### Alternative Approaches (Not Needed)
- Could cache frequency calculations if room names repeated (unlikely)
- Could use heap for top-5 selection (overkill for max 26 letters)
- Could parallelize processing (unnecessary for this input size)

## Dependencies
- `re`: For regex parsing
- `collections.Counter`: For efficient letter frequency counting

Both are part of Python standard library - no external dependencies needed.

## Error Handling
Since this is a script for a specific input (not production code):
- Assume input.md exists and is readable
- Assume all entries are well-formed
- No need for extensive try-except blocks
- Simple assertions for development debugging if needed
