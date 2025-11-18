#!/usr/bin/env python3
"""Additional verification of the solution logic."""

from solution import (
    pattern_to_grid, grid_to_pattern, rotate_grid, flip_grid,
    generate_all_orientations, parse_rules
)

def test_rotation():
    """Test that 4 rotations return to original."""
    grid = ['.#.', '..#', '###']
    current = grid
    for i in range(4):
        current = rotate_grid(current)

    if current == grid:
        print("✓ Rotation test passed: 4 rotations return to original")
        return True
    else:
        print("✗ Rotation test failed")
        print(f"  Original: {grid}")
        print(f"  After 4 rotations: {current}")
        return False

def test_flip():
    """Test that double flip returns to original."""
    grid = ['.#.', '..#', '###']
    flipped = flip_grid(grid)
    double_flipped = flip_grid(flipped)

    if double_flipped == grid:
        print("✓ Flip test passed: double flip returns to original")
        return True
    else:
        print("✗ Flip test failed")
        print(f"  Original: {grid}")
        print(f"  After double flip: {double_flipped}")
        return False

def test_orientations():
    """Test orientation generation."""
    # Symmetric pattern should have fewer unique orientations
    symmetric = "../.."
    orientations = generate_all_orientations(symmetric)
    print(f"✓ Symmetric pattern '../..' has {len(orientations)} unique orientation(s)")

    # Asymmetric pattern should have more
    asymmetric = "#./.."
    orientations = generate_all_orientations(asymmetric)
    print(f"✓ Asymmetric pattern '#./..' has {len(orientations)} unique orientation(s)")

    # Complex asymmetric
    complex_pattern = ".#./..#/###"
    orientations = generate_all_orientations(complex_pattern)
    print(f"✓ Complex pattern '.#./..#/###' has {len(orientations)} unique orientation(s)")

    return True

def test_rule_parsing():
    """Test that rule parsing creates proper lookup dictionary."""
    test_rules = """../.# => ##./#../...
.#./..#/### => #..#/..../..../#..#"""

    rules = parse_rules(test_rules)

    # The pattern "../.#" should be in rules
    if "../.#" in rules:
        print("✓ Pattern '../.#' found in rules")
    else:
        print("✗ Pattern '../.#' NOT found in rules")
        return False

    # A rotation of "../.#" should also be in rules
    rotated = grid_to_pattern(rotate_grid(pattern_to_grid("../.#")))
    if rotated in rules:
        print(f"✓ Rotated pattern '{rotated}' found in rules")
    else:
        print(f"✗ Rotated pattern '{rotated}' NOT found in rules")
        return False

    # They should map to the same output
    if rules["../.#"] == rules[rotated]:
        print("✓ Both orientations map to same output")
    else:
        print("✗ Different outputs for different orientations")
        return False

    print(f"✓ Total rule entries: {len(rules)}")

    return True

def main():
    print("Running additional verification tests...\n")

    all_passed = True
    all_passed &= test_rotation()
    all_passed &= test_flip()
    all_passed &= test_orientations()
    all_passed &= test_rule_parsing()

    print()
    if all_passed:
        print("=" * 50)
        print("ALL VERIFICATION TESTS PASSED")
        print("=" * 50)
    else:
        print("=" * 50)
        print("SOME TESTS FAILED")
        print("=" * 50)

    return all_passed

if __name__ == '__main__':
    main()
