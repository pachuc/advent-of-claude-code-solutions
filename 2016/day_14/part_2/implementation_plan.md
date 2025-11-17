# Implementation Plan: One-Time Pad Key Generation with Key Stretching (Part 2)

## Overview
Part 2 builds on Part 1 by adding **key stretching** - instead of using a single MD5 hash, we apply MD5 a total of 2017 times (1 initial + 2016 additional iterations). The validation logic remains the same, but the hash generation becomes significantly more computationally intensive.

## Key Differences from Part 1
- **Hash generation**: Apply MD5 2017 times instead of just once
- **Expected result**: Different answer (~22551 for example salt vs ~22728 in Part 1)
- **Performance**: Much slower due to repeated MD5 operations (~2017x more MD5 calls)

## Algorithm Efficiency Considerations

### Runtime Analysis
- **Part 1 complexity**: O(n * m) where n = indices checked, m = 1000 (lookahead window)
- **Part 2 complexity**: O(n * m * 2017) due to key stretching on every hash
- **Expected indices to check**: ~20,000-25,000 based on example
- **Total hashes needed**: ~25,000,000 MD5 operations
- **Critical optimization**: Caching is ESSENTIAL to avoid recomputing stretched hashes

### Performance Optimization Strategy
1. **Mandatory caching**: Cache all stretched hashes since they're expensive (2017 MD5 ops each)
2. **Sequential computation**: Must pre-compute or cache hashes in the lookahead window
3. **Memory trade-off**: Storing ~25,000 cached hashes is acceptable vs recomputation cost
4. **No parallelization needed**: Sequential checking is required by problem constraints

## Implementation Steps

### Step 1: Modify Hash Generation Function
**Task**: Update `generate_hash()` to apply key stretching

**Changes needed**:
```python
def generate_stretched_hash(salt, index):
    """Generate MD5 hash with key stretching (2017 total iterations)."""
    # Initial hash
    text = salt + str(index)
    hash_result = hashlib.md5(text.encode('utf-8')).hexdigest()

    # Apply 2016 additional MD5 iterations
    for _ in range(2016):
        hash_result = hashlib.md5(hash_result.encode('utf-8')).hexdigest()

    return hash_result
```

**Rationale**:
- First iteration: hash the salt+index (as before)
- Next 2016 iterations: hash the previous hash result
- Total: 2017 MD5 operations
- Return lowercase hex string (MD5 hexdigest() already returns lowercase)

### Step 2: Verify Key Stretching Logic
**Task**: Ensure implementation matches the example

**Verification approach**:
- Test with salt='abc', index=0
- Initial: MD5('abc0') should give '577571be4de9dcce85a041ba0410f29f'
- After 2016 more iterations: should give 'a107ff634856bb300138cac6568c0f24'
- Add an assert or test to verify this during development

### Step 3: Reuse Part 1 Validation Logic
**Task**: Keep existing triplet/quintuplet validation unchanged

**Functions to reuse from part_1_solution.py**:
- `find_first_triplet(hash_str)` - No changes needed
- `contains_quintuplet(hash_str, char)` - No changes needed
- `is_valid_key(salt, index, hash_cache)` - No changes needed (uses get_hash internally)

**Rationale**: The validation rules are identical; only hash generation changes

### Step 4: Update Hash Cache Integration
**Task**: Ensure `get_hash()` calls the stretched hash function

**Changes needed**:
```python
def get_hash(salt, index, cache):
    """Get hash from cache or generate stretched hash and cache it."""
    if index not in cache:
        cache[index] = generate_stretched_hash(salt, index)  # Call stretched version
    return cache[index]
```

**Rationale**: Cache is critical since each hash now costs 2017 MD5 operations

### Step 5: Reuse Main Search Loop
**Task**: Keep `find_64th_key()` function identical

**No changes needed**:
- Same sequential search logic
- Same key counting (stop at 64th key)
- Same cache usage pattern
- Only the underlying hash generation changes

### Step 6: Update Input/Output
**Task**: Ensure correct input reading and output format

**No changes needed**:
- Still read from 'input.md'
- Still output single integer (the 64th key index)
- Input is still 'ihaygndm'

### Step 7: Handle Expected Runtime
**Task**: Set realistic expectations for execution time

**Considerations**:
- Part 2 is ~2017x slower than Part 1 per hash
- With ~25M MD5 operations total, may take 30 seconds to 5 minutes depending on hardware
- This is expected and acceptable for this problem
- No need for progress bars or optimization beyond caching
- **Optional for debugging**: Can add simple progress indicator (print every 1000 indices) if needed

## Code Structure

### Functions (adapted from Part 1)
1. `generate_stretched_hash(salt, index)` - NEW: Applies key stretching
2. `find_first_triplet(hash_str)` - REUSE: Unchanged from Part 1
3. `contains_quintuplet(hash_str, char)` - REUSE: Unchanged from Part 1
4. `get_hash(salt, index, cache)` - MODIFIED: Calls stretched hash function
5. `is_valid_key(salt, index, hash_cache)` - REUSE: Unchanged logic
6. `find_64th_key(salt)` - REUSE: Unchanged from Part 1
7. `main` block - REUSE: Unchanged from Part 1

### Data Structures
- `hash_cache`: Dictionary mapping index -> stretched hash string
- No other complex data structures needed

## Implementation Checklist
- [ ] Copy part_1_solution.py as starting point
- [ ] Replace `generate_hash()` with `generate_stretched_hash()` implementing 2017 iterations
- [ ] Update `get_hash()` to call `generate_stretched_hash()`
- [ ] Verify all other functions remain unchanged
- [ ] **Manual verification**: Test hash stretching with salt='abc', index=0 - should produce 'a107ff634856bb300138cac6568c0f24'
- [ ] Test with example salt 'abc' - should find 64th key at index 22551
- [ ] Run with actual input 'ihaygndm'
- [ ] Verify output is different from Part 1 answer (15035)

## Expected Behavior
- Input: 'ihaygndm'
- Output: An integer (likely > 20000 based on example pattern)
- Runtime: 30 seconds to 5 minutes depending on hardware (acceptable)
- Memory: Minimal (caching ~25k hash strings @ ~100 bytes each ≈ 2.5 MB)

## Edge Cases (Same as Part 1)
- Triplet at end of hash (positions allow checking 3 chars)
- Quintuplet matches in multiple future hashes (first match counts)
- Hash that is both a key and contains quintuplet for earlier hash
- Cache grows linearly with search progress (acceptable)
