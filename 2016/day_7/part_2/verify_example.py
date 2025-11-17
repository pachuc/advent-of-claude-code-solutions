#!/usr/bin/env python3
"""
Detailed verification of problem example
"""

from solution import parse_address, find_abas, aba_to_bab, supports_ssl

# Example 4 from problem: zazbz[bzb]cdb
test_address = "zazbz[bzb]cdb"

print(f"Testing example: {test_address}")
print(f"Expected: Supports SSL (zbz -> bzb match)\n")

# Parse it
supernets, hypernets = parse_address(test_address)
print(f"Supernets: {supernets}")
print(f"Hypernets: {hypernets}\n")

# Find ABAs in supernets
print("Finding ABAs in supernets:")
all_abas = set()
for supernet in supernets:
    abas = find_abas(supernet)
    print(f"  '{supernet}' -> {abas}")
    all_abas.update(abas)

print(f"\nAll ABAs: {all_abas}\n")

# Find BABs in hypernets
print("Finding BABs in hypernets:")
all_babs = set()
for hypernet in hypernets:
    babs = find_abas(hypernet)
    print(f"  '{hypernet}' -> {babs}")
    all_babs.update(babs)

print(f"\nAll BABs: {all_babs}\n")

# Check for matches
print("Checking for matches:")
for aba in all_abas:
    corresponding_bab = aba_to_bab(aba)
    is_match = corresponding_bab in all_babs
    print(f"  {aba} -> {corresponding_bab}: {'✓ MATCH' if is_match else '✗ no match'}")

result = supports_ssl(test_address)
print(f"\nResult: {result}")
print(f"Expected: True")
print(f"Match: {'✓' if result == True else '✗'}")
