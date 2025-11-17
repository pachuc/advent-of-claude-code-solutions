# Implementation Plan: IPv7 SSL Support Detection (Part 2)

## Overview
This solution builds on Part 1's IPv7 address parsing logic but implements a different pattern matching system. Instead of checking for ABBA patterns, we need to find ABA/BAB correspondence between supernet and hypernet sequences.

## Key Differences from Part 1
- **Pattern type**: 3-character ABA patterns (not 4-character ABBA)
- **Logic**: Must find matching ABA in supernet AND corresponding BAB in hypernet (not exclusion)
- **Pattern definition**: ABA has form `XYX` where X ≠ Y, corresponding BAB is `YXY`

## Algorithm Design

### Time Complexity Analysis
- Input size: ~2000 IPv7 addresses (based on Part 1 input)
- Each address: ~30-60 characters average
- For each address:
  - Parse into sequences: O(n) where n = address length
  - Find all ABAs in supernets: O(m) where m = total supernet chars
  - Find all BABs in hypernets: O(k) where k = total hypernet chars
  - Check for ABA/BAB matches: O(ABAs * BABs) but typically small constants
- **Overall**: O(addresses * avg_length) = O(2000 * 50) = ~100K operations - very efficient

### Space Complexity
- Store sets of ABAs and BABs per address: O(alphabet²) = O(26²) = O(676) max per address
- Using sets for O(1) lookup when checking correspondence

## Implementation Steps

### Step 1: Reuse Part 1 Parsing Logic
- **File reference**: `part_1_solution.py:23-59`
- Copy the `parse_address()` function verbatim
- This function already handles:
  - Splitting addresses into supernet (outside `[]`) and hypernet (inside `[]`) sequences
  - Proper bracket parsing and edge cases
  - Returning `(supernets, hypernets)` tuple

### Step 2: Implement ABA Detection Function
Create `find_abas(sequence)` function:
- **Input**: A single string sequence (e.g., "zazbz")
- **Output**: Set of ABA patterns found (e.g., {"zaz", "zbz"})
- **Logic**:
  1. Use sliding window of size 3
  2. Loop through valid window positions: `for i in range(len(sequence) - 2):`
     - Note: For a sequence of length n, last valid 3-char window starts at index n-3
     - `range(len(sequence) - 2)` gives indices 0 to n-3 inclusive (correct bounds)
  3. For each window at position i:
     - Extract 3-char substring: `window = sequence[i:i+3]`
     - Check if it's valid ABA:
       - `window[0] == window[2]` (first and third match)
       - `window[0] != window[1]` (outer differs from middle)
     - If valid, add to result set
  4. Return set of all found ABAs
- **Why set?**: Avoid duplicate ABAs, enable O(1) lookup later
- **Edge cases**:
  - Empty string returns empty set (range(0 - 2) = range(-2) is empty)
  - Sequences shorter than 3 chars return empty set (range handles this correctly)
- **Type hint**: `def find_abas(sequence: str) -> set[str]:`
- **Docstring**: Include explanation of ABA pattern and examples

### Step 3: Implement BAB Conversion Function
Create `aba_to_bab(aba)` helper function:
- **Input**: An ABA string (e.g., "xyx")
- **Output**: Corresponding BAB string (e.g., "yxy")
- **Logic**: Simple string reconstruction
  - Extract outer char: `outer = aba[0]`
  - Extract middle char: `middle = aba[1]`
  - Return: `middle + outer + middle`
- **Examples**: "aba" → "bab", "eke" → "kek", "xyx" → "yxy", "zbz" → "bzb"
- **Type hint**: `def aba_to_bab(aba: str) -> str:`
- **Docstring**: Explain conversion from ABA to corresponding BAB pattern

### Step 4: Implement SSL Support Check
Create `supports_ssl(address)` function:
- **Input**: Full IPv7 address string
- **Output**: Boolean indicating SSL support
- **Logic**:
  1. Parse address: `supernets, hypernets = parse_address(address)`
  2. Find all ABAs in all supernet sequences:
     ```python
     all_abas = set()
     for supernet in supernets:
         all_abas.update(find_abas(supernet))
     ```
  3. Find all BABs in all hypernet sequences:
     ```python
     all_babs = set()
     for hypernet in hypernets:
         all_babs.update(find_abas(hypernet))  # BABs are also ABA patterns
     ```
  4. Check for correspondence:
     ```python
     for aba in all_abas:
         corresponding_bab = aba_to_bab(aba)
         if corresponding_bab in all_babs:
             return True
     return False
     ```
