# Problem Report: Room Name Decryption and North Pole Object Storage Location

## Context from Part 1
In Part 1, we validated room entries to filter out decoy data. Each room entry consists of:
- An encrypted name (lowercase letters separated by dashes)
- A sector ID (number)
- A checksum (5 letters in square brackets)

We validated rooms by checking if the checksum matches the five most common letters in the encrypted name (with ties broken alphabetically). The sum of valid room sector IDs from Part 1 was **173787**.

## Part 2: What We Are Trying to Solve
Now that we've identified the real rooms (not decoys), we need to:
1. **Decrypt** the encrypted room names using a shift cipher (Caesar cipher)
2. **Find** the specific room where "North Pole objects" are stored
3. **Return** the sector ID of that room

## Input Format
Same as Part 1: A list of room entries, one per line, in the format:
```
encrypted-name-with-dashes-###[checksum]
```

Example: `qzmt-zixmtkozy-ivhz-343[zimth]`

**Important**: We should only decrypt the **real rooms** (those that passed Part 1's checksum validation).

## Decryption Algorithm
The room names are encrypted using a **shift cipher (Caesar cipher)**:

- **Each letter** in the encrypted name is rotated forward through the alphabet by a number of positions equal to the room's **sector ID**
- **Rotation rules**:
  - 'a' shifted by 1 becomes 'b'
  - 'b' shifted by 1 becomes 'c'
  - 'z' shifted by 1 wraps around to 'a'
  - The shift is modulo 26 (there are 26 letters in the alphabet)
- **Dashes** are converted to **spaces** in the decrypted name

### Decryption Example
Given: `qzmt-zixmtkozy-ivhz-343`
- Sector ID: 343
- Decrypt each letter by shifting forward 343 positions (343 % 26 = 5 positions)
- 'q' + 5 = 'v'
- 'z' + 5 = 'e' (wraps around)
- 'm' + 5 = 'r'
- 't' + 5 = 'y'
- (dash becomes space)
- ... and so on

Result: `very encrypted name`

## What We're Looking For
After decrypting all real room names, find the room whose decrypted name contains or relates to **"North Pole objects"**. This could be:
- An exact match: "north pole objects"
- A partial match: "northpole" or "north pole"
- A room description that clearly indicates it stores North Pole objects

## Expected Output
A single integer: the **sector ID** of the room where North Pole objects are stored.

## Algorithm Steps
1. Parse each room entry (reuse Part 1's parsing logic)
2. Validate each room using checksum validation (reuse Part 1's validation logic)
3. For each **real room**:
   - Decrypt the encrypted name using the shift cipher with the room's sector ID
   - Check if the decrypted name relates to "North Pole objects"
4. Return the sector ID of the matching room

## Implementation Notes
- The shift cipher operates on lowercase letters only
- Use modulo 26 for wraparound: `new_letter = (old_letter_index + sector_id) % 26`
- Dashes in encrypted names become spaces in decrypted names
- Search for keywords like "north", "pole", "northpole" in the decrypted names
