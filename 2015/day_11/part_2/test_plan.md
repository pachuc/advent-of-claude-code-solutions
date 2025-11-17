# Test Plan: Santa's Password Generator (Part 2)

## Testing Strategy
Since Part 2 uses the exact same algorithm as Part 1 (just with a different starting password), we can leverage the confidence from Part 1's correctness and focus on:
1. Verifying the correct starting password is used (`vzbxxyzz`)
2. Confirming the output is different from Part 1
3. Validating the output meets all password requirements
4. Edge case testing around the specific starting password

## Test Categories

### 1. Input Validation Tests

#### Test 1.1: Verify Correct Starting Password
**Purpose**: Ensure we're starting from Part 1's answer, not the original input
- **Input**: Read from `part_1_answer.txt`
- **Expected**: Starting password should be `vzbxxyzz`
- **Validation**: Print or assert the starting password before processing

```python
def test_starting_password():
    with open('part_1_answer.txt', 'r') as f:
        password = f.read().strip()
    assert password == 'vzbxxyzz', f"Expected 'vzbxxyzz', got '{password}'"
    print(f"✓ Starting password: {password}")
```

#### Test 1.2: File Reading
**Purpose**: Ensure the Part 1 answer file is read correctly
- **Test**: Check file exists and contains valid data
- **Expected**: File contains 8 lowercase letters with no extra whitespace after stripping

### 2. Algorithm Correctness Tests

#### Test 2.1: First Increment from Part 1 Answer
**Purpose**: Verify the first increment from `vzbxxyzz` works correctly
- **Input**: `vzbxxyzz`
- **Expected first increment**:
  - `vzbxxyzz` → increment rightmost 'z' to 'a' (carry)
  - → next 'z' to 'a' (carry)
  - → 'y' to 'z'
  - **Result**: `vzbxxzaa`
- **Validation**: Manually verify the increment logic

```python
def test_first_increment():
    result = increment_password('vzbxxyzz')
    assert result == 'vzbxxzaa', f"Expected 'vzbxxzaa', got '{result}'"
    print(f"✓ vzbxxyzz → {result}")
```

#### Test 2.2: Forbidden Character Optimization Verification
**Purpose**: Verify that the critical forbidden character optimization from Part 1 is preserved
- **Importance**: This optimization is crucial for performance - without it, the solution could be 100-1000x slower
- **Test**: Verify that when incrementing produces 'i', 'o', or 'l', it skips to the next valid character and resets right positions
- **Validation**:

```python
def test_forbidden_char_optimization():
    """Verify increment skips forbidden chars efficiently."""
    # Test 'i' skip: when incrementing produces 'i', should skip to 'j'
    result = increment_password('abcdefgh')  # h+1 would be i, should become j
    assert 'i' not in result, "Should skip 'i' - got: " + result
    assert result[7] == 'a', "Should reset positions to the right of skip"

    # Test 'o' skip: when incrementing produces 'o', should skip to 'p'
    result = increment_password('abcdefgn')  # n+1 would be o, should become p
    assert 'o' not in result, "Should skip 'o' - got: " + result

    # Test 'l' skip: when incrementing produces 'l', should skip to 'm'
    result = increment_password('abcdefgk')  # k+1 would be l, should become m
    assert 'l' not in result, "Should skip 'l' - got: " + result

    print("✓ Forbidden character optimization working correctly")
```

#### Test 2.3: Starting Password Validation Check
**Purpose**: Verify that the starting password `vzbxxyzz` itself is valid (which it is!)
- **Input**: `vzbxxyzz`
- **Analysis**:
  - Has increasing straight: `xyz` at positions 5-6-7 ✓
  - No forbidden chars: No 'i', 'o', or 'l' ✓
  - Has two pairs: `xx` at positions 3-4, `zz` at positions 6-7 ✓
  - **Conclusion**: `vzbxxyzz` IS VALID
- **Implication**: The algorithm must increment at least once before returning (which `find_next_password` does)

#### Test 2.4: Output Password Validation
**Purpose**: Verify the final output meets ALL three requirements
- **Requirement 1 - Increasing Straight**:
  - Check that output contains at least one sequence of 3 consecutive letters
  - Valid sequences: abc, bcd, cde, ..., xyz
- **Requirement 2 - No Forbidden Characters**:
  - Verify output contains no 'i', 'o', or 'l'
- **Requirement 3 - Two Different Pairs**:
  - Verify output has at least 2 different non-overlapping pairs (e.g., 'aa' and 'bb')

### 3. Output Validation Tests

#### Test 3.1: Output Format
**Purpose**: Ensure output is correctly formatted
- **Expected**: Single line with exactly 8 lowercase letters
- **Validation**:
  ```python
  def test_output_format(output):
      assert len(output) == 8, f"Expected length 8, got {len(output)}"
      assert output.islower(), "Output must be lowercase"
      assert output.isalpha(), "Output must be alphabetic"
      print(f"✓ Output format valid: {output}")
  ```

