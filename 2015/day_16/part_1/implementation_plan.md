# Implementation Plan: Aunt Sue Identification

## Problem Analysis

We need to identify which Aunt Sue (out of 500) sent a gift by matching MFCSAM analysis results against remembered characteristics. Each aunt has exactly 3 known characteristics, and the remaining 7 characteristics are unknown (not remembered). A match occurs when ALL known characteristics for an aunt exactly match the target signature.

### Key Constraints:
- 500 aunts total
- Each aunt has 3 remembered characteristics
- 10 total possible compounds to track
- Target signature is fixed and complete (all 10 compounds specified)
- Unknown characteristics should be ignored (neither match nor mismatch)

### Algorithm Efficiency:
- Input size: 500 aunts, 3 characteristics each = 1,500 data points
- This is a small dataset, so O(n) linear scan is perfectly adequate
- No need for complex data structures or optimization
- Expected runtime: < 1ms

## Implementation Steps

### Step 1: Define the Target Signature
Create a dictionary containing the MFCSAM target compound signature:
```python
target = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1
}
```

### Step 2: Parse Input File
Read the input file and parse each line to extract:
- Sue number (ID)
- Compound names and their counts (3 per aunt)

**Parsing approach:**
- Use string splitting (simpler and more readable than regex)
- Format: `Sue N: compound1: count1, compound2: count2, compound3: count3`
- Store each aunt as a dictionary: `{sue_id: {compound: count, ...}}`

**Implementation details:**
```python
def parse_line(line):
    """
    Parse a line to extract Sue ID and characteristics.
    Returns (sue_id, characteristics_dict) or (None, {}) for invalid lines.
    """
    try:
        # Skip empty lines
        if not line.strip() or 'Sue' not in line:
            return None, {}

        # Split on first colon to separate "Sue N" from characteristics
        parts = line.split(':', 1)
        sue_id = int(parts[0].replace('Sue', '').strip())

        # Parse characteristics
        characteristics = {}
        compounds = parts[1].split(',')
        for compound in compounds:
            name, count = compound.split(':')
            characteristics[name.strip()] = int(count.strip())

        return sue_id, characteristics

    except (ValueError, IndexError, AttributeError) as e:
        # Skip malformed lines
        return None, {}
```

### Step 3: Implement Matching Logic
For each aunt, check if all remembered characteristics match the target:
- Iterate through each compound the aunt has
- Compare the count with the target signature
- If ANY remembered characteristic doesn't match → not a match
- If ALL remembered characteristics match → potential match

**Matching function:**
```python
def matches_target(aunt_characteristics, target_signature):
    for compound, count in aunt_characteristics.items():
        if target_signature[compound] != count:
            return False
    return True
```

### Step 4: Find the Matching Aunt
Iterate through all aunts and find the one where all characteristics match:
```python
def find_matching_sue(aunts_data, target_signature):
    for sue_id, characteristics in aunts_data.items():
        if matches_target(characteristics, target_signature):
            return sue_id
    return None  # No match found
```

### Step 5: Verification Function
Add a function to verify the result and provide diagnostic information:
```python
def verify_result(sue_id, aunts, target):
    """
    Verify the found Sue matches the target and print diagnostic info.
    Returns True if valid match, False otherwise.
    """
    if sue_id is None:
        print("ERROR: No matching Sue found!", file=sys.stderr)
        return False

    print(f"# Found Sue {sue_id}", file=sys.stderr)
    print("# Verification:", file=sys.stderr)

    characteristics = aunts[sue_id]
    all_match = True

    for compound, count in characteristics.items():
        target_val = target[compound]
        match = count == target_val
        all_match = all_match and match
        status = "✓" if match else "✗"
        print(f"#   {compound}: {count} (target: {target_val}) {status}", file=sys.stderr)

    if all_match:
        print(f"# All characteristics match!", file=sys.stderr)

    return all_match
```

### Step 6: Main Program Structure
```python
def main():
    # 1. Define target signature
    target = {
        'children': 3,
        'cats': 7,
        'samoyeds': 2,
        'pomeranians': 3,
        'akitas': 0,
        'vizslas': 0,
        'goldfish': 5,
        'trees': 3,
        'cars': 2,
        'perfumes': 1
    }

    # 2. Read and parse input file
    aunts = {}
    try:
        with open('input.md', 'r') as f:
            for line in f:
                sue_id, characteristics = parse_line(line)
                if sue_id is not None:  # Skip invalid lines
                    aunts[sue_id] = characteristics
    except FileNotFoundError:
        print("ERROR: input.md not found!", file=sys.stderr)
        sys.exit(1)

    # 3. Validate parsed data
    print(f"# Parsed {len(aunts)} Sues", file=sys.stderr)
    if len(aunts) == 0:
        print("ERROR: No valid Sue data found!", file=sys.stderr)
        sys.exit(1)

    # 4. Find matching Sue
    result = find_matching_sue(aunts, target)

    # 5. Verify and output result
    if verify_result(result, aunts, target):
        print(result)  # Only output to stdout for the answer
    else:
        print("ERROR: Verification failed!", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Step 7: Input Parsing Details
Handle the specific format carefully:
- Skip empty lines or lines without "Sue" prefix
- Split by `:` to separate Sue number from characteristics
- Split characteristics by `,` to get individual compounds
- For each compound, split by `:` to get name and count
- Strip whitespace from all strings
- Convert counts to integers

**Note:** We're using string splitting (implemented in Step 2) as it's simpler and more maintainable than regex for this format.

## Data Structures

### Input Data Structure:
```python
aunts = {
    1: {'goldfish': 9, 'cars': 0, 'samoyeds': 9},
    2: {'perfumes': 5, 'trees': 8, 'goldfish': 8},
    # ... 500 total
}
```

### Target Data Structure:
```python
target = {
    'children': 3,
    'cats': 7,
    # ... 10 compounds total
}
```

## Complexity Analysis

- **Time Complexity:** O(n × m) where n=500 aunts, m=3 characteristics per aunt
  - For each aunt: O(3) to check all characteristics
  - Total: O(500 × 3) = O(1500) operations
  - This is linear O(n) but negligible for this problem size

- **Space Complexity:** O(n × m) to store all aunt data
  - Dictionary of 500 aunts with 3 characteristics each = ~1500 entries

- **Expected Runtime:** < 10 milliseconds (tiny dataset)

## Edge Cases to Handle

1. **No matching Sue:** Return None and print error message, exit with code 1
2. **Multiple matching Sues:** Problem states there should be exactly one match (no special handling needed)
3. **Empty input file:** Check if file exists, handle FileNotFoundError
4. **Malformed lines:** Use try-except in parse_line to skip invalid lines silently
5. **Case sensitivity:** Compound names should match exactly (lowercase in input)
6. **Sue ID 0:** Use `if sue_id is not None` instead of `if sue_id` to handle edge case
7. **Missing input file:** Check file exists and provide clear error message

## Output Format

The program should output to two streams:
- **stdout:** Just the Sue number (e.g., `213`)
- **stderr:** Diagnostic information (verification details, parsing info)

This allows the answer to be captured easily while still providing useful debugging information:
```bash
python solution.py > answer.txt  # captures just the number
python solution.py               # shows full diagnostic output
```

Example output:
```
# Parsed 500 Sues
# Found Sue 213
# Verification:
#   akitas: 0 (target: 0) ✓
#   perfumes: 1 (target: 1) ✓
#   vizslas: 0 (target: 0) ✓
# All characteristics match!
213
```
