# Problem Report: IPv7 SSL Support Detection (Part 2)

## Context from Part 1
In Part 1, we analyzed IPv7 addresses to determine TLS support based on ABBA patterns:
- ABBA: A four-character palindrome with two different characters (e.g., `abba`, `xyyx`)
- TLS required an ABBA in supernet sequences (outside brackets) but NO ABBA in hypernet sequences (inside brackets)
- Part 1 answer: 118 addresses supported TLS

## Part 2 Objective
Count how many IPv7 addresses in the input support SSL (super-secret listening).

## Background
We are now checking for SSL support instead of TLS support. SSL uses a different pattern matching system based on ABA/BAB pairs across supernet and hypernet sequences.

## Input
- Same list of IPv7 addresses from Part 1 (one per line)
- Each address consists of:
  - Supernet sequences (outside square brackets)
  - Hypernet sequences (inside square brackets `[...]`)
- Example: `aba[bab]xyz` has supernet sequences "aba" and "xyz", and hypernet sequence "bab"

## ABA Pattern Definition
An ABA is a three-character sequence where:
1. First and third characters are the same
2. The middle character is different from the outer characters
3. Examples:
   - `xyx` - valid ABA
   - `aba` - valid ABA
   - `eke` - valid ABA
   - `aaa` - INVALID (middle character must be different)

## BAB Pattern Definition
A BAB is the reverse of an ABA:
- If the ABA is `xyx`, the corresponding BAB is `yxy`
- If the ABA is `aba`, the corresponding BAB is `bab`
- If the ABA is `eke`, the corresponding BAB is `kek`

## SSL Support Rules
An IPv7 address supports SSL if and only if:
1. **At least one ABA exists in any supernet sequence** (outside brackets)
2. **The corresponding BAB exists in any hypernet sequence** (inside brackets)

The ABA and BAB don't need to be in the same position or adjacent - they just both need to exist somewhere in their respective sequence types.

## Examples
- `aba[bab]xyz` → **Supports SSL** (ABA `aba` outside brackets, corresponding BAB `bab` inside brackets)
- `xyx[xyx]xyx` → **Does NOT support SSL** (`xyx` is an ABA, but corresponding BAB would be `yxy` which doesn't exist)
- `aaa[kek]eke` → **Supports SSL** (ABA `eke` in supernet, corresponding BAB `kek` in hypernet; `aaa` is invalid ABA)
- `zazbz[bzb]cdb` → **Supports SSL** (ABA `zbz` in supernet has corresponding BAB `bzb` in hypernet; overlapping patterns are allowed)

## Expected Output
A single integer: the count of IPv7 addresses that support SSL.

## Implementation Notes
- ABA patterns can overlap with other characters (see `zazbz` → contains both `zaz` and `zbz`)
- Check all possible 3-character windows in each sequence
- For each ABA found in supernet sequences, check if the corresponding BAB exists in any hypernet sequence
- The ABA pattern must have different inner and outer characters
- Parse addresses into supernet and hypernet sequences (can reuse Part 1 parsing logic)
