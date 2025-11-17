# Implementation Plan: AdventCoin Mining

## Problem Overview
Find the lowest positive integer that, when appended to the secret key `ckczppom`, produces an MD5 hash starting with at least five hexadecimal zeroes.

## Algorithm Analysis

### Approach: Brute Force Sequential Search
- **Rationale**: There's no mathematical shortcut to predict which number will produce the desired hash pattern due to MD5's cryptographic properties. We must try integers sequentially.
- **Time Complexity**: O(n) where n is the answer value. Based on examples (609043 and 1048970), expect to test hundreds of thousands to millions of combinations.
- **Space Complexity**: O(1) - only storing current integer and hash result.

### Performance Considerations
1. **MD5 Computation**: Most expensive operation per iteration
2. **String Concatenation**: Relatively cheap but happens millions of times
3. **Hash Comparison**: Very fast - just check first 5 hex characters
4. **Expected Runtime**: Based on examples, likely 1-5 seconds on modern hardware

### Why This is Optimal
- Cannot skip numbers (need the *lowest* integer)
- Cannot parallelize effectively for "lowest" requirement (would need synchronization)
- MD5 is already highly optimized in Python's hashlib
- Hash checking (prefix comparison) is O(1)

## Implementation Steps

### Step 1: Import Required Libraries
```python
import hashlib
```
- Use Python's built-in `hashlib` module for MD5 hashing
- No additional dependencies needed

### Step 2: Read and Parse Input
```python
def read_input(filename='input.md'):
    with open(filename, 'r') as f:
        secret_key = f.read().strip()
    return secret_key
```
- Read the input file (expected format: single line, plain text)
- Strip whitespace (leading/trailing spaces, newlines, tabs)
- Return the secret key as a string
- No validation needed (input format guaranteed for this script)

### Step 3: Implement MD5 Hash Function
```python
def compute_md5_hex(text):
    return hashlib.md5(text.encode()).hexdigest()
```
- Encode string to bytes (MD5 requires bytes)
- Compute MD5 hash
- Convert to hexadecimal string representation
- Return hex string (32 characters)

### Step 4: Implement Hash Validation
```python
def starts_with_five_zeroes(hex_hash):
    return hex_hash.startswith('00000')
```
- Check if hexadecimal hash starts with at least five zeroes
- Using `startswith('00000')` correctly handles both exactly 5 zeroes and 6+ zeroes
- Simple string prefix check (very efficient)
- Alternative: `hex_hash[:5] == '00000'`
- Note: Problem says "at least five zeroes" - hashes with 6+ leading zeroes also qualify

### Step 5: Implement Main Mining Loop
```python
def find_advent_coin(secret_key):
    number = 1
    while True:
        combined = secret_key + str(number)
        hash_result = compute_md5_hex(combined)

        if starts_with_five_zeroes(hash_result):
            return number

        number += 1
```
- Start with integer 1 (not 0, as problem requires positive integers)
- Concatenate secret key with current number using str() conversion
- Compute MD5 hash
- Check if hash starts with five zeroes
- If found, return the number
- Otherwise, increment and continue
- No maximum iteration limit needed (answer guaranteed to exist)

### Step 6: Main Execution Block
```python
if __name__ == '__main__':
    secret_key = read_input()
    result = find_advent_coin(secret_key)
    print(result)
```
- Read input file
- Find the answer
- Print result to stdout

## Complete Code Structure

```python
import hashlib

def read_input(filename='input.md'):
    """Read and parse the secret key from input file."""
    with open(filename, 'r') as f:
        secret_key = f.read().strip()
    return secret_key

def compute_md5_hex(text):
    """Compute MD5 hash and return hexadecimal representation."""
    return hashlib.md5(text.encode()).hexdigest()

def starts_with_five_zeroes(hex_hash):
    """Check if hash starts with five zeroes."""
    return hex_hash.startswith('00000')

def find_advent_coin(secret_key):
    """Find lowest positive integer that produces hash with five leading zeroes."""
    number = 1
    while True:
        combined = secret_key + str(number)
        hash_result = compute_md5_hex(combined)

        if starts_with_five_zeroes(hash_result):
            return number

        number += 1

if __name__ == '__main__':
    secret_key = read_input()
    result = find_advent_coin(secret_key)
    print(result)
```

## Optimization Opportunities (Not Critical)

### Considered but Not Implemented:
1. **Caching string conversions**: Minimal benefit for the effort
2. **Batch processing**: Doesn't help find "lowest" number
3. **Early termination in hex check**: Python's startswith is already optimized
4. **Progress indicator**: Would slow down the loop; unnecessary for script
   - Could add progress every 100k iterations for debugging with minimal impact
   - Example: `if number % 100000 == 0: print(f"Tested {number}...")` (commented out by default)

## Expected Runtime
- Based on example answers (600k-1M range)
- Modern Python can compute ~200k-500k MD5 hashes per second
- Expected runtime: 2-10 seconds for typical inputs

## Error Handling
Not implementing extensive error handling because:
- Input file is guaranteed to exist
- Input format is simple (single line string)
- Loop will always find an answer (mathematical certainty)
- This is a script, not production code
