# Problem Report: High-Entropy Passphrase Validation (Part 2 - Anagram Detection)

## Context from Part 1
In Part 1, we validated passphrases based on a simple rule: a passphrase was valid if it contained no duplicate words. We counted 455 valid passphrases from the input.

## Part 2 Enhancement
For added security, the system has implemented a **stricter validation policy**. Now, a valid passphrase must contain no two words that are **anagrams** of each other.

An anagram means that one word's letters can be rearranged to form another word in the same passphrase. If any two words in a passphrase are anagrams of each other, the entire passphrase is invalid.

## Objective
Count how many passphrases in the given input list are valid under this new, stricter anagram-detection policy.

## Input Specification
- The input is a list of passphrases, one per line (same as Part 1)
- Each passphrase consists of a series of words (lowercase letters) separated by spaces
- Input file: `input.md`

## Validation Rules
A valid passphrase must contain **no two words that are anagrams of each other**.

### Examples:
- `abcde fghij` → **VALID** (no words are anagrams of each other)
- `abcde xyz ecdab` → **INVALID** ("ecdab" is an anagram of "abcde")
- `a ab abc abd abf abj` → **VALID** (all letters must be used, so these are not anagrams of each other)
- `iiii oiii ooii oooi oooo` → **VALID** (none of these are anagrams of each other)
- `oiii ioii iioi iiio` → **INVALID** (any of these words can be rearranged to form any other word - they're all anagrams)

### Key Insight
Two words are anagrams if they contain exactly the same letters with the same frequencies. A practical way to check this is to sort the letters of each word - if two words have identical sorted letter sequences, they are anagrams.

## Output Specification
- Output should be a single integer representing the total count of valid passphrases
- Format: Just the number (e.g., `186`)

## Algorithm Requirements
For each passphrase in the input:
1. Split the passphrase into individual words
2. For each word, create a canonical representation (e.g., sort the letters)
3. Check if any two words have the same canonical representation (meaning they're anagrams)
4. If no anagrams exist, count the passphrase as valid
5. Return the total count of valid passphrases

## Implementation Strategy
A simple approach:
- For each passphrase, convert each word to a sorted tuple/string of its letters
- Use a set to check for duplicates among these sorted representations
- If the count of unique sorted representations equals the count of words, the passphrase is valid
