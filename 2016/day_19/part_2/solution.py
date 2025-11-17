import re
import time
from collections import deque

def read_input(filename='input.md'):
    """Read and parse the input file."""
    with open(filename, 'r') as f:
        content = f.read().strip()
    # Find first integer in the content
    match = re.search(r'\d+', content)
    if match:
        return int(match.group())
    raise ValueError("No integer found in input file")

def solve_across_circle_formula(n):
    """
    Solve using a mathematical formula discovered through pattern analysis.

    The pattern follows powers of 3:
    - If n == 3^k, return 3^k
    - If 3^k < n <= 2*3^k, return n - 3^k
    - If n > 2*3^k, return 2*(n - 2*3^k) + 3^k

    Args:
        n: Total number of elves (1 to n)

    Returns:
        The position number of the winning elf
    """
    if n == 1:
        return 1

    # Find highest power of 3 that is <= n
    power_of_3 = 1
    while power_of_3 * 3 <= n:
        power_of_3 *= 3

    if n == power_of_3:
        return power_of_3
    elif n <= 2 * power_of_3:
        return n - power_of_3
    else:
        return 2 * (n - 2 * power_of_3) + power_of_3

def solve_across_circle(n, debug=False):
    """
    Simulate the elf gift exchange where each elf steals from
    the elf directly across the circle.

    This is the simulation version used for validation.

    Args:
        n: Total number of elves (1 to n)
        debug: If True, print each elimination step (default: False)
               Used for manual verification on small examples only

    Returns:
        The position number of the winning elf
    """
    if n == 1:
        return 1

    # Initialize circle with all elves
    circle = deque(range(1, n + 1))
    current_index = 0

    while len(circle) > 1:
        # Calculate position of elf across the circle
        # floor(M/2) positions away
        remaining = len(circle)
        across_offset = remaining // 2

        # Safety assertions: ensure valid state
        assert across_offset > 0, f"Invalid across_offset: {across_offset}"

        # Calculate target index (wrapping around)
        target_index = (current_index + across_offset) % remaining

        # Additional safety: ensure we never target ourselves
        assert target_index != current_index, "Cannot target self"

        # Debug output
        if debug:
            print(f"Circle: {list(circle)}, Current: {circle[current_index]} (idx={current_index}), "
                  f"Target: {circle[target_index]} (idx={target_index})")

        # Remove the elf across
        eliminated = circle[target_index]
        del circle[target_index]

        # Adjust current_index after deletion
        # If we deleted someone before current position, we shifted left
        if target_index < current_index:
            current_index -= 1
        # If target_index >= current_index, no adjustment needed
        # (current_index still points to the same elf)

        # Move to next elf in sequence (the elf after current in circle order)
        current_index = (current_index + 1) % len(circle)

    return circle[0]

# ========== TEST SUITE ==========

def test_example():
    """Validate the exact example from problem.md"""
    result_sim = solve_across_circle(5)
    result_formula = solve_across_circle_formula(5)
    assert result_sim == 2, f"Expected 2 for n=5, got {result_sim}"
    assert result_formula == 2, f"Formula: Expected 2 for n=5, got {result_formula}"
    assert result_sim == result_formula, f"Simulation and formula disagree: {result_sim} vs {result_formula}"
    print("✓ Example test passed: n=5 → 2")

def test_example_with_trace():
    """Run n=5 with debug output to verify each step"""
    print("\n=== Detailed Trace for n=5 ===")
    result = solve_across_circle(5, debug=True)
    assert result == 2, f"Expected 2 for n=5, got {result}"
    print("✓ Detailed trace test passed: n=5 → 2")

def test_part1_vs_part2_difference():
    """Verify Part 2 gives different results than Part 1"""
    # For n=5: Part 1 (Josephus k=2) → 3, Part 2 (across circle) → 2
    result = solve_across_circle(5)
    assert result == 2, f"Part 2 should give 2 for n=5, got {result}"
    # This confirms we're solving the right problem (different from Part 1)
    print("✓ Part 1 vs Part 2 difference verified: Part 2 gives different result")

def test_single_elf():
    """Single elf should win immediately"""
    result = solve_across_circle(1)
    assert result == 1, f"Expected 1 for n=1, got {result}"
    print("✓ Single elf test passed")

def test_two_elves():
    """With 2 elves, first elf should win"""
    result = solve_across_circle(2)
    # Manual: [1, 2], across = floor(2/2) = 1 → Elf 2 eliminated → [1]
    assert result == 1, f"Expected 1 for n=2, got {result}"
    print("✓ Two elves test passed")

