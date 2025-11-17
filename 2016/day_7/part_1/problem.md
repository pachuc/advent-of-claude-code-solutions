# Problem Report: IPv7 TLS Support Detection

## Objective
Count how many IPv7 addresses in the input support TLS (transport-layer snooping).

## Background
We are analyzing a list of IPv7 addresses to determine which ones support TLS. An IPv7 address supports TLS if it contains an ABBA (Autonomous Bridge Bypass Annotation) pattern in specific locations.

## Input
- A list of IPv7 addresses (one per line)
- Each address consists of:
  - Regular character sequences (supernet sequences)
  - Hypernet sequences enclosed in square brackets `[...]`
- Example: `abba[mnop]qrst` has supernet sequences "abba" and "qrst", and hypernet sequence "mnop"

## ABBA Pattern Definition
An ABBA is a four-character sequence where:
1. It consists of two different characters
2. The pattern is: character A, character B, character B, character A (palindrome)
3. Examples:
   - `xyyx` - valid ABBA
   - `abba` - valid ABBA
   - `oxxo` - valid ABBA
   - `aaaa` - INVALID (both characters must be different)

## TLS Support Rules
An IPv7 address supports TLS if and only if:
1. **At least one ABBA exists outside square brackets** (in supernet sequences)
2. **No ABBA exists inside square brackets** (in hypernet sequences)

## Examples
- `abba[mnop]qrst` → **Supports TLS** (contains `abba` outside brackets)
- `abcd[bddb]xyyx` → **Does NOT support TLS** (`bddb` is an ABBA inside brackets, even though `xyyx` is outside)
- `aaaa[qwer]tyui` → **Does NOT support TLS** (`aaaa` is invalid - not a proper ABBA)
- `ioxxoj[asdfgh]zxcvbn` → **Supports TLS** (`oxxo` is outside brackets within the string "ioxxoj")

## Expected Output
A single integer: the count of IPv7 addresses that support TLS.

## Implementation Notes
- ABBA patterns can overlap with other characters in a sequence (see `ioxxoj` → `oxxo`)
- Check all possible 4-character windows in each sequence
- Keep track of whether sequences are inside or outside brackets
- An address fails immediately if any ABBA is found inside brackets
