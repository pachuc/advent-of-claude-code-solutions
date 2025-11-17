# Problem Report: Firewall IP Whitelist Identification

## Context
You need to set up a hidden computer to access a corporate network, but the corporate firewall only allows communication with certain external IP addresses. The firewall maintains a blacklist of blocked IP ranges, but the list is messy and poorly maintained. You need to identify which IPs are allowed (not blocked).

## Goal
Find the **lowest-valued IP address** that is not blocked by the firewall.

## Input Specifications

### IP Address Format
- IP addresses are represented as plain 32-bit integers (NOT dot-decimal notation)
- Valid range: `0` through `4294967295` (inclusive)
- This represents all possible IPv4 addresses in integer form

### Input Format
The input consists of blocked IP ranges, one per line, in the format:
```
start-end
```

Where:
- `start` is the first IP address in the blocked range (inclusive)
- `end` is the last IP address in the blocked range (inclusive)
- Both start and end are 32-bit integers

### Example Input
```
5-8
0-2
4-7
```

This blacklist blocks:
- IPs 0, 1, 2 (from range 0-2)
- IPs 4, 5, 6, 7 (from range 4-7)
- IPs 5, 6, 7, 8 (from range 5-8)

Note: Ranges may overlap (as shown with 5-7 appearing in both the second and third ranges).

## Expected Output

A single integer representing the lowest-valued IP address that is NOT blocked by any range in the blacklist.

### Example Output
For the example input above with valid IPs from 0-9:
- Blocked IPs: 0, 1, 2, 4, 5, 6, 7, 8
- Allowed IPs: 3, 9
- **Answer: 3** (the lowest allowed IP)

## Algorithm Requirements

1. Parse all blocked IP ranges from the input
2. Determine which IP addresses are blocked (handling overlapping ranges)
3. Find the smallest IP address (starting from 0) that is not in any blocked range
4. Return this IP address as an integer

## Key Considerations

- The input ranges may overlap
- The input ranges may not be in sorted order
- You need to find the LOWEST (minimum) unblocked IP, not just any unblocked IP
- The search space is all 32-bit integers from 0 to 4294967295
