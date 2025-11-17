#!/usr/bin/env python3
"""Verify solution by manually checking some addresses from the input."""

from solution import supports_tls, has_abba, parse_address


def verify_samples():
    """Manually verify a few sample addresses."""
    print("Verifying sample addresses from input:\n")

    # Read a few lines from input
    with open('input.md', 'r') as f:
        lines = f.readlines()

    # Check the first 10 addresses with detailed output
    for i in range(min(10, len(lines))):
        address = lines[i].strip()
        if not address:
            continue

        supernets, hypernets = parse_address(address)
        result = supports_tls(address)

        print(f"Address {i+1}: {address[:60]}..." if len(address) > 60 else f"Address {i+1}: {address}")

        # Check for ABBAs in supernets
        supernet_abbas = []
        for sup in supernets:
            if has_abba(sup):
                supernet_abbas.append(sup)

        # Check for ABBAs in hypernets
        hypernet_abbas = []
        for hyp in hypernets:
            if has_abba(hyp):
                hypernet_abbas.append(hyp)

        print(f"  Supernets with ABBA: {supernet_abbas if supernet_abbas else 'None'}")
        print(f"  Hypernets with ABBA: {hypernet_abbas if hypernet_abbas else 'None'}")
        print(f"  Supports TLS: {result}")
        print()


if __name__ == "__main__":
    verify_samples()
