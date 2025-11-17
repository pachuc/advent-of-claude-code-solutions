# Problem Report: Room Validation and Sector ID Summation

## Context
We have a list of encrypted room names that contains both real rooms and decoy data. We need to filter out the decoy rooms and sum the sector IDs of only the real rooms.

## What We Are Trying to Solve
Determine which rooms in the list are "real" (not decoys) based on a checksum validation algorithm, then calculate the sum of sector IDs for all real rooms.

## Input Format
The input is a list of room entries, one per line. Each entry has the following format:
```
encrypted-name-with-dashes-###[checksum]
```

Where:
- **Encrypted name**: lowercase letters separated by dashes (e.g., `aaaaa-bbb-z-y-x`)
- **Sector ID**: a number following the last dash (e.g., `123`)
- **Checksum**: five lowercase letters enclosed in square brackets (e.g., `[abxyz]`)

Example entries:
```
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
```

## Room Validation Rules
A room is **real** (not a decoy) if and only if:

1. The checksum consists of the **five most common letters** from the encrypted name
2. Letters must be ordered by frequency (most common first)
3. **Ties are broken by alphabetical order** (e.g., if 'x', 'y', 'z' all appear the same number of times, they should be ordered as 'x', 'y', 'z')
4. **Note**: Dashes in the encrypted name are ignored (not counted as letters)

### Validation Examples

**Real room**: `aaaaa-bbb-z-y-x-123[abxyz]`
- Letter frequencies: a=5, b=3, x=1, y=1, z=1
- Top 5 by frequency with alphabetical tiebreaker: a, b, x, y, z
- Checksum `[abxyz]` matches → **REAL**

**Real room**: `a-b-c-d-e-f-g-h-987[abcde]`
- All letters tied at 1 occurrence each
- First 5 alphabetically: a, b, c, d, e
- Checksum `[abcde]` matches → **REAL**

**Real room**: `not-a-real-room-404[oarel]`
- Checksum matches the five most common letters → **REAL**

**Decoy room**: `totally-real-room-200[decoy]`
- Checksum does NOT match the five most common letters → **DECOY**

## Expected Output
A single integer representing the **sum of the sector IDs** of all real rooms.

### Example
Given the example rooms above:
- `aaaaa-bbb-z-y-x-123[abxyz]` → real, sector ID = 123
- `a-b-c-d-e-f-g-h-987[abcde]` → real, sector ID = 987
- `not-a-real-room-404[oarel]` → real, sector ID = 404
- `totally-real-room-200[decoy]` → decoy (excluded)

Sum of real room sector IDs: **123 + 987 + 404 = 1514**

## Algorithm Steps
1. Parse each room entry to extract:
   - Encrypted name (letters only, excluding dashes)
   - Sector ID (the number)
   - Checksum (the 5 letters in brackets)

2. For each room, calculate the expected checksum:
   - Count frequency of each letter in the encrypted name
   - Sort letters by frequency (descending), then alphabetically for ties
   - Take the first 5 letters

3. Compare the calculated checksum with the provided checksum
   - If they match: room is real, add sector ID to sum
   - If they don't match: room is a decoy, skip it

4. Return the total sum of all real room sector IDs
