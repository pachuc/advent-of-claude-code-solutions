# Test Plan: Part 2 - Room Name Decryption

## Updates from Critique (Version 2)

This plan has been updated based on feedback to address the following improvements:

1. **Modulo 26 Boundary Tests**: Added Test 1.2b to verify behavior at sector_id = 25 and 27
2. **More Precise Search Testing**: Updated Test 3.4 to test the precise search logic (`"north pole" or "northpole"`) and verify it doesn't match false positives like "northeastern polynomial"
3. **Better Manual Verification Code**: Fixed Test 4.3 with concrete, runnable code instead of pseudo-code
4. **Comprehensive Validation Function**: Updated validation function to include all critical test cases
5. **Clarified Part 1 Assumptions**: Added note that Part 1 functions are assumed to be already validated

## Testing Objectives
1. Verify Caesar cipher decryption correctness
2. Confirm integration with Part 1's validation logic
3. Validate search logic finds the correct room
4. Test edge cases in decryption algorithm
5. Ensure solution returns correct answer

## Test Categories

### 1. Unit Tests for Decryption Function

#### Test 1.1: Example Verification (Given in Problem)
**Purpose:** Validate decryption matches the provided example

**Input:**
- encrypted_name: `"qzmt-zixmtkozy-ivhz"`
- sector_id: `343`

**Expected Output:**
- `"very encrypted name"`

**Verification Steps:**
1. Call `decrypt_room_name("qzmt-zixmtkozy-ivhz", 343)`
2. Calculate shift: 343 % 26 = 5
3. Manually verify first few characters:
   - 'q' (index 16) + 5 = 21 → 'v' ✓
   - 'z' (index 25) + 5 = 30 % 26 = 4 → 'e' ✓
   - 'm' (index 12) + 5 = 17 → 'r' ✓
   - 't' (index 19) + 5 = 24 → 'y' ✓
4. Verify dashes become spaces
5. Assert full string matches

**Pass Criteria:** Output exactly matches `"very encrypted name"`

#### Test 1.2: Zero Shift (Edge Case)
**Purpose:** Verify sector_id = 0 or multiples of 26 don't change letters

**Test Cases:**
- `decrypt_room_name("abc-xyz", 0)` → `"abc xyz"`
- `decrypt_room_name("abc-xyz", 26)` → `"abc xyz"`
- `decrypt_room_name("abc-xyz", 52)` → `"abc xyz"`

**Pass Criteria:** Letters unchanged, dashes become spaces

#### Test 1.2b: Modulo 26 Boundary Cases (New)
**Purpose:** Verify the modulo 26 boundary is handled correctly

**Test Cases:**
- `decrypt_room_name("abc", 25)` → `"zab"`
  - 'a' (0) + 25 = 25 → 'z'
  - 'b' (1) + 25 = 26 % 26 = 0 → 'a'
  - 'c' (2) + 25 = 27 % 26 = 1 → 'b'
- `decrypt_room_name("abc", 27)` → `"bcd"`
  - 27 % 26 = 1, so same as shift by 1

**Pass Criteria:** Boundary cases at 25 and 27 work correctly

#### Test 1.3: Full Alphabet Rotation (Shift = 1)
**Purpose:** Verify basic shift and wraparound

**Input:**
- `decrypt_room_name("zabc", 1)` → `"abcd"`
- `decrypt_room_name("xyz", 3)` → `"abc"`

**Pass Criteria:** Correct wraparound from z to a

#### Test 1.4: Large Sector IDs
**Purpose:** Verify modulo 26 optimization works

**Test Cases:**
- `decrypt_room_name("abc", 1000)` → same as shift = 1000 % 26 = 12
  - 'a' + 12 = 'm'
  - 'b' + 12 = 'n'
  - 'c' + 12 = 'o'
  - Expected: `"mno"`

**Pass Criteria:** Large IDs handled correctly via modulo

#### Test 1.5: Only Dashes
**Purpose:** Verify dash-only strings work

**Input:**
- `decrypt_room_name("---", 10)` → `"   "` (three spaces)

**Pass Criteria:** All dashes converted to spaces

#### Test 1.6: Single Character
**Purpose:** Verify minimal input

**Input:**
- `decrypt_room_name("a", 1)` → `"b"`
- `decrypt_room_name("z", 1)` → `"a"`

**Pass Criteria:** Single character shifts correctly

### 2. Integration Tests with Part 1 Logic

#### Test 2.1: Validate Part 1 Functions Still Work
**Purpose:** Ensure copied code functions correctly

**Test Cases from Part 1:**
1. `parse_room_entry("aaaaa-bbb-z-y-x-123[abxyz]")`
   - Should return: `("aaaaa-bbb-z-y-x", 123, "abxyz")`

2. `generate_expected_checksum("aaaaa-bbb-z-y-x")`
   - Should return: `"abxyz"`

