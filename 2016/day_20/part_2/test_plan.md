# Testing Plan - Part 2: Count Total Allowed IPs

## Testing Strategy

We need to verify:
1. Correct parsing and merging (already validated in Part 1)
2. Correct counting of blocked IPs from merged ranges
3. Correct subtraction to get allowed IPs
4. Edge cases and boundary conditions

## Test Cases

### Test 1: Example from Problem Statement (Conceptual)
**Note:** This test is for conceptual understanding. The actual implementation uses the full 32-bit IP space (4,294,967,296 IPs).

**Input:**
```
5-8
0-2
4-7
```

**Conceptual Analysis (assuming 10-IP universe 0-9):**
- Merged ranges: [(0, 2), (4, 8)]
- Blocked IPs: 3 (from 0-2) + 5 (from 4-8) = 8 IPs
- Allowed IPs: 3 and 9 (2 total)

**Actual Behavior (32-bit space):**
- Merged ranges: [(0, 2), (4, 8)]
- Blocked IPs: 3 + 5 = 8
- Allowed IPs: 4,294,967,296 - 8 = 4,294,967,288

**Purpose:** Validates basic counting logic with simple example

---

### Test 2: Single Range
**Input:**
```
100-200
```

**Expected Behavior:**
- Merged ranges: [(100, 200)]
- Blocked IPs: 200 - 100 + 1 = 101
- Allowed IPs: 4,294,967,296 - 101 = 4,294,967,195

**Purpose:** Tests simple single-range counting

---

### Test 3: Adjacent Ranges (Merge Required)
**Input:**
```
0-10
11-20
21-30
```

**Expected Behavior:**
- Merged ranges: [(0, 30)] (all adjacent, merged to one)
- Blocked IPs: 30 - 0 + 1 = 31
- Allowed IPs: 4,294,967,296 - 31 = 4,294,967,265

**Purpose:** Validates that adjacent ranges are merged and counted once

---

### Test 4: Overlapping Ranges (No Double-Count)
**Input:**
```
10-20
15-25
18-30
```

**Expected Behavior:**
- Merged ranges: [(10, 30)]
- Blocked IPs: 30 - 10 + 1 = 21
- Allowed IPs: 4,294,967,296 - 21 = 4,294,967,275

**Manual Verification:**
- Without merging: 11 + 11 + 13 = 35 (WRONG - double counts)
- After merging: 21 (CORRECT)

**Purpose:** Critical test to ensure no double-counting of overlapping ranges

---

### Test 5: Multiple Disjoint Ranges
**Input:**
```
0-10
100-200
1000-2000
10000-20000
```

**Expected Behavior:**
- Merged ranges: [(0, 10), (100, 200), (1000, 2000), (10000, 20000)]
- Blocked IPs: 11 + 101 + 1001 + 10001 = 11,114
- Allowed IPs: 4,294,967,296 - 11,114 = 4,294,956,182

**Purpose:** Tests summing multiple non-overlapping ranges

---

### Test 6: Empty Input (No Blocked IPs)
**Input:**
```
(empty file or all blank lines)
```

**Expected Behavior:**
- Merged ranges: []
- Blocked IPs: 0
- Allowed IPs: 4,294,967,296

**Purpose:** Edge case - all IPs allowed

---

### Test 7: Entire Space Blocked
**Input:**
```
0-4294967295
```

**Expected Behavior:**
- Merged ranges: [(0, 4294967295)]
- Blocked IPs: 4,294,967,295 - 0 + 1 = 4,294,967,296
- Allowed IPs: 4,294,967,296 - 4,294,967,296 = 0

**Purpose:** Edge case - no IPs allowed

---

### Test 8: Range at Boundary (0 and MAX)
**Input:**
```
0-0
4294967295-4294967295
```

**Expected Behavior:**
- Merged ranges: [(0, 0), (4294967295, 4294967295)]
- Blocked IPs: 1 + 1 = 2
- Allowed IPs: 4,294,967,296 - 2 = 4,294,967,294

**Purpose:** Tests boundary values (first and last IP)

---

### Test 9: Actual Input File
**Input:** The provided `input.md` with ~946 ranges

**Verification Method:**
1. Run the solution
2. Verify output is a reasonable number (between 0 and 4,294,967,296)
3. Spot-check a few merged ranges manually
4. Verify blocked count calculation for a subset of ranges

