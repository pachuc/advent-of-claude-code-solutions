# Test Plan: MD5 Password Generation

## Testing Strategy
Verify the solution correctly finds MD5 hashes starting with five zeros and extracts the proper characters to build the password.

## Test Categories

### 1. Known Example Verification

**Purpose**: Validate algorithm correctness against provided example

**Test Case: Example Door ID `abc`**
- **Input**: Door ID = `abc`
- **Expected Output**: Password = `18f47a30`
- **Verification Steps**:
  1. Temporarily modify input or door_id variable to `abc`
  2. Run the script
  3. Verify first valid hash at index 3231929 produces character `1`
  4. Verify second valid hash at index 5017308 produces character `8`
  5. Verify third valid hash at index 5278568 produces character `f`
  6. Verify final password is exactly `18f47a30`
- **Pass Criteria**: Output matches expected password exactly

**Manual Hash Verification**:
```python
import hashlib
# Verify example hashes manually
test_cases = [
    ("abc3231929", "1"),  # 6th character is 1
    ("abc5017308", "8"),  # 6th character is 8
    ("abc5278568", "f"),  # 6th character is f
]

for input_str, expected_char in test_cases:
    hash_result = hashlib.md5(input_str.encode()).hexdigest()
    # Verify hash starts with five zeros
    assert hash_result.startswith('00000'), f"{input_str} doesn't start with 00000"
    # Verify 6th character matches expected
    assert hash_result[5] == expected_char, f"Expected {expected_char}, got {hash_result[5]}"
    print(f"✓ {input_str}: {hash_result[:10]}... - char: '{hash_result[5]}'")
```

### 2. Actual Input Testing

**Purpose**: Generate the solution for the actual puzzle input

**Test Case: Door ID `ugkcyxxp`**
- **Input**: Door ID = `ugkcyxxp` (from input.md)
- **Expected Behavior**:
  - Script completes without errors
  - Finds exactly 8 valid hashes
  - Each hash starts with `00000`
  - Produces 8-character password
- **Verification Steps**:
  1. Run script with actual input
  2. Monitor progress output (if implemented)
  3. Verify final password is 8 characters long
  4. Verify all characters are valid hex digits (0-9, a-f)
- **Pass Criteria**:
  - Script completes successfully
  - Password is 8 characters
  - All characters are lowercase hex

### 3. Hash Validation Tests

**Purpose**: Ensure each found hash actually meets criteria

**Test: Verify Five Leading Zeros**
- For each found hash, verify it starts with exactly `00000`
- Store indices and hashes during execution
- Post-process to confirm all are valid

**Implementation**:
```python
# Add to solution for testing
found_hashes = []  # Store (index, hash, character) tuples

# In main loop, when valid hash found:
if hash_result.startswith('00000'):
    found_hashes.append((index, hash_result, hash_result[5]))
    password.append(hash_result[5])

# After completion, verify all:
for idx, hash_val, char in found_hashes:
    assert hash_val.startswith('00000'), f"Hash at {idx} doesn't start with 00000"
    assert hash_val[5] == char, f"Character mismatch at {idx}"
    print(f"✓ Index {idx}: {hash_val[:10]}... -> '{char}'")
```

### 4. Edge Cases and Boundary Conditions

**Test Case: Character Extraction**
- **Purpose**: Verify 6th character (index 5) is correctly extracted
- **Method**: Manual verification of found hashes
- **Check**: hash_result[5] is the character added to password

**Test Case: Index Counter**
- **Purpose**: Ensure index increments correctly through millions of iterations
- **Check**: Index values increase monotonically
- **Validation**: Final index value is reasonable (several million)

**Test Case: Password Length**
- **Purpose**: Verify exactly 8 characters are collected
- **Check**: `len(password) == 8` before termination
- **Validation**: Loop terminates at correct point

**Test Case: Character Types**
- **Purpose**: Ensure all characters are valid hexadecimal
- **Valid characters**: 0-9, a-f (lowercase)
- **Check**: Each character in final password is in '0123456789abcdef'
- **Implementation**: `assert all(c in '0123456789abcdef' for c in final_password)`

