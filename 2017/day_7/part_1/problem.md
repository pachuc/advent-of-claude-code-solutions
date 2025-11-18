# Problem Report: Recursive Circus - Finding the Bottom Program

## Context
We are dealing with a tower of programs arranged in a tree structure. Programs are stacked on top of each other, with one program at the bottom supporting the entire tower. Each program holds a disc, and other programs can be balanced on that disc, creating sub-towers. This forms a recursive tree structure.

## Objective
Find the name of the bottom program (the root of the tree) - the single program that supports the entire tower and is not held by any other program.

## Input Format
The input is an unordered list of program descriptions. Each line contains:
- **Program name**: A string identifier
- **Weight**: An integer in parentheses (e.g., `(66)`)
- **Children programs** (optional): If the program holds a disc with other programs on it, their names are listed after `->` and separated by commas

### Input Format Examples:
```
pbga (66)
fwft (72) -> ktlj, cntj, xhth
tknk (41) -> ugml, padx, fwft
```

- `pbga` has weight 66 and holds no other programs
- `fwft` has weight 72 and holds three programs: `ktlj`, `cntj`, and `xhth`
- `tknk` has weight 41 and holds three programs: `ugml`, `padx`, and `fwft`

## Expected Output
A single string: the name of the bottom program (root of the tree).

### Example:
Given the sample input in the puzzle, the expected output is:
```
tknk
```

This is because `tknk` is at the bottom of the tower - it holds other programs but is not held by any program itself.

## Algorithm Approach
To find the bottom program:
1. Parse all program entries to identify which programs hold other programs (parents) and which programs are held (children)
2. The bottom program is the one that appears as a parent but never appears as a child
3. In other words, find the program that has no parent in the tree structure

## Additional Notes
- The input is NOT ordered - programs are listed randomly
- Every program except the bottom one will appear in exactly one other program's children list
- The bottom program will never appear in any children list
- There is exactly one bottom program (one root node)
