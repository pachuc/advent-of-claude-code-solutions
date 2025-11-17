#!/usr/bin/env python3
"""
Manual verification of a sample address from the input
"""

from solution import parse_address, find_abas, aba_to_bab, supports_ssl

# Let's verify the first address from the input sample
test_address = "nojlhdpfkjbhahgqo[lqrkjabuijutlcbq]caszlkvkofxjyqzsttc[isqicyomykudneq]izuzehgtmwnnvfrlrja"

print(f"Testing address: {test_address}\n")

# Parse it
supernets, hypernets = parse_address(test_address)
print(f"Supernets: {supernets}")
print(f"Hypernets: {hypernets}\n")

# Find ABAs in supernets
all_abas = set()
for supernet in supernets:
    abas = find_abas(supernet)
    if abas:
        print(f"ABAs in '{supernet}': {abas}")
        all_abas.update(abas)

print(f"\nAll ABAs in supernets: {all_abas}\n")

# Find BABs in hypernets
all_babs = set()
for hypernet in hypernets:
    babs = find_abas(hypernet)
    if babs:
        print(f"BABs in '{hypernet}': {babs}")
        all_babs.update(babs)

print(f"\nAll BABs in hypernets: {all_babs}\n")

# Check for matches
print("Checking for ABA -> BAB matches:")
matches = []
for aba in all_abas:
    corresponding_bab = aba_to_bab(aba)
    if corresponding_bab in all_babs:
        print(f"  ✓ Match found: {aba} -> {corresponding_bab}")
        matches.append((aba, corresponding_bab))
    else:
        print(f"  ✗ No match: {aba} -> {corresponding_bab} (not found)")

print(f"\nSupports SSL: {supports_ssl(test_address)}")
if matches:
    print(f"Reason: Found {len(matches)} ABA/BAB match(es)")
else:
    print(f"Reason: No ABA/BAB matches found")
