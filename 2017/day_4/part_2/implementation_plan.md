# Implementation Plan - Part 2: Anagram Detection in Passphrases

## Overview
Extend the Part 1 solution to detect anagrams instead of just duplicate words. Two words are anagrams if they contain the exact same letters with the same frequencies.

## Key Differences from Part 1
- Part 1: Check if any word appears twice (exact duplicates)
- Part 2: Check if any two words are anagrams of each other (letter rearrangements)

## Algorithm Strategy

### Core Approach
Use a canonical representation of each word to detect anagrams:
- Sort the letters of each word alphabetically
- Two words are anagrams if their sorted letter sequences are identical
- Use a set to track canonical forms and detect duplicates

### Example
- `abcde` → sorted: `abcde`
- `ecdab` → sorted: `abcde`
- These sorted forms match, so they're anagrams

## Implementation Steps

### Step 1: Reuse Part 1 Structure
Start with the existing `part_1_solution.py` as the foundation:
- Keep the overall file reading logic
- Keep the main function structure
- Modify only the validation logic

### Step 2: Modify the Validation Function
Update `is_valid_passphrase()` to check for anagrams:

```python
def is_valid_passphrase(passphrase):
    """
    Check if passphrase has no words that are anagrams of each other.

    Two words are anagrams if they contain the same letters with same frequencies.
    We detect this by sorting the letters of each word and comparing.

    Args:
        passphrase (str): A space-separated string of words

    Returns:
        bool: True if valid (no anagrams), False otherwise
    """
    words = passphrase.split()

    # Create canonical form of each word by sorting its letters
    canonical_forms = [''.join(sorted(word)) for word in words]

    # Check if all canonical forms are unique
    # If any two words have the same sorted form, they are anagrams
    return len(canonical_forms) == len(set(canonical_forms))
```

**Optional Enhancement for Debugging:**
If needed for troubleshooting, a debug version can help verify the logic:
```python
def is_valid_passphrase(passphrase, debug=False):
    words = passphrase.split()
    canonical_forms = [''.join(sorted(word)) for word in words]

    if debug:
        print(f"Passphrase: {passphrase}")
        print(f"Words: {words}")
        print(f"Sorted forms: {canonical_forms}")
        print(f"Unique sorted forms: {len(set(canonical_forms))}")

    return len(canonical_forms) == len(set(canonical_forms))
```
This debug mode is not required for the solution but can be useful for manual testing.

### Step 3: Keep Main Function Unchanged
The main function from Part 1 can remain exactly the same:
- Read from `input.md`
- Filter empty lines
- Count valid passphrases
- Print result

## Complexity Analysis

### Time Complexity
For n passphrases with average m words per passphrase and average k characters per word:
- **Per passphrase**: O(m * k log k) for sorting all words
- **Overall**: O(n * m * k log k)

Given the input size (~512 passphrases, ~5-10 words per line, ~5-10 chars per word):
- This is approximately O(512 * 7 * 7 * log(7)) ≈ O(70,000) operations
- Very efficient and will run in milliseconds

### Space Complexity
- O(m) for storing canonical forms of words in each passphrase
- O(m) for the set used in comparison
- Overall: O(m) per passphrase, which is minimal

## Edge Cases to Handle
1. **Empty lines**: Skip them (Part 1 code already handles this with `line.strip()` check in main())
2. **Single word passphrases**: Always valid (no pairs to compare - set will have 1 element = len 1)
3. **All identical anagrams**: Should be invalid (e.g., "abc bca cab" all sort to "abc")
4. **Words with different lengths**: Cannot be anagrams (sorting handles this naturally - "ab" → "ab", "abc" → "abc")
5. **Same word repeated**: This is both a duplicate AND an anagram (will be caught - same sorted form)

## Code Modifications Summary
- **Minimal changes**: Only need to modify the word comparison logic
- **Line 11-12**: Change from comparing words directly to comparing sorted letters
- **Everything else**: Remains identical to Part 1

## Expected Output
Based on the problem description, the answer should be **less than 455** (Part 1 answer), since the anagram check is stricter than the duplicate check.

**Validation Steps Before Full Run:**
1. Test the 5 provided examples from problem.md manually to verify logic
2. If all examples pass, run on full input.md
3. Verify result is < 455 (if not, there's a bug in the implementation)
