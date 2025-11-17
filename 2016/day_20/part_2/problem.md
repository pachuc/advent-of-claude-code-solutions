# Problem Report: Count Total Allowed IPs in Firewall

## Context from Part 1

You are setting up a hidden computer to access a corporate network. The corporate firewall maintains a blacklist of blocked IP ranges. In Part 1, you found the **lowest-valued IP address** that was not blocked (answer: 14975795).

### Part 1 Solution Approach
The Part 1 solution:
1. Parsed blocked IP ranges from the input (format: `start-end` per line)
2. Sorted and merged overlapping/adjacent ranges to simplify the blacklist
3. Found the first gap in the merged ranges to identify the lowest unblocked IP

## Part 2 Goal

Now you need to determine **how many total IPs are allowed** by the blacklist.

Instead of finding just the lowest unblocked IP, you must count ALL IPs that are not blocked across the entire 32-bit IP address space.

## Input Specifications

### IP Address Format
- IP addresses are represented as plain 32-bit integers (NOT dot-decimal notation)
- Valid range: `0` through `4294967295` (inclusive)
- This represents all possible IPv4 addresses in integer form
- **Total possible IPs: 4,294,967,296** (2^32)

### Input Format
The input consists of blocked IP ranges, one per line, in the format:
```
start-end
```

Where:
- `start` is the first IP address in the blocked range (inclusive)
- `end` is the last IP address in the blocked range (inclusive)
- Both start and end are 32-bit integers
- Ranges may overlap
- Ranges may not be in sorted order

### Example Input
```
5-8
0-2
4-7
```

For a simplified universe where valid IPs are 0-9 (10 total IPs):
- Blocked IPs: 0, 1, 2, 4, 5, 6, 7, 8
- Allowed IPs: 3, 9
- **Count of allowed IPs: 2**

## Expected Output

A single integer representing the **total count** of IP addresses that are NOT blocked by any range in the blacklist.

## Algorithm Requirements

1. Parse all blocked IP ranges from the input
2. Merge overlapping/adjacent ranges (can reuse Part 1 logic)
3. Calculate the total number of blocked IPs from the merged ranges
4. Subtract blocked IPs from the total IP space (4,294,967,296) to get allowed IPs
5. Return the count as an integer

## Calculation Strategy

After merging ranges, for each merged range `(start, end)`:
- Number of blocked IPs in that range = `end - start + 1`

Total blocked IPs = sum of all blocked IPs across merged ranges

**Total allowed IPs = 4,294,967,296 - Total blocked IPs**

## Key Considerations

- The total IP address space is 4,294,967,296 (from 0 to 4,294,967,295 inclusive)
- You must account for ALL IPs in this space, not just those explicitly mentioned
- Merging overlapping ranges is crucial to avoid double-counting blocked IPs
- The answer will be the count of gaps between blocked ranges, plus any IPs after the last blocked range and before the first blocked range
