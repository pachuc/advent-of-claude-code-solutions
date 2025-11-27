from solution import parse_input

# Test parsing with actual input
immune_groups, infection_groups = parse_input("input.md")

print("=== Immune System Groups ===")
for g in immune_groups:
    print(f"Group {g.id}: {g.units} units, {g.hit_points} HP, {g.attack_damage} {g.attack_type} damage, init {g.initiative}")
    if g.weaknesses:
        print(f"  Weaknesses: {g.weaknesses}")
    if g.immunities:
        print(f"  Immunities: {g.immunities}")

print("\n=== Infection Groups ===")
for g in infection_groups:
    print(f"Group {g.id}: {g.units} units, {g.hit_points} HP, {g.attack_damage} {g.attack_type} damage, init {g.initiative}")
    if g.weaknesses:
        print(f"  Weaknesses: {g.weaknesses}")
    if g.immunities:
        print(f"  Immunities: {g.immunities}")

print(f"\nTotal Immune System groups: {len(immune_groups)}")
print(f"Total Infection groups: {len(infection_groups)}")

# Verify specific groups from input
print("\n=== Verification ===")
print(f"First Immune group: {immune_groups[0].units} units (expected 6638)")
print(f"First Immune group weaknesses: {immune_groups[0].weaknesses} (expected {{'radiation'}})")
print(f"Second Immune group immunities: {immune_groups[1].immunities} (expected {{'bludgeoning', 'cold', 'fire'}})")
print(f"First Infection group: {infection_groups[0].units} units (expected 1756)")
print(f"First Infection group immunities: {infection_groups[0].immunities} (expected {{'bludgeoning'}})")