3. `is_real_room("aaaaa-bbb-z-y-x", "abxyz")`
   - Should return: `True`

4. `is_real_room("totally-real-room", "decoy")`
   - Should return: `False`

**Pass Criteria:** All Part 1 logic works identically

#### Test 2.2: End-to-End Flow for Decoy Room
**Purpose:** Verify decoy rooms are NOT decrypted

**Input:** `"totally-real-room-200[decoy]"`

**Expected Behavior:**
1. Parse successfully
2. Validation fails (checksum doesn't match)
3. Room is skipped, NOT decrypted
4. Does not contribute to search

**Pass Criteria:** Decoy rooms ignored in search

#### Test 2.3: End-to-End Flow for Real Room
**Purpose:** Verify real rooms are decrypted

**Input:** `"aaaaa-bbb-z-y-x-123[abxyz]"`

**Expected Behavior:**
1. Parse successfully
2. Validation passes
3. Room name gets decrypted with sector_id = 123
4. Shift = 123 % 26 = 19
5. Result searchable

**Pass Criteria:** Real rooms processed correctly

### 3. Search Logic Tests

#### Test 3.1: Exact Match "north pole"
**Purpose:** Verify detection of "north pole" as separate words

**Mock Data:**
- Decrypted name: `"north pole objects"`
- Should match: Both "north" and "pole" present

**Pass Criteria:** Returns True/matches

#### Test 3.2: Compound "northpole"
**Purpose:** Verify detection of compound form

**Mock Data:**
- Decrypted name: `"northpole storage"`
- Should match: Contains "north" and "pole" as substring

**Note:** Our search uses `"north" in name and "pole" in name`, so this works for both formats

**Pass Criteria:** Returns True/matches

#### Test 3.3: Case Sensitivity (Should Not Be Issue)
**Purpose:** Verify lowercase search works

**Mock Data:**
- All input is lowercase (per problem spec)
- Decrypted output is lowercase
- Search terms are lowercase

**Pass Criteria:** No case sensitivity issues

#### Test 3.4: Partial Matches Don't False Positive
**Purpose:** Ensure we don't match unrelated rooms

**Mock Data:**
- `"northern alliance"` - has "north" but not "pole" → NO MATCH
- `"pole vault"` - has "pole" but not "north" → NO MATCH
- `"northeastern polynomial"` - has "north" and "pole" as substrings but not the phrase → NO MATCH
- `"north pole objects"` - exact phrase match → MATCH
- `"northpole storage"` - compound form → MATCH

**Search Implementation:** Use `"north pole" in name or "northpole" in name` for precise matching

**Pass Criteria:** Only true matches accepted (rooms with "north pole" or "northpole" as complete phrases)

#### Test 3.5: Multiple Rooms (Only Return First)
**Purpose:** Verify we return first match (though problem implies only one exists)

**Expected Behavior:**
- If multiple rooms contain "north pole", return first found
- Function returns single integer, not list

**Pass Criteria:** Returns single sector ID

### 4. Full Solution Tests

#### Test 4.1: Validation Function Passes
**Purpose:** Ensure validation code runs successfully

**Steps:**
1. Run `validate_solution()`
2. Should test example: `qzmt-zixmtkozy-ivhz-343` → `very encrypted name`
3. Should print success message
4. Should not raise any assertions

**Pass Criteria:** Validation completes without errors

#### Test 4.2: Solution Runs on Full Input
**Purpose:** Verify solution processes all 947 rooms

**Steps:**
1. Run `solve('input.md')`
2. Should process all lines
3. Should find exactly one match
4. Should return an integer sector ID

**Pass Criteria:**
- Returns an integer (not None, not list)
- Completes in under 1 second
- No errors or exceptions

#### Test 4.3: Manual Verification of Result
**Purpose:** Spot-check the answer makes sense

**Steps:**
1. Run solution, get sector ID (e.g., `result = 548`)
2. Find that room in input file
3. Manually verify:
   - Room is real (checksum valid)
   - Decrypted name contains "north pole" or "northpole"
   - Sector ID matches returned value

**Example Manual Check:**
```python
# If solution returns a sector_id, verify it manually:
result = solve('input.md')
print(f"Solution returned sector ID: {result}")

# Find and verify the room
with open('input.md', 'r') as f:
    for line in f:
        line = line.strip()
        if line:
            parsed = parse_room_entry(line)
            if parsed:
                encrypted_name, sector_id, checksum = parsed
                if sector_id == result:
                    # Verify this is a real room
                    assert is_real_room(encrypted_name, checksum), "Room must be real"

                    # Decrypt and display
                    decrypted = decrypt_room_name(encrypted_name, sector_id)
                    print(f"Encrypted: {encrypted_name}")
                    print(f"Decrypted: {decrypted}")

                    # Verify it contains "north pole"
                    assert "north pole" in decrypted or "northpole" in decrypted, \
                        f"Decrypted name must contain 'north pole': {decrypted}"

                    print("Manual verification PASSED!")
                    break
```

**Pass Criteria:** Manual verification confirms answer

### 5. Edge Case Tests

#### Test 5.1: Empty Input
**Purpose:** Verify graceful handling (though not expected)

**Input:** Empty file or no valid rooms

**Expected:** Return None or handle gracefully

**Note:** Not critical since problem guarantees valid input

#### Test 5.2: Malformed Lines
**Purpose:** Verify parsing skips invalid entries

**Input:** Line without proper format

**Expected:** `parse_room_entry()` returns None, line skipped

**Pass Criteria:** No crashes on malformed input

#### Test 5.3: All Decoy Rooms
**Purpose:** What if no real rooms exist?

**Expected:** Would return None (though impossible with real input)

**Note:** Not critical for this problem

### 6. Performance Tests

#### Test 6.1: Runtime Measurement
**Purpose:** Confirm solution is efficient

**Steps:**
1. Import `time` module
2. Measure: `start = time.time()`
3. Run: `solve('input.md')`
4. Measure: `elapsed = time.time() - start`
5. Print: `f"Solved in {elapsed:.4f} seconds"`

**Pass Criteria:**
- Runtime < 1 second (should be ~0.01-0.1 seconds)
- Acceptable: anything under 5 seconds

#### Test 6.2: Memory Usage
**Purpose:** Verify no excessive memory consumption

**Expected:**
- Peak memory: < 10 MB
- No memory leaks

**Note:** Not critical for script, but good practice

**Pass Criteria:** No memory issues observed

## Test Execution Order

1. **Unit Tests First** (Tests 1.1-1.6)
   - Validate decryption logic in isolation
   - Quick to run, easy to debug

2. **Integration Tests** (Tests 2.1-2.3)
   - Verify Part 1 code works
   - Test combined functionality

3. **Search Logic** (Tests 3.1-3.5)
   - Mock search scenarios
   - Edge cases in matching

4. **Full Solution** (Tests 4.1-4.3)
   - Run complete solution
   - Manual verification

5. **Performance** (Tests 6.1-6.2)
   - Final validation
   - Ensure efficiency

## Success Criteria Summary

### Must Pass (Critical)
- ✓ Example validation (Test 1.1)
- ✓ Wraparound works (Test 1.3)
- ✓ Part 1 logic intact (Test 2.1)
- ✓ Solution runs successfully (Test 4.2)
- ✓ Manual verification (Test 4.3)

### Should Pass (Important)
- ✓ Large sector IDs (Test 1.4)
- ✓ Search logic accurate (Test 3.1-3.4)
- ✓ Performance acceptable (Test 6.1)

### Nice to Pass (Edge Cases)
- ✓ Zero shift (Test 1.2)
- ✓ Malformed input (Test 5.2)

## Implementation in Code

```python
def validate_solution():
    """Run all validation tests."""
    print("Running validation tests...")

    # Test 1.1: Example verification
    result = decrypt_room_name("qzmt-zixmtkozy-ivhz", 343)
    assert result == "very encrypted name", f"Test 1.1 failed: {result}"
    print("✓ Test 1.1: Example verification passed")

    # Test 1.2: Zero shift
    assert decrypt_room_name("abc-xyz", 0) == "abc xyz"
    assert decrypt_room_name("abc-xyz", 26) == "abc xyz"
    print("✓ Test 1.2: Zero shift passed")

    # Test 1.2b: Modulo 26 boundary cases
    assert decrypt_room_name("abc", 25) == "zab"
    assert decrypt_room_name("abc", 27) == "bcd"
    print("✓ Test 1.2b: Modulo 26 boundaries passed")

    # Test 1.3: Full rotation
    assert decrypt_room_name("zabc", 1) == "abcd"
    assert decrypt_room_name("xyz", 3) == "abc"
    print("✓ Test 1.3: Alphabet wraparound passed")

    # Test 1.4: Large sector IDs
    assert decrypt_room_name("abc", 1000) == "mno"
    print("✓ Test 1.4: Large sector IDs passed")

    # Test 2.1: Part 1 logic (assumes Part 1 functions are already validated)
    encrypted, sid, checksum = parse_room_entry("aaaaa-bbb-z-y-x-123[abxyz]")
    assert sid == 123
    assert is_real_room(encrypted, checksum) == True
    print("✓ Test 2.1: Part 1 integration passed")

    print("All validation tests passed!")
```

## Final Verification Checklist

Before submitting solution:
- [ ] Validation function runs without errors
- [ ] Solution returns an integer
- [ ] Manual check confirms room exists and is valid
- [ ] Decrypted name contains "north" and "pole"
- [ ] Runtime is acceptable (< 1 second)
- [ ] Code is clean and readable
- [ ] No unnecessary dependencies