#### Test 3.2: Output is Different from Part 1
**Purpose**: Confirm Part 2 produces a different result than Part 1
- **Part 1 answer**: `vzbxxyzz`
- **Part 2 answer**: Should be different (the NEXT valid password after Part 1's answer)
- **Validation**:
  ```python
  def test_different_from_part1(output):
      assert output != "vzbxxyzz", "Part 2 answer must differ from Part 1"
      print(f"✓ Part 2 answer differs from Part 1: {output}")
  ```

#### Test 3.3: Output is Greater than Input
**Purpose**: Verify the output password comes after the input in lexicographic order
- **Input**: `vzbxxyzz`
- **Output**: Should be lexicographically greater than `vzbxxyzz`
- **Validation**:
  ```python
  def test_output_greater_than_input(output):
      assert output > 'vzbxxyzz', f"{output} should be > 'vzbxxyzz'"
      print(f"✓ Output comes after input: vzbxxyzz < {output}")
  ```

### 4. Manual Validation Tests

#### Test 4.1: Manual Validation of Output
**Purpose**: Manually verify the output meets all requirements

**Process**:
1. Take the output password (e.g., `vzcaabcc`)
2. Check forbidden chars: No 'i', 'o', or 'l'
3. Check increasing straight: Look for abc, bcd, etc. and identify specific sequence
4. Check two pairs: Find pairs and verify they're different letters

**Manual Checklist Template**:
```
Output: _________

Forbidden chars check:
- Contains 'i': [ ] Yes [ ] No
- Contains 'o': [ ] Yes [ ] No
- Contains 'l': [ ] Yes [ ] No
Result: [ ] Pass [ ] Fail

Increasing straight check:
- Found sequence: _____ at positions _____
Result: [ ] Pass [ ] Fail

Two pairs check:
- First pair: __ at positions _____
- Second pair: __ at positions _____
- Are they different letters?: [ ] Yes [ ] No
Result: [ ] Pass [ ] Fail

Overall: [ ] VALID [ ] INVALID
```

#### Test 4.2: Verify It's the NEXT Valid Password
**Purpose**: Ensure no valid password exists between the input and output
- **Method**: This is implicitly verified by the Part 1 regression tests (Tests 5.1-5.2)
  - If Part 1's algorithm correctly finds the next valid password for known examples
  - And we're using the exact same algorithm for Part 2
  - Then Part 2's result will also be the next valid password
- **Additional check**: Starting from `vzbxxyzz`, the first increment is `vzbxxzaa`
  - We can manually verify this specific password is invalid to confirm iteration continues

### 5. Regression Tests from Part 1

#### Test 5.1: Reuse Part 1 Test Cases
**Purpose**: Verify helper functions still work correctly
- **Test cases from Part 1 problem examples**:
  - `hijklmmn` → should be invalid (forbidden chars)
  - `abbceffg` → should be invalid (no straight)
  - `abbcegjk` → should be invalid (only one pair)
  - `abcdffaa` → should be valid
  - `ghjaabcc` → should be valid

```python
def test_part1_examples():
    assert is_valid_password('hijklmmn') == False  # forbidden i, l
    assert is_valid_password('abbceffg') == False  # no straight
    assert is_valid_password('abbcegjk') == False  # one pair only
    assert is_valid_password('abcdffaa') == True
    assert is_valid_password('ghjaabcc') == True
    print("✓ All Part 1 validation examples pass")
```

#### Test 5.2: Part 1 Complete Examples
**Purpose**: Verify the complete algorithm works for Part 1 test cases
- **Test cases**:
  - `abcdefgh` → `abcdffaa`
  - `ghijklmn` → `ghjaabcc`

```python
def test_part1_complete_examples():
    assert find_next_password('abcdefgh') == 'abcdffaa'
    assert find_next_password('ghijklmn') == 'ghjaabcc'
    print("✓ Part 1 complete examples pass")
```

### 6. Performance Test

#### Test 6.1: Performance Verification
**Purpose**: Ensure the solution is found within reasonable time
- **Expected**: Should find answer in < 1 second (excellent), < 5 seconds (acceptable)
- **Validation with tiered thresholds**:
  ```python
  import time

  def test_performance():
      with open('part_1_answer.txt', 'r') as f:
          start_password = f.read().strip()

      start_time = time.time()
      result = find_next_password(start_password)
      end_time = time.time()

      elapsed = end_time - start_time

      # Tiered performance assessment
      if elapsed < 1.0:
          print(f"✓ Excellent performance: {elapsed:.4f} seconds")
      elif elapsed < 5.0:
          print(f"⚠ Acceptable performance: {elapsed:.4f} seconds")
      else:
          print(f"⚠ Slow performance: {elapsed:.4f} seconds (check optimization)")

      # Hard limit: 10 seconds
      assert elapsed < 10.0, f"Too slow: {elapsed} seconds - optimization may be missing"
      return result
  ```

## Test Execution Plan

### Phase 1: Pre-Execution Validation
1. Verify `part_1_answer.txt` exists and contains `vzbxxyzz`
2. Verify all helper functions are present in the solution
3. Run Part 1 regression tests to ensure algorithm is correct

### Phase 2: Execution
1. Run the solution script
2. Capture the output
3. Record execution time

### Phase 3: Output Validation
1. Check output format (8 lowercase letters)
2. Verify output != `vzbxxyzz` (different from Part 1 answer)
3. Verify output > `vzbxxyzz` (lexicographically)
4. Validate all three password requirements:
   - No forbidden characters ('i', 'o', 'l')
   - Has at least one increasing straight
   - Has at least two different non-overlapping pairs

### Phase 4: Manual Verification
1. Print the output clearly
2. Manually check each requirement:
   - Visual inspection for forbidden characters
   - Find and mark the increasing straight
   - Find and mark the two different pairs
3. Confirm all requirements are satisfied

## Success Criteria
The solution passes all tests if:
- ✓ Reads `vzbxxyzz` as starting password
- ✓ Produces output of exactly 8 lowercase letters
- ✓ Output is different from `vzbxxyzz`
- ✓ Output passes all three validation rules:
  - No 'i', 'o', or 'l'
  - Contains at least one 3-letter increasing straight
  - Contains at least two different non-overlapping pairs
- ✓ Output is lexicographically greater than `vzbxxyzz`
- ✓ Completes in reasonable time (< 10 seconds)
- ✓ All Part 1 regression tests pass

## Testing Checklist
- [ ] Verify starting password is `vzbxxyzz`
- [ ] Verify Part 1 regression tests pass
- [ ] Run solution and capture output
- [ ] Check output is 8 lowercase letters
- [ ] Verify no forbidden characters in output
- [ ] Find and verify increasing straight in output
- [ ] Find and verify two different pairs in output
- [ ] Confirm output != `vzbxxyzz`
- [ ] Confirm output > `vzbxxyzz`
- [ ] Check execution completes in < 10 seconds
- [ ] Manually verify all three requirements on paper

## Expected Result
Based on the algorithm and starting password `vzbxxyzz`, the Part 2 answer should be the very next valid password in the sequence after `vzbxxyzz`.

## Sample Test Script

```python
# test_solution.py
from solution import (
    increment_password,
    has_no_forbidden_chars,
    has_increasing_straight,
    has_two_pairs,
    is_valid_password,
    find_next_password
)
import time

def run_all_tests():
    print("=" * 60)
    print("PART 2 TEST SUITE")
    print("=" * 60)

    # Test 1: Starting password
    print("\n[Test 1] Verify starting password")
    with open('part_1_answer.txt', 'r') as f:
        start = f.read().strip()
    assert start == 'vzbxxyzz'
    print(f"✓ Starting password: {start}")

    # Test 2: Forbidden character optimization
    print("\n[Test 2] Forbidden character optimization")
    result = increment_password('abcdefgh')
    assert 'i' not in result, f"Should skip 'i' - got: {result}"
    assert result[7] == 'a', "Should reset positions to the right"
    print("✓ Optimization working correctly")

    # Test 3: Part 1 regression tests
    print("\n[Test 3] Part 1 regression tests")
    assert find_next_password('abcdefgh') == 'abcdffaa'
    assert find_next_password('ghijklmn') == 'ghjaabcc'
    print("✓ Part 1 examples pass")

    # Test 4: Run Part 2
    print("\n[Test 4] Solve Part 2")
    start_time = time.time()
    result = find_next_password(start)
    elapsed = time.time() - start_time
    print(f"✓ Found password: {result}")

    # Performance assessment
    if elapsed < 1.0:
        print(f"✓ Excellent performance: {elapsed:.4f} seconds")
    elif elapsed < 5.0:
        print(f"⚠ Acceptable performance: {elapsed:.4f} seconds")
    else:
        print(f"⚠ Slow performance: {elapsed:.4f} seconds")
    assert elapsed < 10.0, f"Too slow: {elapsed}s"

    # Test 5: Validate output
    print("\n[Test 5] Validate output")
    assert len(result) == 8
    assert result.islower() and result.isalpha()
    assert result != 'vzbxxyzz'
    assert result > 'vzbxxyzz'
    assert is_valid_password(result)
    print("✓ Output format valid")
    print("✓ Different from Part 1")
    print("✓ Greater than input")
    print("✓ Passes all validation rules")

    # Manual verification prompt
    print("\n[Manual Verification Required]")
    print(f"Password: {result}")
    print("Please verify:")
    print("1. No 'i', 'o', or 'l'")
    print("2. Has increasing straight (abc, bcd, ...)")
    print("3. Has two different pairs")

    print("\n" + "=" * 60)
    print("ALL AUTOMATED TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()
```