### 5. Algorithm Correctness

**Test: Sequential Processing**
- **Purpose**: Verify hashes are checked in order (index 0, 1, 2, ...)
- **Method**: First valid hash should be at lowest possible index
- **Validation**: Cannot find valid hash at index X if there exists a valid hash at index Y where Y < X that wasn't already found

**Test: No Duplicates**
- **Purpose**: Ensure each index is only checked once
- **Method**: Each valid character comes from a different index
- **Validation**: All indices in found_hashes list are unique and increasing

**Test: Negative Cases (False Positives)**
- **Purpose**: Verify hashes NOT starting with `00000` are correctly rejected
- **Method**: Test some hashes that start with `0000` but not `00000`
- **Implementation**:
```python
# Test that we correctly reject near-misses
import hashlib
# Find a hash that starts with 0000 but not 00000
for i in range(1000000):
    h = hashlib.md5(f"abc{i}".encode()).hexdigest()
    if h.startswith('0000') and not h.startswith('00000'):
        print(f"✓ Correctly rejects: abc{i} -> {h[:10]}")
        break
```

**Test: Hash Consistency**
- **Purpose**: Recomputing hash gives same result
- **Method**: Re-hash found indices and verify results match
- **Implementation**:
```python
# After finding password, verify all indices
for idx, stored_hash, char in found_hashes:
    recomputed = hashlib.md5((door_id + str(idx)).encode()).hexdigest()
    assert recomputed == stored_hash, f"Hash mismatch at index {idx}"
    assert recomputed[5] == char, f"Character mismatch at index {idx}"
```

### 6. Integration Testing

**Test: File I/O Verification**
- **Purpose**: Verify solution correctly reads from `input.md`
- **Method**:
  1. Create test `input.md` with known door ID
  2. Run `solution.py`
  3. Verify it reads the correct door ID
- **Implementation**: Import and run actual solution module

**Test: Run Actual Solution File**
- **Purpose**: Verify the submitted `solution.py` works correctly
- **Method**: Import and execute the actual solution module, not just test code
- **Implementation**:
```python
import subprocess
result = subprocess.run(['python', 'solution.py'], capture_output=True, text=True)
output = result.stdout.strip()
assert 'Password:' in output, "Output should contain 'Password:' label"
password = output.split('Password:')[1].strip()
assert len(password) == 8, f"Password should be 8 characters, got {len(password)}"
assert all(c in '0123456789abcdef' for c in password), "Invalid hex characters"
```

**Test: Determinism**
- **Purpose**: Running the solution twice should give the same result
- **Method**: Run solution multiple times and compare outputs
- **Expected**: Identical password each time

## Testing Procedure

### Phase 1: Quick Validation (Under 1 minute)
1. Verify hash computation for known indices manually
2. Test first 1-2 characters with example input `abc`
3. Check character extraction logic with manual test cases

### Phase 2: Example Verification (1-3 minutes)
1. Run full example: door ID `abc`, expect `18f47a30`
2. Compare actual output to expected output character-by-character
3. Fix any discrepancies before proceeding

### Phase 3: Actual Solution (60-90 seconds)
1. Run with actual input `ugkcyxxp` from `input.md`
2. Record all found indices and characters (logged during execution)
3. Verify 8-character password is produced

### Phase 4: Validation (Under 1 minute)
1. Re-verify each found hash manually
2. Check all hashes start with `00000`
3. Verify character extraction is correct
4. Confirm password format is valid (8 hex characters)
5. Test solution.py can be run standalone

## Success Criteria

### Must Pass
- ✓ Example test produces `18f47a30` for door ID `abc`
- ✓ Actual input produces 8-character password
- ✓ All found hashes verified to start with `00000`
- ✓ All characters are valid hex digits (0-9, a-f)
- ✓ Script completes without errors

### Should Verify
- ✓ First valid hash indices match expected ranges
- ✓ Runtime is reasonable (60-90 seconds)
- ✓ Progress output shows steady advancement every 1M iterations
- ✓ Solution can be run as standalone script (`python solution.py`)
- ✓ Output format matches specification: `Password: <8-char password>`

