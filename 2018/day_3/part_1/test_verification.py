#!/usr/bin/env python3
"""Verification tests for the fabric claim solution."""

from solution import parse_claim, get_fabric_dimensions, create_fabric_grid, mark_claim_on_grid, count_overlaps, Claim


def test_parse_claim():
    """Test claim parsing."""
    print("Testing parse_claim...")

    # Test 1.1: Standard claim
    result = parse_claim("#123 @ 3,2: 5x4")
    assert result == Claim(123, 3, 2, 5, 4), f"Expected Claim(123, 3, 2, 5, 4), got {result}"

    # Test 1.2: Single digit values
    result = parse_claim("#1 @ 0,0: 1x1")
    assert result == Claim(1, 0, 0, 1, 1), f"Expected Claim(1, 0, 0, 1, 1), got {result}"

    # Test 1.3: Large values
    result = parse_claim("#1286 @ 999,999: 29x29")
    assert result == Claim(1286, 999, 999, 29, 29), f"Expected Claim(1286, 999, 999, 29, 29), got {result}"

    print("✓ Parse claim tests passed")


def test_rectangle_edge_inclusion():
    """Test 0: Verify rectangle edges are correctly inclusive/exclusive."""
    print("\nTesting rectangle edge inclusion...")

    # Claims that are adjacent but don't overlap
    claim1 = Claim(1, 2, 2, 3, 3)  # covers columns 2,3,4 and rows 2,3,4
    claim2 = Claim(2, 5, 2, 3, 3)  # covers columns 5,6,7 and rows 2,3,4

    # Create grid
    claims = [claim1, claim2]
    width, height = get_fabric_dimensions(claims)
    grid = create_fabric_grid(width, height)

    # Mark claims
    mark_claim_on_grid(grid, claim1)
    mark_claim_on_grid(grid, claim2)

    # Count overlaps
    overlaps = count_overlaps(grid)
    assert overlaps == 0, f"Expected 0 overlaps for adjacent rectangles, got {overlaps}"

    print("✓ Rectangle edge inclusion test passed")


def test_example_from_problem():
    """Test 2: Example from problem statement."""
    print("\nTesting example from problem...")

    claims = [
        parse_claim("#1 @ 1,3: 4x4"),
        parse_claim("#2 @ 3,1: 4x4"),
        parse_claim("#3 @ 5,5: 2x2")
    ]

    # Calculate dimensions
    width, height = get_fabric_dimensions(claims)

    # Create grid
    grid = create_fabric_grid(width, height)

    # Mark all claims
    for claim in claims:
        mark_claim_on_grid(grid, claim)

    # Count overlaps
    overlaps = count_overlaps(grid)
    assert overlaps == 4, f"Expected 4 overlaps, got {overlaps}"

    print("✓ Example test passed")


def test_no_overlaps():
    """Test 3: No overlapping claims."""
    print("\nTesting no overlaps...")

    claims = [
        Claim(1, 0, 0, 5, 5),
        Claim(2, 10, 10, 5, 5),
        Claim(3, 20, 20, 5, 5)
    ]

    width, height = get_fabric_dimensions(claims)
    grid = create_fabric_grid(width, height)

    for claim in claims:
        mark_claim_on_grid(grid, claim)

    overlaps = count_overlaps(grid)
    assert overlaps == 0, f"Expected 0 overlaps, got {overlaps}"

    print("✓ No overlaps test passed")


def test_complete_overlap():
    """Test 4: Complete overlap of multiple claims."""
    print("\nTesting complete overlap...")

    claims = [
        Claim(1, 5, 5, 3, 3),
        Claim(2, 5, 5, 3, 3),
        Claim(3, 5, 5, 3, 3)
    ]

    width, height = get_fabric_dimensions(claims)
    grid = create_fabric_grid(width, height)

    for claim in claims:
        mark_claim_on_grid(grid, claim)

    overlaps = count_overlaps(grid)
    assert overlaps == 9, f"Expected 9 overlaps, got {overlaps}"

    print("✓ Complete overlap test passed")


def test_partial_overlaps():
    """Test 5: Partial overlaps."""
    print("\nTesting partial overlaps...")

    claims = [
        Claim(1, 0, 0, 4, 4),
        Claim(2, 2, 2, 4, 4),
        Claim(3, 4, 4, 4, 4)
    ]

    width, height = get_fabric_dimensions(claims)
    grid = create_fabric_grid(width, height)

    for claim in claims:
        mark_claim_on_grid(grid, claim)

    overlaps = count_overlaps(grid)
    assert overlaps == 8, f"Expected 8 overlaps, got {overlaps}"

    print("✓ Partial overlaps test passed")


def test_adjacent_claims():
    """Test 6: Adjacent claims that don't overlap."""
    print("\nTesting adjacent claims...")

    claims = [
        Claim(1, 0, 0, 5, 5),
        Claim(2, 5, 0, 5, 5),
        Claim(3, 0, 5, 5, 5)
    ]

    width, height = get_fabric_dimensions(claims)
    grid = create_fabric_grid(width, height)

    for claim in claims:
        mark_claim_on_grid(grid, claim)

    overlaps = count_overlaps(grid)
    assert overlaps == 0, f"Expected 0 overlaps for adjacent claims, got {overlaps}"

    print("✓ Adjacent claims test passed")


def test_single_claim():
    """Test 7: Single claim."""
    print("\nTesting single claim...")

    claims = [Claim(1, 100, 100, 10, 10)]

    width, height = get_fabric_dimensions(claims)
    grid = create_fabric_grid(width, height)

    for claim in claims:
        mark_claim_on_grid(grid, claim)

    overlaps = count_overlaps(grid)
    assert overlaps == 0, f"Expected 0 overlaps for single claim, got {overlaps}"

    print("✓ Single claim test passed")


def test_three_way_overlap():
    """Test 9: Three-way overlap."""
    print("\nTesting three-way overlap...")

    claims = [
        Claim(1, 0, 0, 4, 4),
        Claim(2, 1, 1, 4, 4),
        Claim(3, 2, 2, 4, 4)
    ]

    width, height = get_fabric_dimensions(claims)
    grid = create_fabric_grid(width, height)

    for claim in claims:
        mark_claim_on_grid(grid, claim)

    overlaps = count_overlaps(grid)

    # Manual calculation from test plan: should be 14 cells with 2+ claims
    assert overlaps == 14, f"Expected 14 overlaps, got {overlaps}"

    print("✓ Three-way overlap test passed")


def main():
    """Run all verification tests."""
    print("="*60)
    print("Running verification tests...")
    print("="*60)

    test_parse_claim()
    test_rectangle_edge_inclusion()
    test_example_from_problem()
    test_no_overlaps()
    test_complete_overlap()
    test_partial_overlaps()
    test_adjacent_claims()
    test_single_claim()
    test_three_way_overlap()

    print("\n" + "="*60)
    print("All verification tests passed! ✓")
    print("="*60)


if __name__ == '__main__':
    main()
