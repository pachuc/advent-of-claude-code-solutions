"""Test the solution with the example from the problem."""
from solution import State, solve

# Example from problem:
# F4 .  .  .  .  .
# F3 .  .  .  LG .
# F2 .  HG .  .  .
# F1 E  .  HM .  LM
#
# Expected: 11 steps

# Create the initial state
# Floor 0 (F1): Hydrogen microchip, Lithium microchip
# Floor 1 (F2): Hydrogen generator
# Floor 2 (F3): Lithium generator
# Floor 3 (F4): Empty

initial_state = State(
    elevator_floor=0,
    floors=(
        frozenset([('hydrogen', 'M'), ('lithium', 'M')]),  # Floor 0
        frozenset([('hydrogen', 'G')]),                     # Floor 1
        frozenset([('lithium', 'G')]),                      # Floor 2
        frozenset()                                          # Floor 3
    )
)

print("Testing with example from problem...")
print("Expected: 11 steps")
result = solve(initial_state)
print(f"Result: {result} steps")

if result == 11:
    print("✓ Test PASSED!")
else:
    print("✗ Test FAILED!")
