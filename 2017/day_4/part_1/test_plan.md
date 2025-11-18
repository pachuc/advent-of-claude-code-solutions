# Test Plan: High-Entropy Passphrase Validation

## Testing Strategy

Since this is a script to solve a specific problem (not production code), we'll focus on:
1. **Correctness verification** using provided examples
2. **Edge case validation** for boundary conditions
3. **Manual verification** against actual input
4. **Unit testing** for the core validation function

We do NOT need:
- Integration tests
- Performance benchmarking (algorithm is already O(n))
- Stress testing with massive inputs
- Error recovery testing

## Test Categories

### 1. Example Test Cases (from problem statement)

**Test 1.1: All unique words (VALID)**
```python
Input: "aa bb cc dd ee"
Expected: True (valid)
Reasoning: All words are unique
```

**Test 1.2: Duplicate word (INVALID)**
```python
Input: "aa bb cc dd aa"
Expected: False (invalid)
Reasoning: "aa" appears twice
```

**Test 1.3: Similar but different words (VALID)**
```python
Input: "aa bb cc dd aaa"
Expected: True (valid)
Reasoning: "aa" and "aaa" are different words
```

### 2. Edge Case Tests

**Test 2.1: Single word passphrase**
```python
Input: "word"
Expected: True (valid)
Reasoning: Cannot have duplicates with one word
```

**Test 2.2: Two identical words**
```python
Input: "word word"
Expected: False (invalid)
Reasoning: Simplest duplicate case
```

**Test 2.3: Two different words**
```python
Input: "word1 word2"
Expected: True (valid)
Reasoning: Simplest valid case
```

**Test 2.4: Empty passphrase**
```python
Input: ""
Expected: True (valid)
Reasoning: No duplicates in empty set (len([]) == len(set([])) == 0)
Note: This tests the validation function directly; empty lines are skipped in the main pipeline
```

**Test 2.5: Multiple spaces between words**
```python
Input: "aa  bb   cc"
Expected: True (valid)
Reasoning: split() handles multiple spaces correctly
```

**Test 2.6: Leading/trailing whitespace**
```python
Input: "  aa bb cc  "
Expected: True (valid)
Reasoning: strip() and split() handle whitespace
```

**Test 2.7: Three instances of same word**
```python
Input: "aa aa aa"
Expected: False (invalid)
Reasoning: Multiple duplicates
```

**Test 2.8: Duplicate at different positions**
```python
Input: "aa bb cc dd ee aa"
Expected: False (invalid)
Reasoning: Duplicate at start and end
```

**Test 2.9: Long passphrase with unique words**
```python
Input: "a b c d e f g h i j k l m n o p"
Expected: True (valid)
Reasoning: Many unique words
```

**Test 2.10: Long passphrase with one duplicate**
```python
Input: "a b c d e f g h i j k l m n o p a"
Expected: False (invalid)
Reasoning: One duplicate among many words
```

### 3. Actual Input Validation

**Test 3.1: Sample from actual input (line 1)**
```python
Input: "bdwdjjo avricm cjbmj ran lmfsom ivsof"
Expected: True (valid)
Reasoning: All words appear unique
Manual verification: Count unique words = 6, total words = 6
```

**Test 3.2: Sample from actual input (line 7)**
```python
Input: "srceh xdwao reshc shecr"
Expected: True (valid)
Words: ["srceh", "xdwao", "reshc", "shecr"]
Manual check:
- srceh vs reshc: different strings (not exact duplicates)
- srceh vs shecr: different strings (not exact duplicates)
- reshc vs shecr: different strings (not exact duplicates)
Note: Part 1 checks for exact duplicate words only, not anagrams
All words unique as strings: True (valid)
```

**Test 3.3: Sample from actual input (line 20)**
```python
Input: "hmo fdayx duciqf cgt duciqf"
Expected: False (invalid)
Reasoning: "duciqf" appears twice (positions 3 and 5)
Note: Pre-verified by manual inspection of input.md
```

**Test 3.4: Sample from actual input (line 46)**
```python
Input: "hnio shccluw cpu ivaby tormn vkef abv vkef ivaby"
Expected: False (invalid)
Reasoning: "vkef" appears at positions 6 and 8, "ivaby" appears at positions 4 and 9
Note: Pre-verified by manual inspection of input.md
```

**Test 3.5: Sample from actual input (line 54)**
```python
Input: "oicgs rrol zvnbna rrol"
Expected: False (invalid)
Reasoning: "rrol" appears twice
Note: Pre-verified by manual inspection of input.md
```

### 4. Full Input Test

**Test 4.1: Count all valid passphrases**
```python
Steps:
1. Run the script on the full input.md file
2. Get the count of valid passphrases
3. Manually verify a sample:
   - Pick 10 random lines
   - Manually check each for duplicates
   - Ensure classification matches script output
```

