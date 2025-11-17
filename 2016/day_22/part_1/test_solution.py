from solution import parse_input, count_viable_pairs


def test_parsing():
    """Test the parsing function"""
    print("Testing parsing...")

    # Test 1.1: Basic parsing
    test_input = """root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     89T   65T    24T   73%
/dev/grid/node-x0-y1     92T   64T    28T   69%
/dev/grid/node-x1-y0     90T    0T    90T    0%"""

    nodes = parse_input(test_input)
    assert len(nodes) == 3, f"Expected 3 nodes, got {len(nodes)}"
    assert nodes[0] == (65, 24), f"Expected (65, 24), got {nodes[0]}"
    assert nodes[1] == (64, 28), f"Expected (64, 28), got {nodes[1]}"
    assert nodes[2] == (0, 90), f"Expected (0, 90), got {nodes[2]}"
    print("  ✓ Basic parsing test passed")

    # Test 1.2: Large numbers
    test_input_large = """root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0    501T  495T     6T   98%"""

    nodes = parse_input(test_input_large)
    assert nodes[0] == (495, 6), f"Expected (495, 6), got {nodes[0]}"
    print("  ✓ Large numbers test passed")


def test_counting():
    """Test the counting function"""
    print("Testing counting...")

    # Test 2.1: All pairs viable
    nodes = [(10, 50), (20, 60), (30, 70)]
    result = count_viable_pairs(nodes)
    assert result == 6, f"Expected 6 pairs, got {result}"
    print("  ✓ All pairs viable test passed")

    # Test 2.2: Empty node (used = 0)
    nodes = [(0, 50), (20, 60), (30, 70)]
    result = count_viable_pairs(nodes)
    assert result == 4, f"Expected 4 pairs, got {result}"
    print("  ✓ Empty node test passed")

    # Test 2.3: No available space
    nodes = [(50, 10), (60, 20), (70, 30)]
    result = count_viable_pairs(nodes)
    assert result == 0, f"Expected 0 pairs, got {result}"
    print("  ✓ No available space test passed")

    # Test 2.4: Exact fit
    nodes = [(50, 50), (50, 60)]
    result = count_viable_pairs(nodes)
    assert result == 2, f"Expected 2 pairs, got {result}"
    print("  ✓ Exact fit test passed")

    # Test 2.5: Single node
    nodes = [(50, 50)]
    result = count_viable_pairs(nodes)
    assert result == 0, f"Expected 0 pairs, got {result}"
    print("  ✓ Single node test passed")

    # Test 2.6: Two nodes
    nodes = [(10, 50), (20, 60)]
    result = count_viable_pairs(nodes)
    assert result == 2, f"Expected 2 pairs, got {result}"
    print("  ✓ Two nodes test passed")


def test_edge_cases():
    """Test edge cases"""
    print("Testing edge cases...")

    # Test 5.1: All empty nodes
    nodes = [(0, 100), (0, 100), (0, 100)]
    result = count_viable_pairs(nodes)
    assert result == 0, f"Expected 0 pairs, got {result}"
    print("  ✓ All empty nodes test passed")

    # Test 5.2: All full nodes
    nodes = [(100, 0), (100, 0), (100, 0)]
    result = count_viable_pairs(nodes)
    assert result == 0, f"Expected 0 pairs, got {result}"
    print("  ✓ All full nodes test passed")

    # Test 5.3: One large node
    nodes = [(495, 6), (65, 24), (70, 20)]
    result = count_viable_pairs(nodes)
    assert result == 0, f"Expected 0 pairs, got {result}"
    print("  ✓ One large node test passed")


def test_integration():
    """Test integration with small example"""
    print("Testing integration with small example...")

    test_input = """root@ebhq-gridcenter# df -h
Filesystem              Size  Used  Avail  Use%
/dev/grid/node-x0-y0     10T    8T     2T   80%
/dev/grid/node-x0-y1     10T    5T     5T   50%
/dev/grid/node-x1-y0     10T    0T    10T    0%"""

    nodes = parse_input(test_input)
    result = count_viable_pairs(nodes)
    # Node 0 (8, 2): fits in node 2 (avail=10) → 1 pair
    # Node 1 (5, 5): fits in node 2 (avail=10) → 1 pair
    # Node 2 (0, 10): empty, skip → 0 pairs
    assert result == 2, f"Expected 2 pairs, got {result}"
    print("  ✓ Integration test passed")


def test_actual_input():
    """Test with actual input file"""
    print("Testing with actual input...")

    with open('input.md', 'r') as f:
        input_text = f.read()

    nodes = parse_input(input_text)
    print(f"  Parsed {len(nodes)} nodes from actual input")

    # Sanity checks
    assert len(nodes) > 0, "No nodes parsed"
    assert all(isinstance(u, int) and isinstance(a, int) for u, a in nodes), "Invalid node data types"
    assert all(u >= 0 and a >= 0 for u, a in nodes), "Negative values found"

    result = count_viable_pairs(nodes)
    max_possible = len(nodes) * (len(nodes) - 1)
    assert 0 < result <= max_possible, f"Result {result} out of valid range [1, {max_possible}]"
    print(f"  Result: {result} viable pairs")
    print("  ✓ Actual input test passed")


if __name__ == "__main__":
    test_parsing()
    test_counting()
    test_edge_cases()
    test_integration()
    test_actual_input()
    print("\n✓ All tests passed!")
