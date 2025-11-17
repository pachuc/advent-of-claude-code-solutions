# Testing Plan: IPv7 TLS Support Detection

## Testing Strategy Overview

### Goals:
1. Verify ABBA pattern detection correctness
2. Validate address parsing (supernet/hypernet separation)
3. Confirm TLS support logic
4. Test edge cases and boundary conditions
5. Validate against expected output

### Testing Approach:
- Unit tests for individual functions
- Integration tests for complete addresses
- Validation with provided examples
- Edge case verification
- Full input validation

### Key Assumptions (Based on Problem):
- Input addresses are well-formed (brackets are properly matched)
- Addresses contain lowercase alphabetic characters (based on problem examples)
- Empty sequences should be filtered out during parsing

## Unit Tests

### Test 1: ABBA Detection Function (`has_abba()`)

#### Test 1.1: Valid ABBA Patterns
**Purpose**: Verify function correctly identifies valid ABBAs

**Test cases**:
```python
# Basic valid ABBAs
assert has_abba("abba") == True      # Simple ABBA
assert has_abba("xyyx") == True      # Different chars
assert has_abba("oxxo") == True      # Another valid pattern

# ABBAs within longer strings
assert has_abba("ioxxoj") == True    # ABBA in middle: "oxxo"
assert has_abba("zabbaz") == True    # ABBA in middle: "abba"
assert has_abba("xabba") == True     # ABBA after first char
assert has_abba("abbax") == True     # ABBA before last char

# Different character ABBAs
assert has_abba("deed") == True      # d-e-e-d
assert has_abba("qppq") == True      # q-p-p-q
```

#### Test 1.2: Invalid ABBA Patterns
**Purpose**: Verify function correctly rejects invalid patterns

**Test cases**:
```python
# All same character (not valid ABBA)
assert has_abba("aaaa") == False     # Must have 2 different chars
assert has_abba("zzzz") == False

# No ABBA pattern at all
assert has_abba("abcd") == False     # No palindrome
assert has_abba("abcdef") == False   # No ABBA in sequence
assert has_abba("abc") == False      # Too short

# Empty or minimal strings
assert has_abba("") == False         # Empty string
assert has_abba("a") == False        # Single char
assert has_abba("ab") == False       # Two chars
assert has_abba("abc") == False      # Three chars
```

#### Test 1.3: Overlapping Patterns
**Purpose**: Verify sliding window correctly finds ABBAs in overlapping scenarios

**Test cases**:
```python
assert has_abba("abbba") == True     # Contains "abba" at positions 0-3
assert has_abba("baabab") == True    # Contains "baab" at start
assert has_abba("cabbabc") == True   # Multiple potential windows, "abba" at positions 1-4
assert has_abba("ioxxoj") == True    # "oxxo" at positions 1-4
```

### Test 2: Address Parsing Function (`parse_address()`)

#### Test 2.1: Basic Parsing
**Purpose**: Verify correct separation of supernet and hypernet sequences

**Test cases**:
```python
# Single bracket pair
supernets, hypernets = parse_address("abcd[efgh]ijkl")
assert supernets == ["abcd", "ijkl"]
assert hypernets == ["efgh"]

# Multiple bracket pairs
supernets, hypernets = parse_address("abc[def]ghi[jkl]mno")
assert supernets == ["abc", "ghi", "mno"]
assert hypernets == ["def", "jkl"]

# No brackets (all supernet)
supernets, hypernets = parse_address("abcdefgh")
assert supernets == ["abcdefgh"]
assert hypernets == []

# Many consecutive bracket pairs
supernets, hypernets = parse_address("[a][b][c]xyyx[d][e]")
assert hypernets == ["a", "b", "c", "d", "e"]
assert "xyyx" in supernets  # ABBA in supernet sequence
```

#### Test 2.2: Edge Cases in Parsing
**Purpose**: Test boundary conditions and unusual formats

**Test cases**:
```python
# Starting with bracket (filter empty sequences)
supernets, hypernets = parse_address("[abc]def")
assert supernets == ["def"]  # Empty sequences filtered out
assert hypernets == ["abc"]

# Ending with bracket (filter empty sequences)
supernets, hypernets = parse_address("abc[def]")
assert supernets == ["abc"]  # Empty sequences filtered out
assert hypernets == ["def"]

# Empty sequences (filter empty sequences)
supernets, hypernets = parse_address("[]abc")
assert hypernets == []  # Empty string filtered out
assert supernets == ["abc"]

# Consecutive brackets
supernets, hypernets = parse_address("[abc][def]")
assert hypernets == ["abc", "def"]
assert supernets == []  # No supernet sequences (after filtering)

# Note: Implementation should filter out empty sequences for cleaner processing
```

### Test 3: TLS Support Function (`supports_tls()`)

#### Test 3.1: Provided Examples
**Purpose**: Verify against problem statement examples

**Test cases**:
```python
# Example 1: Supports TLS (ABBA outside, none inside)
assert supports_tls("abba[mnop]qrst") == True

# Example 2: Does NOT support (ABBA inside brackets)
assert supports_tls("abcd[bddb]xyyx") == False

# Example 3: Does NOT support (no valid ABBA)
assert supports_tls("aaaa[qwer]tyui") == False

# Example 4: Supports TLS (ABBA in middle of supernet)
assert supports_tls("ioxxoj[asdfgh]zxcvbn") == True
```

