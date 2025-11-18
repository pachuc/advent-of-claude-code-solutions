# Problem Report: Circular Digit Sum (Inverse Captcha)

## Objective
Calculate the sum of all digits in a sequence where each digit matches the next digit in the sequence. The sequence is circular (wraps around).

## Context
This is a captcha-solving problem. We need to validate a sequence of digits by finding matching consecutive pairs and summing the first digit of each matching pair.

## Input Specification
- **Format**: A single string of digits (0-9)
- **Length**: Variable length (the provided input is 2000 digits long)
- **Location**: The input can be found in `input.md`
- **Characteristics**: The sequence is treated as circular, meaning the last digit should be compared with the first digit

## Algorithm Requirements

1. Iterate through each digit in the sequence
2. Compare each digit with the next digit in the sequence
3. For the last digit, compare it with the first digit (circular property)
4. If a digit matches the next digit, add that digit's value to the running sum
5. Return the total sum

## Output Specification
- **Format**: A single integer representing the sum
- **Example outputs**:
  - Input: `1122` → Output: `3` (first `1` matches second `1`, third `2` matches fourth `2`: 1 + 2 = 3)
  - Input: `1111` → Output: `4` (all four `1`s match their next digit: 1 + 1 + 1 + 1 = 4)
  - Input: `1234` → Output: `0` (no consecutive matches)
  - Input: `91212129` → Output: `9` (only the last `9` matches the first `9`: 9)

## Key Implementation Notes
- The sequence is **circular**: after the last element comes the first element
- Only sum the digit when it **matches the next** digit (not both digits, just the first one of the pair)
- All characters in the input are guaranteed to be numeric digits
