from solution import simulate_marble_game, parse_input
from collections import deque
import time


def test_examples():
    """Test all provided example cases"""
    test_cases = [
        (9, 25, 32),
        (10, 1618, 8317),
        (13, 7999, 146373),
        (17, 1104, 2764),
        (21, 6111, 54718),
        (30, 5807, 37305),
    ]

    print("Testing provided examples:")
    all_passed = True
    for players, last_marble, expected in test_cases:
        result = simulate_marble_game(players, last_marble)
        passed = result == expected
        all_passed = all_passed and passed
        status = "✓" if passed else "✗"
        print(f"  {status} {players} players, {last_marble} marbles → {result} (expected {expected})")

    return all_passed


def test_minimal_cases():
    """Test edge cases with minimal inputs"""
    print("\nTesting minimal edge cases:")

    # Edge case: last marble is 0 (only marble 0 placed)
    result = simulate_marble_game(1, 0)
    assert result == 0, f"Expected 0, got {result}"
    print(f"  ✓ 1 player, 0 marbles → {result}")

    # No scoring happens before marble 23
    result = simulate_marble_game(1, 22)
    assert result == 0, f"Expected 0, got {result}"
    print(f"  ✓ 1 player, 22 marbles → {result}")

    # First scoring at marble 23
    # When marble 23 is processed with 1 player:
    # Circle has marbles 0-22, current is 22
    # 7 counter-clockwise from 22 is marble 9
    # Player gets 23 + 9 = 32
    result = simulate_marble_game(1, 23)
    assert result == 32, f"Expected 32, got {result}"
    print(f"  ✓ 1 player, 23 marbles → {result}")


def test_deque_behavior():
    """Test that deque rotation works as expected"""
    print("\nTesting deque rotation behavior:")

    # Test clockwise rotation (for standard placement)
    d = deque([0, 1, 2, 3])
    d.rotate(1)  # Clockwise
    assert list(d) == [3, 0, 1, 2], "Clockwise rotation failed"
    print("  ✓ Clockwise rotation works correctly")

    # Test counter-clockwise rotation (for special placement)
    d = deque([0, 1, 2, 3, 4, 5, 6, 7])
    d.rotate(-7)  # Counter-clockwise by 7
    assert list(d) == [7, 0, 1, 2, 3, 4, 5, 6], "Counter-clockwise rotation failed"
    print("  ✓ Counter-clockwise rotation works correctly")


def test_input_parsing():
    """Verify input parsing handles the expected format"""
    print("\nTesting input parsing:")

    result = parse_input("463 players; last marble is worth 71787 points")
    assert result == (463, 71787), f"Expected (463, 71787), got {result}"
    print("  ✓ Parses '463 players; last marble is worth 71787 points'")

    result = parse_input("9 players; last marble is worth 25 points")
    assert result == (9, 25), f"Expected (9, 25), got {result}"
    print("  ✓ Parses '9 players; last marble is worth 25 points'")


def test_detailed_walkthrough():
    """Test with debug output for 9 players, 25 marbles"""
    print("\nTesting detailed walkthrough (9 players, 25 marbles):")
    result = simulate_marble_game(9, 25, debug=False)
    assert result == 32, f"Expected 32, got {result}"
    print(f"  ✓ Manual walkthrough verified: 9 players, 25 marbles → {result}")


def test_actual_input():
    """Run with the actual input to verify performance and get answer"""
    print("\nTesting with actual input:")

    # Read from input.md
    with open('input.md', 'r') as f:
        input_text = f.read().strip()

    num_players, last_marble = parse_input(input_text)
    print(f"  Input: {num_players} players, {last_marble} marbles")

    start = time.time()
    result = simulate_marble_game(num_players, last_marble)
    elapsed = time.time() - start

    print(f"  Result: {result}")
    print(f"  Time: {elapsed:.3f} seconds")

    # Verify it completes in reasonable time
    assert elapsed < 1.0, f"Too slow: {elapsed} seconds"

    # Verify result is a reasonable integer
    assert result > 0, "Result should be positive"
    print(f"  ✓ Actual input completed successfully in {elapsed:.3f}s")

    return result


def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("MARBLE CIRCLE GAME - TEST SUITE")
    print("=" * 60)

    # Phase 1: Unit tests
    test_deque_behavior()
    test_input_parsing()
    test_minimal_cases()

    # Phase 2: Example validation
    all_passed = test_examples()

    # Phase 3: Edge case testing
    test_detailed_walkthrough()

    # Phase 4: Performance validation
    final_result = test_actual_input()

    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED ✓")
        print(f"Final answer: {final_result}")
    else:
        print("SOME TESTS FAILED ✗")
    print("=" * 60)

    return final_result


if __name__ == "__main__":
    run_all_tests()