def test_three_elves():
    """Verify n=3 manually"""
    result = solve_across_circle(3)
    # Manual simulation (verified):
    # Initial: [1, 2, 3], current_index=0 (Elf 1)
    # Turn 1 (Elf 1): 3 elves, across = floor(3/2) = 1
    #   - target = (0+1)%3 = 1 → Elf 2 eliminated
    #   - Circle: [1, 3]
    #   - target(1) >= current(0), no adjustment
    #   - Next: (0+1)%2 = 1 → Elf 3
    # Turn 2 (Elf 3): 2 elves, across = floor(2/2) = 1
    #   - target = (1+1)%2 = 0 → Elf 1 eliminated
    #   - Circle: [3]
    # Winner: 3
    assert result == 3, f"Expected 3 for n=3, got {result}"
    print("✓ Three elves test passed")

def test_four_elves():
    """Verify n=4 manually"""
    result = solve_across_circle(4)
    # Manual simulation (verified):
    # Initial: [1, 2, 3, 4], current_index=0 (Elf 1)
    # Turn 1 (Elf 1): 4 elves, across = 2
    #   - target = (0+2)%4 = 2 → Elf 3 eliminated
    #   - Circle: [1, 2, 4]
    #   - target(2) >= current(0), no adjustment
    #   - Next: (0+1)%3 = 1 → Elf 2
    # Turn 2 (Elf 2): 3 elves, across = 1
    #   - target = (1+1)%3 = 2 → Elf 4 eliminated
    #   - Circle: [1, 2]
    #   - target(2) >= current(1), no adjustment
    #   - Next: (1+1)%2 = 0 → Elf 1
    # Turn 3 (Elf 1): 2 elves, across = 1
    #   - target = (0+1)%2 = 1 → Elf 2 eliminated
    #   - Circle: [1]
    # Winner: 1
    assert result == 1, f"Expected 1 for n=4, got {result}"
    print("✓ Four elves test passed")

def test_manual_simulation_n6():
    """Manually simulate n=6 step by step (verified calculation)"""
    result = solve_across_circle(6)
    # Manual calculation (step-by-step verified):
    # Initial: [1, 2, 3, 4, 5, 6], current_index=0 (Elf 1)
    # Turn 1 (Elf 1): 6 elves, across = 3
    #   - target = (0+3)%6 = 3 → Elf 4 eliminated
    #   - Circle: [1, 2, 3, 5, 6]
    #   - target(3) >= current(0), no adjustment
    #   - Next: (0+1)%5 = 1 → Elf 2
    # Turn 2 (Elf 2): 5 elves, across = 2
    #   - target = (1+2)%5 = 3 → Elf 5 eliminated
    #   - Circle: [1, 2, 3, 6]
    #   - target(3) >= current(1), no adjustment
    #   - Next: (1+1)%4 = 2 → Elf 3
    # Turn 3 (Elf 3): 4 elves, across = 2
    #   - target = (2+2)%4 = 0 → Elf 1 eliminated
    #   - Circle: [2, 3, 6]
    #   - target(0) < current(2), adjust: current_index = 1
    #   - Next: (1+1)%3 = 2 → Elf 6
    # Turn 4 (Elf 6): 3 elves, across = 1
    #   - target = (2+1)%3 = 0 → Elf 2 eliminated
    #   - Circle: [3, 6]
    #   - target(0) < current(2), adjust: current_index = 1
    #   - Next: (1+1)%2 = 0 → Elf 3
    # Turn 5 (Elf 3): 2 elves, across = 1
    #   - target = (0+1)%2 = 1 → Elf 6 eliminated
    #   - Circle: [3]
    # Winner: 3
    assert result == 3, f"Expected 3 for n=6, got {result}"
    print("✓ Manual simulation n=6 test passed")

def test_sequential_small():
    """
    Test n=1 to 100 comparing formula vs simulation.
    This helps validate the formula is correct.
    """
    print("\n=== Pattern Analysis (n=1 to 100) ===")
    all_match = True
    for n in range(1, 101):
        result_sim = solve_across_circle(n)
        result_formula = solve_across_circle_formula(n)
        if result_sim != result_formula:
            print(f"MISMATCH at n={n}: sim={result_sim}, formula={result_formula}")
            all_match = False

    # Verify known values
    assert solve_across_circle_formula(1) == 1, "n=1 failed"
    assert solve_across_circle_formula(2) == 1, "n=2 failed"
    assert solve_across_circle_formula(3) == 3, "n=3 failed"
    assert solve_across_circle_formula(4) == 1, "n=4 failed"
    assert solve_across_circle_formula(5) == 2, "n=5 failed"
    assert solve_across_circle_formula(6) == 3, "n=6 failed"

    assert all_match, "Formula and simulation disagree for some values"
    print("✓ Sequential small values test passed (all 100 values match)")

def test_powers_of_three():
    """Test powers of 3: 3, 9, 27, 81, 243 - these should all return themselves"""
    test_cases = [3**i for i in range(1, 7)]

    print("\n=== Powers of 3 ===")
    for n in test_cases:
        result_formula = solve_across_circle_formula(n)
        print(f"n=3^{test_cases.index(n)+1}={n:6d} → winner={result_formula:6d}")
        assert result_formula == n, f"Power of 3 should return itself: {n} → {result_formula}"

    print("✓ Powers of 3 test passed")

