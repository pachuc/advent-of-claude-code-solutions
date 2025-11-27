#!/usr/bin/env python3
"""Test the solution with the example from the problem statement."""

from solution import count_differences, get_common_letters, find_prototype_boxes

def test_example():
    """Test with the example data from problem.md"""
    example_ids = [
        "abcde",
        "fghij",
        "klmno",
        "pqrst",
        "fguij",
        "axcye",
        "wvxyz"
    ]

    # Test count_differences
    assert count_differences("fghij", "fguij") == 1, "fghij vs fguij should differ by 1"
    assert count_differences("abcde", "axcye") == 2, "abcde vs axcye should differ by 2"
    print("✓ count_differences tests passed")

    # Test get_common_letters
    assert get_common_letters("fghij", "fguij") == "fgij", "Common letters should be 'fgij'"
    print("✓ get_common_letters tests passed")

    # Test find_prototype_boxes
    result = find_prototype_boxes(example_ids)
    assert result == "fgij", f"Expected 'fgij', got '{result}'"
    print("✓ find_prototype_boxes test passed")

    print("\n✓ All example tests PASSED")

if __name__ == '__main__':
    test_example()
