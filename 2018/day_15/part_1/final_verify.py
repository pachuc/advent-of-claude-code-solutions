#!/usr/bin/env python3
"""Final verification of the solution"""

from solution import parse_input, simulate_combat, calculate_outcome

# Test with actual input
with open('input.md', 'r') as f:
    input_text = f.read()

grid, units = parse_input(input_text)

initial_elves = sum(1 for u in units if u.type == 'E')
initial_goblins = sum(1 for u in units if u.type == 'G')

print("INITIAL STATE:")
print(f"  Elves: {initial_elves}")
print(f"  Goblins: {initial_goblins}")
print(f"  Total units: {len(units)}")
print()

# Run combat
rounds = simulate_combat(grid, units)

# Get results
living = [u for u in units if u.alive]
living_elves = sum(1 for u in living if u.type == 'E')
living_goblins = sum(1 for u in living if u.type == 'G')
total_hp = sum(u.hp for u in living)
outcome = calculate_outcome(rounds, units)

print("FINAL STATE:")
print(f"  Completed rounds: {rounds}")
print(f"  Living Elves: {living_elves}")
print(f"  Living Goblins: {living_goblins}")
print(f"  Total HP: {total_hp}")
print()

print("VERIFICATION:")
# All living units should be same type
if living:
    types = set(u.type for u in living)
    if len(types) == 1:
        print(f"  ✓ All survivors are same type: {types.pop()}")
    else:
        print(f"  ✗ ERROR: Multiple types survived: {types}")

# Should have survivors
if len(living) > 0:
    print(f"  ✓ At least one unit survived")
else:
    print(f"  ✗ ERROR: No units survived")

# Outcome should be positive
if outcome > 0:
    print(f"  ✓ Outcome is positive: {outcome}")
else:
    print(f"  ✗ ERROR: Outcome is not positive: {outcome}")

print()
print(f"ANSWER: {outcome}")
