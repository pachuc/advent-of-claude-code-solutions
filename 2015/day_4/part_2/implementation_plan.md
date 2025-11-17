# Implementation Plan: AdventCoin Mining (Part 2)

## Problem Summary
Find the lowest positive integer that, when appended to the secret key "ckczppom", produces an MD5 hash starting with at least six zeroes in hexadecimal representation.

## Algorithm Analysis

### Approach
This is a brute-force search problem with no mathematical shortcut due to the nature of cryptographic hash functions (MD5). We must iterate through positive integers sequentially until we find one that satisfies the condition.

### Time Complexity
- **Per iteration**: O(1) - constant time for MD5 hash computation and string operations
- **Total iterations**: Unknown beforehand, depends on when a valid hash is found
- **Expected complexity**: O(n) where n is the answer we're searching for

### Space Complexity
- O(1) - only storing current integer, concatenated string, and hash result

### Performance Considerations
1. **Expected search space**: With 6 leading zeroes, we expect to search approximately 16^6 = 16,777,216 candidates on average (since each hex digit has 16 possible values, probability of six zeroes is 1/16^6)
2. **Optimization opportunities**:
   - Use efficient string concatenation
   - Convert hash to hex efficiently
   - Early termination on first match
   - Could use multiple threads/processes, but for simplicity, single-threaded is sufficient

## Implementation Steps

### Step 1: Import Required Libraries
```python
import hashlib
```
- Use Python's built-in `hashlib` for MD5 computation
- No external dependencies needed

### Step 2: Read and Parse Input
```python
def read_input(filename='input.md'):
    with open(filename, 'r') as f:
        secret_key = f.read().strip()
    return secret_key
```
- Read the input file
- Strip whitespace (leading/trailing) as specified in problem
- Return the secret key string

### Step 3: Implement Hash Checking Function
```python
def find_adventcoin(secret_key, num_zeroes=6):
    n = 1
    while True:
        # Concatenate secret key with current integer
        test_string = f"{secret_key}{n}"

        # Compute MD5 hash
        hash_object = hashlib.md5(test_string.encode())
        hash_hex = hash_object.hexdigest()

        # Check if hash starts with required number of zeroes
        if hash_hex.startswith('0' * num_zeroes):
            return n

        n += 1
```

**Design decisions**:
- Parameter `num_zeroes` allows reusability (could work for Part 1 with value 5)
- Use f-string for efficient string concatenation
- Encode string to bytes for MD5 (required by hashlib)
- Use `hexdigest()` for hexadecimal representation
- Use `startswith()` for clean, readable prefix checking
- Increment counter and continue until match found

### Step 4: Implement Main Execution Logic
```python
def main():
    # Read input
    secret_key = read_input('input.md')

    # Find the answer
    result = find_adventcoin(secret_key, num_zeroes=6)

    # Output the result
    print(result)

    # Optional: verify the result
    test_string = f"{secret_key}{result}"
    hash_hex = hashlib.md5(test_string.encode()).hexdigest()
    print(f"Hash: {hash_hex}")

if __name__ == "__main__":
    main()
```

**Design decisions**:
- Separate main() function for clean structure
- Print the result (single integer as required)
- Optionally print the hash for verification
- Use `if __name__ == "__main__"` for proper script execution

### Step 5: Complete Script Structure
```
solution.py
├── Imports (hashlib)
├── read_input() function
├── find_adventcoin() function
├── main() function
└── Entry point check
```

## Alternative Implementations Considered

### 1. **Parallel Processing**
- Could split search space across multiple processes
- **Rejected**: Adds complexity, single-threaded is sufficient for this problem size

### 2. **String Caching**
- Pre-compute secret_key as bytes
- **Accepted**: Minor optimization, could include

### 3. **Early Hash Comparison**
- Compare hash bytes directly instead of hex string
- **Rejected**: Hex string comparison is clearer and fast enough

### 4. **Progress Indicators**
- Print progress every 1,000,000 iterations
- **Recommended**: Helpful for user feedback during 2-5 minute execution
- Example: `if n % 1000000 == 0: print(f"Checked {n:,} candidates...")`

## Expected Runtime
- Approximately 2-5 minutes on modern hardware, up to 10 minutes on slower CPUs
- Expected around 16.7 million iterations based on probability (16^6)
- Actual runtime depends on the specific answer and CPU speed
- Consider adding progress indicators (print every 1M iterations) for user feedback during execution

## File Output
- Primary output: Print the integer to stdout
- No file writing required (problem asks for single integer output)

## Code Quality Considerations
- Clear variable names
- Simple, readable logic
- Minimal dependencies
- Input validation intentionally omitted (input is well-defined for this puzzle)
- No extensive error handling needed (file assumed to exist with valid content)
- No need for logging (simple script)
- Optional: Add progress printing for long-running executions
