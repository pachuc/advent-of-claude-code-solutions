from solution import *


# Read input from input.md
with open('input.md', 'r') as f:
    input_text = f.read()

# Parse input
grid, units = parse_input(input_text)

print(f"Initial state:")
print(f"Total units: {len(units)}")
print(f"Elves: {len([u for u in units if u.type == 'E'])}")
print(f"Goblins: {len([u for u in units if u.type == 'G'])}")

# Simulate combat
rounds = simulate_combat(grid, units)

# Check final state
living = [u for u in units if u.alive]
print(f"\nFinal state after {rounds} complete rounds:")
print(f"Living units: {len(living)}")
if living:
    print(f"Winner: {living[0].type}")
    print(f"Living {living[0].type}s: {len(living)}")
    total_hp = sum(u.hp for u in living)
    print(f"Total HP: {total_hp}")

    # Calculate outcome
    result = calculate_outcome(rounds, units)
    print(f"\nOutcome: {rounds} × {total_hp} = {result}")

# Verify all living units are same type
types = set(u.type for u in living)
assert len(types) == 1, "Not all living units are same type!"

print("\n✓ Result verified!")
