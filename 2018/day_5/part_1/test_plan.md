# Testing Plan: Polymer Reaction Simulation

## Updates from Critique

This plan has been updated to address the following key points from the critique:

1. **Verified Complex Test Case**: Added detailed step-by-step walkthrough for `dabAcCaCBAcCcaDA` example with algorithm verification
2. **Input Parsing Test**: Added Test 4.2 to verify `input.md` is parsed correctly (filters whitespace, markdown, etc.)
3. **Enhanced Performance Testing**: Improved Test 3.2 to test 50K character input where all units react (worst case)
4. **Answer Verification**: Added recommendation to submit answer to Advent of Code for final verification
5. **Updated Test Function**: Modified `react_polymer()` calls to use `return_polymer=True` parameter for verification
6. **Better Test Runner**: Enhanced manual test implementation to show final polymer on failures for debugging
7. **Expanded Checklist**: Added verification items for input parsing and both performance scenarios

## Testing Objectives

1. Verify correct implementation of reaction rules
2. Validate handling of edge cases
3. Ensure algorithm efficiency with large inputs
4. Confirm output correctness for the actual problem input

## Test Categories

### 1. Unit Tests - Reaction Logic

#### Test 1.1: Basic Reaction Check Function
**Purpose**: Verify the `reacts()` helper function correctly identifies reactive pairs

**Test Cases**:
| Input | Expected | Reason |
|-------|----------|--------|
| ('a', 'A') | True | Same letter, opposite case |
| ('A', 'a') | True | Same letter, opposite case (reversed) |
| ('b', 'B') | True | Same letter, opposite case |
| ('a', 'a') | False | Same letter, same case |
| ('A', 'A') | False | Same letter, same case |
| ('a', 'b') | False | Different letters, same case |
| ('a', 'B') | False | Different letters, different case |
| ('Z', 'z') | True | Same letter, opposite case |

**Verification Method**:
```python
def test_reacts():
    assert reacts('a', 'A') == True
    assert reacts('A', 'a') == True
    assert reacts('a', 'a') == False
    assert reacts('A', 'A') == False
    assert reacts('a', 'b') == False
    assert reacts('a', 'B') == False
    # Add all test cases
```

### 2. Integration Tests - Full Polymer Reactions

#### Test 2.1: Example Cases from Problem Statement

**Test Case 2.1.1**: Simple single reaction
- **Input**: `"aA"`
- **Expected Output**: `0`
- **Reasoning**: Both units react and destroy each other

**Test Case 2.1.2**: Chain reaction
- **Input**: `"abBA"`
- **Expected Output**: `0`
- **Reasoning**:
  - `bB` reacts → `"aA"`
  - `aA` reacts → `""`

**Test Case 2.1.3**: No reactions possible
- **Input**: `"abAB"`
- **Expected Output**: `4`
- **Reasoning**: No adjacent pairs have same letter

**Test Case 2.1.4**: Same polarity units
- **Input**: `"aabAAB"`
- **Expected Output**: `6`
- **Reasoning**: All adjacent same-letter pairs have same polarity

