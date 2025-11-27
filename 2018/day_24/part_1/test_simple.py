from solution import parse_input, simulate_combat

# Enable debug mode
import solution
solution.DEBUG = True

# Test with simple example
immune_groups, infection_groups = parse_input("test_simple.md")

print("=== Parsed Groups ===")
print("Immune System:")
for g in immune_groups:
    print(f"  {g}")
print("\nInfection:")
for g in infection_groups:
    print(f"  {g}")

print("\n=== Starting Combat ===")
winner, units = simulate_combat(immune_groups, infection_groups)

print(f"\n=== Result ===")
print(f"Winner: {winner}")
print(f"Units remaining: {units}")
print(f"\nExpected: Immune System wins with 100 units (Infection takes 10000 damage from 5000*2, all 50 units die)")