**Manual verification samples to check:**
- Lines with duplicates (pre-verified):
  - Line 20: "hmo fdayx duciqf cgt duciqf" (duplicate: duciqf)
  - Line 46: "hnio shccluw cpu ivaby tormn vkef abv vkef ivaby" (duplicates: vkef, ivaby)
  - Line 54: "oicgs rrol zvnbna rrol" (duplicate: rrol)
- Lines that appear valid (should verify during testing):
  - Line 1: "bdwdjjo avricm cjbmj ran lmfsom ivsof"
  - Line 2: "mxonybc fndyzzi gmdp gdfyoi inrvhr kpuueel wdpga vkq"

### 5. Unit Test Implementation

```python
import unittest

class TestPassphraseValidation(unittest.TestCase):

    def test_example_valid(self):
        """Test from problem: all unique words"""
        self.assertTrue(is_valid_passphrase("aa bb cc dd ee"))

    def test_example_invalid(self):
        """Test from problem: duplicate word"""
        self.assertFalse(is_valid_passphrase("aa bb cc dd aa"))

    def test_example_similar_words(self):
        """Test from problem: similar but different words"""
        self.assertTrue(is_valid_passphrase("aa bb cc dd aaa"))

    def test_single_word(self):
        """Edge case: single word"""
        self.assertTrue(is_valid_passphrase("word"))

    def test_two_identical(self):
        """Edge case: two identical words"""
        self.assertFalse(is_valid_passphrase("word word"))

    def test_two_different(self):
        """Edge case: two different words"""
        self.assertTrue(is_valid_passphrase("word1 word2"))

    def test_empty(self):
        """Edge case: empty passphrase"""
        self.assertTrue(is_valid_passphrase(""))

    def test_multiple_spaces(self):
        """Edge case: multiple spaces between words"""
        self.assertTrue(is_valid_passphrase("aa  bb   cc"))

    def test_whitespace(self):
        """Edge case: leading/trailing whitespace"""
        self.assertTrue(is_valid_passphrase("  aa bb cc  "))

    def test_triple_duplicate(self):
        """Edge case: word appears three times"""
        self.assertFalse(is_valid_passphrase("aa aa aa"))

    def test_duplicate_at_ends(self):
        """Edge case: duplicate at start and end"""
        self.assertFalse(is_valid_passphrase("aa bb cc aa"))

    def test_input_line_20(self):
        """Real input: line 20 has duplicate 'duciqf'"""
        self.assertFalse(is_valid_passphrase("hmo fdayx duciqf cgt duciqf"))

    def test_input_line_54(self):
        """Real input: line 54 has duplicate 'rrol'"""
        self.assertFalse(is_valid_passphrase("oicgs rrol zvnbna rrol"))

    def test_input_line_1(self):
        """Real input: line 1 is valid"""
        self.assertTrue(is_valid_passphrase("bdwdjjo avricm cjbmj ran lmfsom ivsof"))

if __name__ == '__main__':
    unittest.main()
```

## Verification Procedure

### Step 1: Run Unit Tests
```bash
python -m unittest test_passphrase.py
```
Expected: All tests pass (15/15)

### Step 2: Run on Example Data
Create a test file named `test_examples.txt` with the three examples from the problem:
```
aa bb cc dd ee
aa bb cc dd aa
aa bb cc dd aaa
```
Modify the script temporarily to read from `test_examples.txt` instead of `input.md`, or create a parameterized version.
Expected output: 2 (first and third are valid)

### Step 3: Run on Actual Input
```bash
python solution.py
```
Expected output: A specific integer (will verify during execution)

### Step 4: Manual Spot Checks
Manually verify at least 10 lines from input:
- 5 that should be valid
- 5 that should be invalid
- Confirm script classification matches manual analysis

### Step 5: Boundary Check
Verify the script handles:
- First line correctly
- Last line correctly
- Empty line at end (if exists)

## Success Criteria

✓ All unit tests pass
✓ Example cases produce expected output (2 valid out of 3)
✓ Manual verification of 10 random input lines matches script output
✓ Script produces a single integer output
✓ No runtime errors or exceptions
✓ Execution completes in < 1 second

## Known Limitations (By Design)

1. **No anagram detection**: Part 1 explicitly only checks for exact duplicate words, not anagrams
   - "srceh" and "reshc" are considered different words (correct behavior for Part 1)
   - Anagram detection may be required in Part 2 (future enhancement)

2. **Case sensitivity**: Assumes all input is lowercase (per problem specification)
   - No case normalization needed based on input format

3. **No special character handling**: Assumes words contain only lowercase letters (per spec)
   - No punctuation or number handling needed

## Validation Checklist

- [ ] Problem examples produce correct output
- [ ] Edge cases handled correctly
- [ ] Unit tests all pass
- [ ] Manual verification of sample inputs matches script
- [ ] Full input produces a valid integer output
- [ ] No runtime errors
- [ ] Performance is acceptable (< 1 second)
