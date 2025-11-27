from solution import count_differences, get_common_letters, find_prototype_boxes, parse_input

def test_count_differences():
    print("Testing count_differences()...")
    assert count_differences("fghij", "fguij") == 1, "Expected 1 difference between fghij and fguij"
    assert count_differences("abcde", "axcye") == 2, "Expected 2 differences between abcde and axcye"
    assert count_differences("abcde", "abcde") == 0, "Expected 0 differences for identical strings"
    assert count_differences("aaaa", "aaab") == 1, "Expected 1 difference at last position"
    assert count_differences("aaaa", "baaa") == 1, "Expected 1 difference at first position"
    print("✓ count_differences tests passed")

def test_get_common_letters():
    print("\nTesting get_common_letters()...")
    assert get_common_letters("fghij", "fguij") == "fgij", "Expected fgij from fghij and fguij"
    assert get_common_letters("abcde", "abcde") == "abcde", "Expected abcde from identical strings"
    assert get_common_letters("abcde", "axcye") == "ace", "Expected ace from abcde and axcye"
    print("✓ get_common_letters tests passed")

def test_example_input():
    print("\nTesting with example data...")
    box_ids = parse_input('test_input.txt')
    result = find_prototype_boxes(box_ids)
    assert result == "fgij", f"Expected 'fgij' but got '{result}'"
    print(f"✓ Example test passed: {result}")

def test_input_parsing():
    print("\nTesting input parsing...")
    box_ids = parse_input('input.md')
    assert len(box_ids) == 250, f"Expected 250 box IDs, got {len(box_ids)}"
    assert all(len(box_id) == 26 for box_id in box_ids), "All box IDs should be 26 characters"
    assert all(box_id.islower() for box_id in box_ids), "All box IDs should be lowercase"
    print(f"✓ Input parsing test passed: {len(box_ids)} box IDs, all 26 characters")

if __name__ == '__main__':
    test_count_differences()
    test_get_common_letters()
    test_example_input()
    test_input_parsing()
    print("\n✅ All tests passed!")