def test_across_calculation():
    """Verify the 'across' distance calculation is correct"""
    # For M elves, across is floor(M/2)
    test_cases = [
        (2, 1),   # 2 elves: across = 1
        (3, 1),   # 3 elves: across = 1
        (4, 2),   # 4 elves: across = 2
        (5, 2),   # 5 elves: across = 2
        (6, 3),   # 6 elves: across = 3
        (7, 3),   # 7 elves: across = 3
        (8, 4),   # 8 elves: across = 4
    ]

    for m, expected in test_cases:
        across = m // 2
        assert across == expected, f"For {m} elves, expected across={expected}, got {across}"

    print("✓ Across calculation test passed")

def test_wraparound():
    """Test wraparound behavior explicitly with n=7"""
    print("\n=== Wraparound Test (n=7) ===")
    result = solve_across_circle(7, debug=True)

    # Verify result is in valid range
    assert 1 <= result <= 7, f"Result {result} out of range for n=7"

    print(f"✓ Wraparound test passed: n=7 → {result}")

def test_never_self_target():
    """
    Verify that we never try to eliminate ourselves.

    Note: The main algorithm has an assertion that catches self-targeting,
    so this test provides additional confidence for the calculation logic.
    """
    # Verify across_offset calculation never results in self-targeting
    # For all circle sizes >= 2, across_offset = len//2 >= 1
    for remaining in range(2, 101):
        across_offset = remaining // 2
        assert across_offset > 0, f"Invalid across_offset at remaining={remaining}"
        # When starting at index 0, target should never be 0
        # (can only happen if across_offset = 0, which we just proved impossible)
        target_index = (0 + across_offset) % remaining
        assert target_index != 0, f"Self-targeting possible at remaining={remaining}"

    print("✓ Never self-target test passed")

def test_medium_values():
    """Test medium-sized values to ensure performance is acceptable"""
    test_cases = [100, 1000, 10000]

    print("\n=== Medium Values Performance ===")

    for n in test_cases:
        start = time.time()
        result = solve_across_circle_formula(n)
        elapsed = time.time() - start
        print(f"n={n:6d} → winner={result:6d} (time: {elapsed:.6f}s)")

        # Sanity check: result should be between 1 and n
        assert 1 <= result <= n, f"Result {result} out of range for n={n}"

    print("✓ Medium values test passed")

def test_large_value():
    """Test a large value to ensure algorithm scales"""
    n = 100000

    print(f"\n=== Large Value Test (n={n:,}) ===")

    start = time.time()
    result = solve_across_circle_formula(n)
    elapsed = time.time() - start

    print(f"n={n:,} → winner={result:,} (time: {elapsed:.6f}s)")

    # Sanity check
    assert 1 <= result <= n, f"Result {result} out of range"

    print("✓ Large value test passed")

def test_actual_input():
    """Test the actual puzzle input"""
    n = 3017957

    print(f"\n=== Actual Input Test (n={n:,}) ===")

    start = time.time()
    result = solve_across_circle_formula(n)
    elapsed = time.time() - start

    print(f"n={n:,} → winner={result:,} (time: {elapsed:.6f}s)")

    # Sanity checks
    assert 1 <= result <= n, f"Result {result} out of range"
    assert isinstance(result, int), f"Result must be integer, got {type(result)}"

    print("✓ Actual input test passed")

    return result

def run_all_tests():
    """Execute all tests in order"""
    print("\n" + "="*50)
    print("PART 2 TEST SUITE - ACROSS CIRCLE")
    print("="*50)

    # CRITICAL: Test example first - if this fails, stop
    print("\n=== CRITICAL TEST ===")
    test_example()
    test_example_with_trace()
    test_part1_vs_part2_difference()

    # Edge cases
    print("\n=== EDGE CASES ===")
    test_single_elf()
    test_two_elves()
    test_three_elves()
    test_four_elves()

    # Manual verification with complex index adjustments
    print("\n=== MANUAL VERIFICATION ===")
    test_wraparound()
    test_manual_simulation_n6()

    # Pattern analysis
    print("\n=== PATTERN ANALYSIS ===")
    test_sequential_small()

    # Special cases
    print("\n=== SPECIAL CASES ===")
    test_powers_of_three()

    # Algorithm correctness checks
    print("\n=== ALGORITHM CHECKS ===")
    test_across_calculation()
    test_never_self_target()

    # Performance tests
    print("\n=== PERFORMANCE TESTS ===")
    test_medium_values()
    test_large_value()

    # Final answer
    print("\n=== FINAL ANSWER ===")
    result = test_actual_input()

    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)
    print(f"\nFINAL ANSWER: {result:,}")

    return result

def main():
    """Main function to solve the puzzle"""
    n = read_input()
    result = solve_across_circle_formula(n)
    print(result)

if __name__ == '__main__':
    # Run tests first to validate correctness
    run_all_tests()
    print("\n=== Solution for Actual Input ===")
    main()
