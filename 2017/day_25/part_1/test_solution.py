from solution import parse_input, simulate_turing_machine, calculate_checksum, main
from collections import defaultdict
import time


def test_6_step_example():
    """Test with the 6-step example from the problem description."""
    test_input = """Begin in state A.
Perform a diagnostic checksum after 6 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state B.
  If the current value is 1:
    - Write the value 0.
    - Move one slot to the left.
    - Continue with state B.

In state B:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the left.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""

    initial_state, num_steps, states = parse_input(test_input)
    tape = simulate_turing_machine(states, initial_state, num_steps)
    checksum = calculate_checksum(tape)

    print(f"6-step example test:")
    print(f"  Expected checksum: 3")
    print(f"  Actual checksum: {checksum}")
    assert checksum == 3, f"Expected 3, got {checksum}"
    print("  ✓ PASSED\n")


def test_step_count_validation():
    """Test that we execute exactly the specified number of steps (no off-by-one)."""
    test_input = """Begin in state A.
Perform a diagnostic checksum after 10 steps.

In state A:
  If the current value is 0:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
  If the current value is 1:
    - Write the value 1.
    - Move one slot to the right.
    - Continue with state A.
"""

    initial_state, num_steps, states = parse_input(test_input)
    tape = simulate_turing_machine(states, initial_state, num_steps)
    checksum = calculate_checksum(tape)

    print(f"Step count validation test:")
    print(f"  Expected: 10 ones (after 10 steps)")
    print(f"  Actual checksum: {checksum}")
    assert checksum == 10, f"Expected 10 steps to write 10 ones, got {checksum}"
    print("  ✓ PASSED (no off-by-one error)\n")


def test_tape_structure():
    """Test that tape structure handles positive/negative indices correctly."""
    print("Tape structure test:")
    tape = defaultdict(int)
    tape[-5] = 1
    tape[0] = 1
    tape[5] = 1
    assert tape[-5] == 1, "Negative index should work"
    assert tape[0] == 1, "Zero index should work"
    assert tape[5] == 1, "Positive index should work"
    assert tape[1000] == 0, "Uninitialized position should default to 0"
    tape[0] = 0
    assert tape[0] == 0, "Should be able to overwrite values"
    print("  ✓ All tape structure tests passed\n")


def test_checksum_calculation():
    """Test checksum calculation with various tape states."""
    print("Checksum calculation test:")

    # Empty tape
    tape = defaultdict(int)
    assert calculate_checksum(tape) == 0, "Empty tape should have checksum 0"

    # Mixed values with explicit zeros
    tape = defaultdict(int)
    tape[0] = 1
    tape[1] = 0
    tape[2] = 1
    tape[3] = 1
    tape[-1] = 0
    assert calculate_checksum(tape) == 3, "Should count only 1s, not 0s"

    # All zeros
    tape = defaultdict(int)
    tape[0] = 0
    tape[1] = 0
    tape[2] = 0
    assert calculate_checksum(tape) == 0, "All zeros should have checksum 0"

    # All ones
    tape = defaultdict(int)
    tape[0] = 1
    tape[1] = 1
    tape[2] = 1
    assert calculate_checksum(tape) == 3, "All ones should count all values"

    print("  ✓ All checksum tests passed\n")


def test_parsing():
    """Test input parsing with actual input."""
    print("Parsing test with actual input:")
    with open('input.md', 'r') as f:
        input_text = f.read()

    initial_state, num_steps, states = parse_input(input_text)

    print(f"  Initial state: {initial_state}")
    print(f"  Number of steps: {num_steps}")
    print(f"  States parsed: {sorted(states.keys())}")

    assert initial_state == 'A', f"Expected initial state 'A', got '{initial_state}'"
    assert num_steps == 12172063, f"Expected 12172063 steps, got {num_steps}"
    assert len(states) == 6, f"Expected 6 states, got {len(states)}"

    # Verify state A rules match input
    assert states['A'][0]['write'] == 1
    assert states['A'][0]['move'] == 1  # right
    assert states['A'][0]['next_state'] == 'B'
    assert states['A'][1]['write'] == 0
    assert states['A'][1]['move'] == -1  # left
    assert states['A'][1]['next_state'] == 'C'

    print("  ✓ Parsing test passed\n")


def test_full_solution():
    """Test the full solution with actual input."""
    print("Full solution test:")
    print("  Running simulation with 12,172,063 steps...")

    # Run 1
    start = time.time()
    result1 = main('input.md')
    time1 = time.time() - start

    # Run 2 (for determinism check)
    start = time.time()
    result2 = main('input.md')
    time2 = time.time() - start

    print(f"  Result 1: {result1} (took {time1:.2f}s)")
    print(f"  Result 2: {result2} (took {time2:.2f}s)")

    # Validation checks
    assert result1 == result2, "Results should be deterministic"
    assert isinstance(result1, int), "Result should be an integer"
    assert result1 > 0, "Should have some 1s on tape"
    assert result1 < 12172063, "Can't have more 1s than steps executed"

    print("  ✓ All validation checks passed\n")
    print(f"FINAL ANSWER: {result1}")

    return result1


if __name__ == "__main__":
    print("=" * 60)
    print("Running Turing Machine Simulator Tests")
    print("=" * 60 + "\n")

    # Run unit tests first
    test_tape_structure()
    test_checksum_calculation()
    test_parsing()
    test_6_step_example()
    test_step_count_validation()

    # Run full solution
    test_full_solution()

    print("\n" + "=" * 60)
    print("All tests passed successfully!")
    print("=" * 60)
