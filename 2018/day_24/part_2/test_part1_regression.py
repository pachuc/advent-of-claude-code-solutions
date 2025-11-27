#!/usr/bin/env python3
"""
Regression test to verify boost=0 matches Part 1 result.
"""

from solution import parse_input, apply_boost, simulate_combat

def test_part1_regression():
    """Test that boost=0 matches Part 1 result."""

    # Read Part 1 answer
    with open("part_1_answer.txt", "r") as f:
        part1_answer = int(f.read().strip())

    print(f"Part 1 answer: {part1_answer}")

    # Simulate with boost=0
    immune_groups, infection_groups = parse_input("input.md")
    apply_boost(immune_groups, 0)  # No boost
    winner, units = simulate_combat(immune_groups, infection_groups)

    print(f"Boost 0 result: Winner={winner}, Units={units}")

    if winner == "Infection" and units == part1_answer:
        print("✓ PASS: Boost=0 matches Part 1 result")
        return True
    else:
        print(f"❌ FAIL: Expected Infection to win with {part1_answer} units, got {winner} with {units} units")
        return False

if __name__ == "__main__":
    success = test_part1_regression()
    exit(0 if success else 1)