#### Test 3.2: TLS Logic Edge Cases
**Purpose**: Test specific TLS rule scenarios

**Test cases**:
```python
# ABBA only in hypernet (should fail)
assert supports_tls("abcd[xyyx]efgh") == False

# ABBA only in supernet (should pass)
assert supports_tls("abba[mnop]qrst") == True

# ABBA in both (should fail due to hypernet)
assert supports_tls("abba[xyyx]qrst") == False

# Multiple ABBAs in supernet, none in hypernet (should pass)
assert supports_tls("abba[mnop]xyyx") == True

# Multiple hypernets, one has ABBA (should fail)
assert supports_tls("test[good][xyyx]nice") == False

# No ABBA anywhere (should fail)
assert supports_tls("abcd[efgh]ijkl") == False

# Multiple supernets, ABBA in different positions (should pass)
assert supports_tls("test[good]xyyx[okay]normal") == True  # ABBA in second supernet
assert supports_tls("baab[safe]normal[okay]test") == True  # ABBA in first supernet
```

## Integration Tests

### Test 4: End-to-End Validation

#### Test 4.1: Small Input Set
**Purpose**: Verify complete processing pipeline

**Test case**:
```python
# Create test input file with known addresses
test_input = """
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""

# Expected: 2 addresses support TLS (lines 1 and 4)
# Run main() on test input
# Assert count == 2
```

#### Test 4.2: Edge Case Addresses
**Purpose**: Test unusual but valid address formats

**Test cases**:
```python
# Very long address
long_addr = "a" * 500 + "[" + "b" * 500 + "]" + "xyyx"
assert supports_tls(long_addr) == True

# Many bracket pairs
many_brackets = "[a][b][c][d]xyyx[e][f]"
# Verify correct parsing and TLS check

# Minimal valid address with TLS
assert supports_tls("abba") == True
```

## Edge Cases and Boundary Conditions

### Edge Case 1: Empty and Minimal Inputs
- Empty string: Should not crash, return False
- Single character: No ABBA possible, return False
- Three characters: Too short for ABBA, return False

### Edge Case 2: Special Character Patterns
- All same character: "aaaaaaa" - no valid ABBA
- Alternating pattern: "ababab" - no ABBA
- Near-ABBA: "abbc" - not quite an ABBA

### Edge Case 3: Bracket Edge Cases
- Empty brackets: "abc[]def"
- Nested brackets: Not mentioned in problem, assume invalid format
- Unmatched brackets: Not mentioned, assume well-formed input

### Edge Case 4: ABBA Position Variations
- ABBA at very start: "abbaxyz"
- ABBA at very end: "xyzabba"
- Multiple non-overlapping ABBAs: "abba xyyx"
- Overlapping ABBA candidates: "abbba" (contains "abba")

## Validation Strategy

### Phase 1: Unit Test Validation
1. Test `has_abba()` with 15-20 test cases
2. Test `parse_address()` with 10-15 test cases
3. Test `supports_tls()` with problem examples + 10 additional cases
4. **Success criteria**: All unit tests pass

### Phase 2: Integration Testing
1. Create small test input file (10-20 addresses)
2. Manually calculate expected TLS count
3. Run solution and compare output
4. **Success criteria**: Counts match

### Phase 3: Example Validation
1. Test all 4 examples from problem statement individually
2. Verify each returns expected result
3. **Success criteria**: 100% match with examples

### Phase 4: Full Input Validation
1. Run solution on full input.md (2000 addresses)
2. Verify output is a reasonable integer (likely 50-500 range)
3. Spot-check random addresses from input for correctness
4. **Success criteria**: Solution completes in <1 second, produces integer output

### Phase 5: Manual Verification (Sample)
1. Select 10-20 random addresses from input
2. Manually determine if they support TLS
3. Compare with function output
4. **Success criteria**: 100% agreement

## Test Execution Order

1. **has_abba() tests** - Foundation function
2. **parse_address() tests** - Build on string processing
3. **supports_tls() tests** - Combines both functions
4. **Provided examples** - Validate against problem statement
5. **Integration tests** - Full pipeline verification
6. **Edge cases** - Boundary condition verification
7. **Full input run** - Final validation

## Debugging Strategies

### If ABBA detection fails:
- Print each 4-char window being checked
- Verify character comparison logic
- Check for off-by-one errors in loop bounds

### If parsing fails:
- Print supernet and hypernet lists for each address
- Verify bracket state tracking
- Check for empty sequence handling

### If TLS check fails:
- Print which sequences contain ABBAs
- Verify fail-fast logic for hypernets
- Check boolean logic flow

### If count is wrong:
- Add verbose mode to print each address + TLS result
- Compare subset of results with manual calculation
- Check for off-by-one in counting or file reading

## Success Criteria

### Must Pass:
✓ All 4 provided examples return correct results
✓ Unit tests have >95% pass rate
✓ Solution runs in <1 second on full input
✓ Output is a single integer
✓ Manual verification of 10 random addresses matches output

### Quality Indicators:
✓ No crashes or exceptions on full input
✓ Code handles edge cases gracefully
✓ Clear separation between supernet/hypernet checking
✓ Efficient algorithm (no unnecessary iterations)

## Test Implementation Notes

- Tests can be implemented as simple assert statements
- For quick validation, use print statements to verify logic
- Focus on correctness over test framework sophistication
- Prioritize testing the examples first - they're the ground truth