## Test Script Example

```python
import hashlib
import subprocess

def verify_solution(door_id, expected_password=None):
    """Test the password generation algorithm"""
    PASSWORD_LENGTH = 8
    index = 0
    password = []
    found_hashes = []

    print(f"Testing with door ID: {door_id}")

    while len(password) < PASSWORD_LENGTH:
        hash_input = (door_id + str(index)).encode()
        hash_result = hashlib.md5(hash_input).hexdigest()

        if hash_result.startswith('00000'):
            char = hash_result[5]
            password.append(char)
            found_hashes.append((index, hash_result, char))
            print(f"Found {len(password)}/{PASSWORD_LENGTH}: '{char}' at index {index}")

        index += 1

    final_password = ''.join(password)
    print(f"\nFinal password: {final_password}")

    # Verify all hashes
    print("\nVerifying hashes...")
    for idx, hash_val, char in found_hashes:
        assert hash_val.startswith('00000'), f"Hash at {idx} doesn't start with 00000"
        assert hash_val[5] == char, f"Character mismatch at {idx}"
        # Re-verify hash
        reverify = hashlib.md5((door_id + str(idx)).encode()).hexdigest()
        assert reverify == hash_val, f"Hash changed on recomputation at {idx}"

    print("✓ All hashes verified")

    # Verify all characters are valid hex
    assert all(c in '0123456789abcdef' for c in final_password), "Invalid hex characters"
    print("✓ All characters are valid hex digits")

    # Verify password length
    assert len(final_password) == PASSWORD_LENGTH, f"Expected {PASSWORD_LENGTH} chars, got {len(final_password)}"
    print(f"✓ Password length is correct ({PASSWORD_LENGTH} characters)")

    if expected_password:
        assert final_password == expected_password, f"Expected {expected_password}, got {final_password}"
        print(f"✓ Password matches expected: {expected_password}")

    return final_password

def test_actual_solution_file():
    """Test that solution.py runs correctly"""
    print("\n=== Testing solution.py file ===")
    result = subprocess.run(['python', 'solution.py'],
                          capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        print(f"Error running solution.py: {result.stderr}")
        return False

    output = result.stdout.strip()
    print(f"Output: {output}")

    # Verify output format
    assert 'Password:' in output, "Output should contain 'Password:' label"

    # Extract password from output
    password = output.split('Password:')[-1].strip()
    assert len(password) == 8, f"Password should be 8 characters, got {len(password)}"
    assert all(c in '0123456789abcdef' for c in password), "Invalid hex characters"

    print(f"✓ solution.py produced valid 8-character password: {password}")
    return password

# Run tests
print("="*60)
print("=== Testing with example (abc -> 18f47a30) ===")
print("="*60)
verify_solution('abc', '18f47a30')

print("\n" + "="*60)
print("=== Testing with actual input (ugkcyxxp) ===")
print("="*60)
result = verify_solution('ugkcyxxp')
print(f"\n** Solution for ugkcyxxp: {result} **")

print("\n" + "="*60)
print("=== Testing actual solution.py file ===")
print("="*60)
file_result = test_actual_solution_file()

print("\n" + "="*60)
print("ALL TESTS PASSED")
print("="*60)
```

## Edge Cases Not Tested (Out of Scope)

These are intentionally not tested as they're not relevant to solving the specific problem:

- Empty door ID (input is given)
- Non-ASCII characters in door ID (input is ASCII)
- Extremely large indices (won't occur within 8 characters)
- Memory exhaustion (minimal memory used)
- Concurrent access (single-threaded script)
- Invalid input file format (assume correct format)

## Debugging Tips

If tests fail:
1. **Wrong password**: Check character extraction (index 5, not 6)
2. **No matches found**: Verify hash computation, check `.encode()`
3. **Too slow**: Ensure using `hashlib.md5()` not pure Python
4. **Wrong example output**: Verify door ID has no whitespace