**Expected Characteristics:**
- Result should be > 0 (not all IPs blocked)
- Result should be < 4,294,967,296 (some IPs blocked)
- Merged ranges should be significantly fewer than 946 input ranges

---

## Validation Techniques

### Manual Calculation Spot-Check
For a small subset of merged ranges, manually verify:
1. Pick 3-5 merged ranges
2. Calculate blocked IPs: sum of (end - start + 1) for each
3. Verify this matches the partial sum in the code

### Arithmetic Verification
Check formula correctness:
```
blocked_count = Σ(end - start + 1) for all merged ranges
allowed_count = 4,294,967,296 - blocked_count
```

Verify:
- `blocked_count + allowed_count == 4,294,967,296`
- `blocked_count >= 0`
- `allowed_count >= 0`

### Logging for Debug
Add optional debug output via `--debug` flag to verify intermediate steps:
```python
if '--debug' in sys.argv:
    print(f"Total ranges parsed: {len(ranges)}")
    print(f"Merged ranges: {len(merged)}")
    print(f"First merged range: {merged[0] if merged else 'N/A'}")
    print(f"Last merged range: {merged[-1] if merged else 'N/A'}")
    print(f"Total blocked IPs: {blocked_count}")
    print(f"Total allowed IPs: {allowed_count}")
    print(f"Verification: {blocked_count + allowed_count} == 4294967296")
```

### Cross-Reference with Part 1
The Part 1 answer (14975795) tells us:
- The lowest allowed IP is 14,975,795
- This means IPs 0 to 14,975,794 are all blocked
- There must be a merged range covering [0, 14975794]
- This is consistent if the first gap starts at 14975795

**Verification steps:**
1. Run solution with `--debug` flag to see merged ranges
2. Verify first merged range starts at 0 and ends at 14975794 (or extends past it)
3. Verify next merged range starts at 14975796 or later (creating gap at 14975795)

---

## Edge Cases & Boundary Conditions

### 1. Integer Overflow
- **Risk:** Summing large ranges might overflow
- **Mitigation:** Python handles arbitrary precision integers automatically
- **Verification:** Test with multiple large ranges

### 2. Off-by-One Errors
- **Risk:** Incorrect counting (e.g., using `end - start` instead of `end - start + 1`)
- **Mitigation:** Use inclusive counting formula
- **Test:** Ranges like [5, 5] should count as 1, not 0

### 3. Unsorted Input
- **Risk:** Input ranges not in order
- **Mitigation:** `merge_ranges()` sorts before merging
- **Test:** Provide input with ranges out of order

### 4. Duplicate Ranges
- **Risk:** Same range listed multiple times
- **Mitigation:** Merging eliminates duplicates
- **Test:** Input with identical ranges

---

## Testing Execution Plan

### Phase 1: Unit Tests
1. Test `count_allowed_ips()` with known merged ranges
2. Verify arithmetic: blocked + allowed = 4,294,967,296
3. Test edge cases (empty, full coverage)

### Phase 2: Integration Tests
1. Run examples from problem statement
2. Test with custom small inputs
3. Verify against manual calculations

### Phase 3: Actual Input
1. Run on provided `input.md`
2. Verify output is reasonable
3. Add debug logging to inspect intermediate values
4. Cross-check with Part 1 answer

### Phase 4: Validation
1. Verify no integer overflow
2. Check blocked + allowed = total IP space
3. Ensure result is within valid range [0, 4,294,967,296]

---

## Success Criteria

The solution is correct if:
1. ✓ All test cases pass with expected outputs
2. ✓ Blocked + Allowed = 4,294,967,296 for all inputs
3. ✓ Works correctly with overlapping ranges (no double-count)
4. ✓ Works correctly with adjacent ranges (proper merge)
5. ✓ Handles edge cases (empty, full, boundaries)
6. ✓ Produces reasonable output for actual input file
7. ✓ First merged range is consistent with Part 1 answer (includes 0 to ~14,975,794)

---

## Debugging Strategy

If the answer is incorrect:

1. **Add debug prints:**
   - Number of input ranges
   - Number of merged ranges
   - First few merged ranges
   - Total blocked count
   - Total allowed count
   - Sum verification

2. **Check merge logic:**
   - Print merged ranges
   - Manually verify a few merges
   - Look for gaps or overlaps

3. **Verify counting:**
   - Manually calculate blocked IPs for first 5 merged ranges
   - Compare with code output

4. **Test with simple input:**
   - Use example from problem statement
   - Verify each step manually
