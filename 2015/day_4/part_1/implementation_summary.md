# Implementation Summary: AdventCoin Mining

## Overview
Successfully implemented a solution to find the lowest positive integer that, when appended to the secret key "ckczppom", produces an MD5 hash starting with at least five hexadecimal zeroes.

## Final Answer
**117946**

The hash of `ckczppom117946` is `00000fe1c139a2c710e9a5c03ec1af03`, which starts with five zeroes as required.

## Files Created
- **solution.py**: Main solution file containing the MD5 mining algorithm

## Implementation Details

### Algorithm
Implemented a brute-force sequential search algorithm that:
1. Starts with positive integer 1
2. For each integer, concatenates it with the secret key
3. Computes the MD5 hash of the combined string
4. Checks if the hash starts with "00000"
5. Returns the first integer that satisfies the condition

### Key Functions
1. **read_input(filename='input.md')**: Reads and strips the secret key from the input file
2. **compute_md5_hex(text)**: Computes MD5 hash and returns hexadecimal representation
3. **starts_with_five_zeroes(hex_hash)**: Validates if hash starts with five zeroes
4. **find_advent_coin(secret_key)**: Main mining loop to find the answer

### Code Structure
The implementation follows the provided plan exactly:
- Used Python's built-in `hashlib` module for MD5 hashing
- Simple, straightforward implementation without unnecessary complexity
- No external dependencies required

## Testing Process

### Test 1: Example Validation - "abcdef"
- **Expected**: 609043
- **Result**: 609043
- **Hash**: 000001dbbfa3a5c83a2d506429c7b00e
- **Status**: PASSED

### Test 2: Example Validation - "pqrstuv"
- **Expected**: 1048970
- **Result**: 1048970
- **Hash**: 000006136ef2ff3b291c85725f17325c
- **Status**: PASSED

### Test 3: Actual Input - "ckczppom"
- **Result**: 117946
- **Hash**: 00000fe1c139a2c710e9a5c03ec1af03
- **Starts with 00000**: Yes
- **Status**: PASSED

### Test 4: Verification - Lowest Number Check
- **Hash of ckczppom117945**: da5b171a8f9df315774ab7150a974696
- **Starts with 00000**: No
- **Conclusion**: 117946 is confirmed as the lowest valid number
- **Status**: PASSED

## Performance

All tests completed within expected timeframes:
- Example tests ran in a few seconds each
- Actual solution found in reasonable time (< 10 seconds)
- No performance issues encountered

## Verification Checklist

- [x] Solution produces correct answer for "abcdef" (609043)
- [x] Solution produces correct answer for "pqrstuv" (1048970)
- [x] MD5 hashing is correct (verified with known examples)
- [x] Result hash starts with exactly "00000" (five zeroes)
- [x] Previous number (117945) does NOT produce valid hash
- [x] Solution completes in reasonable time
- [x] Input is correctly read and whitespace stripped
- [x] Actual input "ckczppom" produces valid result: 117946

## Conclusion

The implementation successfully solves the AdventCoin mining problem. All test cases passed, including both provided examples and the actual input. The solution is deterministic, efficient for the problem size, and produces the correct answer of **117946** for the secret key "ckczppom".
