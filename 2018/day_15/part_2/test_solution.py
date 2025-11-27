from solution import parse_input, simulate_combat, calculate_outcome, simulate_with_elf_check

# Test Part 1 regression
print("Test 1: Part 1 regression (attack power 3 for both)")
with open('input.md', 'r') as f:
    input_text = f.read()

grid, units = parse_input(input_text, 3, 3)
rounds = simulate_combat(grid, units)
outcome = calculate_outcome(rounds, units)

print(f"  Part 1 outcome: {outcome}")
print(f"  Expected: 218272")
print(f"  Match: {outcome == 218272}")
print()

# Test minimum attack power is ≥ 4
print("Test 2: Minimum attack power is ≥ 4")
from solution import find_minimum_elf_attack_power
min_power, rounds, outcome = find_minimum_elf_attack_power(input_text, verbose=False)
print(f"  Minimum power: {min_power}")
print(f"  Is ≥ 4: {min_power >= 4}")
print()

# Test that all Elves survive with minimum power
print("Test 3: All Elves survive with minimum power")
grid, units = parse_input(input_text, min_power, 3)
initial_elves = sum(1 for u in units if u.type == 'E')
simulate_combat(grid, units)
surviving_elves = sum(1 for u in units if u.alive and u.type == 'E')
surviving_goblins = sum(1 for u in units if u.alive and u.type == 'G')

print(f"  Initial Elves: {initial_elves}")
print(f"  Surviving Elves: {surviving_elves}")
print(f"  All Elves survived: {surviving_elves == initial_elves}")
print(f"  All Goblins dead: {surviving_goblins == 0}")
print()

# Test that min_power - 1 fails
print("Test 4: Attack power (min_power - 1) fails")
if min_power > 4:
    success_lower, _, _ = simulate_with_elf_check(input_text, min_power - 1)
    print(f"  Testing attack power {min_power - 1}: {'SUCCESS' if success_lower else 'FAILURE'}")
    print(f"  Should fail: {not success_lower}")
else:
    print(f"  Skipped (min_power = {min_power}, cannot test lower)")
print()

# Test that min_power succeeds
print("Test 5: Attack power min_power succeeds")
success, _, _ = simulate_with_elf_check(input_text, min_power)
print(f"  Testing attack power {min_power}: {'SUCCESS' if success else 'FAILURE'}")
print(f"  Should succeed: {success}")
print()

# Test determinism
print("Test 6: Solution is deterministic")
results = []
for i in range(3):
    success, rounds, outcome = simulate_with_elf_check(input_text, min_power)
    results.append((success, rounds, outcome))

all_same = all(r == results[0] for r in results)
print(f"  All runs produced identical results: {all_same}")
print(f"  Result: {results[0]}")
print()

# Test outcome calculation
print("Test 7: Outcome calculation is correct")
grid, units = parse_input(input_text, min_power, 3)
actual_rounds = simulate_combat(grid, units)
surviving_units = [u for u in units if u.alive]
total_hp = sum(u.hp for u in surviving_units)
expected_outcome = actual_rounds * total_hp
_, _, calculated_outcome = simulate_with_elf_check(input_text, min_power)

print(f"  Calculated outcome: {calculated_outcome}")
print(f"  Expected outcome: {expected_outcome}")
print(f"  Match: {calculated_outcome == expected_outcome}")
print()

print("=" * 50)
print("All tests completed!")
print(f"Final Answer: {outcome}")
