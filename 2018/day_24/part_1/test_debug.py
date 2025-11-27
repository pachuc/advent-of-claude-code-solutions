#!/usr/bin/env python3
"""Run solution with debug mode to see first few rounds."""

import solution

# Enable debug mode
solution.DEBUG = True

# Parse input
immune_groups, infection_groups = solution.parse_input("input.md")

# Show initial state
print("=" * 60)
print("INITIAL STATE")
print("=" * 60)
print(f"\nImmune System ({len(immune_groups)} groups):")
for g in immune_groups[:3]:  # Show first 3
    print(f"  {g}")

print(f"\nInfection ({len(infection_groups)} groups):")
for g in infection_groups[:3]:  # Show first 3
    print(f"  {g}")

print("\n" + "=" * 60)
print("STARTING COMBAT (showing first 2 rounds)")
print("=" * 60)

# Run just a few rounds manually to verify combat mechanics
round_num = 0
max_rounds_to_show = 2

while round_num < max_rounds_to_show:
    round_num += 1
    print(f"\n=== Round {round_num} ===")

    # Filter out dead groups
    immune_groups = [g for g in immune_groups if g.is_alive()]
    infection_groups = [g for g in infection_groups if g.is_alive()]

    immune_units = sum(g.units for g in immune_groups)
    infection_units = sum(g.units for g in infection_groups)

    print(f"Immune System: {immune_units} units in {len(immune_groups)} groups")
    print(f"Infection: {infection_units} units in {len(infection_groups)} groups")

    if not immune_groups or not infection_groups:
        print("Combat ended!")
        break

    # Target selection phase
    print("\nTarget selection:")
    targets = solution.target_selection(immune_groups, infection_groups)

    if not targets:
        print("No valid targets - stalemate!")
        break

    # Attack phase
    print("\nAttacks:")
    units_killed = solution.attack_phase(targets)

    if units_killed == 0:
        print("No units killed - stalemate!")
        break

    print(f"Total units killed this round: {units_killed}")

print("\n" + "=" * 60)
print("Running full combat simulation...")
print("=" * 60)

# Now run the full simulation
solution.DEBUG = False
immune_groups, infection_groups = solution.parse_input("input.md")
winner, units = solution.simulate_combat(immune_groups, infection_groups)

print(f"\nFinal Result:")
print(f"  Winner: {winner}")
print(f"  Remaining units: {units}")
