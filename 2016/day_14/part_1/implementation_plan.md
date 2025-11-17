# Implementation Plan: One-Time Pad Key Generation

## Overview
Create a Python script that finds the index producing the 64th valid key for a one-time pad system using MD5 hashing with specific validation rules.

## Algorithm Efficiency Considerations

### Performance Analysis
- **Input size**: We need to find the 64th key. Based on the example (salt `abc` → index 22728), we may need to check ~20,000-30,000+ indices
- **Each validation**: Requires checking up to 1000 future hashes
- **Worst case**: ~30,000 indices × 1,000 lookups = 30 million hash computations
- **Optimization critical**: Pre-compute and cache hashes to avoid redundant MD5 calculations

### Optimization Strategy
1. **Hash Caching**: Store computed hashes in a dictionary/array to avoid recomputation
2. **Lazy Computation**: Only compute hashes as needed (when checking for quintuplets)
3. **Early Termination**: Stop checking future hashes once quintuplet is found

## Step-by-Step Implementation Plan

### Step 1: Import Required Libraries
```python
import hashlib
import re
```
- `hashlib` for MD5 computation
- `re` for regex pattern matching (triplets and quintuplets)

### Step 2: Create Hash Generation Function
**Function**: `generate_hash(salt, index)`
- **Input**: salt string, integer index
- **Process**:
  1. Concatenate salt + str(index)
  2. Encode to bytes (UTF-8)
  3. Compute MD5 hash
  4. Return hexadecimal digest as lowercase string
- **Output**: 32-character hex string
- **Optimization**: This will be called frequently, keep it simple and direct

### Step 3: Create Triplet Detection Function
**Function**: `find_first_triplet(hash_str)`
- **Input**: 32-character hash string
- **Process**:
  1. Iterate through hash string (positions 0 to 29)
  2. Check if hash[i] == hash[i+1] == hash[i+2]
  3. Return the character if found (first occurrence only)
  4. Return None if no triplet found
- **Output**: Single character or None
- **Alternative approach**: Use regex `r'(.)\1{2}'` to find first triplet
- **Decision**: Use simple iteration for clarity (both approaches are functionally equivalent in performance)

### Step 4: Create Quintuplet Detection Function
**Function**: `contains_quintuplet(hash_str, char)`
- **Input**: hash string, character to search for
- **Process**:
  1. Create pattern: char repeated 5 times
  2. Check if pattern exists in hash_str
  3. Return True/False
- **Output**: Boolean
- **Implementation**: Use `char * 5 in hash_str` for simplicity

### Step 5: Create Hash Cache Structure
**Data Structure**: Dictionary or list
- **Option 1**: `hash_cache = {}` (dictionary with index as key)
- **Option 2**: `hash_cache = []` (list, append in order)
- **Decision**: Use dictionary for O(1) lookup with arbitrary indices
- **Function**: `get_hash(salt, index, cache)`
  - Check if index in cache
  - If not, generate and store
  - Return hash

### Step 6: Create Key Validation Function
**Function**: `is_valid_key(salt, index, hash_cache)`
- **Input**: salt, current index, hash cache
- **Process**:
  1. Get hash for current index (from cache or generate)
  2. Find first triplet in hash
  3. If no triplet, return False
  4. Loop through next 1000 indices using `range(index+1, index+1001)`
     - This checks indices [index+1, index+2, ..., index+1000] exactly 1000 hashes
     - For each future index:
       - Get hash from cache (or generate and cache)
       - Check if contains quintuplet of triplet character
       - If found, return True (early termination)
  5. If no quintuplet found in range, return False
- **Output**: Boolean
- **Note**: Cache all hashes checked for future reuse
- **Important**: Only the FIRST triplet character matters; ignore any subsequent triplets in the same hash

### Step 7: Create Main Key Finding Function
**Function**: `find_64th_key(salt)`
- **Input**: salt string
- **Process**:
  1. Initialize hash_cache = {}
  2. Initialize keys_found = 0
  3. Initialize current_index = 0
  4. While keys_found < 64:
     - Check if current_index is valid key
     - If valid:
       - Increment keys_found
       - If keys_found == 64, return current_index
     - Increment current_index
  5. Return current_index (when 64 keys found)
- **Output**: Integer index

### Step 8: Create Main Execution Block
```python
if __name__ == "__main__":
    # Read salt from input
    with open('input.md', 'r') as f:
        salt = f.read().strip()

    # Find 64th key
    result = find_64th_key(salt)

    # Print result
    print(result)
```

## Code Structure

```
solution.py
├── generate_hash(salt, index) -> str
│   └── Creates MD5 hash from salt + index
├── find_first_triplet(hash_str) -> str | None
│   └── Finds first triplet character in hash
├── contains_quintuplet(hash_str, char) -> bool
│   └── Checks if hash contains 5 consecutive chars
├── get_hash(salt, index, cache) -> str
│   └── Returns hash from cache or generates and caches it
├── is_valid_key(salt, index, hash_cache) -> bool
│   └── Validates if hash is a key (uses get_hash for all lookups)
├── find_64th_key(salt) -> int
│   └── Main loop to find the 64th valid key
└── main block
    └── Reads input and executes find_64th_key
```

## Complexity Analysis

### Time Complexity
- **Per key validation**: O(1000) hash computations in worst case
- **Total**: O(N × 1000) where N is the index of 64th key (~25,000)
- **With caching**: Many hashes reused, effective complexity reduced

### Space Complexity
- **Hash cache**: O(N + 1000) ≈ O(N) for storing ~26,000 hashes
- **Each hash**: 32 bytes + overhead
- **Total**: ~1-2 MB memory usage (acceptable)

## Expected Runtime
- MD5 is fast (~1-2 microseconds per hash)
- 25,000,000 hashes × 2μs = ~50 seconds worst case
- With caching optimization: ~5-10 seconds expected

## Implementation Notes
1. Keep functions pure and simple
2. Use descriptive variable names
3. Add minimal comments for clarity
4. Focus on correctness first, optimization second
5. No need for extensive error handling (controlled input)
6. No logging required (script execution context)
