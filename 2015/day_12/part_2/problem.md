# Problem Report: JSON Number Summation with Red Object Filtering

## Context
The Accounting-Elves have discovered they double-counted everything marked as "red" in their JSON data. We need to recalculate the sum of all numbers in the JSON structure while applying specific filtering rules.

## Objective
Calculate the sum of all numbers in a JSON document, with a specific rule: ignore any object (and all of its children) that has any property with the value `"red"`.

## Important Distinction
- **Objects** (`{...}`): If an object contains ANY property with the value `"red"`, ignore the entire object and all of its nested content
- **Arrays** (`[...]`): The value `"red"` appearing in an array has NO effect - continue processing the array normally

## Input
- A JSON document containing nested structures of:
  - Objects (key-value pairs in curly braces)
  - Arrays (lists in square brackets)
  - Numbers (integers, positive or negative)
  - Strings (text values)

## Output
- A single integer: the sum of all numbers in the JSON document after applying the red-object filtering rule

## Examples

### Example 1: Array with red string
**Input:** `[1,2,3]`
**Output:** `6`
**Explanation:** Simple sum, no red objects to filter

### Example 2: Object with red value inside array
**Input:** `[1,{"c":"red","b":2},3]`
**Output:** `4`
**Explanation:** The middle object has a property with value "red", so the entire object (including the number 2) is ignored. Sum: 1 + 3 = 4

### Example 3: Top-level object with red value
**Input:** `{"d":"red","e":[1,2,3,4],"f":5}`
**Output:** `0`
**Explanation:** The entire object has a property with value "red", so everything (including the nested array and all numbers) is ignored

### Example 4: Red string in array
**Input:** `[1,"red",5]`
**Output:** `6`
**Explanation:** "red" appears in an array, not as an object property value, so it has no effect. Sum: 1 + 5 = 6

## Algorithm Requirements
1. Parse the JSON structure
2. Recursively traverse all elements
3. For each object encountered:
   - Check if ANY property has the value `"red"` (as a string)
   - If yes: skip the entire object and all its children
   - If no: continue processing its contents
4. For arrays: always process all elements (red strings in arrays don't matter)
5. Sum all numbers that weren't filtered out
6. Return the final sum