- **Optimization**: Early return on first match (no need to check all pairs)
- **Type hint**: `def supports_ssl(address: str) -> bool:`
- **Docstring**: Explain SSL support rules and include problem examples as comments:
  ```python
  # Examples from problem.md:
  # aba[bab]xyz -> True (aba -> bab match)
  # xyx[xyx]xyx -> False (xyx -> yxy, but only xyx in hypernet)
  # aaa[kek]eke -> True (eke -> kek match, aaa invalid)
  # zazbz[bzb]cdb -> True (zbz -> bzb match)
  ```

### Step 5: Main Function
Create `main()` function:
- **Logic**:
  1. Initialize counter: `count = 0`
  2. Read input file line by line: `open('input.md', 'r')`
     - **Assumption**: input.md exists in current directory (no error handling needed for script)
  3. For each line:
     - Strip whitespace: `address = line.strip()`
     - Skip empty lines: `if address:` (handles trailing newlines or blank lines in input)
     - Check SSL support: `if supports_ssl(address):`
     - Increment counter: `count += 1`
  4. Print final count: `print(count)` (just the number, no label - following Advent of Code convention)
- **Type hint**: `def main() -> None:`
- **Optional debug mode** (for development/validation):
  ```python
  DEBUG = False  # Set to True for verbose output

  if DEBUG:
      print(f"Address: {address}")
      print(f"Supernets: {supernets}")
      print(f"Hypernets: {hypernets}")
      print(f"ABAs found: {all_abas}")
      print(f"BABs found: {all_babs}")
      print(f"Supports SSL: {result}")
  ```

### Step 6: Script Entry Point
```python
if __name__ == "__main__":
    main()
```

## Code Structure
```
solution.py
├── find_abas(sequence: str) -> set[str]
├── aba_to_bab(aba: str) -> str
├── parse_address(address: str) -> tuple[list[str], list[str]]  [from Part 1]
├── supports_ssl(address: str) -> bool
└── main() -> None
```

## Code Quality Standards
To match Part 1's quality:
- **Include type hints** for all function parameters and return values
- **Add docstrings** to all functions explaining purpose, parameters, and examples
- **Follow Part 1's style** for consistency across solutions

## Implementation Order
1. Copy `parse_address()` from Part 1 solution
2. Implement `find_abas()` - core pattern detection
3. Implement `aba_to_bab()` - simple helper
4. Implement `supports_ssl()` - orchestration logic
5. Implement `main()` - file I/O and counting
6. Add entry point guard

## Example Walkthrough
For address `aba[bab]xyz`:
1. Parse: supernets=["aba", "xyz"], hypernets=["bab"]
2. Find ABAs in supernets: {"aba"} (from "aba")
3. Find BABs in hypernets: {"bab"} (from "bab")
4. Check correspondence: aba_to_bab("aba") = "bab", "bab" in {"bab"} ✓
5. Result: **Supports SSL**

For address `xyx[xyx]xyx`:
1. Parse: supernets=["xyx", "xyx"], hypernets=["xyx"]
2. Find ABAs in supernets: {"xyx"}
3. Find BABs in hypernets: {"xyx"}
4. Check correspondence: aba_to_bab("xyx") = "yxy", "yxy" NOT in {"xyx"} ✗
5. Result: **Does NOT support SSL**

## Efficiency Considerations
- **Set operations**: O(1) average case for lookups and insertions
- **Early termination**: Return True immediately when first ABA/BAB match found
- **No redundant parsing**: Single pass through each address
- **Memory efficient**: Sets contain at most 676 unique 3-char patterns (26² alphabet combinations)

## Edge Cases Handled
1. **Empty sequences**: Handled by range bounds in `find_abas()` - empty range produces no iterations
2. **Short sequences** (< 3 chars): `range(len(sequence) - 2)` handles correctly
3. **No brackets**: Handled by `parse_address()` (all text goes to supernets)
4. **Overlapping ABAs**: Set automatically handles duplicates, sliding window catches all occurrences
5. **Invalid ABAs** (like "aaa"): Filtered by `window[0] != window[1]` check
6. **Multiple ABAs with one matching BAB**: Early return optimization handles this efficiently
7. **Empty or blank lines in input**: `if address:` check after `strip()` skips these

## Assumptions
- Input file (input.md) exists and is readable
- Input format is valid (lowercase letters and brackets, balanced brackets, no nesting)
- No input validation needed (trust the input format per Advent of Code standards)
