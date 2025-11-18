# Problem Report: Stream Processing

## Objective
Calculate the total score for all groups in a stream of characters.

## Context
We need to parse a stream of characters that represents nested groups and garbage. The stream follows specific syntax rules and we need to count groups while properly handling garbage and cancellation characters.

## Input Format
- A single line of text containing a character stream
- The stream consists of groups (delimited by `{` and `}`) and garbage (delimited by `<` and `>`)

## Parsing Rules

### Groups
- Groups start with `{` and end with `}`
- Groups can contain:
  - Other groups (nested)
  - Garbage
  - Both, separated by commas
- Groups are nestable - a `}` closes the most-recently-opened unclosed group
- The entire input represents one large outer group containing many smaller groups

### Garbage
- Garbage starts with `<` and ends with `>`
- Between `<` and `>`, almost any character can appear, including `{` and `}`
- Inside garbage, `<` has no special meaning
- Garbage is not counted as a group

### Cancellation
- Inside garbage, the `!` character cancels the next character
- Any character following `!` should be ignored, including:
  - `<`
  - `>`
  - Another `!`
- The canceled character does not contribute to garbage termination

## Scoring System
Each group receives a score based on its nesting level:
- The outermost group gets a score of 1
- Each nested group gets a score one more than the group that contains it
- Score = nesting depth

**Total score** = sum of all individual group scores

## Examples

### Garbage Examples
- `<>` - empty garbage
- `<random characters>` - garbage with content
- `<<<<>` - extra `<` are ignored
- `<{!>}>` - first `>` is canceled
- `<!!>` - second `!` is canceled, allowing `>` to terminate
- `<!!!>>` - second `!` and first `>` are canceled
- `<{o"i!a,<{i<a>` - ends at first `>`

### Group Count Examples
- `{}` - 1 group
- `{{{}}}` - 3 groups
- `{{},{}}` - 3 groups
- `{{{},{},{{}}}}` - 6 groups
- `{<{},{},{{}}>}` - 1 group (garbage inside)
- `{<a>,<a>,<a>,<a>}` - 1 group
- `{{<a>},{<a>},{<a>},{<a>}}` - 5 groups
- `{{<!>},{<!>},{<!>},{<a>}}` - 2 groups (cancellation prevents `>` from closing garbage)

### Score Examples
- `{}` - score of 1
- `{{{}}}` - score of 1 + 2 + 3 = 6
- `{{},{}}` - score of 1 + 2 + 2 = 5
- `{{{},{},{{}}}}` - score of 1 + 2 + 3 + 3 + 3 + 4 = 16
- `{<a>,<a>,<a>,<a>}` - score of 1
- `{{<ab>},{<ab>},{<ab>},{<ab>}}` - score of 1 + 2 + 2 + 2 + 2 = 9
- `{{<!!>},{<!!>},{<!!>},{<!!>}}` - score of 1 + 2 + 2 + 2 + 2 = 9
- `{{<a!>},{<a!>},{<a!>},{<ab>}}` - score of 1 + 2 = 3

## Expected Output
A single integer representing the total score of all groups in the input stream.

## Algorithm Approach
1. Iterate through the character stream one character at a time
2. Track whether we are currently inside garbage
3. Handle cancellation characters (`!`) when inside garbage
4. Track the current nesting depth
5. When encountering `{` (outside garbage), increment depth and add current depth to total score
6. When encountering `}` (outside garbage), decrement depth
7. Ignore all characters inside garbage (except for cancellation processing)
8. Return the total accumulated score
