#!/usr/bin/env python3
"""Test script for IPv7 TLS detection solution."""

from solution import has_abba, parse_address, supports_tls


def test_has_abba():
    """Test the has_abba function with various inputs."""
    print("Testing has_abba()...")

    # Valid ABBAs
    assert has_abba("abba") == True, "Simple ABBA 'abba' should be detected"
    assert has_abba("xyyx") == True, "ABBA 'xyyx' should be detected"
    assert has_abba("oxxo") == True, "ABBA 'oxxo' should be detected"
    assert has_abba("ioxxoj") == True, "ABBA 'oxxo' in middle should be detected"
    assert has_abba("zabbaz") == True, "ABBA 'abba' in middle should be detected"

    # Invalid ABBAs
    assert has_abba("aaaa") == False, "'aaaa' should NOT be valid ABBA"
    assert has_abba("abcd") == False, "'abcd' has no ABBA"
    assert has_abba("abc") == False, "'abc' is too short"
    assert has_abba("") == False, "Empty string should return False"
    assert has_abba("a") == False, "Single char should return False"

    print("  ✓ All has_abba() tests passed!")


def test_parse_address():
    """Test the parse_address function."""
    print("Testing parse_address()...")

    # Single bracket pair
    supernets, hypernets = parse_address("abcd[efgh]ijkl")
    assert supernets == ["abcd", "ijkl"], f"Expected ['abcd', 'ijkl'], got {supernets}"
    assert hypernets == ["efgh"], f"Expected ['efgh'], got {hypernets}"

    # Multiple bracket pairs
    supernets, hypernets = parse_address("abc[def]ghi[jkl]mno")
    assert supernets == ["abc", "ghi", "mno"], f"Expected ['abc', 'ghi', 'mno'], got {supernets}"
    assert hypernets == ["def", "jkl"], f"Expected ['def', 'jkl'], got {hypernets}"

    # No brackets
    supernets, hypernets = parse_address("abcdefgh")
    assert supernets == ["abcdefgh"], f"Expected ['abcdefgh'], got {supernets}"
    assert hypernets == [], f"Expected [], got {hypernets}"

    print("  ✓ All parse_address() tests passed!")


def test_supports_tls():
    """Test the supports_tls function with provided examples."""
    print("Testing supports_tls() with problem examples...")

    # Example 1: Supports TLS (ABBA outside, none inside)
    assert supports_tls("abba[mnop]qrst") == True, \
        "abba[mnop]qrst should support TLS"

    # Example 2: Does NOT support (ABBA inside brackets)
    assert supports_tls("abcd[bddb]xyyx") == False, \
        "abcd[bddb]xyyx should NOT support TLS (ABBA in hypernet)"

    # Example 3: Does NOT support (no valid ABBA)
    assert supports_tls("aaaa[qwer]tyui") == False, \
        "aaaa[qwer]tyui should NOT support TLS (no valid ABBA)"

    # Example 4: Supports TLS (ABBA in middle of supernet)
    assert supports_tls("ioxxoj[asdfgh]zxcvbn") == True, \
        "ioxxoj[asdfgh]zxcvbn should support TLS"

    print("  ✓ All provided examples passed!")

    # Additional test cases
    print("Testing additional edge cases...")

    # ABBA only in hypernet (should fail)
    assert supports_tls("abcd[xyyx]efgh") == False, \
        "ABBA only in hypernet should fail"

    # ABBA in both (should fail due to hypernet)
    assert supports_tls("abba[xyyx]qrst") == False, \
        "ABBA in both supernet and hypernet should fail"

    # Multiple ABBAs in supernet, none in hypernet (should pass)
    assert supports_tls("abba[mnop]xyyx") == True, \
        "Multiple ABBAs in supernet should pass"

    # No ABBA anywhere (should fail)
    assert supports_tls("abcd[efgh]ijkl") == False, \
        "No ABBA anywhere should fail"

    print("  ✓ All edge case tests passed!")


def main():
    """Run all tests."""
    print("=" * 50)
    print("Running IPv7 TLS Detection Tests")
    print("=" * 50)

    test_has_abba()
    test_parse_address()
    test_supports_tls()

    print("=" * 50)
    print("✓ All tests passed successfully!")
    print("=" * 50)


if __name__ == "__main__":
    main()