**Test Case 2.1.5**: Complex reduction
- **Input**: `"dabAcCaCBAcCcaDA"`
- **Expected Output**: `10`
- **Reasoning**: Multiple cascading reactions
- **Final State**: `"dabCBAcaDA"`
- **Correct step-by-step walkthrough**:
  1. 'd': [d]
  2. 'a': [d, a]
  3. 'b': [d, a, b]
  4. 'A': [d, a, b, A]
  5. 'c': [d, a, b, A, c]
  6. 'C': cC react! → [d, a, b, A]
  7. 'a': Aa react! → [d, a, b]
  8. 'C': [d, a, b, C] (C and b don't react - different letters)
  9. 'B': [d, a, b, C, B] (B and C don't react - different letters)
  10. 'A': [d, a, b, C, B, A] (A and B don't react - different letters)
  11. 'c': [d, a, b, C, B, A, c] (c and A don't react)
  12. 'C': cC react! → [d, a, b, C, B, A]
  13. 'c': [d, a, b, C, B, A, c] (c and A don't react)
  14. 'a': [d, a, b, C, B, A, c, a] (a and c don't react)
  15. 'D': [d, a, b, C, B, A, c, a, D]
  16. 'A': [d, a, b, C, B, A, c, a, D, A] (A and D don't react)
  - **Final**: `"dabCBAcaDA"` (length 10) ✓

#### Test 2.2: Edge Cases

**Test Case 2.2.1**: Empty string
- **Input**: `""`
- **Expected Output**: `0`
- **Reasoning**: No polymer to process

**Test Case 2.2.2**: Single character
- **Input**: `"a"`
- **Expected Output**: `1`
- **Reasoning**: Nothing to react with

**Test Case 2.2.3**: Two characters, same case
- **Input**: `"aa"`
- **Expected Output**: `2`
- **Reasoning**: Same polarity, no reaction

**Test Case 2.2.4**: All units react (long chain)
- **Input**: `"aAaAaA"`
- **Expected Output**: `0`
- **Reasoning**: All pairs react sequentially

**Test Case 2.2.5**: All units react (reversed)
- **Input**: `"AaAaAa"`
- **Expected Output**: `0`
- **Reasoning**: All pairs react sequentially

**Test Case 2.2.6**: Alternating non-reactive
- **Input**: `"aAbBcC"`
- **Expected Output**: `0`
- **Reasoning**: Each adjacent pair reacts

**Test Case 2.2.7**: Complete cascading reaction
- **Input**: `"abcCBA"`
- **Expected Output**: `0`
- **Reasoning**:
  - `cC` reacts → `"abBA"`
  - `bB` reacts → `"aA"`
  - `aA` reacts → `""`

**Test Case 2.2.8**: Partial cascading
- **Input**: `"xabBAy"`
- **Expected Output**: `2`
- **Reasoning**: Middle reacts, ends remain
- **Final State**: `"xy"`

**Test Case 2.2.9**: No reactions at all
- **Input**: `"aBcDeFg"`
- **Expected Output**: `7`
- **Reasoning**: No adjacent same letters

**Test Case 2.2.10**: Multiple separate reactions
- **Input**: `"aAbBcCdD"`
- **Expected Output**: `0`
- **Reasoning**: All pairs react independently then cascadingly

### 3. Performance Tests

#### Test 3.1: Large Input Performance
**Purpose**: Ensure algorithm handles 50,000 character input efficiently

**Test Approach**:
```python
import time

def test_performance():
    # Generate large test case
    large_polymer = "ab" * 25000  # 50,000 characters, no reactions

    start_time = time.time()
    result = react_polymer(large_polymer)
    end_time = time.time()

    elapsed = end_time - start_time
    assert elapsed < 1.0  # Should complete in under 1 second
    assert result == 50000  # All units remain
```

#### Test 3.2: Worst Case Cascading at Scale
**Purpose**: Test maximum stack operations with large input where all units react

**Test Approach**:
```python
def test_worst_case_cascading():
    # Create 50K character polymer where all units eventually react
    # Pattern: build alphabet forward then backward repeatedly
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    # Each cycle is 52 chars (26 + 26), need ~961 cycles for 50K
    pattern = alphabet + alphabet.upper()[::-1]
    cycles = 50000 // len(pattern)
    polymer = pattern * cycles

    import time
    start_time = time.time()
    result = react_polymer(polymer)
    end_time = time.time()

    elapsed = end_time - start_time
    assert elapsed < 2.0  # Should complete in under 2 seconds
    assert result == 0  # All should react
```

### 4. Actual Problem Input Test

#### Test 4.1: Full Input Validation
**Purpose**: Verify solution works on actual problem input

**Test Approach**:
1. Run solution on `input.md`
2. Capture output
3. Verify output is a reasonable integer (likely in range 0-50000)
4. Check execution time is acceptable (<2 seconds)

**Manual Verification**:
- Run the solution and note the output
- Spot-check a small portion of input manually if needed
- Verify the output makes logical sense (should be significantly less than 50,000 due to reactions)
- If this is an Advent of Code problem, submit the answer to verify correctness

#### Test 4.2: Input Parsing Validation
**Purpose**: Verify `input.md` is parsed correctly

**Test Approach**:
```python
def test_input_parsing():
    # Test that input file is read and parsed correctly
    polymer = read_input('input.md')

    # Verify all characters are alphabetic
    assert all(c.isalpha() for c in polymer), "Input contains non-alphabetic characters"

    # Verify no whitespace
    assert ' ' not in polymer, "Input contains spaces"
    assert '\n' not in polymer, "Input contains newlines"
    assert '\t' not in polymer, "Input contains tabs"

    # Verify reasonable length (around 50,000)
    assert 40000 < len(polymer) < 60000, f"Input length {len(polymer)} unexpected"

    print(f"Input parsed successfully: {len(polymer)} characters")
```

### 5. Algorithm Correctness Tests

#### Test 5.1: Stack State Verification
**Purpose**: Ensure stack correctly maintains non-reactive polymer

**Test Approach**:
- Use `react_polymer` with `return_polymer=True` to get final polymer state
- Verify no adjacent characters in final polymer react
- Verify all characters in final polymer are from original input

**Example**:
```python
def verify_no_reactions(polymer_input):
    """Verify final polymer has no reactive adjacent pairs"""
    length, polymer_result = react_polymer(polymer_input, return_polymer=True)

    # Check length matches
    assert len(polymer_result) == length

    # Verify no adjacent pairs react
    for i in range(len(polymer_result) - 1):
        assert not reacts(polymer_result[i], polymer_result[i+1]), \
            f"Found reactive pair at positions {i},{i+1}: {polymer_result[i]}{polymer_result[i+1]}"

    # Verify all characters are from original input
    for char in polymer_result:
        assert char in polymer_input, f"Character {char} not in original input"
```

#### Test 5.2: Order Preservation
**Purpose**: Verify that non-reacting units maintain their order

**Test Case**:
- **Input**: `"aBbCcDdEeFfG"`
- **Process**: All pairs react except `a` and `G`
- **Expected**: Final polymer is `"aG"` (not `"Ga"`)
- **Verification**: Order is preserved
- **Step-by-step walkthrough**:
  1. 'a': [a]
  2. 'B': [a, B]
  3. 'b': Bb react! [a]
  4. 'C': [a, C]
  5. 'c': Cc react! [a]
  6. 'D': [a, D]
  7. 'd': Dd react! [a]
  8. 'E': [a, E]
  9. 'e': Ee react! [a]
  10. 'F': [a, F]
  11. 'f': Ff react! [a]
  12. 'G': [a, G]
  13. Final: "aG" (length 2) ✓

### 6. Boundary Condition Tests

#### Test 6.1: All Uppercase
- **Input**: `"ABCDEF"`
- **Expected**: `6` (no reactions)

#### Test 6.2: All Lowercase
- **Input**: `"abcdef"`
- **Expected**: `6` (no reactions)

#### Test 6.3: Alternating Case, Different Letters
- **Input**: `"aBcDeFg"`
- **Expected**: `7` (no reactions)

#### Test 6.4: Maximum Reaction Depth
- **Input**: Deeply nested like `"aXbYcZzCyBxA"`
- **Expected**: Verify cascading reactions work through multiple levels

## Test Execution Plan

### Phase 1: Unit Tests
1. Test `reacts()` function with all character combinations
2. Verify reaction logic is correct
3. **Success Criteria**: All reaction check tests pass

### Phase 2: Simple Integration Tests
1. Run all example cases from problem statement
2. Verify outputs match expected values
3. **Success Criteria**: All example cases produce correct output

### Phase 3: Edge Case Tests
1. Test empty string, single character, and other edge cases
2. Verify graceful handling
3. **Success Criteria**: All edge cases handled correctly

### Phase 4: Complex Cases
1. Test cascading reactions
2. Test partial reactions
3. Verify final polymer has no reactive pairs
4. **Success Criteria**: Complex scenarios produce correct output

### Phase 5: Performance Tests
1. Test with large generated inputs
2. Measure execution time
3. **Success Criteria**: Completes in <1 second for 50,000 characters

### Phase 6: Actual Input
1. Test input parsing (Test 4.2)
2. Run on actual `input.md` (Test 4.1)
3. Verify output is reasonable
4. Check performance
5. Submit answer (if Advent of Code) to verify correctness
6. **Success Criteria**: Produces integer output in reasonable time and answer is verified correct

## Test Implementation Strategy

### Option 1: Quick Manual Testing (Recommended)
Create a simple test script with example cases:

```python
def run_tests():
    """Run all test cases and report results."""
    test_cases = [
        ("aA", 0, "Simple single reaction"),
        ("abBA", 0, "Chain reaction"),
        ("abAB", 4, "No reactions possible"),
        ("aabAAB", 6, "Same polarity units"),
        ("dabAcCaCBAcCcaDA", 10, "Complex reduction"),
        ("", 0, "Empty string"),
        ("a", 1, "Single character"),
        ("aAaAaA", 0, "All units react"),
        ("aAbBcC", 0, "Alternating reactions"),
        ("aBbCcDdEeFfG", 2, "Order preservation"),
        ("abcCBA", 0, "Complete cascading"),
        ("xabBAy", 2, "Partial cascading"),
        ("aBcDeFg", 7, "No reactions at all"),
    ]

    passed = 0
    failed = 0

    for polymer, expected, description in test_cases:
        result = react_polymer(polymer)
        if result == expected:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1
        print(f"{status}: {description}")
        print(f"  Input: '{polymer}' -> Output: {result} (expected {expected})")
        if result != expected:
            # Show final polymer for debugging
            _, final = react_polymer(polymer, return_polymer=True)
            print(f"  Final polymer: '{final}'")
        print()

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0
```

### Option 2: Pytest Framework (More formal)
Use pytest for structured testing, but this may be overkill for a one-off script.

## Verification Checklist

- [ ] Reaction function correctly identifies reactive pairs
- [ ] All problem statement examples produce correct output
- [ ] Edge cases (empty, single char) handled correctly
- [ ] Cascading reactions work properly
- [ ] Order of non-reactive units is preserved
- [ ] Final polymer contains no reactive adjacent pairs
- [ ] Input parsing handles markdown formatting and whitespace correctly
- [ ] Input contains only alphabetic characters after parsing
- [ ] Performance is acceptable for 50,000 character input (all react scenario)
- [ ] Performance is acceptable for 50,000 character input (no react scenario)
- [ ] Actual problem input produces reasonable output
- [ ] Output format is correct (single integer)
- [ ] Answer verified correct (if submittable to Advent of Code)

## Expected Output Characteristics

For the actual 50,000 character input:
- Output should be an integer
- Should be between 0 and 50,000
- Likely significantly less than 50,000 (reactions will occur)
- Execution should complete in under 2 seconds

## Debugging Strategy

If tests fail:
1. **Reaction logic wrong**: Check `reacts()` function logic
2. **Wrong order**: Verify stack operations (push/pop)
3. **Missing reactions**: Check if all pairs are being considered
4. **Performance issues**: Verify using stack (O(n)) not repeated string operations
5. **Wrong output**: Add debug prints to trace stack state

## Success Criteria

The solution is correct if:
1. All test cases from problem statement pass
2. Edge cases are handled properly
3. Performance is O(n) and completes quickly
4. Actual input produces a valid integer result
5. Final polymer (if returned) contains no adjacent reactive pairs
