#!/usr/bin/env python3
"""Test script to validate the solution with known examples."""

from solution import parse_address, find_abas, aba_to_bab, supports_ssl


def test_aba_to_bab():
    """Test the ABA to BAB conversion function."""
    print("Testing aba_to_bab()...")
    test_cases = [
        ("aba", "bab"),
        ("xyx", "yxy"),
        ("eke", "kek"),
        ("zbz", "bzb"),
    ]

    for aba, expected_bab in test_cases:
        result = aba_to_bab(aba)
        status = "✓" if result == expected_bab else "✗"
        print(f"  {status} {aba} -> {result} (expected {expected_bab})")


def test_find_abas():
    """Test the ABA detection function."""
    print("\nTesting find_abas()...")
    test_cases = [
        ("zazbz", {"zaz", "zbz"}),
        ("aaaa", set()),
        ("", set()),
        ("ab", set()),
        ("aba", {"aba"}),
        ("abcdef", set()),
    ]

    for sequence, expected_abas in test_cases:
        result = find_abas(sequence)
        status = "✓" if result == expected_abas else "✗"
        print(f"  {status} '{sequence}' -> {result} (expected {expected_abas})")


def test_supports_ssl():
    """Test the SSL support function with problem examples."""
    print("\nTesting supports_ssl() with problem examples...")
    test_cases = [
        ("aba[bab]xyz", True, "aba -> bab match"),
        ("xyx[xyx]xyx", False, "xyx -> yxy not in hypernet"),
        ("aaa[kek]eke", True, "eke -> kek match"),
        ("zazbz[bzb]cdb", True, "zbz -> bzb match"),
    ]

    for address, expected_result, reason in test_cases:
        result = supports_ssl(address)
        status = "✓" if result == expected_result else "✗"
        print(f"  {status} {address}")
        print(f"      Expected: {expected_result}, Got: {result}")
        print(f"      Reason: {reason}")

        # Debug info for failures
        if result != expected_result:
            supernets, hypernets = parse_address(address)
            all_abas = set()
            for supernet in supernets:
                all_abas.update(find_abas(supernet))
            all_babs = set()
            for hypernet in hypernets:
                all_babs.update(find_abas(hypernet))
            print(f"      DEBUG: supernets={supernets}, hypernets={hypernets}")
            print(f"      DEBUG: ABAs={all_abas}, BABs={all_babs}")


def test_example_file():
    """Test with the example file."""
    print("\nTesting with test_examples.txt...")
    count = 0
    with open('test_examples.txt', 'r') as f:
        for line in f:
            address = line.strip()
            if address and supports_ssl(address):
                count += 1

    expected_count = 3
    status = "✓" if count == expected_count else "✗"
    print(f"  {status} Count: {count} (expected {expected_count})")


if __name__ == "__main__":
    test_aba_to_bab()
    test_find_abas()
    test_supports_ssl()
    test_example_file()
    print("\nAll tests completed!")
